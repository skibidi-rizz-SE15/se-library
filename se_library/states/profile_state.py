import reflex as rx
from se_library.models import User, BookTransaction, Book, BorrowStatusEnum, BookInventory, Author, ConditionEnum, AvailabilityEnum
from se_library.states.base import BaseState
from pydantic import BaseModel
from sqlalchemy import or_
from sqlmodel import select, func
from typing import List

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
    lent_transactions: List[TransactionDetails] = []

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
        pass

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
                    BookTransaction.book_inventory_id.in_(lent_book_instance_ids)
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