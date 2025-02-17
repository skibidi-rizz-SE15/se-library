import reflex as rx
from ..state.registeration_page_state import BookRegisterationPageState
from .book_library import book_slot

class PatternFormat(rx.NoSSRComponent):
    library = "react-number-format"
    tag = "PatternFormat"

    format: rx.Var[str]
    mask: rx.Var[str]
    displayType: rx.Var[str] = "input"
    placeholder: rx.Var[str]
    name: rx.Var[str] = "raw_isbn"

def isbn_searchbar() -> rx.Component:
    return rx.flex(
        rx.text("ISBN-13", class_name="font-semibold text-sm"),
        PatternFormat(
            format="### # ### ##### #",
            placeholder="ISBN",
            name="raw_isbn",
            class_name="w-full rounded-md h-[30%] border border-gray-300 p-2",
        ),
        rx.text("Format: 978-X-XXXXXX-XX-X or 979-X-XXXXXX-XX-X", class_name="text-[0.7rem] text-gray-500 italic"),
        class_name="w-full h-[70%] flex-col space-y-2",
    )

def book_registeration_form() -> rx.Component:
    return rx.flex(
        rx.form(
            rx.text("Book Registeration", class_name="font-semibold text-xl self-center font-Roboto mb-2"),
            isbn_searchbar(),
            rx.button("Search", class_name="w-full h-[17%]"),
            on_submit=BookRegisterationPageState.handle_search,
            reset_on_submit=True,
            class_name="h-[12rem] max-w-[25rem] flex-col bg-[#FDFDFD] shadow-xl rounded-xl p-3 mt-4 border border-gray-300",
        ),
        class_name="w-full justify-center mb-4"
    )

def book_registeration_details() -> rx.Component:
    return rx.cond(
        BookRegisterationPageState.book_exists,
        rx.grid(
            book_slot(title=BookRegisterationPageState.title, authors=BookRegisterationPageState.get_formatted_authors, image_src=BookRegisterationPageState.cover_image_link, has_quantity=False, class_name="w-full"),
            rx.grid(
                rx.text("Name", class_name="font-semibold"),
                rx.text(BookRegisterationPageState.title),
                rx.text("ISBN", class_name="font-semibold"),
                rx.text(BookRegisterationPageState.isbn),
                rx.text("Publisher", class_name="font-semibold"),
                rx.text(BookRegisterationPageState.publisher),
                rx.text("Authors", class_name="font-semibold"),
                rx.text(BookRegisterationPageState.get_formatted_authors),
                rx.text("Description", class_name="font-semibold"),
                rx.text(BookRegisterationPageState.description, class_name="overflow-y-auto pr-1 max-h-[15rem]"),
                class_name="grid grid-cols-[minmax(5rem,max-content)_1fr] h-fit gap-4"
            ),
            # add condition dropdown
            rx.button("Lend Book", class_name="col-span-2 w-fit mx-auto px-4 py-2"),
            class_name="grid grid-cols-[minmax(10rem,25%)_1fr] w-full gap-x-4 gap-y-2 max-h-min overflow-hidden"
        ),
        rx.text("ISBN not found.", class_name="flex self-center")
    )