import reflex as rx
from se_library.models import AvailabilityEnum, Book, BookInventory, ConditionEnum, User, BorrowStatusEnum, BookTransaction
from typing import List
from sqlalchemy.orm import Session
import asyncio
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from se_library.states.base import BaseState
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

class BookPageState(rx.State):
    authors: str = ""
    publisher: str = ""
    pages: int = 0
    isbn13: str = ""
    title: str = ""
    description: str = ""
    cover_image_link: str = ""
    is_book_exists: bool = False
    remaining: int = 0
    stock: List[BookInventory] = []
    available_condition: List[str] = []
    actual: int = 0

    @rx.event
    def reset_states(self):
        self.reset()

    @rx.event
    async def handle_on_load(self):
        """Should fetch database and reset state of all the other pages."""
        self.reset()
        self.isbn13 = self.router.page.params["isbn13"]
        with rx.session() as session:
            book = session.exec(
                Book.select().where(Book.isbn13 == self.isbn13)
            ).first()
            if book:
                self.authors = ", ".join([author.name for author in book.authors])
                self.publisher = book.publisher.name
                self.pages = book.pages
                self.isbn13 = book.isbn13
                self.title = book.title
                self.description = book.description
                self.cover_image_link = book.cover_image_link
                self.is_book_exists = True
                self.remaining = len(session.exec(
                    BookInventory.select().where(
                        BookInventory.book_id == book.id,
                        BookInventory.availability == AvailabilityEnum.AVAILABLE
                    )
                ).all())
                self.stock = session.exec(
                    BookInventory.select().where(
                        BookInventory.book_id == book.id
                    )
                ).all()
                for book in self.stock:
                    if len(self.available_condition) == len(ConditionEnum):
                        break
                    match book.condition:
                        case ConditionEnum.FACTORY_NEW:
                            if "Factory New" not in self.available_condition:
                                self.available_condition.append("Factory New")
                            else:
                                continue
                        case ConditionEnum.MINIMAL_WEAR:
                            if "Minimal Wear" not in self.available_condition:
                                self.available_condition.append("Minimal Wear")
                            else:
                                continue
                        case ConditionEnum.FIELD_TESTED:
                            if "Field Tested" not in self.available_condition:
                                self.available_condition.append("Field Tested")
                            else:
                                continue
                        case ConditionEnum.WELL_WORN:
                            if "Well Worn" not in self.available_condition:
                                self.available_condition.append("Well Worn")
                            else:
                                continue
                        case ConditionEnum.BATTLE_SCARRED:
                            if "Battle Scarred" not in self.available_condition:
                                self.available_condition.append("Battle Scarred")
                            else:
                                continue
                        case _:
                            continue
                self.actual = len(self.stock)
            else:
                self.is_book_exists = False

class result:
    error: bool = False
    message: str = ""

    def __init__(self, error: bool, message: str):
        self.error = error
        self.message = message

class BorrowDialogState(BookPageState):
    is_open: bool = False
    is_submitted: bool = False
    is_error: bool = False
    error_message: str = ""
    
    @rx.event
    def reset_states(self):
        self.reset()

    @rx.event
    async def handle_on_submit(self, form_data: dict):
        self.is_submitted = True
        yield
        await asyncio.sleep(1)
        result = await self.make_transaction(form_data.get("condition"))
        if result.error:
            self.is_submitted = False
            self.is_error = True
            self.error_message = result.message
            yield
            return
        self.is_submitted = False
        self.is_error = False
        self.error_message = ""
        yield rx.toast.success(result.message, position="top-center")
        self.is_open = False

    def condition_to_enum(self, condition: str) -> ConditionEnum:
        match condition:
            case "Factory New":
                return ConditionEnum.FACTORY_NEW
            case "Minimal Wear":
                return ConditionEnum.MINIMAL_WEAR
            case "Field Tested":
                return ConditionEnum.FIELD_TESTED
            case "Well Worn":
                return ConditionEnum.WELL_WORN
            case "Battle Scarred":
                return ConditionEnum.BATTLE_SCARRED
            case _:
                return None
            
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

    async def make_transaction(self, condition: str) -> result:
        if condition not in self.available_condition:
            return result(error=True, message="Please select a valid condition")
        try:
            with rx.session() as session:
                base_state = await self.get_state(BaseState)
                user = base_state.user
                res = await self.database_execute(db=session, condition=condition, user=user)
                if res.error:
                    raise Exception(res.message)
                res = await self.send_email(db=session, user=user)
                if res.error:
                    raise Exception(res.message)
                return result(error=False, message="Transaction successful")
        except Exception as e:
            return result(error=True, message=f"Error: {e}")
        
    async def database_execute(self, db: Session, condition: str, user: User):
        try:
            book_details = db.exec(
                Book.select().where(Book.isbn13 == self.isbn13)
            ).first()
            book_to_borrow = db.exec(
                BookInventory.select().where(
                    BookInventory.book_id == book_details.id,
                    BookInventory.availability == AvailabilityEnum.AVAILABLE,
                    BookInventory.condition == self.condition_to_enum(condition)
                )
            ).first()
            if not book_to_borrow:
                return result(error=True, message="Book not available")
            book_to_borrow.availability = AvailabilityEnum.UNAVAILABLE
            transaction = BookTransaction(
                borrower_id=user.id,
                book_inventory_id=book_to_borrow.id,
                borrow_status=BorrowStatusEnum.PENDING,
                duration=7,
                borrow_date=datetime.now(),
                return_date=datetime.now() + timedelta(days=7)
            )
            db.add(transaction)
            db.commit()
            return result(error=False, message="Transaction successful")
        except Exception as e:
            return result(error=True, message=f"{e}")
        
    async def send_email(self, db: Session, user: User):
        try:
            transaction = db.exec(
                BookTransaction.select().where(
                    BookTransaction.borrower_id == user.id,
                    BookTransaction.borrow_status == BorrowStatusEnum.PENDING
                ).order_by(BookTransaction.id.desc())
            ).first()
            book_to_borrow = db.exec(
                BookInventory.select().where(BookInventory.id == transaction.book_inventory_id)
            ).first()
            book_details = db.exec(
                Book.select().where(Book.id == book_to_borrow.book_id)
            ).first()
            owner = db.exec(
                User.select().where(User.id == book_to_borrow.owner_id)
            ).first()

            lender_template_data = {
                "company_name": "SE Library",
                "lender_name": owner.username,
                "borrow_request": True,
                "approval_success": False,
                "reject": False,
                "request_id": transaction.id,
                "borrower_name": user.username,
                "book_title": book_details.title,
                "book_condition": self.enum_to_condition(book_to_borrow.condition),
                "submission_date": transaction.borrow_date,
                "status": "Pending",
                "action_url": "http://localhost:3000/profile/transactions"
            }
            borrower_template_data = {
                "company_name": "SE Library",
                "borrower_name": user.username,
                "borrow_request": True,
                "request_status": False,
                "picked_up": False,
                "approved": False,
                "request_id": transaction.id,
                "lender_name": owner.username,
                "book_title": book_details.title,
                "book_condition": self.enum_to_condition(book_to_borrow.condition),
                "submission_date": transaction.borrow_date,
                "status": "Pending",
            }

            current_dir = os.path.dirname(os.path.join(os.path.abspath(__file__)))
            templates_dir = os.path.abspath(os.path.join(current_dir, '..', '..', "assets", "html"))
            
            env = Environment(loader=FileSystemLoader(templates_dir))
            lender_template = env.get_template("lender_template.html")
            borrower_template = env.get_template("borrower_template.html")

            lender_html = lender_template.render(**lender_template_data)
            borrower_html = borrower_template.render(**borrower_template_data)

            lender_mail = Mail(
                from_email="noreply@se-library.org",
                to_emails=owner.email,
                subject="Borrow Request",
                html_content=lender_html
            )
            borrower_mail = Mail(
                from_email="noreply@se-library.org",
                to_emails=user.email,
                subject="Borrow Request",
                html_content=borrower_html
            )

            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = sg.send(lender_mail)
            response = sg.send(borrower_mail)
            return result(error=False, message="Email sent")
        except Exception as e:
            return result(error=True, message=f"{e}")