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
        rx.menu.trigger(rx.button(button_title, rx.icon("chevron-right"), class_name="rounded-xl font-semibold font-Verela text-lg")),
        rx.menu.content(
            rx.menu.item("All Genres", on_click=ExplorePageState.set_genre(None)),
            rx.separator(),
            rx.menu.item("Programming Languages", on_click=ExplorePageState.set_genre(GenreEnum.PROGRAMMING_LANGUAGES)),
            rx.separator(),
            rx.menu.item("Design Patterns", on_click=ExplorePageState.set_genre(GenreEnum.DESIGN_PATTERNS)),
            rx.separator(),
            rx.menu.item("Software Architecture", on_click=ExplorePageState.set_genre(GenreEnum.SOFTWARE_ARCHITECTURE)),
            rx.separator(),
            rx.menu.item("DevOps", on_click=ExplorePageState.set_genre(GenreEnum.DEVOPS)),
            rx.separator(),
            rx.menu.item("Software Testing", on_click=ExplorePageState.set_genre(GenreEnum.SOFTWARE_TESTING)),
            rx.separator(),
            rx.menu.item("Project Management", on_click=ExplorePageState.set_genre(GenreEnum.PROJECT_MANAGEMENT)),
            rx.separator(),
            rx.menu.item("UX/UI", on_click=ExplorePageState.set_genre(GenreEnum.USER_EXPERIENCE)),
            rx.separator(),
            rx.menu.item("Security", on_click=ExplorePageState.set_genre(GenreEnum.SECURITY)),
            class_name="rounded-xl"
        )
    )

def all_button() -> rx.Component:
    return rx.cond(
        ExplorePageState.is_all_books,
        rx.button("All Books", class_name="rounded-xl font-Verela text-lg"),
        rx.color_mode_cond(
            light=rx.button("All Books", class_name="rounded-xl bg-white text-[#3358D4] font-Verela text-lg", on_click=ExplorePageState.handle_select_all),
            dark=rx.button("All Books", class_name="rounded-xl bg-[#111113] text-[#FDFDFD] font-Verela text-lg", on_click=ExplorePageState.handle_select_all)
        )
    )

def available_button() -> rx.Component:
    return rx.cond(
        ExplorePageState.is_available_books,
        rx.button("Available Books", class_name="rounded-xl font-Verela text-lg"),
        rx.color_mode_cond(
            light=rx.button("Available Books", class_name="rounded-xl bg-white text-[#3358D4] font-Verela text-lg", on_click=ExplorePageState.handle_select_available),
            dark=rx.button("Available Books", class_name="rounded-xl bg-[#111113] text-[#FDFDFD] font-Verela text-lg", on_click=ExplorePageState.handle_select_available)
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
                class_name="rounded-xl font-Verela text-lg",
                color=rx.color_mode_cond(light=rx.color("indigo", 10), dark=rx.color("white")),
                background_color=rx.color_mode_cond(light=rx.color("white"), dark=rx.color("black"))
            )
        ),
        rx.menu.content(
            rx.menu.item("Newest", on_click=ExplorePageState.set_sort_by("Newest")),
            rx.separator(),
            rx.menu.item("Oldest", on_click=ExplorePageState.set_sort_by("Oldest")),
            rx.separator(),
            rx.menu.item("Highest Quantity", on_click=ExplorePageState.set_sort_by("Highest Quantity")),
            rx.separator(),
            rx.menu.item("Lowest Quantity", on_click=ExplorePageState.set_sort_by("Lowest Quantity")),
            rx.separator(),
            rx.menu.item("Title", on_click=ExplorePageState.set_sort_by("Title")),
            class_name="rounded-xl"
        ),
        class_name="self-end"
    )

def sort_option_desktop() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(f"{ExplorePageState.search_query}", class_name="font-bold text-xl text-[#182449]"),
            class_name="w-[50%] h-full justify-start p-4"
        ),
        rx.flex(
            genre_dropdown(),
            all_button(),
            available_button(),
            sort_by_dropdown(),
            class_name="items-center w-[50%] h-full justify-end space-x-4 p-4"                
        ),
        class_name="w-full h-[10%] mt-4"
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