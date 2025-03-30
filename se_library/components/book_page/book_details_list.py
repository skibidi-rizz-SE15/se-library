import reflex as rx
from se_library.models import Publisher

def book_details_list(isbn13: str, publisher: str, pages: int) -> rx.Component:
    return rx.data_list.root(
            rx.data_list.item(
                rx.data_list.label("ISBN-13"),
                rx.data_list.value(rx.code(isbn13, variant="ghost")),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("Publisher"),
                rx.data_list.value(publisher),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("Pages"),
                rx.data_list.value(f"{pages} pages"),
                align="center",
            ),
            class_name="text-gray-400"
    )