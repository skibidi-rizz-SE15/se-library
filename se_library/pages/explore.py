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
        rx.mobile_and_tablet(
            rx.flex(
                navbar_mobile_tablet(),
                searchbar(),
                sort_option_mobile_and_tablet(),
                rx.mobile_only(
                    book_library(min_item_width=5),
                ),
                rx.tablet_only(
                    book_library(min_item_width=10),
                ),
                class_name="w-svw h-svh flex flex-col",
            ),
        ),
        rx.desktop_only(
            rx.flex(
                navbar_desktop(),
                searchbar(),
                sort_option_desktop(),
                book_library(),
                class_name="flex flex-col h-screen w-screen",
            ),
        ),
    )
