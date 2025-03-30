import reflex as rx
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from se_library.models import BookTransaction, ConditionEnum, BorrowStatusEnum, BORROW_DURATION
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import asyncio
import base64
import requests
from datetime import datetime, timedelta

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
BASE_URL = os.getenv("BASE_URL")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

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
                if transaction.borrow_status != BorrowStatusEnum.PENDING:
                    print("Transaction not pending")
                    raise Exception
                transaction.borrow_status = BorrowStatusEnum.APPROVED
                transaction.borrow_date = datetime.now()
                transaction.return_date = datetime.now() + timedelta(days=BORROW_DURATION)
                db.commit()
                res = await self.get_qrcode(transaction=transaction, db=db)
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
            
            lender_template_data = {
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
                "qr_image": transaction.qr_code_image_link,
                "action_url": f"{BASE_URL}/confirm?q={transaction_id}&role=lender"
            }
            borrower_template_data = {
                "company_name": "SE Library",
                "borrower_name": transaction.borrower.username,
                "borrow_request": False,
                "request_status": True,
                "picked_up": False,
                "approved": True,
                "request_id": transaction.id,
                "lender_name": transaction.book_inventory.owner.username,
                "book_title": transaction.book_inventory.book.title,
                "book_condition": self.enum_to_condition(transaction.book_inventory.condition),
                "submission_date": transaction.borrow_date,
                "status": "Approved",
                "color": "#4CAF50"
            }

            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.abspath(os.path.join(current_dir, '..', '..', "..", "assets", "html"))
            env = Environment(loader=FileSystemLoader(templates_dir))
            
            lender_template = env.get_template("lender_template.html")
            lender_html = lender_template.render(**lender_template_data)

            borrower_template = env.get_template("borrower_template.html")
            borrower_html = borrower_template.render(**borrower_template_data)
            
            borrower_mail = Mail(
                from_email="noreply@se-library.org",
                to_emails=transaction.borrower.email,
                subject="Borrow Request Approved",
                html_content=borrower_html,
            )
            lender_mail = Mail(
                from_email="noreply@se-library.org",
                to_emails=transaction.book_inventory.owner.email,
                subject="Borrow Request Approved",
                html_content=lender_html,
            )
            
            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = sg.send(lender_mail)
            response = sg.send(borrower_mail)
            return Result(error=False, message="Email sent successfully")
        except Exception as e:
            return Result(error=True, message=str(e))

    async def get_qrcode(self, transaction, db):
        """Should implement for requesting for QR code generation"""
        await asyncio.sleep(2)
        fake_base64 = None
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_dir = os.path.abspath(os.path.join(current_dir, '..', '..', "..", "assets", "static", "image.png"))
            with open(image_dir, 'rb') as image_file:
                fake_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                payload = {
                    "key": IMGBB_API_KEY,
                    "image": fake_base64,
                    "expiration": 500,
                    "name": "qrcode.png",
                }
                # Call the API to upload the image
                res = requests.post("https://api.imgbb.com/1/upload", data=payload)
                data = res.json().get("data")
                image_url = data.get("image").get("url")
                transaction.qr_code_image_link = image_url
                db.commit()
            return Result(error=False, message="QR Code generated successfully")
        except Exception as e:
            print(str(e))
            return Result(error=False, message=str(e))
