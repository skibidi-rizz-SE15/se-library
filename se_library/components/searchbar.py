import reflex as rx
from ..states.explore_page import ExplorePageState

def searchbar() -> rx.Component:
    return rx.flex(
        rx.icon("search", color="black", size=20),
        rx.input(class_name="flex grow rounded-xl h-[2.5rem]", placeholder="Search for books", on_change=ExplorePageState.set_search_input),
        rx.button("Search", class_name="rounded-xl bg-[#3358D4] font-semibold font-Roboto text-lg text-white", on_click=ExplorePageState.handle_search),
        class_name="grow items-center gap-2 justify-center",
    )