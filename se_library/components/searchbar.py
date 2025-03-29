import reflex as rx
from ..states.explore_page import ExplorePageState

def searchbar() -> rx.Component:
    return rx.form(
        rx.icon("search", color="black", size=20),
        rx.input(class_name="flex grow rounded-xl h-[2.5rem]", name="search_query", placeholder="Search for books"),
        rx.input(type="submit", class_name="hidden"),
        rx.button("Search", class_name="rounded-xl bg-[#3358D4] font-semibold font-Roboto text-lg text-white"),
        on_submit=ExplorePageState.handle_search,
        reset_on_submit=True,
        # implicit w-100
        class_name="flex grow !w-auto items-center gap-2 justify-center",
    )