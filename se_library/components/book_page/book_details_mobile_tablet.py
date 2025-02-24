import reflex as rx

from .borrow_dialog import borrow_dialog
from .book_details_list import book_details_list
from se_library.states.book_page_state import BookPageState

def author_name(name: str) -> rx.Component:
    return rx.text(f"{name}, ", class_name="font-Valera text-gray-500")

def book_details_mobile_tablet() -> rx.Component:
    return rx.flex(
        rx.text(f"{BookPageState.title}", class_name="font-semibold font-Varela text-sm text-center", trim="normal"),
        rx.image(src=BookPageState.cover_image_link, class_name="max-w-[45rem] max-h-[35rem] w-[300px] mx-auto rounded-sm shadow-md"),
        rx.text(f"By: {rx.foreach(BookPageState.authors, author_name)}", class_name="text-center text-sm font-Varela text-gray-500"),
        borrow_dialog(dialog_btn=rx.flex("Borrow", class_name="col-span-2 w-fit justify-center mx-auto px-8 py-2 mt-4 rounded-xl text-white font-semibold cursor-pointer", background_color=rx.Color("indigo", 10))),
        rx.separator(),
        rx.text("Details", class_name="text-xl text-gray-400 font-Varela font-semibold"),
        book_details_list(isbn13=BookPageState.isbn13, publisher=BookPageState.publisher, pages=BookPageState.pages),
        rx.separator(),
        rx.text("Description", class_name="text-xl text-gray-400 font-Varela font-semibold"),
        rx.text(
            f"{BookPageState.description}",
            class_name="text-sm text-gray-400 font-Varela text-justify"
        ),
        class_name="flex flex-col gap-4 px-2 py-4 h-max",
    )