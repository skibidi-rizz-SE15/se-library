import reflex as rx

from .borrow_dialog import borrow_dialog
from .book_details_list import book_details_list


def book_details_mobile_tablet() -> rx.Component:
    return rx.flex(
        rx.text(f"Practical Object-Oriented Design with UML (UK Higher Education Computing Computer Science)", class_name="font-semibold font-Varela text-sm text-center mt-2", trim="normal"),
        rx.image(src="/static/pok_uml.jpg", class_name="max-w-[45rem] max-h-[35rem] w-[300px] mx-auto rounded-sm shadow-md"),
        rx.text(f"By: Mark Priestley", class_name="text-center text-sm font-Varela text-gray-500"),
        rx.flex(
            borrow_dialog(dialog_btn=rx.flex("Reserve", class_name="col-span-2 w-fit mx-auto px-8 py-2 mt-4 rounded-xl bg-[#F7F9FF] border-2 border-[#5472E4] text-[#5472E4] font-semibold cursor-pointer")),
            borrow_dialog(dialog_btn=rx.flex("Borrow", class_name="col-span-2 w-[60%] justify-center mx-auto px-8 py-2 mt-4 rounded-xl text-white font-semibold cursor-pointer", background_color=rx.Color("indigo", 10))),
            class_name="w-full justify-between"
        ),
        rx.separator(),
        rx.text("Details", class_name="text-xl text-gray-400 font-Varela font-semibold"),
        book_details_list(),
        rx.separator(),
        rx.text("Description", class_name="text-xl text-gray-400 font-Varela font-semibold"),
        rx.text(
            "Provides an introduction to the design of object-oriented programs using UML. This book focuses on the application of UML in the development of software, and offers a tutorial to the UML notation and its application. The book is useful for undergraduates taking modules as part of a Computer Science or Software Engineering degree programme.",
                class_name="text-sm text-gray-400 font-Varela text-justify"),
        class_name="flex flex-col gap-4 p-2 h-svh",
    )