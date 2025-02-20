import reflex as rx

class BookPageState(rx.State):

    @rx.event
    def handle_on_load(self):
        """Should fetch database and reset state of all the other pages."""
        pass