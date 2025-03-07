import asyncio
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

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

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
                    borrow_status=self.get_formatted_borrow_status(lent_book.borrow_status),
                    duration=lent_book.duration,
                    borrow_date=self.get_formatted_datetime(lent_book.borrow_date),
                    return_date=self.get_formatted_datetime(lent_book.return_date),
                    book_inventory_details=book_inventory_details,
                    borrower=lent_book.borrower.username,
                    approval_rate=accept_rate
                )
                self.pending_approvals.append(transaction_details)

class ConfirmDialogState(ProfileState):
    opened: bool = False
    is_confirming: bool = False

    @rx.event
    def dialog_open(self):
        self.opened = True

    @rx.event
    def dialog_close(self):
        self.opened = False

    @rx.event
    async def handle_on_reject(self, transaction: TransactionDetails):
        self.is_confirming = True
        yield
        await asyncio.sleep(2)
        try:
            with rx.session() as db:
                transaction_db = db.exec(
                    BookTransaction.select().where(BookTransaction.id == transaction.id)
                ).first
                if not transaction_db:
                    raise Exception
                transaction_db.borrow_status = BorrowStatusEnum.REJECTED
                db.commit()
                res = await self.send_email_to_borrower(transaction=transaction)
                if res.error:
                    raise Exception
            self.opened = False
            self.is_confirming = False
            yield rx.toast.success("Transaction successfully rejected")
        except Exception as e:
            self.opened = False
            self.is_confirming = False
            yield rx.toast.error(f"Failed to reject transaction: {str(e)}")


    async def send_email_to_borrower(self, transaction: TransactionDetails):
        try:
            transaction_db = db.exec(
                BookTransaction.select().where(BookTransaction.id == transaction.id)
            ).first()
            if not transaction_db:
                return Result(error=True, message="Transaction not found")
            template_data = {
                "company_name": "SE Library",
                "borrower_name": transaction.borrower.username,
                "borrow_request": False,
                "request_status": True,
                "picked_up": False,
                "approved": False,
                "request_id": transaction.id,
                "lender_name": transaction.book_inventory.owner.username,
                "book_title": transaction.book_inventory.book.title,
                "book_condition": self.enum_to_condition(transaction.book_inventory.condition),
                "submission_date": transaction.borrow_date,
                "status": "Reject",
                "color": "#E53935"
            }

            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "assets", "html"))

            env = Enviroment(loader=FileSystemLoader(templates_dir))
            template = env.get_template("email_template.html")
            html_content = template.render(**template_data)
            mail = Mail(
                from_email="noreply@se-library.org",
                to_emails=transaction.borrower.email,
                subject="Borrow Request Reject",
                html_content=html_content
            )

            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            res = sg.send(mail)
            return Result(error=False, message="")
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
