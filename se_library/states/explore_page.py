import reflex as rx
from .registration_page_state import BookRegistrationPageState
from .book_page_state import BookPageState
from .base import BaseState
from se_library.models import AvailabilityEnum, Book, BookInventory
from typing import List
from pydantic import BaseModel

class BookDetails(BaseModel):
    id: int
    isbn13: str
    title: str
    authors: str
    image_src: str
    quantity: int
class ExplorePageState(rx.State):
    search_input: str = ""
    search_query: str = ""
    genre: str = "All Genres"
    sort_by: str = "Newest"
    is_all_selected: bool = True
    is_available_selected: bool = False
    books: List[Book] = []
    book_details: List[BookDetails] = []

    @rx.event
    def handle_search(self) -> None:
        self.search_query = "Result for: " + self.search_input

    @rx.event
    def handle_select_all(self) -> None:
        self.is_all_selected = True
        self.is_available_selected = False

    @rx.event
    def handle_select_available(self) -> None:
        self.is_all_selected = False
        self.is_available_selected = True

    @rx.event
    def handle_change_genre(self, genre: str) -> None:
        self.genre = genre

    def handle_on_load(self):
        yield BaseState.check_login()
        yield self.reset()
        yield self.load_books()
        yield BookRegistrationPageState.reset_states()
        yield BookPageState.reset_states()

    def load_books(self):
        with rx.session() as session:
            self.books = session.exec(
                Book.select()
            ).all()
            for book in self.books:
                quantity = len(session.exec(
                    BookInventory.select().where(
                        BookInventory.book_id == book.id,
                        BookInventory.availability == AvailabilityEnum.AVAILABLE
                    )
                ).all())
                self.book_details.append(BookDetails(
                    id=book.id, 
                    isbn13=book.isbn13,
                    title=book.title, 
                    authors=", ".join([author.name for author in book.authors]), 
                    image_src=book.cover_image_link,
                    quantity=quantity
                ))