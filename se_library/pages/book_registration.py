import reflex as rx

from ..components.navbar import navbar_desktop
from ..components.book_registration_form import book_registration_form, book_registration_details

@rx.page("/book-registration", title="Book Registration")
def book_registration_page() -> rx.Component:
    return rx.flex(
        rx.grid(
            navbar_desktop(class_name="h-fit"),
            rx.flex(
                rx.flex(
                    book_registration_form(),
                    book_registration_details(),
                    class_name="flex-col gap-4 p-4 mx-auto w-[max(30rem,70%)] min-h-full h-max"
                ),
                class_name="w-full overflow-y-auto"
            ),
            class_name="grid-rows-[min-content_1fr] h-screen w-screen",
        ),
    )