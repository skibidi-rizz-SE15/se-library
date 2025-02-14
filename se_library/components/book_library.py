import reflex as rx

# contains book cover, name, details, bla bla bla (dont set explicit height)
def book_slot(class_name: str="", has_quantity: bool=True) -> rx.Component:
    return rx.flex(
        rx.icon("book-copy", class_name="self-center border-2 w-full h-[20rem]"), # book cover
        rx.text("very extremely really long book name", class_name="font-semibold text-[1.1rem] leading-[1.2rem]"),
        rx.text("authorson authorman, auth von authorington", class_name="text-[#636363] text-[0.9rem] leading-[1.2rem]"),
        rx.text("[NUM] available", class_name=f"self-end text-[0.9rem] leading-[1.2rem] {'' if has_quantity else 'collapse'}"),
        class_name=f"flex-col gap-2 {class_name}"
    )

def book_display(class_name: str="") -> rx.Component:
    return rx.grid(
        book_slot(class_name="w-full"),
        book_slot(class_name="w-full"),
        book_slot(class_name="w-full"),
        book_slot(class_name="w-full"),
        book_slot(class_name="w-full"),
        book_slot(class_name="w-full"),
        book_slot(class_name="w-full"),
        book_slot(class_name="w-full"),
        book_slot(class_name="w-full"),
        book_slot(class_name="w-full"),
        class_name=f"grid grid-cols-[repeat(auto-fill,minmax(12rem,1fr))] gap-5 {class_name}"
    )

def genre_dropdown() -> rx.Component:
    return rx.flex(
        rx.text("Genre"),
        rx.select(
            ["All Books", "Python Books", "Rust Books"],  
            placeholder="Select a genre",  
            default_value="All Books",
            class_name="w-full p-2 border rounded-md cursor-pointer"
        ),
        class_name="items-center gap-2"
    )

def library_navbar() -> rx.Component:
    return rx.flex(
        rx.text("[TOPIC] Books", class_name="mr-auto font-bold text-xl"),
        genre_dropdown(),
        class_name="items-center"
    )

def book_library() -> rx.Component:
    return rx.flex(
        library_navbar(),
        book_display(),
        class_name="flex flex-col overflow-y-auto px-8 py-4 gap-8"
    )