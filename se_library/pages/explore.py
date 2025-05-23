import reflex as rx

from ..components.navbar import navbar_desktop, navbar_mobile_tablet 
from ..components.searchbar import searchbar
from ..components.sort_option import sort_option_mobile_and_tablet, sort_option_desktop
from ..components.book_library import book_library
from se_library.states.base import BaseState
from se_library.states.explore_page import ExplorePageState

@rx.page("/explore", title="Explore", on_load=ExplorePageState.handle_on_load())
def explore():
    return rx.fragment(
        rx.cond(
            BaseState.logged_in,
            page(),
            rx.flex(),
        )
    )

def page() -> rx.Component:
    return rx.flex(
        # desktop only
        rx.flex(
            navbar_desktop(),
            rx.flex(
                sort_option_desktop(),
                searchbar(),
                class_name="flex-wrap-reverse gap-x-8 gap-y-4 p-4"
            ),
            book_library(),
            class_name="flex flex-col h-screen w-screen",
        ),
    )
