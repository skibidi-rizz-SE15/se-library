import reflex as rx
from .borrow_dialog import borrow_dialog
from .stock_status import stock_status
from .queue_status import queue_status
from .borrowed_status import borrowed_status
from .book_details_list import book_details_list
from .queue_duration_status import queue_duration_status
from se_library.models import Author
from se_library.states.book_page_state import BookPageState

def author_name(name: str) -> rx.Component:
    return rx.text(f"{name}, ", class_name="font-Valera text-gray-500")

def book_details_desktop() -> rx.Component:
    return rx.grid(
        rx.text(f"{BookPageState.title}", class_name="font-semibold col-span-2 font-Valera text-center text-2xl mb-2"),
        rx.flex(
            rx.image(src=BookPageState.cover_image_link, class_name="rounded-md shadow-lg w-full"),
            rx.flex(
                rx.text("By: ", class_name="font-Valera text-gray-500"),
                rx.foreach(BookPageState.authors, author_name),
                class_name="max-w-full space-x-1"
            ),
            class_name="flex-col gap-1 max-w-full"
        ),
        rx.grid(
            rx.grid(
                stock_status(),
                queue_status(),
                borrowed_status(),
                queue_duration_status(class_name="col-span-3 text-center"),
                class_name="grid-cols-[1fr_1fr_1fr] w-full gap-1"
            ),
            rx.separator(),
            book_details_list(isbn13=BookPageState.isbn13, publisher=BookPageState.publisher, pages=BookPageState.pages),
            borrow_dialog(
                dialog_btn=rx.flex(
                    "Borrow", 
                    class_name="justify-center px-8 py-2 h-fit w-fit mx-auto rounded-3xl text-white font-semibold cursor-pointer", 
                    background_color=rx.Color("indigo", 10)
                )
            ),
            class_name="h-fit w-full gap-8"
        ),
        rx.separator(class_name="col-span-2"),
        rx.flex(
            rx.text("Description", class_name="font-Valera text-2xl text-gray-400 font-semibold"),
            rx.text(
                BookPageState.description,
                class_name="font-Valera text-gray-400 text-justify"
            ),
            class_name="w-full flex-col col-span-2 space-y-4"
        ),

        class_name="grid-cols-[2fr_3fr] mx-auto w-[max(35rem,70%)] h-fit gap-x-6 gap-y-4 p-4"
    )
