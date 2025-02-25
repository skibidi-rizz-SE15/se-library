import reflex as rx
from .registration_page_state import BookRegistrationPageState
from .base import BaseState
from se_library.models import Book
from typing import List

class ExplorePageState(rx.State):
    search_input: str = ""
    search_query: str = ""
    genre: str = "All Genres"
    sort_by: str = "Newest"
    is_all_selected: bool = True
    is_available_selected: bool = False
    books: List[Book] = []

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
        yield BookRegistrationPageState.reset_states()
        yield self.load_books()

    def load_books(self):
        with rx.session() as session:
            self.books = session.exec(
                Book.select()
            ).all()
            for book in self.books:
                for author in book.authors:
                    print(author.name)