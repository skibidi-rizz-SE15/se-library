import reflex as rx
from se_library.models import Book
from typing import List

class BookPageState(rx.State):
    authors: List[str] = []
    publisher: str = ""
    pages: int = 0
    isbn13: str = ""
    title: str = ""
    description: str = ""
    cover_image_link: str = ""

    @rx.event
    async def handle_on_load(self):
        """Should fetch database and reset state of all the other pages."""
        id = self.router.page.params["id"]
        with rx.session() as session:
            book = session.exec(
                Book.select().where(Book.id == id)
            ).first()
            self.authors = [author.name for author in book.authors]
            self.publisher = book.publisher.name
            self.pages = book.pages
            self.isbn13 = book.isbn13
            self.title = book.title
            self.description = book.description
            self.cover_image_link = book.cover_image_link
