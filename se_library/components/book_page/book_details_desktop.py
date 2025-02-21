import reflex as rx
from .borrow_dialog import borrow_dialog
from .stock_status import stock_status
from .queue_status import queue_status
from .borrowed_status import borrowed_status
from .book_details_list import book_details_list
from .queue_duration_status import queue_duration_status

def book_details_desktop() -> rx.Component:
    return rx.grid(
        rx.text("Practical Object-Oriented Design with UML (UK Higher Education Computing Computer Science)", class_name="font-semibold col-span-2 font-Valera text-center text-2xl mb-2"),
        rx.flex(
            rx.image(src="/static/pok_uml.jpg", class_name="rounded-md shadow-lg w-full"),
            rx.text("By: Mark Priestley", class_name=" font-Valera text-gray-500"),
            class_name="flex-col gap-1 max-w-full"
        ),
        rx.grid(
            rx.grid(
                stock_status(),
                queue_status(),
                borrowed_status(),
                queue_duration_status(class_name="col-span-3 text-center"),
                class_name="grid-cols-[1fr_1fr_1fr] w-full gap-1"
            ),
            rx.separator(),
            book_details_list(),
            borrow_dialog(
                dialog_btn=rx.flex(
                    "Borrow", 
                    class_name="justify-center px-8 py-2 h-fit w-fit mx-auto rounded-3xl text-white font-semibold cursor-pointer", 
                    background_color=rx.Color("indigo", 10)
                )
            ),
            class_name="h-fit w-full gap-8"
        ),
        rx.separator(class_name="col-span-2"),
        rx.flex(
            rx.text("Description", class_name="font-Valera text-2xl text-gray-400 font-semibold"),
            rx.text(
                "Provides an introduction to the design of object-oriented programs using UML. This book focuses on the application of UML in the development of software, and offers a tutorial to the UML notation and its application. The book is useful for undergraduates taking modules as part of a Computer Science or Software Engineering degree programme.",
                class_name="font-Valera text-gray-400 text-justify"
            ),
            class_name="w-full flex-col col-span-2 space-y-4"
        ),

        class_name="grid-cols-[2fr_3fr] mx-auto w-[max(35rem,70%)] h-fit gap-x-6 gap-y-4 p-4"
    )
