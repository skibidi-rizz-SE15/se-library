import reflex as rx

# BOOK contains book cover, name, details, bla bla bla (dont set explicit height)

def book_display(class_name: str="") -> rx.Component:
    return rx.grid(
        rx.card(f"Card aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba aba ", class_name="w-full"),
        rx.card(f"Card 1\n2\n3\n4\n5\n6", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        rx.card(f"Card 1", class_name="w-full"),
        class_name=f"grid grid-cols-[repeat(auto-fill,minmax(12rem,1fr))] gap-5 {class_name}"
    )

def genre_dropdown() -> rx.Component:
    return rx.flex(
        rx.text("Genre"),
        rx.select(
            ["All Books", "Python Books", "Rust Books"],  
            placeholder="Select a genre",  
            default_value="All Books",
            class_name="w-full p-2 border rounded-md"
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
        class_name="flex flex-col p-4 gap-8"
    )