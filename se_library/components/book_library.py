import reflex as rx

# contains book cover, name, details, bla bla bla (dont set explicit height)
def book_slot(title: str, authors: str, quantity: int=0, image_src:str="", class_name: str="", has_quantity: bool=True) -> rx.Component:
    return rx.flex(
        rx.cond(
            image_src,
            rx.image(src=image_src, alt="BOOK COVER", class_name="self-center shadow max-h-[20rem] rounded-sm"),
            rx.icon("book-copy", class_name="self-center border-2 w-full h-[20rem]"),
        ),
        rx.text(title, class_name="font-semibold text-[1.1rem] leading-[1.2rem] font-Varela"),
        rx.text(authors, class_name="text-gray-500 font-Varela text-[0.9rem] leading-[1.2rem]"),
        rx.text(f"{quantity} available", class_name=f"self-end text-[0.9rem] leading-[1.2rem] {'' if has_quantity else 'collapse'}"),
        class_name=f"flex-col gap-2 {class_name}"
    )

def book_display(class_name: str="", min_item_width=12) -> rx.Component:
    return rx.grid(
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        book_slot(title="very extremely really long book name", authors="authorson authorman, auth von authorington", class_name="w-full"),
        class_name=f"grid grid-cols-[repeat(auto-fill,minmax({min_item_width}rem,1fr))] gap-5 {class_name}"
    )


def book_library(min_item_width=12) -> rx.Component:
    return rx.flex(
        book_display(min_item_width=min_item_width),
        class_name="flex flex-col overflow-y-auto px-8 py-4 gap-2 bg-[#FDFDFD] rounded-t-xl mt-4"
    )