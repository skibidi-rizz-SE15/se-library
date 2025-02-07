import reflex as rx

class HomePageState(rx.State):
    """homepage state."""

    ...

def navbar() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.box(
                rx.text("SELibrary",
                        class_name="text-4xl text-[#253974] font-Outfit font-semibold"),
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

def hero():
    return rx.flex(
        rx.flex(
            rx.mobile_and_tablet(
                rx.flex(
                    rx.image(src="/static/numnan.png", placeholder="numnan", class_name="w-[19rem] h-[20rem]"),
                    rx.text("Discover and Exchange Books", class_name="text-5xl font-Outfit font-semibold text-[#182449] w-4/5"),
                    rx.text("A seamless way to discover, borrow and exchange books", class_name="text-lg font-Roboto text-[#182449] w-4/5 mt-2"),
                    rx.flex(
                        rx.button("Borrow", class_name="text-white text-lg rounded-full px-4 py-2 font-Roboto cursor-pointer w-2/5 h-[3rem] bg-[#1F2D5C]"),
                        rx.button("Lend", class_name="text-[#1F2D5C] text-lg rounded-full px-4 py-2 font-Roboto cursor-pointer w-2/5 h-[3rem] bg-[#D6E1FF]"),
                        class_name="w-3/5 mt-8 justify-evenly",
                    ),
                    class_name="flex-col w-full h-full items-center justify-center",
                ),
            ),
            rx.desktop_only(
                rx.flex(
                    rx.flex(
                        rx.text("Discover and Exchange Books", class_name="text-8xl font-Outfit font-semibold text-[#182449] w-4/5"),
                        rx.text("A seamless way to discover, borrow and exchange books", class_name="text-2xl font-Roboto text-[#182449] w-4/5 mt-4"),
                        rx.flex(
                            rx.button("Borrow", class_name="text-white text-lg rounded-full px-4 py-2 font-Roboto cursor-pointer w-2/5 h-[3rem] bg-[#1F2D5C] hover:bg-[#25366E]"),
                            rx.button("Lend", class_name="text-[#1F2D5C] text-lg rounded-full px-4 py-2 font-Roboto cursor-pointer w-2/5 h-[3rem] bg-[#D6E1FF] hover:bg-[#ABB4E1]"),
                            class_name="w-3/5 mt-8 justify-evenly",
                        ),
                        class_name="w-3/5 h-2/5 items-start justify-center flex-col",
                    ),
                    rx.image(src="/static/numnan.png", placeholder="numnan", class_name="w-[30rem] h-[30rem]"),
                    class_name="w-full h-full justify-between items-center mt-16",
                ),
            ),
            class_name="w-10/12 h-[70%] items-center justify-center mt-20",
        ),
        class_name="w-full h-2/5 items-center justify-center flex-col",
    ),

def about() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            rx.flex(
                rx.text("About", class_name="font-Roboto text-4xl text-[#182449] font-semibold"),
                rx.text("SE-Library is a web-based platform designed to facilitate book sharing within the community. Members can register books they own, making them available for borrowing, while interested borrowers can request access. The system ensures a fair allocation of books by queueing requests and managing handovers through a Smart Locker (Por’s Project), streamlining the borrowing process. Owners have the flexibility to accept or reject requests, and administrators oversee operations to maintain a smooth experience and resolve disputes. SE-Library aims to foster a collaborative learning environment by making knowledge more accessible and promoting resource sharing among students.",
                        class_name="font-Roboto text-base text-[#182449] w-4/5 mt-4"),
                class_name="w-full h-4/5 items-center justify-center flex-col mt-48",
            )
        ),
        rx.desktop_only(
            rx.flex(
                rx.text("About", class_name="font-Roboto text-4xl text-[#182449] font-semibold"),
                rx.flex(
                    rx.text("SE-Library is a web-based platform designed to facilitate book sharing within the community. Members can register books they own, making them available for borrowing, while interested borrowers can request access. The system ensures a fair allocation of books by queueing requests and managing handovers through a Smart Locker (Por’s Project), streamlining the borrowing process. Owners have the flexibility to accept or reject requests, and administrators oversee operations to maintain a smooth experience and resolve disputes. SE-Library aims to foster a collaborative learning environment by making knowledge more accessible and promoting resource sharing among students.",
                            class_name="font-Roboto text-base text-[#182449] w-4/5 mt-4"),
                    class_name="w-4/5 h-4/5 items-center justify-between",
                ),
                class_name="w-full h-4/5 items-center justify-center mt-48 flex-col",
            ),
            class_name="w-full"
        ),
        class_name="w-full h-1/5 items-center justify-center flex-col",
    )

def faqs() -> rx.Component:
    return rx.flex(
        rx.text("FAQs", class_name="font-Roboto text-4xl text-[#182449] font-semibold"),
        rx.mobile_and_tablet(
            rx.flex(
                rx.popover.root(
                    rx.popover.trigger(
                        rx.text("Who can use SELibrary?", class_name="font-Roboto text-lg text-[#182449] cursor-pointer"),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text(
                                "SE-Library is designed for ",
                                rx.text.strong("Software Engineering students "),
                                "and ",
                                rx.text.strong("community members "),
                                "who want to ",
                                rx.text.strong("borrow and share books."),
                                " User can sign up as ",
                                rx.text.strong("borrowers, book owners, "),
                                "or ",
                                rx.text.strong("administrators"),
                                " who oversee system operations and dispute resolutions.",
                                class_name="font-Roboto text-base text-[#182449]"),
                        ),
                        side="bottom",
                        align="start",
                        size="1"
                        
                    ),
                ),
                class_name="w-full h-1/5 items-start justify-start flex-col",
            ),
            class_name="w-4/5 mt-10",
        ),
        class_name="w-full h-1/5 items-center justify-center flex-col mt-48",
    )


@rx.page(route="/")
def homepage() -> rx.Component:
    return rx.flex(
        navbar(),
        hero(),
        about(),
        faqs(),
        class_name="w-full h-full min-h-screen bg-[#FDFDFD] flex-col justify-start py-4",
    )