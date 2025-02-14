import reflex as rx


def searchbar() -> rx.Component:
    return rx.flex(
        rx.icon("search", color="black", size=20),
        rx.input(class_name="w-[60%] rounded-xl h-[2.5rem]", placeholder="Search for books"),
        rx.button("Search", class_name="rounded-xl bg-[#3358D4] font-semibold font-Roboto text-lg text-white"),
        class_name="items-center gap-2 justify-center w-full h-[10%] mt-5",
    )