import reflex as rx
from se_library.models import BookTransaction, ConditionEnum, BorrowStatusEnum, AvailabilityEnum
import asyncio
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta
import hashlib

load_dotenv()

EMAIL = os.getenv("EMAIL")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
BASE_URL = os.getenv("BASE_URL")

class Result:
    error: bool = False
    message: str = ""

    def __init__(self, error: bool, message: str):
        self.error = error
        self.message = message

class ConfirmState(rx.State):
    confirming: bool
    is_success: bool
    is_borrower: bool

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
    async def handle_confirming(self):
        self.confirming = True
        self.is_success = False
        self.is_borrower = False
        yield
        await asyncio.sleep(10)
        try:
            role = self.router.page.params["role"]
            if role == "":
                raise Exception
            if role == "borrower":
                res = await self.confirming_return()
            else:
                res = await self.confirming_ready()
            if res.error:
                print(res.message)
                raise Exception
            self.is_success = True
            self.is_borrower = role == "borrower"
        except Exception as e:
            self.is_success = False
        self.confirming = False
        return

    async def confirming_return(self):
        key = os.getenv("SECRET_KEY")
        if not key:
            return Result(error=True, message="Secret key not found")
        cipher_suite = Fernet(key)
        token = self.router.page.params["q"]
        transaction_id = cipher_suite.decrypt(token.encode()).decode()
        with rx.session() as db:
            transaction = db.exec(
                BookTransaction.select().where(BookTransaction.id == transaction_id)
            ).first()
            if not transaction:
                return Result(error=True, message="Transaction not found")
            if transaction.borrow_status != "borrowed":
                return Result(error=True, message="Transaction not in borrowed status")
            if transaction.return_date < datetime.now():
                res = await self.send_billing_email(transaction=transaction)
                if res.error:
                    return res
            transaction.borrow_status = BorrowStatusEnum.RETURNED
            transaction.book_inventory.availability = AvailabilityEnum.AVAILABLE
            db.commit()
            res = await self.send_email_to_lender(transaction=transaction)
            if res.error:
                return res
        return Result(error=False, message="")

    async def send_email_to_lender(self, transaction):
        try:
            template_data = {
                "company_name": "SE Library",
                "lender_name": transaction.book_inventory.owner.username,
                "borrow_request": False,
                "approval_succeed": False,
                "pick_up": True,
                "request_id": transaction.id,
                "borrower_name": transaction.borrower.username,
                "book_title": transaction.book_inventory.book.title,
                "book_condition": self.enum_to_condition(transaction.book_inventory.condition),
                "submission_date": transaction.borrow_date,
                "status": "Returned",
                "color": "#9E9E9E",
                "qr_image": transaction.qr_code_image_link
            }

            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "assets", "html"))
            env = Environment(loader=FileSystemLoader(templates_dir))
            template = env.get_template("lender_template.html")
            html = template.render(**template_data)

            mail = Mail(
                from_email=EMAIL,
                to_emails=transaction.book_inventory.owner.email,
                subject="Book Return Confirmation",
                html_content=html
            )
            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = sg.send(mail)
            return Result(error=False, message="")
        except Exception as e:
            return Result(error=True, message=str(e))

    async def confirming_ready(self):
        key = os.getenv("SECRET_KEY")
        if not key:
            return Result(error=True, message="Secret key not found")
        cipher_suite = Fernet(key)
        token = self.router.page.params["q"]
        transaction_id = cipher_suite.decrypt(token.encode()).decode()
        with rx.session() as db:
            transaction = db.exec(
                BookTransaction.select().where(BookTransaction.id == transaction_id)
            ).first()
            if not transaction:
                return Result(error=True, message="Transaction not found")
            if transaction.borrow_status != "approved":
                return Result(error=True, message="Transaction not in approved status")
            transaction.borrow_status = BorrowStatusEnum.BORROWED
            db.commit()
            res = await self.send_email_to_borrower(transaction=transaction, cipher_suite=cipher_suite)
            if res.error:
                return res
        return Result(error=False, message="")

    async def send_email_to_borrower(self, transaction, cipher_suite):
        try:
            transaction_id = cipher_suite.encrypt(str(transaction.id).encode()).decode()
            template_data = {
                "company_name": "SE Library",
                "borrower_name": transaction.borrower.username,
                "lender_name": transaction.book_inventory.owner.username,
                "borrow_request": False,
                "request_status": False,
                "pick_up": True,
                "request_id": transaction.id,
                "lender_name": transaction.book_inventory.owner.username,
                "book_title": transaction.book_inventory.book.title,
                "book_condition": self.enum_to_condition(transaction.book_inventory.condition),
                "return_date": transaction.borrow_date,
                "status": "Borrowed",
                "color": "#4CAF50",
                "qr_image": transaction.qr_code_image_link,
                "action_url": f"{BASE_URL}/confirm?q={transaction_id}&role=borrower"
            }

            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "assets", "html"))
            env = Environment(loader=FileSystemLoader(templates_dir))
            template = env.get_template("borrower_template.html")
            html = template.render(**template_data)

            mail = Mail(
                from_email=EMAIL,
                to_emails=transaction.borrower.email,
                subject="Book Borrow Confirmation",
                html_content=html
            )
            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = sg.send(mail)
            return Result(error=False, message="")
        except Exception as e:
            return Result(error=True, message=str(e))
        
    async def send_billing_email(self, transaction):
        try:
            bill_id = self.hash_string_sha256_truncated(str(transaction.id))
            template_data = {
                "company_name": "SELibrary",
                "request_id": transaction.id,
                "lender_name": transaction.book_inventory.owner.username,
                "borrower_name": transaction.borrower.username,
                "title": transaction.book_inventory.book.title,
                "condition": self.enum_to_condition(transaction.book_inventory.condition),
                "borrow_date": transaction.borrow_date,
                "return_date": transaction.return_date,
                "status": "Returned",
                "color": "#FF9800",
                "hash_id": bill_id,
            }

            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "assets", "html"))
            env = Environment(loader=FileSystemLoader(templates_dir))
            template = env.get_template("billing_template.html")
            html = template.render(**template_data)

            mail = Mail(
                from_email=EMAIL,
                to_emails=transaction.borrower.email,
                subject="Billing Due to Return Delay",
                html_content=html
            )
            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = sg.send(mail)
            return Result(error=False, message="")
        except Exception as e:
            return Result(error=True, message=str(e))

    def hash_string_sha256_truncated(self, input_string, length=16):
        full_hash = hashlib.sha256(input_string.encode()).hexdigest()
        return full_hash[:length]
