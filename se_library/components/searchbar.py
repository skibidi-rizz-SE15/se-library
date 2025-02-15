import reflex as rx
from ..state.explore_page import ExplorePageState

def searchbar() -> rx.Component:
    return rx.flex(
        rx.icon("search", color="black", size=20),
        rx.input(class_name="w-[60%] rounded-xl h-[2.5rem]", placeholder="Search for books", on_change=ExplorePageState.set_search_input),
        rx.button("Search", class_name="rounded-xl bg-[#3358D4] font-semibold font-Roboto text-lg text-white", on_click=ExplorePageState.handle_search),
        class_name="items-center gap-2 justify-center w-full h-[10%] mt-5",
    )