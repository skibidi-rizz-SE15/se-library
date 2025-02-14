import reflex as rx

# contains book cover, name, details, bla bla bla (dont set explicit height)
def book_slot(class_name: str="") -> rx.Component:
    return rx.flex(
        rx.icon("book-copy", class_name="self-center border-2 w-full h-[20rem]"), # book cover
        rx.text("very extremely really long book name", class_name="font-semibold text-[1.1rem] leading-[1.2rem]"),
        rx.text("authorson authorman, auth von authorington", class_name="text-[#636363] text-[0.9rem] leading-[1.2rem]"),
        rx.text("[NUM] available", class_name="self-end text-[0.9rem] leading-[1.2rem]"),
        class_name=f"flex-col w-full gap-2 {class_name}"
    )

def book_display(class_name: str="", min_item_width=12) -> rx.Component:
    return rx.grid(
        book_slot(),
        book_slot(),
        book_slot(),
        book_slot(),
        book_slot(),
        book_slot(),
        book_slot(),
        book_slot(),
        book_slot(),
        book_slot(),
        book_slot(),
        book_slot(),
        class_name=f"grid grid-cols-[repeat(auto-fill,minmax({min_item_width}rem,1fr))] gap-5 {class_name}"
    )


def book_library(min_item_width=12) -> rx.Component:
    return rx.flex(
        book_display(min_item_width=min_item_width),
        class_name="flex flex-col overflow-y-auto px-2 py-4 gap-2 bg-[#FDFDFD] rounded-t-xl mt-4"
    )