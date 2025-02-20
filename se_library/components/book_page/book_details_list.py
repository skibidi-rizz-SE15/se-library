import reflex as rx

def book_details_list() -> rx.Component:
    return rx.data_list.root(
            rx.data_list.item(
                rx.data_list.label("ISBN-13"),
                rx.data_list.value(rx.code("9780077103934", variant="ghost")),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("Publisher"),
                rx.data_list.value("McGraw-Hill Education"),
                align="center",
            ),
            rx.data_list.item(
                rx.data_list.label("Pages"),
                rx.data_list.value("372 pages"),
                align="center",
            ),
            class_name="text-gray-400"
    )