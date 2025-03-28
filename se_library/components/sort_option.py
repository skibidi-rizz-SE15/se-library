import reflex as rx

from se_library.models import GenreEnum
from ..states.explore_page import ExplorePageState

def genre_dropdown() -> rx.Component:
    button_title = rx.cond(
        ExplorePageState.genre,
        rx.text(f"{ExplorePageState.get_formatted_genre}"),
        rx.text("All Genres")
    )

    return rx.menu.root(
        rx.menu.trigger(rx.button(button_title, rx.icon("chevron-right"), class_name="rounded-xl font-semibold font-Verela")),
        rx.menu.content(
            rx.menu.item("All Genres", on_click=ExplorePageState.handle_genre_selection(None)),
            rx.separator(),
            rx.menu.item("Programming Languages", on_click=ExplorePageState.handle_genre_selection(GenreEnum.PROGRAMMING_LANGUAGES)),
            rx.separator(),
            rx.menu.item("Design Patterns", on_click=ExplorePageState.handle_genre_selection(GenreEnum.DESIGN_PATTERNS)),
            rx.separator(),
            rx.menu.item("Software Architecture", on_click=ExplorePageState.handle_genre_selection(GenreEnum.SOFTWARE_ARCHITECTURE)),
            rx.separator(),
            rx.menu.item("DevOps", on_click=ExplorePageState.handle_genre_selection(GenreEnum.DEVOPS)),
            rx.separator(),
            rx.menu.item("Software Testing", on_click=ExplorePageState.handle_genre_selection(GenreEnum.SOFTWARE_TESTING)),
            rx.separator(),
            rx.menu.item("Project Management", on_click=ExplorePageState.handle_genre_selection(GenreEnum.PROJECT_MANAGEMENT)),
            rx.separator(),
            rx.menu.item("UX/UI", on_click=ExplorePageState.handle_genre_selection(GenreEnum.USER_EXPERIENCE)),
            rx.separator(),
            rx.menu.item("Security", on_click=ExplorePageState.handle_genre_selection(GenreEnum.SECURITY)),
            class_name="rounded-xl"
        )
    )

def all_button() -> rx.Component:
    return rx.cond(
        ExplorePageState.is_all_books,
        rx.button("All Books", class_name="rounded-xl font-Verela"),
        rx.color_mode_cond(
            light=rx.button("All Books", class_name="rounded-xl bg-white text-[#3358D4] font-Verela", on_click=ExplorePageState.handle_select_option(True)),
            dark=rx.button("All Books", class_name="rounded-xl bg-[#111113] text-[#FDFDFD] font-Verela", on_click=ExplorePageState.handle_select_option(True))
        )
    )

def available_button() -> rx.Component:
    return rx.cond(
        ExplorePageState.is_available_books,
        rx.button("Available Books", class_name="rounded-xl font-Verela"),
        rx.color_mode_cond(
            light=rx.button("Available Books", class_name="rounded-xl bg-white text-[#3358D4] font-Verela", on_click=ExplorePageState.handle_select_option(False)),
            dark=rx.button("Available Books", class_name="rounded-xl bg-[#111113] text-[#FDFDFD] font-Verela", on_click=ExplorePageState.handle_select_option(False))
        )
    )

def sort_by_dropdown() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.text(
                    rx.text.strong("Sort By ", class_name="font-Roboto font-semibold"),
                    f"{ExplorePageState.sort_by}",
                ),
                rx.icon("chevron-down"),
                class_name="rounded-xl font-Verela",
                color=rx.color_mode_cond(light=rx.color("indigo", 10), dark=rx.color("white")),
                background_color=rx.color_mode_cond(light=rx.color("white"), dark=rx.color("black"))
            )
        ),
        rx.menu.content(
            rx.menu.item("Title", on_click=ExplorePageState.handle_sort_by_option("Title")),
            rx.separator(),
            rx.menu.item("Highest Quantity", on_click=ExplorePageState.handle_sort_by_option("Highest Quantity")),
            rx.separator(),
            rx.menu.item("Lowest Quantity", on_click=ExplorePageState.handle_sort_by_option("Lowest Quantity")),
            class_name="rounded-xl"
        ),
        class_name="self-end"
    )

def sort_option_desktop() -> rx.Component:
    return rx.flex(
        genre_dropdown(),
        all_button(),
        available_button(),
        sort_by_dropdown(),
        class_name="items-center justify-end space-x-2"                
    )

def sort_option_mobile_and_tablet() -> rx.Component:
    return rx.flex(
            rx.flex(
                genre_dropdown(),
                class_name="items-center w-[80%] justify-evenly"                
            ),
            rx.flex(
                all_button(),
                available_button(),
                class_name="w-full items-center justify-evenly"
            ),
            sort_by_dropdown(),
            class_name="w-full h-[30%] items-center flex-col space-y-4 mt-4",
        )