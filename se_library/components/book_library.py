import reflex as rx
from se_library.states.explore_page import ExplorePageState

def book_slot(isbn13: str, title: str, authors: str, image_src:str="", quantity: int=0, has_quantity: bool=False, class_name: str="") -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.cond(
                image_src,
                rx.image(src=image_src, alt="BOOK COVER", class_name="self-center shadow-lg max-h-[20rem] rounded-md mt-auto"),
                rx.icon("book-copy", class_name="self-center border-2 w-full h-[20rem] mt-auto"),
            ),
            class_name="self-center"
        ),
        rx.text(title, title=title, class_name="line-clamp-3 text-ellipsis font-semibold text-[14px] leading-[1.2rem] font-Varela"),
        rx.text(authors, class_name="text-gray-500 font-Varela text-[0.9rem] leading-[1.2rem]"),
        rx.text(f"{quantity} available", class_name=f"self-end mt-auto text-[0.9rem] leading-[1.2rem] {'' if has_quantity else 'collapse'}"),
        on_click=rx.redirect(f"/book?isbn13={isbn13}"),
        class_name=f"flex-col gap-2 {class_name} cursor-pointer"
    )

def book_display(class_name: str="", min_item_width=12) -> rx.Component:
    return rx.grid(
        query_result_display(class_name="col-span-full"),
        rx.foreach(ExplorePageState.book_details, lambda book: book_slot(book.isbn13, book.title, book.authors, book.image_src, book.quantity,has_quantity=True, class_name="w-full")),
        class_name=f"grid grid-cols-[repeat(auto-fill,minmax({min_item_width}rem,1fr))] gap-5 {class_name}"
    )


def book_library(min_item_width=12) -> rx.Component:
    return rx.flex(
        book_display(min_item_width=min_item_width),
        class_name="flex flex-col overflow-y-auto px-8 py-4 gap-2 rounded-t-xl grow",
        background_color=rx.color_mode_cond(light="#F7F9FF", dark="#11131F")
    )

def query_result_display(class_name="") -> rx.Component:
    return rx.cond(
        ExplorePageState.query_input,
        rx.flex(
            ExplorePageState.query_display,
            rx.text(
                "x", 
                on_click=ExplorePageState.reset_search_query,
                class_name="cursor-pointer peer px-2 rounded-full text-white bg-red-400 hover:bg-red-300"
            ),
            class_name=f"w-full gap-2 font-semibold text-lg {class_name}"
        )
    )