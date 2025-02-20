import reflex as rx

from se_library.states.book_page_state import BookPageState
from se_library.components.book_page.book_details_mobile_tablet import book_details_mobile_tablet
from se_library.components.book_page.book_details_desktop import book_details_desktop
from se_library.components.navbar import navbar_mobile_tablet, navbar_desktop
from se_library.pages.homepage import footer

@rx.page("/book/[book_id]", on_load=BookPageState.handle_on_load)
def book_page() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            navbar_mobile_tablet(),
            book_details_mobile_tablet(),
            footer(),
        ),
        rx.desktop_only(
            rx.flex(
                navbar_desktop(),
                book_details_desktop(),
                class_name="flex-col h-full w-full",
            ),
        ),
        class_name="w-screen",
        background_color=rx.color_mode_cond(light="#F7F9FF", dark="#11131F")
    )