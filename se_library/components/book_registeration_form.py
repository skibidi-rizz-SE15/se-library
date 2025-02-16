import reflex as rx

class PatternFormat(rx.NoSSRComponent):
    library = "react-number-format"
    tag = "PatternFormat"

    format: rx.Var[str]
    mask: rx.Var[str]
    displayType: rx.Var[str] = "input"
    placeholder: rx.Var[str]


def isbn_searchbar() -> rx.Component:
    return rx.flex(
        rx.text("ISBN-13", class_name="font-semibold text-sm"),
        PatternFormat(
            format="### # ### ##### #",
            placeholder="ISBN",
            class_name="w-full rounded-md h-[30%] border border-gray-300 p-2",
        ),
        rx.text("Format: 978-X-XXXXXX-XX-X or 979-X-XXXXXX-XX-X", class_name="text-[0.7rem] text-gray-500 italic"),
        class_name="w-full h-[70%] flex-col space-y-2",
    )

def book_registeration_form() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text("Book Registeration", class_name="font-semibold text-xl self-center font-Roboto mb-2"),
            isbn_searchbar(),
            rx.button("Search", class_name="w-full h-[17%]"),
            class_name="h-[12rem] max-w-[25rem] flex-col bg-[#FDFDFD] shadow-xl rounded-xl p-3 mt-4 border border-gray-300",
        ),
        class_name="w-full justify-center mb-4"
    )