import reflex as rx
from se_library.states.explore_page import ExplorePageState
from se_library.models import Author
from typing import List

# contains book cover, name, details, bla bla bla (dont set explicit height)
def book_slot(isbn13: str, title: str, authors: str, image_src:str="", quantity: int=0, has_quantity: bool=False, class_name: str="") -> rx.Component:
    return rx.flex(
        rx.cond(
            image_src,
            rx.image(src=image_src, alt="BOOK COVER", class_name="self-center shadow-lg max-h-[20rem] rounded-md"),
            rx.icon("book-copy", class_name="self-center border-2 w-full h-[20rem]"),
        ),
        rx.text(title, class_name="font-semibold text-[14px] leading-[1.2rem] font-Varela"),
        rx.text(authors, class_name="text-gray-500 font-Varela text-[0.9rem] leading-[1.2rem]"),
        rx.text(f"{quantity} available", class_name=f"self-end text-[0.9rem] leading-[1.2rem] {'' if has_quantity else 'collapse'}"),
        on_click=rx.redirect(f"/book?isbn13={isbn13}"),
        class_name=f"flex-col gap-2 {class_name} cursor-pointer"
    )

def book_display(class_name: str="", min_item_width=12) -> rx.Component:
    return rx.grid(
        rx.foreach(ExplorePageState.book_details, lambda book: book_slot(book.isbn13, book.title, book.authors, book.image_src, book.quantity,has_quantity=True, class_name="w-full")),
        class_name=f"grid grid-cols-[repeat(auto-fill,minmax({min_item_width}rem,1fr))] gap-5 {class_name}"
    )


def book_library(min_item_width=12) -> rx.Component:
    return rx.flex(
        book_display(min_item_width=min_item_width),
        class_name="flex flex-col overflow-y-auto px-8 py-4 gap-2 rounded-t-xl mt-4 grow",
        background_color=rx.color_mode_cond(light="#F7F9FF", dark="#11131F")
    )