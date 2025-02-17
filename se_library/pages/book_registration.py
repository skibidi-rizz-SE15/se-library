import reflex as rx

from ..components.navbar import navbar_desktop, navbar_mobile_tablet
from ..components.book_registration_form import book_registration_form, book_registration_details, book_registration_details_mobile_and_tablet

@rx.page("/book-registration", title="Book registration")
def book_registration_page() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            rx.flex(
                navbar_mobile_tablet(),
                book_registration_form(),
                book_registration_details_mobile_and_tablet(),
                class_name="w-svw h-svh flex-col bg-[#F7F9FF]",
            ),
        ),
        rx.desktop_only(
            rx.grid(
                navbar_desktop(class_name="h-fit"),
                rx.flex(
                    rx.flex(
                        rx.text("Lend a Book", class_name="font-bold text-xl mb-4 self-center"),
                        book_registration_form(),
                        rx.text("Selected Book", class_name="font-bold text-xl mb-4 self-center"),
                        book_registration_details(),
                        class_name="flex-col gap-4 p-4 mx-auto bg-[#F7F9FF] w-[max(30rem,70%)] min-h-full h-max"
                    ),
                    class_name="w-full overflow-y-auto"
                ),
                class_name="grid-rows-[min-content_1fr] h-screen w-screen bg-[#F7F9FF]",
            ),
        ),
    )