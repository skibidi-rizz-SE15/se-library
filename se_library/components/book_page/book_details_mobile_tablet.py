import reflex as rx

from .borrow_dialog import borrow_dialog
from .book_details_list import book_details_list
from se_library.states.book_page_state import BookPageState, BorrowDialogState
from .stock_status import stock_status
from .queue_status import queue_status
from .borrowed_status import borrowed_status
from .queue_duration_status import queue_duration_status

def book_details_mobile_tablet() -> rx.Component:
    return rx.flex(
        rx.cond(
            BookPageState.book_exists,
            content(),
            rx.text("Book not found", class_name="font-semibold font-Varela text-sm text-center", trim="normal")
        ),
        class_name="flex flex-col gap-4 px-2 py-4 h-max",
    )

def content() -> rx.Component:
    borrowed_amount = BookPageState.total_copies_amount - BookPageState.available_copies_amount

    return rx.fragment(
        rx.text(BookPageState.title, class_name="text-sm font-Varela font-semibold text-center"),
        rx.image(src=BookPageState.cover_image_link, class_name="max-w-[45rem] max-h-[35rem] w-[300px] mx-auto rounded-sm shadow-md"),
        rx.text(f"By: {BookPageState.authors}", class_name="text-sm font-Varela text-gray-500 text-center"),
        borrow_dialog(available_conditions=BookPageState.available_conditions, state=BorrowDialogState, dialog_btn=rx.flex("Borrow", class_name="col-span-2 w-fit justify-center mx-auto px-8 py-2 mt-4 rounded-xl text-white font-semibold cursor-pointer", background_color=rx.Color("indigo", 10))),
        rx.grid(
            stock_status(remaining=BookPageState.available_copies_amount, actual=BookPageState.total_copies_amount),
            borrowed_status(borrowed_amount),
            class_name="grid-cols-[1fr_1fr] w-full gap-1"
        ),
        rx.separator(),
        rx.text("Details", class_name="text-xl text-gray-400 font-Varela font-semibold"),
        book_details_list(isbn13=BookPageState.isbn13, publisher=BookPageState.publisher, pages=BookPageState.pages),
        rx.separator(),
        rx.text("Description", class_name="text-xl text-gray-400 font-Varela font-semibold"),
        rx.text(
            f"{BookPageState.description}",
            class_name="text-sm text-gray-400 font-Varela text-justify"
        ),
    )