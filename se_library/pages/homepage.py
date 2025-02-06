import reflex as rx

class HomePageState(rx.State):
    """homepage state."""

    ...

def navbar() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.box(
                rx.text("SELibrary",
                        class_name="text-2xl text-[#3E63DD] font-Outfit font-semibold"),
            ),
            rx.mobile_and_tablet(
                rx.drawer.root(
                    rx.drawer.trigger(rx.icon("menu", class_name="text-black cursor-pointer")),
                    rx.drawer.overlay(z_index="1"),
                    rx.drawer.portal(
                        rx.drawer.content(
                            rx.flex(
                                rx.text("About",
                                        class_name="text-neutral-500 font-Roboto text-lg cursor-pointer"),
                                rx.separator(),
                                rx.text("FAQs",
                                        class_name="text-neutral-500 font-Roboto text-lg cursor-pointer"),
                                rx.separator(),
                                rx.text("Contact",
                                        class_name="text-neutral-500 font-Roboto text-lg cursor-pointer"),
                                rx.separator(),
                                rx.button("Login",
                                        class_name="text-white border border-black rounded-md font-Roboto w-1/5 cursor-pointer",
                                        color_scheme="indigo"),
                                class_name="flex-col w-full h-full items-center justify-evenly bg-white px-4",
                            ),
                            class_name="w-full h-[30%] bg-white",
                        )
                    ),
                    direction="top"
                ),
            ),
            rx.desktop_only(
                rx.flex(
                    rx.text("Home",
                            class_name="text-black font-Roboto cursor-pointer"),
                    rx.text("About",
                            class_name="text-black font-Roboto cursor-pointer"),
                    rx.text("Contact",
                            class_name="text-black font-Robot cursor-pointer"),
                    rx.button("Login",
                            class_name="text-white border border-black rounded-md px-2 py-1 font-Roboto cursor-pointer",
                            color_scheme="indigo"),
                    class_name="justify-between w-full items-center px-4",
                ),
                class_name="w-2/5"
            ),
        class_name="justify-between w-10/12 items-center",
        ),
        class_name="justify-center w-full items-center py-2",
    )


@rx.page(route="/")
def homepage() -> rx.Component:
    return rx.flex(
        navbar(),
        class_name="w-full h-full min-h-screen bg-[#FDFDFD] flex-col justify-start py-4",
    )