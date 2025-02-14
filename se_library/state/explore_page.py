import reflex as rx

class ExplorePageState(rx.State):
    search_query: str = ""
    genre: str = "All Genres"
    sort_by: str = "Newest"
    is_all_selected: bool = True
    is_available_selected: bool = False

    @rx.event
    def handle_change_search_query(self, query: str) -> None:
        self.search_query = query

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