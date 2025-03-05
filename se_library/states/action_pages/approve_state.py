import reflex as rx
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from se_library.models import BookTransaction, ConditionEnum, BorrowStatusEnum
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import asyncio

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
BASE_URL = os.getenv("BASE_URL")

class Result:
    error: bool = False
    message: str = ""

    def __init__(self, error: bool, message: str):
        self.error = error
        self.message = message

class ApproveState(rx.State):

    approving: bool
    is_success: bool

    def enum_to_condition(self, condition: ConditionEnum) -> str:
        match condition:
            case ConditionEnum.FACTORY_NEW:
                return "Factory New"
            case ConditionEnum.MINIMAL_WEAR:
                return "Minimal Wear"
            case ConditionEnum.FIELD_TESTED:
                return "Field Tested"
            case ConditionEnum.WELL_WORN:
                return "Well Worn"
            case ConditionEnum.BATTLE_SCARRED:
                return "Battle Scarred"
            case _:
                return None

    @rx.event
    async def handle_approve(self):
        self.reset()
        yield
        self.approving = True
        yield
        await asyncio.sleep(2)
        try:
            key = os.getenv("SECRET_KEY")
            if not key:
                raise Exception
            cipher_suite = Fernet(key)
            token = self.router.page.params["q"]
            transaction_id = cipher_suite.decrypt(token.encode()).decode()
            with rx.session() as db:
                transaction = db.exec(
                    BookTransaction.select().where(BookTransaction.id == transaction_id)
                ).first()
                if not transaction:
                    print("Transaction not found")
                    raise Exception
                transaction.borrow_status = BorrowStatusEnum.APPROVED
                db.commit()
                res = await self.get_qrcode(transaction=transaction)
                if res.error:
                    print(res.message)
                    raise Exception
                res = await self.send_email(transaction=transaction, cipher_suite=cipher_suite)
                if res.error:
                    print(res.message)
                    raise Exception
            self.approving = False
            self.is_success = True
            return
        except Exception as e:
            print(str(e))
            self.approving = False
            self.is_success = False
            yield
            return

    async def send_email(self, transaction, cipher_suite):
        try:
            transaction_id = cipher_suite.encrypt(str(transaction.id).encode()).decode()
            template_data = {
                "company_name": "SE Library",
                "lender_name": transaction.book_inventory.owner.username,
                "borrow_request": False,
                "approval_succeed": True,
                "reject": False,
                "request_id": transaction.id,
                "borrower_name": transaction.borrower.username,
                "book_title": transaction.book_inventory.book.title,
                "book_condition": self.enum_to_condition(transaction.book_inventory.condition),
                "submission_date": transaction.borrow_date,
                "status": "Approved",
                "color": "#4CAF50",
                "qr_image": f"{BASE_URL}/assets/static/image.png",
                "action_url": f"{BASE_URL}/confirm?q={transaction_id}&role=lender"
            }

            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.abspath(os.path.join(current_dir, '..', '..', "..", "assets", "html"))
            env = Environment(loader=FileSystemLoader(templates_dir))
            template = env.get_template("lender_template.html")
            html = template.render(**template_data)

            mail = Mail(
                from_email="noreply@se-library.org",
                to_emails=transaction.book_inventory.owner.email,
                subject="Borrow Request Approved",
                html_content=html,
            )
            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = sg.send(mail)
            return Result(error=False, message="Email sent successfully")
        except Exception as e:
            return Result(error=True, message=str(e))

    async def get_qrcode(self, transaction):
        return Result(error=False, message="QR Code generated successfully")
