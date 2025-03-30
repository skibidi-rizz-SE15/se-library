import asyncio
import asyncio.selector_events
import reflex as rx
from se_library.models import User, BookTransaction, Book, BorrowStatusEnum, BookInventory, Author, ConditionEnum, AvailabilityEnum
from se_library.states.base import BaseState
from pydantic import BaseModel
from sqlalchemy import or_
from sqlmodel import select, func
from typing import List, Dict, Tuple
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import requests
import base64
from cryptography.fernet import Fernet

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
BASE_URL = os.getenv("BASE_URL")

class BookDetails(BaseModel):
    title: str
    authors: str
    cover_image_link: str

class BookInventoryDetails(BaseModel):
    condition: str
    availability: str

    book_details: BookDetails
    owner: str

class TransactionDetails(BaseModel):
    id: int
    borrow_status: str
    duration: int
    borrow_date: str
    return_date: str

    book_inventory_details: BookInventoryDetails
    borrower: str
    approval_rate: float

class ProfileState(rx.State):
    user: User = None
    borrowed_transactions: List[TransactionDetails] = []
    pending_approvals: List[TransactionDetails] = []
    lent_transactions: List[Tuple[BookDetails, Dict[ConditionEnum, int]]] = []

    def get_formatted_authors(self, authors) -> str:
        return ", ".join(author.name for author in authors)

    def get_formatted_condition(self, condition: ConditionEnum) -> str:
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
                return "Unknown"

    def get_formatted_availability(self, availability: AvailabilityEnum) -> str:
        match availability:
            case AvailabilityEnum.AVAILABLE:
                return "Available"
            case AvailabilityEnum.RESERVED:
                return "Borrowed"
            case AvailabilityEnum.UNAVAILABLE:
                return "Unavailable"
            case _:
                return

    def get_formatted_borrow_status(self, borrow_status: BorrowStatusEnum) -> str:
        match borrow_status:
            case BorrowStatusEnum.BORROWED:
                return "Borrowed"
            case BorrowStatusEnum.APPROVED:
                return "Approved"
            case BorrowStatusEnum.REJECTED:
                return "Rejected"
            case BorrowStatusEnum.PENDING:
                return "Pending"
            case BorrowStatusEnum.RETURNED:
                return "Returned"
            case _:
                return "Unknown"

    def get_formatted_datetime(self, datetime) -> str:
        return datetime.strftime("%B %d, %Y")

    @rx.event
    async def handle_on_load(self):
        yield self.reset()
        await self.load_user()
        self.load_pending_approvals()
        self.load_lent_transactions()
        yield self.load_borrowed_transactions()

    async def load_user(self):
        base_state = await self.get_state(BaseState)
        self.user = base_state.user

    def load_borrowed_transactions(self):
        self.borrowed_transactions = []
        with rx.session() as db:
            transactions = db.exec(
                    BookTransaction.select().where(
                        BookTransaction.borrower_id == self.user.id,
                        or_(
                            BookTransaction.borrow_status == BorrowStatusEnum.BORROWED,
                            BookTransaction.borrow_status == BorrowStatusEnum.APPROVED,
                            BookTransaction.borrow_status == BorrowStatusEnum.PENDING
                        )
                    )
                ).all()
            for transaction in transactions:
                format_authors = self.get_formatted_authors(transaction.book_inventory.book.authors)
                book_details = BookDetails(
                    title=transaction.book_inventory.book.title,
                    authors=format_authors,
                    cover_image_link=transaction.book_inventory.book.cover_image_link,
                )
                book_inventory_details = BookInventoryDetails(
                    condition=self.get_formatted_condition(transaction.book_inventory.condition),
                    availability=self.get_formatted_availability(transaction.book_inventory.availability),
                    book_details=book_details,
                    owner=transaction.book_inventory.owner.username
                )
                transaction_details = TransactionDetails(
                    id=transaction.id,
                    borrow_status=self.get_formatted_borrow_status(transaction.borrow_status),
                    duration=transaction.duration,
                    borrow_date=self.get_formatted_datetime(transaction.borrow_date),
                    return_date=self.get_formatted_datetime(transaction.return_date),
                    book_inventory_details=book_inventory_details,
                    borrower=transaction.borrower.username,
                    approval_rate=-2
                )
                self.borrowed_transactions.append(transaction_details)

    def load_lent_transactions(self):
        self.lent_transactions = []
        with rx.session() as db:
            lent_books = db.exec(
                select(Book).join(BookInventory).where(
                    BookInventory.owner_id == self.user.id
                ).group_by(
                    Book.id
                )
            ).all()

            for lent_book in lent_books:
                conditions = db.exec(
                    select(BookInventory.condition).where(
                        BookInventory.book_id == lent_book.id
                    )
                ).all()

                condition_quantities = {
                    ConditionEnum.FACTORY_NEW: 0,
                    ConditionEnum.MINIMAL_WEAR: 0,
                    ConditionEnum.FIELD_TESTED: 0,
                    ConditionEnum.WELL_WORN: 0,
                    ConditionEnum.BATTLE_SCARRED: 0,
                }
                for condition in conditions:
                    condition_quantities[condition] += 1

                lent_book_details = BookDetails(
                    title=lent_book.title,
                    authors=self.get_formatted_authors(lent_book.authors),
                    cover_image_link=lent_book.cover_image_link
                )
                self.lent_transactions.append((lent_book_details, condition_quantities))

    def load_pending_approvals(self):
        self.pending_approvals = []
        with rx.session() as db:
            lent_book_instance_ids = db.exec(
                select(BookInventory.id).where(
                    BookInventory.owner_id == self.user.id
                )
            ).all()

            lent_book_instances = db.exec(
                BookTransaction.select().where(
                    BookTransaction.book_inventory_id.in_(lent_book_instance_ids),
                    BookTransaction.borrow_status == BorrowStatusEnum.PENDING
                )
            ).all()

            for lent_book in lent_book_instances:
                total_accepts = db.exec(
                    select(func.count(BookTransaction.id)).where(
                        BookTransaction.borrower_id == lent_book.borrower.id,
                        BookTransaction.borrow_status == BorrowStatusEnum.APPROVED
                    )
                ).one()
                total_rejections = db.exec(
                    select(func.count(BookTransaction.id)).where(
                        BookTransaction.borrower_id == lent_book.borrower.id,
                        BookTransaction.borrow_status == BorrowStatusEnum.REJECTED
                    )
                ).one()
                total_accepts_and_rejects = total_accepts + total_rejections
                accept_rate = total_accepts / total_accepts_and_rejects if total_accepts_and_rejects != 0 else -1

                format_authors = self.get_formatted_authors(lent_book.book_inventory.book.authors)
                book_details = BookDetails(
                    title=lent_book.book_inventory.book.title,
                    authors=format_authors,
                    cover_image_link=lent_book.book_inventory.book.cover_image_link,
                )
                book_inventory_details = BookInventoryDetails(
                    condition=self.get_formatted_condition(lent_book.book_inventory.condition),
                    availability=self.get_formatted_availability(lent_book.book_inventory.availability),
                    book_details=book_details,
                    owner=lent_book.book_inventory.owner.username
                )
                transaction_details = TransactionDetails(
                    id=lent_book.id,
                    borrow_status=self.get_formatted_borrow_status(lent_book.borrow_status),
                    duration=lent_book.duration,
                    borrow_date=self.get_formatted_datetime(lent_book.borrow_date),
                    return_date=self.get_formatted_datetime(lent_book.return_date),
                    book_inventory_details=book_inventory_details,
                    borrower=lent_book.borrower.username,
                    approval_rate=accept_rate
                )
                self.pending_approvals.append(transaction_details)

class Result:
    error: bool = False
    message: str = ""

    def __init__(self, error: bool, message: str):
        self.error = error
        self.message = message

class ConfirmDialogState(ProfileState):
    opened: bool = False
    is_loading: bool = False
    selected_id: int = 0

    @rx.event
    def dialog_open(self, id: int):
        self.opened = True
        self.selected_id = id

    @rx.event
    def dialog_close(self):
        self.opened = False

    @rx.event
    async def handle_on_approve(self, id: int):
        self.is_loading = True
        yield
        await asyncio.sleep(2)
        try:
            with rx.session() as db:
                transaction_db = db.exec(
                    BookTransaction.select().where(BookTransaction.id == id)
                ).first()
                if not transaction_db:
                    raise Exception
                if transaction_db.borrow_status != BorrowStatusEnum.PENDING:
                    raise Exception("Transaction is not pending")
                transaction_db.borrow_status = BorrowStatusEnum.APPROVED
                db.commit()
                res = await self.get_qrcode(transaction=transaction_db, db=db)
                if res.error:
                    print(res.message)
                    raise Exception(res.message)
                res = await self.send_email(transaction_id=transaction_db.id, db=db)
                if res.error:
                    print(res.message)
                    raise Exception(res.message)
                self.is_loading = False
                self.pending_approvals = [
                    transaction for transaction in self.pending_approvals if transaction.id != id
                ]
                yield rx.toast.info("Transaction successfully approved")
        except Exception as e:
            self.is_loading = False
            yield rx.toast.error(f"Failed to approve transaction: {str(e)}")

    @rx.event
    async def handle_on_reject(self):
        self.is_loading = True
        yield
        await asyncio.sleep(2)
        try:
            with rx.session() as db:
                transaction_db = db.exec(
                    BookTransaction.select().where(BookTransaction.id == self.selected_id)
                ).first()
                if not transaction_db:
                    raise Exception
                if transaction_db.borrow_status != BorrowStatusEnum.PENDING:
                    raise Exception("Transaction is not pending")
                transaction_db.borrow_status = BorrowStatusEnum.REJECTED
                transaction_db.book_inventory.availability = AvailabilityEnum.AVAILABLE
                db.commit()
                res = await self.send_email_to_borrower(db=db, transaction_id=self.selected_id)
                if res.error:
                    raise Exception(res.message)
            self.opened = False
            self.is_loading = False
            self.pending_approvals = [
                transaction for transaction in self.pending_approvals if transaction.id != self.selected_id
            ]
            yield rx.toast.info("Transaction successfully rejected")
        except Exception as e:
            self.opened = False
            self.is_loading = False
            print(str(e))
            yield rx.toast.error(f"Failed to reject transaction: {str(e)}")

    async def send_email_to_borrower(self, transaction_id: int, db):
        try:
            transaction_db = db.exec(
                BookTransaction.select().where(BookTransaction.id == transaction_id)
            ).first()
            if not transaction_db:
                return Result(error=True, message="Transaction not found")
            
            template_data = {
                "company_name": "SE Library",
                "borrower_name": transaction_db.borrower.username,
                "borrow_request": False,
                "request_status": True,
                "picked_up": False,
                "approved": False,
                "request_id": transaction_db.id,
                "lender_name": transaction_db.book_inventory.owner.username,
                "book_title": transaction_db.book_inventory.book.title,
                "book_condition": self.enum_to_condition(transaction_db.book_inventory.condition),
                "submission_date": transaction_db.borrow_date,
                "status": "Reject",
                "color": "#E53935"
            }

            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "assets", "html"))

            env = Environment(loader=FileSystemLoader(templates_dir))
            template = env.get_template("borrower_template.html")
            html_content = template.render(**template_data)
            mail = Mail(
                from_email="noreply@se-library.org",
                to_emails=transaction_db.borrower.email,
                subject="Borrow Request Reject",
                html_content=html_content
            )

            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            # res = sg.send(mail)
            return Result(error=False, message="")
        except Exception as e:
            return Result(error=True, message=str(e))
        
    async def send_email(self, transaction_id: int, db):
        try:
            transaction_db = db.exec(
                BookTransaction.select().where(BookTransaction.id == transaction_id)
            ).first()
            if not transaction_db:
                raise Exception("Transaction not found")
            
            key = os.getenv("SECRET_KEY")
            if not key:
                raise Exception
            cipher_suite = Fernet(key)
            transaction_id_hash = cipher_suite.encrypt(str(transaction_id).encode()).decode()
            
            lender_template_data = {
                "company_name": "SELibrary",
                "lender_name": transaction_db.book_inventory.owner.username,
                "borrow_request": False,
                "approval_succeed": True,
                "reject": False,
                "request_id": transaction_id,
                "borrower_name": transaction_db.borrower.username,
                "book_title": transaction_db.book_inventory.book.title,
                "book_condition": self.enum_to_condition(transaction_db.book_inventory.condition),
                "submission_date": transaction_db.borrow_date,
                "status": "Approved",
                "color": "#4CAF50",
                "qr_image": transaction_db.qr_code_image_link,
                "action_url": f"{BASE_URL}/confirm?q={transaction_id_hash}&role=lender"
            }
            borrower_template_data = {
                "company_name": "SELibrary",
                "borrower_name": transaction_db.borrower.username,
                "borrow_request": False,
                "request_status": True,
                "picked_up": False,
                "approved": True,
                "request_id": transaction_id,
                "lender_name": transaction_db.book_inventory.owner.username,
                "book_title": transaction_db.book_inventory.book.title,
                "book_condition": self.enum_to_condition(transaction_db.book_inventory.condition),
                "submission_date": transaction_db.borrow_date,
                "status": "Approved",
                "color": "#4CAF50"
            }

            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "assets", "html"))
            env = Environment(loader=FileSystemLoader(templates_dir))

            lender_template = env.get_template("lender_template.html")
            lender_html = lender_template.render(**lender_template_data)
            borrower_template = env.get_template("borrower_template.html")
            borrower_html = borrower_template.render(**borrower_template_data)

            lender_mail = Mail(
                from_email="noreply@se-library.org",
                to_emails=transaction_db.book_inventory.owner.email,
                subject="Borrow Request Approved",
                html_content=lender_html,
            )
            borrower_mail = Mail(
                from_email="noreply@se-library.org",
                to_emails=transaction_db.borrower.email,
                subject="Borrow Request Approved",
                html_content=borrower_html,
            )

            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            # res = sg.send(lender_mail)
            # res = sg.send(borrower_mail)
            return Result(error=False, message="Email sent successfully")
        except Exception as e:
            return Result(error=True, message=str(e))

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
                return "Unknown"
            
    async def get_qrcode(self, transaction, db):
        """Should implement for requesting for QR code generation"""
        await asyncio.sleep(2)
        fake_base64 = None
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_dir = os.path.abspath(os.path.join(current_dir, '..', '..', "assets", "static", "image.png"))
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
                if res.json().get("status") != 200:
                    print(res.status)
                    raise Exception("Failed to upload image")
                data = res.json().get("data")
                image_url = data.get("image").get("url")
                transaction.qr_code_image_link = image_url
                db.commit()
            return Result(error=False, message="QR Code generated successfully")
        except Exception as e:
            print(str(e))
            return Result(error=False, message=str(e))
