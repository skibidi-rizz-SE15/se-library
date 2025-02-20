import reflex as rx
from .borrow_dialog import borrow_dialog
from .stock_status import stock_status
from .queue_status import queue_status
from .borrowed_status import borrowed_status
from .book_details_list import book_details_list

def book_details_desktop() -> rx.Component:
    return rx.box(
        rx.grid(
            rx.flex(
                rx.text("Practical Object-Oriented Design with UML (UK Higher Education Computing Computer Science)", class_name="font-semibold font-Valera text-center text-2xl"),
                rx.flex(
                    rx.image(src="/static/pok_uml.jpg", class_name="w-[45%] mx-auto rounded-md shadow-lg h-[550px]"),
                    rx.flex(
                        rx.text("By: Mark Priestley", class_name=" font-Valera text-gray-500 mb-[1rem]"),
                        rx.grid(
                            stock_status(),
                            queue_status(),
                            borrowed_status(),
                            class_name="grid-cols-[1fr_1fr_1fr] w-full"
                        ),
                        rx.separator(),
                        rx.flex(
                            book_details_list(),
                            rx.badge("Trusted by Dr. Visit", class_name="w-fit"),
                            class_name="w-full flex-col space-y-4"
                        ),
                        rx.flex(
                            borrow_dialog(dialog_btn=rx.flex("Reserve", class_name="w-fit px-8 py-2 rounded-3xl bg-[#F7F9FF] border-2 border-[#5472E4] text-[#5472E4] font-semibold cursor-pointer")),
                            borrow_dialog(dialog_btn=rx.flex("Borrow", class_name="w-[50%] justify-center px-8 py-2 rounded-3xl text-white font-semibold cursor-pointer", background_color=rx.Color("indigo", 10))),
                            class_name="w-full justify-center space-x-2"
                        ),
                        class_name="w-[55%] flex-col space-y-8"
                    ),
                    class_name="w-full space-x-2"
                ),
                rx.separator(),
                rx.flex(
                    rx.text("Synopsis", class_name="font-Valera text-2xl text-gray-400 font-semibold"),
                    rx.text(
                        "Provides an introduction to the design of object-oriented programs using UML. This book focuses on the application of UML in the development of software, and offers a tutorial to the UML notation and its application. The book is useful for undergraduates taking modules as part of a Computer Science or Software Engineering degree programme.",
                        class_name="font-Valera text-gray-400 text-justify"
                    ),
                    class_name="w-full flex-col space-y-4"
                ),
                class_name="w-full col-start-2 col-span-1 flex-col space-y-4"
            ),
            class_name="grid-cols-[minmax(0px,1fr)_minmax(900px,3fr)_minmax(0px,1fr)] h-full"
        ),
        class_name="w-full mx-auto mt-4 mb-[24px] px-[2rem]"
    )
