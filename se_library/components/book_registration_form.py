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

def confirmation_dialog(dialog_button: rx.Component) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(dialog_button),
        rx.dialog.content(
            rx.dialog.title("Please choose the condition of your book"),
            rx.flex(
                rx.text("Condition:"),
                rx.select(["test1", "test2"]),
            ),
            rx.dialog.close(
                rx.button("Close Dialog", size="3"),
            ),
            class_name="flex flex-col items-center justify-center"
        ),
    )

def book_details_list() -> rx.Component:
    return rx.data_list.root(
            rx.data_list.item(
                rx.data_list.label("ISBN"),
                rx.data_list.value(rx.code(BookRegistrationPageState.isbn, variant="ghost")),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("ISBN-13"),
                rx.data_list.value(rx.code(BookRegistrationPageState.isbn13, variant="ghost")),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("Language"),
                rx.data_list.value(BookRegistrationPageState.language),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("Publisher"),
                rx.data_list.value(BookRegistrationPageState.publisher),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("Edition"),
                rx.data_list.value(BookRegistrationPageState.edition),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("Pages"),
                rx.data_list.value(BookRegistrationPageState.pages),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("Is Already Registered"),
                rx.data_list.value(rx.cond(BookRegistrationPageState.is_found_in_db, "Yes", "No")),
                align="center",
            ),
            class_name="text-gray-400"
    )

def book_registration_details_mobile_and_tablet() -> rx.Component:
    return rx.flex(
        rx.text(f"{BookRegistrationPageState.title}", class_name="font-semibold font-Varela text-sm text-center", trim="normal"),
        rx.image(src=BookRegistrationPageState.cover_image_link, class_name="max-w-[45rem] max-h-[35rem] w-[300px] mx-auto"),
        rx.text(f"By: {BookRegistrationPageState.get_formatted_authors}", class_name="text-center text-sm font-Varela text-gray-500"),
        confirmation_dialog(dialog_button=rx.flex("Lend Book", class_name="col-span-2 w-fit mx-auto px-8 py-2 mt-4 rounded-xl bg-[#F7F9FF] border-2 border-[#5472E4] text-[#5472E4] font-semibold cursor-pointer")),
        rx.separator(),
        rx.text("Details", class_name="text-xl text-gray-400 font-Varela mt-5 font-semibold"),
        book_details_list(),
        rx.separator(),
        rx.text("Description", class_name="text-xl text-gray-400 font-Varela mt-5 font-semibold"),
        rx.text(BookRegistrationPageState.description, class_name="text-sm text-gray-400 font-Varela text-justify"),
        class_name="w-svw h-fit flex-col bg-[#F7F9FF] border border-gray-300 rounded-xl mt-2 p-2 space-y-4",
    )

def book_registration_details() -> rx.Component:
    return rx.cond(
        BookRegistrationPageState.book_exists,
        rx.grid(
            book_slot(title=BookRegistrationPageState.title, authors=BookRegistrationPageState.get_formatted_authors, image_src=BookRegistrationPageState.cover_image_link, has_quantity=False, class_name="w-full"),
            rx.grid(
                rx.text("Title", class_name="font-semibold font-Roboto"),
                rx.text(BookRegistrationPageState.title, class_name="font-Varela text-gray-500"),
                rx.text("ISBN", class_name="font-semibold font-Roboto"),
                rx.code(BookRegistrationPageState.isbn, variant="ghost", color_scheme="gray"),
                rx.text("Publisher", class_name="font-semibold font-Roboto"),
                rx.text(BookRegistrationPageState.publisher, class_name="font-Varela text-gray-500"),
                rx.text("Authors", class_name="font-semibold font-Roboto"),
                rx.text(BookRegistrationPageState.get_formatted_authors, class_name="font-Varela text-gray-500"),
                rx.text("Description", class_name="font-semibold font-Roboto"),
                rx.text(BookRegistrationPageState.description, class_name="overflow-y-auto pr-1 max-h-[15rem] font-Varela text-gray-500"),
                class_name="grid grid-cols-[minmax(5rem,max-content)_1fr] h-fit gap-4"
            ),
            confirmation_dialog(dialog_button=rx.flex("Lend Book", class_name="col-span-2 w-fit mx-auto px-8 py-2 mt-4 rounded-xl bg-[#F7F9FF] border-2 border-[#5472E4] text-[#5472E4] font-semibold cursor-pointer")),
            class_name="grid grid-cols-[minmax(10rem,25%)_1fr] w-full gap-x-4 gap-y-2 max-h-min overflow-hidden border border-gray-300 rounded-xl p-4"
        ),
        rx.text("ISBN not found.", class_name="flex self-center")
    )