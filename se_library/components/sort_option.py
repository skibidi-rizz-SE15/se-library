import reflex as rx
from ..state.explore_page import ExplorePageState

def genre_dropdown() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(rx.button(rx.text(f"{ExplorePageState.genre}"), rx.icon("chevron-right", color="#3358D4"), class_name="rounded-xl bg-[#F7F9FF] text-[#3358D4] font-semibold font-Roboto text-lg")),
        rx.menu.content(
            rx.menu.item("All Genres", on_click=ExplorePageState.set_genre("All Genres")),
            rx.separator(),
            rx.menu.item("Fiction", on_click=ExplorePageState.set_genre("Fiction")),
            rx.separator(),
            rx.menu.item("Non-fiction", on_click=ExplorePageState.set_genre("Non-fiction")),
            rx.separator(),
            rx.menu.item("Mystery/Thriller", on_click=ExplorePageState.set_genre("Mystery/Thriller")),
            rx.separator(),
            rx.menu.item("Fantasy", on_click=ExplorePageState.set_genre("Fantasy")),
            rx.separator(),
            rx.menu.item("Science Fiction (Sci-Fi)", on_click=ExplorePageState.set_genre("Science Fiction (Sci-Fi)")),
            rx.separator(),
            rx.menu.item("Romance", on_click=ExplorePageState.set_genre("Romance")),
            rx.separator(),
            rx.menu.item("Historical Fiction", on_click=ExplorePageState.set_genre("Historical Fiction")),
            rx.separator(),
            rx.menu.item("Biography/Autobiography", on_click=ExplorePageState.set_genre("Biography/Autobiography")),
            rx.separator(),
            rx.menu.item("Self-Help/Personal Development", on_click=ExplorePageState.set_genre("Self-Help/Personal Development")),
            rx.separator(),
            rx.menu.item("Horror", on_click=ExplorePageState.set_genre("Horror")),
            class_name="rounded-xl"
        )
    )

def all_button() -> rx.Component:
    return rx.cond(
        ExplorePageState.is_all_selected,
        rx.button("All Books", class_name="rounded-xl bg-[#3358D4] font-semibold font-Roboto text-lg"),
        rx.button("All Books", class_name="rounded-xl bg-[#F7F9FF] text-[#3358D4] font-semibold font-Roboto text-lg", on_click=ExplorePageState.handle_select_all),
    )

def available_button() -> rx.Component:
    return rx.cond(
        ExplorePageState.is_available_selected,
        rx.button("Available Books", class_name="rounded-xl bg-[#3358D4] font-semibold font-Roboto text-lg"),
        rx.button("Available Books", class_name="rounded-xl bg-[#F7F9FF] text-[#3358D4] font-semibold font-Roboto text-lg", on_click=ExplorePageState.handle_select_available),
    )

def sort_by_dropdown() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(rx.button(rx.text(rx.text.strong("Sort By ", class_name="text-[#182449]"), f"{ExplorePageState.sort_by}"), rx.icon("chevron-down", color="#3358D4"), class_name="rounded-xl bg-[#F7F9FF] text-[#3358D4] font-semibold font-Roboto text-lg")),
        rx.menu.content(
            rx.menu.item("Newest", on_click=ExplorePageState.set_sort_by("Newest")),
            rx.separator(),
            rx.menu.item("Oldest", on_click=ExplorePageState.set_sort_by("Oldest")),
            rx.separator(),
            rx.menu.item("Publication Year First", on_click=ExplorePageState.set_sort_by("Publication Year First")),
            rx.separator(),
            rx.menu.item("Publication Year Last", on_click=ExplorePageState.set_sort_by("Publication Year Last")),
            rx.separator(),
            rx.menu.item("Title", on_click=ExplorePageState.set_sort_by("Title")),
            rx.separator(),
            rx.menu.item("Author", on_click=ExplorePageState.set_sort_by("Author")),
            rx.separator(),
            rx.menu.item("Popularity", on_click=ExplorePageState.set_sort_by("Popularity")),
            class_name="rounded-xl"
        ),
        class_name="self-end"
    )

def sort_option_desktop() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text("[Search Query] Books", class_name="font-bold text-xl text-[#182449]"),
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