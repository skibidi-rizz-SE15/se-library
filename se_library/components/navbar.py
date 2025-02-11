import reflex as rx


def profile_section() -> rx.Component:
    return rx.flex(
        rx.flex(rx.icon("circle-user-round", color="black", size=50), class_name="w-full justify-center"),
        rx.flex(
            rx.text("User", class_name="text-2xl font-semibold text-[#253974] font-Outfit"),
            rx.text("Software Engineering", class_name="text-sm text-neutral-500 italic"),
            class_name="w-full h-1/2 justify-center flex-col"
        ),
        rx.flex(
            rx.badge("User", color_scheme="indigo", size="1", class_name="w-fit text-center"),
            rx.badge("Lender", color_scheme="indigo", size="1", high_contrast=True, class_name="w-fit text-center"),
            class_name="space-x-2"
        ),
        class_name="w-full h-1/4 p-4 flex-col"
    )

def search_menu() -> rx.Component:
    return rx.flex(
        rx.icon("search", color="#737373", size=16),
        rx.text("Search", class_name="text-lg text-neutral-500 font-Roboto"),
        class_name="w-full h-fit items-center justify-center space-x-2"
    )

def profile_menu() -> rx.Component:
    return rx.flex(
        rx.icon("user", color="#737373", size=16),
        rx.text("Profile", class_name="text-lg text-neutral-500 font-Roboto"),
        class_name="w-full h-fit items-center justify-center space-x-2"
    )

def add_book_menu() -> rx.Component:
    return rx.flex(
        rx.icon("book-copy", color="#737373", size=16),
        rx.text("Add Book", class_name="text-lg text-neutral-500 font-Roboto"),
        class_name="w-full h-fit items-center justify-center space-x-2"
    )

def logout_menu() -> rx.Component:
    return rx.flex(
        rx.button(
            rx.icon("log-out", size=16),
            rx.text("Logout"),
            class_name="w-full h-1/4 text-left",
            color_scheme="red",
            variant="soft",
        ),
        class_name="w-full h-1/4 items-center p-1"        
    )


def menu_section() -> rx.Component:
    return rx.flex(
        search_menu(),
        profile_menu(),
        add_book_menu(),
        class_name="w-full h-1/4 p-4 flex-col justify-between items-center"
    )

def drawer_content() -> rx.Component:
    return rx.flex(
        profile_section(),
        rx.separator(),
        menu_section(),
        rx.separator(),
        logout_menu(),
        class_name="w-full h-full flex-col"
    )

def searchbar() -> rx.Component:
    return rx.flex(
        rx.icon("search", color="#FDFDFD", size=20),
        rx.input(class_name="w-1/2 h-[60%]", placeholder="Search for books"),
        class_name="w-full h-full items-center space-x-2 justify-center"
    )

def profile_menu_desktop() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.icon("circle-user-round", color="#FDFDFD", size=24, class_name="cursor-pointer"),
        ),
        rx.menu.content(
            rx.menu.item("Profile"),
            rx.separator(),
            rx.menu.item("Logout", color_scheme="red"),
        )
    )

def navbar() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            rx.flex(
                rx.text("SELibrary", class_name="text-3xl font-semibold text-[#FDFDFD] font-Outfit"),
                rx.drawer.root(
                    rx.drawer.trigger(rx.icon("menu", color="white", size=32)),
                    rx.drawer.overlay(z_index="1"),
                    rx.drawer.portal(
                        rx.drawer.content(
                            drawer_content(),
                            class_name="w-[65%] bg-neutral-200 h-full",
                        ),
                    ),
                    direction="left"
                ),
                class_name="w-full h-full items-center justify-between p-2"
            ),
            class_name="w-full h-full"
        ),
        rx.desktop_only(
            rx.flex(
                rx.flex(
                    rx.text("SELibrary", class_name="text-3xl font-semibold text-[#FDFDFD] font-Outfit"),
                    class_name="w-1/4 justify-center items-center"
                ),
                rx.flex(
                    searchbar(),
                    class_name="w-1/2 h-full items-center"
                ),
                rx.flex(
                    rx.icon("book-copy", color="#FDFDFD", size=24, class_name="cursor-pointer"),
                    profile_menu_desktop(),
                    class_name="w-1/4 h-full items-center justify-around"
                ),
                class_name="w-full h-full"
            ),
            class_name="w-full h-full"
        ),
        
        class_name="w-full h-[8%] items-center drop-shadow-lg p-2 rounded-b-md bg-[#253974]",
    )