import reflex as rx
from ..states.registration_page_state import BookRegistrationPageState
from .book_library import book_slot

class PatternFormat(rx.NoSSRComponent):
    library = "react-number-format"
    tag = "PatternFormat"

    format: rx.Var[str]
    mask: rx.Var[str]
    displayType: rx.Var[str] = "input"
    placeholder: rx.Var[str]
    name: rx.Var[str] = "raw_isbn"

def book_registration_form() -> rx.Component:
    return rx.form(
        rx.text("Enter ISBN-13", class_name="font-semibold text-xl font-Roboto mb-2"),
        PatternFormat(
            format="### # ### ##### #",
            placeholder="XXX-X-XXXXXX-XX-X",
            name="raw_isbn",
            class_name="w-full rounded-md border border-gray-300 p-2",
        ),
        rx.button("Search", class_name="w-fit px-4 py-2 mt-auto"),
        on_submit=BookRegistrationPageState.handle_search,
        reset_on_submit=True,
        class_name="flex flex-col gap-4 items-center h-[12rem] max-w-[25rem] bg-[#FDFDFD] shadow-xl rounded-xl p-3 mx-auto border border-gray-300",
    )

def book_registration_details() -> rx.Component:
    return rx.cond(
        BookRegistrationPageState.book_exists,
        rx.grid(
            book_slot(title=BookRegistrationPageState.title, authors=BookRegistrationPageState.get_formatted_authors, image_src=BookRegistrationPageState.cover_image_link, has_quantity=False, class_name="w-full"),
            rx.grid(
                rx.text("Name", class_name="font-semibold"),
                rx.text(BookRegistrationPageState.title),
                rx.text("ISBN", class_name="font-semibold"),
                rx.text(BookRegistrationPageState.isbn),
                rx.text("Publisher", class_name="font-semibold"),
                rx.text(BookRegistrationPageState.publisher),
                rx.text("Authors", class_name="font-semibold"),
                rx.text(BookRegistrationPageState.get_formatted_authors),
                rx.text("Description", class_name="font-semibold"),
                rx.text(BookRegistrationPageState.description, class_name="overflow-y-auto pr-1 max-h-[15rem]"),
                class_name="grid grid-cols-[minmax(5rem,max-content)_1fr] h-fit gap-4"
            ),
            # add condition dropdown
            rx.button("Lend Book", class_name="col-span-2 w-fit mx-auto px-4 py-2"),
            class_name="grid grid-cols-[minmax(10rem,25%)_1fr] w-full gap-x-4 gap-y-2 max-h-min overflow-hidden"
        ),
        rx.text("ISBN not found.", class_name="flex self-center")
    )