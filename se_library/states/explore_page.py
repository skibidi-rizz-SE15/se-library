import reflex as rx
from .registration_page_state import BookRegistrationPageState
from .book_page_state import BookPageState
from .base import BaseState
from se_library.models import AvailabilityEnum, Book, BookInventory, GenreEnum
from typing import List
from pydantic import BaseModel

class BookDetails(BaseModel):
    id: int
    isbn13: str
    title: str
    authors: str
    image_src: str
    quantity: int
    genre: GenreEnum

class ExplorePageState(rx.State):
    search_input: str = ""
    search_query: str = ""
    genre: str = None
    sort_by: str = "Title"
    is_all_books: bool = True
    is_available_books: bool = False
    books: List[Book] = []
    book_details: List[BookDetails] = []

    @rx.var(cache=False)
    def get_formatted_genre(self) -> str:
        match self.genre:
            case GenreEnum.PROGRAMMING_LANGUAGES:
                return "Programming Languages"
            case GenreEnum.DESIGN_PATTERNS:
                return "Design Patterns"
            case GenreEnum.SOFTWARE_ARCHITECTURE:
                return "Software Architecture"
            case GenreEnum.DEVOPS:
                return "DevOps"
            case GenreEnum.SOFTWARE_TESTING:
                return "Software Testing"
            case GenreEnum.PROJECT_MANAGEMENT:
                return "Project Management"
            case GenreEnum.USER_EXPERIENCE:
                return "UX/UI"
            case GenreEnum.SECURITY:
                return "Security"
            case _:
                return "All Genres"

    @rx.event
    def handle_search(self) -> None:
        self.search_query = "Result for: " + self.search_input

    @rx.event
    def handle_select_option(self, selects_all_books: bool):
        if selects_all_books:
            self.is_all_books = True
            self.is_available_books = False
        else:
            self.is_all_books = False
            self.is_available_books = True
        yield self.load_books()

    @rx.event
    def handle_genre_selection(self, genre: GenreEnum):
        self.genre = genre
        yield self.load_books()

    @rx.event
    def handle_sort_by_option(self, option: str):
        self.sort_by = option
        yield self.sort_books()

    def handle_on_load(self):
        yield BaseState.check_login()
        yield self.reset()
        yield self.load_books()
        yield self.sort_books()
        yield BookRegistrationPageState.reset_states()
        yield BookPageState.reset_states()

    def load_books(self):
        self.book_details = []
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

                book_detail = BookDetails(
                        id=book.id, 
                        isbn13=book.isbn13,
                        title=book.title, 
                        authors=", ".join([author.name for author in book.authors]), 
                        image_src=book.cover_image_link,
                        quantity=quantity,
                        genre=book.genre
                )
                if self.is_all_books and self.genre:
                    if book_detail.genre == self.genre:
                        self.book_details.append(book_detail)
                elif self.is_all_books:
                    self.book_details.append(book_detail)
                elif quantity > 0 and self.genre:
                    if book_detail.genre == self.genre:
                        self.book_details.append(book_detail)
                elif quantity > 0:
                    self.book_details.append(book_detail)

    def sort_books(self):
        match self.sort_by:
            case "Highest Quantity":
                self.book_details.sort(reverse=True, key=lambda book: book.quantity)
            case "Lowest Quantity":
                self.book_details.sort(key=lambda book: book.quantity)
            case "Title":
                self.book_details.sort(key=lambda book: book.title)
            case _:
                pass