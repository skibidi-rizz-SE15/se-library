import reflex as rx
from se_library.states.base import BaseState
from reflex.style import toggle_color_mode

def profile_section() -> rx.Component:
    return rx.flex(
        rx.flex(rx.icon("circle-user-round", size=50), class_name="w-full justify-center"),
        rx.flex(
            rx.text("User", class_name="text-2xl font-semibold font-Outfit"),
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
        class_name="w-full h-fit items-center justify-center space-x-2",
        on_click=rx.redirect("/book-registration")
    )

def logout_menu() -> rx.Component:
    return rx.flex(
        rx.button(
            rx.icon("log-out", size=16),
            rx.text("Logout"),
            class_name="w-full h-1/4 text-left",
            color_scheme="red",
            variant="soft",
            on_click=BaseState.logout
        ),
        class_name="w-full h-1/4 items-center p-1"        
    )

class SwitchState(rx.State):
    is_on: bool = False

    @rx.event
    def toggle(self):
        self.is_on = not self.is_on
        


def toggle_color_mode_switch() -> rx.Component:
    return rx.flex(
        rx.icon("sun", color="#737373", size=16),
        rx.switch(on_change=SwitchState.toggle, checked=SwitchState.is_on, on_click=toggle_color_mode),
        rx.icon("moon", color="#737373", size=16),
        class_name="w-full h-1/4 items-center justify-center space-x-2",
    )

def menu_section() -> rx.Component:
    return rx.flex(
        profile_menu(),
        rx.separator(),
        add_book_menu(),
        class_name="w-full h-1/4 p-4 flex-col justify-evenly items-center"
    )

def drawer_content() -> rx.Component:
    return rx.flex(
        profile_section(),
        rx.separator(),
        menu_section(),
        rx.separator(),
        logout_menu(),
        toggle_color_mode_switch(),
        class_name="w-full h-full flex-col"
    )

def searchbar() -> rx.Component:
    return rx.flex(
        rx.icon("search", color="#FDFDFD", size=20),
        rx.input(class_name="w-[15rem]", placeholder="Search for books"),
        class_name="items-center gap-2 justify-center",
    )

def dark_mode_toggle() -> rx.Component:
    return rx.button(rx.icon("moon", color="#FDFDFD", size=20), class_name="cursor-pointer", on_click=toggle_color_mode)

def profile_menu_desktop() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.icon("circle-user-round", color="#FDFDFD", size=24, class_name="flex cursor-pointer"),
        ),
        rx.menu.content(
            rx.menu.item("Profile", on_click=rx.redirect("/profile"), class_name="cursor-pointer"),
            rx.separator(),
            rx.menu.item("Logout", on_click=BaseState.logout, color_scheme="red", class_name="cursor-pointer"),
        )
    )

def book_menu_desktop() -> rx.Component:
    return rx.menu.root(
            rx.menu.trigger(
                rx.icon("book-copy", color="#FDFDFD", size=24, class_name="flex cursor-pointer"),
            ),
            rx.menu.content(
                rx.menu.item("Borrow a book", class_name="cursor-pointer"),
                rx.separator(),
                rx.menu.item("Lend a book", on_click=rx.redirect("/book-registration"), class_name="cursor-pointer"),
            ),
        )

def navbar_desktop(class_name: str="") -> rx.Component:
    return rx.flex(
        rx.text(
            "SELibrary", 
            on_click=rx.redirect("/explore"), 
            class_name="mr-auto text-3xl font-semibold text-[#FDFDFD] font-Outfit cursor-pointer"
        ),
        dark_mode_toggle(),
        book_menu_desktop(),
        profile_menu_desktop(),
        class_name=f"w-full items-center justify-center drop-shadow-lg px-8 py-2 gap-6 rounded-b-md {class_name}",
        background_color=rx.color_mode_cond(light=rx.color("indigo", 10), dark=rx.color("indigo", 10))
    )

def navbar_mobile_tablet() -> rx.Component:
    return rx.flex(
        rx.text("SELibrary", class_name="text-3xl font-semibold text-[#FDFDFD] font-Outfit", on_click=rx.redirect("/explore")),
        rx.drawer.root(
            rx.drawer.trigger(rx.icon("menu", color="white", size=32)),
            rx.drawer.overlay(z_index="10"),
            rx.drawer.portal(
                rx.drawer.content(
                    drawer_content(),
                    class_name="w-[65%] h-full",
                    background_color=rx.color_mode_cond(light=rx.color("sage", 6), dark=rx.color("indigo", 1))
                ),
            ),
            direction="left",
        ),
        class_name="w-full h-fit items-center justify-between drop-shadow-lg p-2 rounded-b-md",
        background_color=rx.color_mode_cond(light=rx.color("indigo", 10), dark=rx.color("indigo", 10))
    )
