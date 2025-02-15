import reflex as rx

from ..components.navbar import navbar_desktop, navbar_mobile_tablet
from ..components.lend_form import lend_form, lend_confirmation_section

@rx.page("/lend", title="Lend a Book")
def lend_page() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            rx.flex(
                navbar_mobile_tablet(),
                class_name="w-svw h-svh"
            ),
        ),
        rx.desktop_only(
            rx.grid(
                navbar_desktop(class_name="h-fit"),
                rx.flex(
                    rx.flex(
                        rx.text("Lend a Book", class_name="font-bold text-xl mb-4 self-center"),
                        lend_form(),
                        rx.text("Selected Book", class_name="font-bold text-xl mb-4 self-center"),
                        lend_confirmation_section(),
                        class_name="flex-col gap-4 p-4 mx-auto bg-[#cecaca] w-[max(30rem,60%)] min-h-full h-max"
                    ),
                    class_name="w-full overflow-y-auto"
                ),
                class_name="grid-rows-[min-content_1fr] h-screen w-screen bg-neutral-300",
            ),
        ),
    )