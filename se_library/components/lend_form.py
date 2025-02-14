import reflex as rx
from typing import List
from enum import Enum
from .book_library import book_slot

class ConditionEnum(Enum):
    FACTORY_NEW = "factory_new"
    MINIMAL_WEAR = "minimal_wear"
    FIELD_TESTED = "field_tested"
    WELL_WORN = "well_worn"
    BATTLE_SCARRED = "battle_scarred"

class BookInfo(rx.State):
    name: str
    synopsis: str
    authors: List[str]
    publisher: str
    condition: ConditionEnum = ConditionEnum.FACTORY_NEW

def lend_form() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text("ISBN", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
            rx.input(placeholder="X-XX-XXXXXX-X", class_name="w-full h-10 border-2 border-[#253974] rounded-lg"),
            class_name="items-center gap-2"
        ),
        rx.button("Select Book", class_name="w-fit py-2 px-4 self-center border-2 border-[#111111]"),
        class_name="justify-center items-center gap-8"
    )

def lend_confirmation_section() -> rx.Component:
    return rx.grid(
        book_slot(has_quantity=False, class_name="w-full"),
        rx.grid(
            rx.text("Name", class_name="font-semibold"),
            rx.text("very extremely really long book name"),
            rx.text("Publisher", class_name="font-semibold"),
            rx.text("some publisher"),
            rx.text("Authors", class_name="font-semibold"),
            rx.text("authorson authorman, auth von authorington"),
            rx.text("Synopsis", class_name="font-semibold"),
            rx.text("long time ago in a galaxy far, far away..."),
            class_name="grid grid-cols-[fit-content(1rem)_1fr] h-fit gap-4"
        ),
        rx.button("Lend Book", class_name="col-span-2 self-center w-fit px-4 py-2"),
        class_name="grid grid-cols-[minmax(10rem,25%)_1fr] w-full gap-x-4 gap-y-2"
    )