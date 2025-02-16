import reflex as rx
from typing import List
from enum import Enum
from .book_library import book_slot
import requests
import json

class ConditionEnum(Enum):
    FACTORY_NEW = "factory_new"
    MINIMAL_WEAR = "minimal_wear"
    FIELD_TESTED = "field_tested"
    WELL_WORN = "well_worn"
    BATTLE_SCARRED = "battle_scarred"

class BookInfo(rx.State):
    name: str = ""
    description: str = ""
    authors: List[str] = []
    publisher: str = ""
    cover_image_link: str = ""
    isbn: str = ""
    condition: ConditionEnum = None

    does_exist: bool = None

    @rx.event
    def handle_submit_isbn(self, form_data: dict):
        formatted_isbn = self.get_formatted_isbn(form_data["raw_isbn"])
        self.isbn = formatted_isbn
        self.fill_details(formatted_isbn)

    def get_formatted_isbn(self, isbn):
        return isbn.strip().replace("-", "")

    @rx.event
    def fill_details(self, isbn):
        r = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers={
            "Host": "api2.isbndb.com",
            "User-Agent": "insomnia/5.12.4",
            "Authorization": "59216_fcf89c5986222e95f3c0a14ed62b61fb",
            "Accept": "*/*"
        })
        data_json = r.content
        data_dict = json.loads(data_json)
        
        if "book" in data_dict:
            self.does_exist = True

            book = data_dict["book"]
            self.name = book["title"]
            self.description = book["synopsis"].replace("<br/>", " ")
            self.authors = book["authors"]
            self.publisher = book["publisher"]
            self.cover_image_link = book["image"]
        else:
            self.does_exist = False
    
    @rx.var
    def get_formatted_authors(self) -> str:
        return ", ".join(self.authors)

def lend_form() -> rx.Component:
    return rx.form(
        rx.flex(
            rx.text("ISBN", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
            rx.input(placeholder="X-XX-XXXXXX-X", name="raw_isbn", class_name="w-full h-10 border-2 border-[#253974] rounded-lg"),
            class_name="items-center gap-2"
        ),
        rx.button("Select Book", class_name="w-fit py-2 px-4 self-center border-2 border-[#111111]"),
        on_submit=BookInfo.handle_submit_isbn,
        reset_on_submit=True,
        class_name="flex justify-center items-center gap-8"
    )

def lend_confirmation_section() -> rx.Component:
    return rx.cond(
        BookInfo.does_exist,
        rx.grid(
            book_slot(title=BookInfo.name, authors=BookInfo.get_formatted_authors, image_src=BookInfo.cover_image_link, has_quantity=False, class_name="w-full"),
            rx.grid(
                rx.text("Name", class_name="font-semibold"),
                rx.text(BookInfo.name),
                rx.text("ISBN", class_name="font-semibold"),
                rx.text(BookInfo.isbn),
                rx.text("Publisher", class_name="font-semibold"),
                rx.text(BookInfo.publisher),
                rx.text("Authors", class_name="font-semibold"),
                rx.text(BookInfo.get_formatted_authors),
                rx.text("Description", class_name="font-semibold"),
                rx.text(BookInfo.description, class_name="overflow-y-auto pr-1 max-h-[15rem]"),
                class_name="grid grid-cols-[minmax(5rem,max-content)_1fr] h-fit gap-4"
            ),
            # add condition dropdown
            rx.button("Lend Book", class_name="col-span-2 w-fit mx-auto px-4 py-2"),
            class_name="grid grid-cols-[minmax(10rem,25%)_1fr] w-full gap-x-4 gap-y-2 max-h-min overflow-hidden"
        ),
        rx.text("ISBN not found.", class_name="flex self-center")
    )