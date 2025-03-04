import reflex as rx
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from se_library.models import User, BookTransaction, ConditionEnum
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

class Result:
    error: bool = False
    message: str = ""

    def __init__(self, error: bool, message: str):
        self.error = error
        self.message = message

class ApproveState(rx.State):

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
        key = os.getenv("SECRET_KEY")
        if not key:
            return rx.redirect("/login")
        cipher_suite = Fernet(key)
        token = self.router.page.params["q"]
        try:
            transaction_id = cipher_suite.decrypt(token.encode()).decode()
            with rx.session() as db:
                transaction = db.exec(
                    BookTransaction.select().where(BookTransaction.id == transaction_id)
                ).first()
                if not transaction:
                    raise Exception
                transaction.borrow_status = "approved"
                db.commit()
                res = await self.get_qrcode(transaction=transaction)
                if res.error:
                    print(res.message)
                    raise Exception
                res = await self.send_email(transaction=transaction)
                if res.error:
                    print(res.message)
                    raise Exception
                return rx.redirect("/profile")
        except Exception:
            return rx.redirect("/login")
        
    async def send_email(self, transaction):
        try:
            template_data = {
                "company_name": "SE Library",
                "lender_name": transaction.book_inventory.owner.username,
                "borrow_request": False,
                "approval_success": True,
                "reject": False,
                "request_id": transaction.id,
                "borrower_name": transaction.borrower.username,
                "book_title": transaction.book_inventory.book.title,
                "book_condition": self.enum_to_condition(transaction.book_inventory.condition),
                "submission_date": transaction.borrow_date,
                "status": "Approved",
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
        
    async def get_qrcode(transaction):
        pass