import reflex as rx
from se_library.models import AvailabilityEnum, Book, BookInventory
from typing import List

class BookPageState(rx.State):
    authors: List[str] = []
    publisher: str = ""
    pages: int = 0
    isbn13: str = ""
    title: str = ""
    description: str = ""
    cover_image_link: str = ""
    is_book_exists: bool = False
    remaining: int = 0
    actual: int = 0

    @rx.event
    async def handle_on_load(self):
        """Should fetch database and reset state of all the other pages."""
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
                self.actual = len(session.exec(
                    BookInventory.select().where(
                        BookInventory.book_id == book.id
                    )
                ).all())
            else:
                self.is_book_exists = False