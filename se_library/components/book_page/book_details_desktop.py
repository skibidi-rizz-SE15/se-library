import reflex as rx
from .borrow_dialog import borrow_dialog
from .stock_status import stock_status
from .queue_status import queue_status
from .borrowed_status import borrowed_status
from .book_details_list import book_details_list
from .queue_duration_status import queue_duration_status
from se_library.states.book_page_state import BookPageState, BorrowDialogState

def book_details_desktop() -> rx.Component:
    return rx.grid(
        rx.cond(
            BookPageState.book_exists,
            content(),
            rx.text("Book not found", class_name="font-semibold font-Varela text-sm text-center", trim="normal")
        ),
        class_name="grid-cols-[2fr_3fr] mx-auto w-[max(35rem,70%)] h-fit gap-x-6 gap-y-4 p-4"
    )

def content() -> rx.Component:
    borrowed_amount = BookPageState.total_copies_amount - BookPageState.available_copies_amount

    return rx.fragment(
        rx.text(f"{BookPageState.title}", class_name="font-semibold col-span-2 font-Valera text-center text-2xl mb-2"),
        rx.flex(
            rx.image(src=BookPageState.cover_image_link, class_name="rounded-md shadow-lg w-full"),
            rx.text(f"By: {BookPageState.authors}", class_name="font-Valera text-gray-500"),
            class_name="flex-col gap-1 max-w-full"
        ),
        rx.grid(
            rx.grid(
                stock_status(remaining=BookPageState.available_copies_amount, actual=BookPageState.total_copies_amount),
                borrowed_status(borrowed_amount),
                class_name="grid-cols-[1fr_1fr] w-full gap-1"
            ),
            rx.separator(),
            book_details_list(isbn13=BookPageState.isbn13, publisher=BookPageState.publisher, pages=BookPageState.pages),
            borrow_dialog(
                state=BorrowDialogState,
                available_conditions=BookPageState.available_conditions,
                dialog_btn=rx.button(
                        "Borrow", 
                        class_name="flex justify-center px-8 py-2 disabled:bg-slate-400 h-fit w-fit mx-auto rounded-3xl text-white font-semibold cursor-pointer", 
                        disabled=BookPageState.is_out_of_stock,
                        background_color=rx.Color("indigo", 10),
                        on_click=BorrowDialogState.set_is_open(True)
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
    )
