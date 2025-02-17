import reflex as rx

from ..components.navbar import navbar_desktop, navbar_mobile_tablet
from ..components.book_registeration_form import book_registeration_form, book_registeration_details

@rx.page("/book-registeration", title="Book Registeration")
def book_registeration_page() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            rx.flex(
                navbar_mobile_tablet(),
                book_registeration_form(),
                book_registeration_details(),
                class_name="w-svw h-svh flex-col bg-[#F7F9FF]",
            ),
        ),
        rx.desktop_only(
            rx.grid(
                navbar_desktop(class_name="h-fit"),
                rx.flex(
                    rx.flex(
                        rx.text("Lend a Book", class_name="font-bold text-xl mb-4 self-center"),
                        book_registeration_form(),
                        rx.text("Selected Book", class_name="font-bold text-xl mb-4 self-center"),
                        book_registeration_details(),
                        class_name="flex-col gap-4 p-4 mx-auto bg-[#cecaca] w-[max(30rem,60%)] min-h-full h-max"
                    ),
                    class_name="w-full overflow-y-auto"
                ),
                class_name="grid-rows-[min-content_1fr] h-screen w-screen bg-[#F7F9FF]",
            ),
        ),
    )