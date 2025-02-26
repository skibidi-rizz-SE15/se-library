import reflex as rx
from se_library.models import AvailabilityEnum, Book, BookInventory, ConditionEnum
from typing import List
import asyncio

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

    async def make_transaction(self, condition: str) -> result:
        if condition not in self.available_condition:
            return result(error=True, message="Please select a valid condition")
        return result(error=False, message="Transaction successful")