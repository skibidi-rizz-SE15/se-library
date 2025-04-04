import reflex as rx
import os

class HomePageState(rx.State):
    """homepage state."""

class DrawerState(rx.State):
    """drawer state."""
    open: bool = False

    @rx.event
    def toggle_drawer(self) -> None:
        self.open = not self.open


class GoogleMaps(rx.NoSSRComponent):
    library = "@vis.gl/react-google-maps"
    tag = "Map"

    mapId: rx.Var[str] = "32206e377f7208e8"
    center: rx.Var[dict] = {"lat": 13.72923954932653, "lng": 100.77556859978873}
    zoom: rx.Var[int] = 16

class GoogleMapsAPI(rx.NoSSRComponent):
    library = "@vis.gl/react-google-maps"
    tag = "APIProvider"

    apiKey: rx.Var[str] = os.getenv("GOOGLE_MAPS_API")

class Marker(rx.NoSSRComponent):
    library = "@vis.gl/react-google-maps"
    tag = "AdvancedMarker"

    position: rx.Var[dict] = {"lat": 13.72923954932653, "lng": 100.77556859978873}

Map = GoogleMaps.create
APIProvider = GoogleMapsAPI.create
AdvancedMarker = Marker.create

def navbar() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.box(
                rx.text("SELibrary",
                        class_name="text-4xl text-[#253974] font-Outfit font-semibold"),
            ),
            rx.mobile_and_tablet(
                rx.drawer.root(
                    rx.drawer.trigger(rx.icon("menu", class_name="text-black cursor-pointer"), on_click=DrawerState.toggle_drawer),
                    rx.drawer.overlay(z_index="1"),
                    rx.drawer.portal(
                        rx.drawer.content(
                            rx.flex(
                                rx.link("About",
                                        href="#about",
                                        class_name="text-neutral-500 font-Roboto text-lg cursor-pointer",
                                        on_click=DrawerState.toggle_drawer),
                                rx.separator(),
                                rx.link("FAQs",
                                        href="#faqs",
                                        class_name="text-neutral-500 font-Roboto text-lg cursor-pointer",
                                        on_click=DrawerState.toggle_drawer),
                                rx.separator(),
                                rx.text("Contact",
                                        class_name="text-neutral-500 font-Roboto text-lg cursor-pointer",
                                        on_click=rx.set_clipboard("admin@domain.com")),
                                rx.separator(),
                                rx.flex(
                                    rx.button("Login",
                                            class_name="text-white rounded-md font-Roboto w-2/5 cursor-pointer",
                                            color_scheme="indigo",
                                            on_click=rx.redirect("/login")),
                                    rx.button("Close",
                                            class_name="font-Roboto cursor-pointer w-1/5",
                                            color_scheme="red",
                                            on_click=DrawerState.toggle_drawer,),
                                    class_name="w-full justify-evenly",
                                ),
                                class_name="flex-col w-full h-full items-center justify-evenly bg-white px-4",
                            ),
                            class_name="w-full h-[30%] bg-white",
                        )
                    ),
                    direction="top",
                    open=DrawerState.open,
                ),
            ),
            rx.desktop_only(
                rx.flex(
                    rx.text("About",
                            class_name="text-black font-Roboto cursor-pointer",
                            on_click=rx.scroll_to("about")),
                    rx.text("FAQs",
                            class_name="text-black font-Roboto cursor-pointer",
                            on_click=rx.scroll_to("faqs")),
                    rx.text("Contact",
                            class_name="text-black font-Robot cursor-pointer",
                            on_click=rx.scroll_to("contact")),
                    rx.button("Login",
                            class_name="text-white border border-black rounded-md px-6 py-4 ml-10 font-Roboto cursor-pointer",
                            color_scheme="indigo",
                            on_click=rx.redirect("/login")),
                    class_name="gap-10 w-full items-center px-4",
                ),
            ),
            class_name="justify-between w-10/12 items-center",
        ),
        class_name="justify-center w-full items-center py-2 mt-4",
    )

def hero():
    return rx.flex(
        rx.flex(
            rx.mobile_only(
                rx.flex(
                    rx.image(src="/static/numnan.png", placeholder="numnan", class_name="w-[12rem] h-[12rem]"),
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
            rx.tablet_only(
                rx.flex(
                    rx.image(src="/static/numnan.png", placeholder="numnan", class_name="w-[19rem] h-[20rem]"),
                    rx.text("Discover and Exchange Books", class_name="text-5xl font-Outfit font-semibold text-[#182449] w-4/5"),
                    rx.text("A seamless way to discover, borrow and exchange books", class_name="text-lg font-Roboto text-[#182449] w-4/5 mt-2"),
                    rx.flex(
                        rx.button("Borrow", class_name="text-white text-lg rounded-full px-4 py-2 font-Roboto cursor-pointer w-2/5 h-[3rem] bg-[#1F2D5C]"),
                        rx.button("Lend", class_name="text-[#1F2D5C] text-lg rounded-full px-4 py-2 font-Roboto cursor-pointer w-2/5 h-[3rem] bg-[#D6E1FF]"),
                        class_name="w-3/5 mt-8 justify-evenly",
                    ),
                    class_name="flex-col w-full h-full items-center justify-center mt-5",
                ),
            ),
            rx.desktop_only(
                rx.flex(
                    rx.flex(
                        rx.text("Discover and Exchange Books", class_name="break-normal text-8xl font-Outfit font-semibold text-[#182449] w-4/5"),
                        rx.text("A seamless way to discover, borrow and exchange books", class_name="text-2xl font-Roboto text-[#182449] w-4/5 mt-4"),
                        rx.flex(
                            rx.button("Borrow", class_name="text-white text-lg rounded-full px-4 py-2 font-Roboto cursor-pointer w-2/5 h-[3rem] bg-[#1F2D5C] hover:bg-[#25366E]"),
                            rx.button("Lend", class_name="text-[#1F2D5C] text-lg rounded-full px-4 py-2 font-Roboto cursor-pointer w-2/5 h-[3rem] bg-[#D6E1FF] hover:bg-[#ABB4E1]"),
                            class_name="w-3/5 mt-8 justify-evenly",
                        ),
                        class_name="w-3/5 h-2/5 items-start justify-center flex-col",
                    ),
                    rx.image(src="/static/numnan.png", placeholder="numnan", class_name="w-[30rem] h-[30rem]"),
                    class_name="w-full h-full justify-between items-center mt-36",
                ),
            ),
            class_name="w-10/12 h-[70%] items-center justify-center mt-10",
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
                            class_name="font-Roboto text-base text-[#182449] w-full mt-8"),
                    class_name="w-4/5 h-4/5 items-center justify-between",
                ),
                class_name="w-full h-4/5 items-center justify-center mt-60 flex-col",
            ),
            class_name="w-full"
        ),
        class_name="w-full h-1/5 items-center justify-center flex-col",
        id="about",
    )

def faqs() -> rx.Component:
    return rx.flex(
        rx.text("FAQs", class_name="font-Roboto text-4xl text-[#182449] font-semibold"),
        rx.mobile_only(
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
                                class_name="font-Roboto text-base text-[#182449] w-[18rem]"),
                        ),
                        side="bottom",
                        align="start",
                        size="1"
                    ),
                ),
                rx.popover.root(
                    rx.popover.trigger(
                        rx.text("Is SE-Library free to use?", class_name="font-Roboto text-lg text-[#182449] cursor-pointer mt-8"),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text(
                                "Yes, SE-Library is ",
                                rx.text.strong("free to use "),
                                "for all registered users. The platform aims to promote ",
                                rx.text.strong("knowledge-sharing "),
                                "within community without any charges for borrowing or lending books. However, ",
                                "penalties or retrictions may apply if users violate borrowing policies.",
                                class_name="font-Roboto text-base text-[#182449] w-[18rem]"),
                        ),
                    ),
                ),
                rx.popover.root(
                    rx.popover.trigger(
                        rx.text("What happens if a borrower doesn't return a book on time?", class_name="font-Roboto text-lg text-[#182449] cursor-pointer mt-8"),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text(
                                "If a borrower ",
                                rx.text.strong("does not return a book by the due date"),
                                " the system will send a bill of 150 THB per request. The book owner can receive the payment by reaching out to a contact listed in the footer below.",
                                class_name="font-Roboto text-base text-[#182449] w-[18rem]"
                            ),
                        ),
                    ),
                ),
                rx.popover.root(
                    rx.popover.trigger(
                        rx.text("How does the Smart Locker work?", class_name="font-Roboto text-lg text-[#182449] cursor-pointer mt-8"),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text(
                                "The ",
                                rx.text.strong("Smart Locker "),
                                "is an ",
                                "automated book handover system ",
                                "that helps manage pickers and returns. Here's how it works: ",
                                rx.list.unordered(
                                    rx.list.item(rx.text("When a borrow request is ", rx.text.strong("approved, "), "the book owner ", "places the book in the Smart Locker.")),
                                    rx.list.item(rx.text("The system generates a ", rx.text.strong("unique access code "), "for the borrower.")),
                                    rx.list.item(rx.text("The borrower receives a ", rx.text.strong("notification "), "with the ", rx.text.strong("locker location "), "and access code.")),
                                    rx.list.item(rx.text("The borrower enters the code at the Smart Locker to ", rx.text.strong("retrieve the book"))),
                                    rx.list.item(rx.text("When returning the book, the borrower places it back into the Smart Locker, and the system", rx.text.strong(" notifies the owner.")))
                                ),
                                class_name="font-Roboto text-base text-[#182449] w-[18rem]"
                            ),
                        )
                    )
                ),
                class_name="w-full h-1/5 items-start justify-start flex-col",
            ),
            class_name="w-4/5 mt-10",
        ),
        rx.tablet_and_desktop(
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
                                class_name="font-Roboto text-base text-[#182449] w-[18rem]"),
                        ),
                        side="bottom",
                        align="start",
                        size="1"
                    ),
                ),
                rx.popover.root(
                    rx.popover.trigger(
                        rx.text("Is SE-Library free to use?", class_name="font-Roboto text-lg text-[#182449] cursor-pointer mt-8"),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text(
                                "Yes, SE-Library is ",
                                rx.text.strong("free to use "),
                                "for all registered users. The platform aims to promote ",
                                rx.text.strong("knowledge-sharing "),
                                "within community without any charges for borrowing or lending books. However, ",
                                "penalties or retrictions may apply if users violate borrowing policies.",
                                class_name="font-Roboto text-base text-[#182449]"),
                        ),
                    ),
                ),
                rx.popover.root(
                    rx.popover.trigger(
                        rx.text("What happens if a borrower doesn't return a book on time?", class_name="font-Roboto text-lg text-[#182449] cursor-pointer mt-8"),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text(
                                "If a borrower ",
                                rx.text.strong("does not return a book by the due date"),
                                " the system will send a bill of 150 THB per request. The book owner can receive the payment by reaching out to a contact listed in the footer below.",
                                class_name="font-Roboto text-base text-[#182449]"
                            ),
                        ),
                    ),
                ),
                rx.popover.root(
                    rx.popover.trigger(
                        rx.text("How does the Smart Locker work?", class_name="font-Roboto text-lg text-[#182449] cursor-pointer mt-8"),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text(
                                "The ",
                                rx.text.strong("Smart Locker "),
                                "is an ",
                                "automated book handover system ",
                                "that helps manage pickers and returns. Here's how it works: ",
                                rx.list.unordered(
                                    rx.list.item(rx.text("When a borrow request is ", rx.text.strong("approved, "), "the book owner ", "places the book in the Smart Locker.")),
                                    rx.list.item(rx.text("The system generates a ", rx.text.strong("unique access code "), "for the borrower.")),
                                    rx.list.item(rx.text("The borrower receives a ", rx.text.strong("notification "), "with the ", rx.text.strong("locker location "), "and access code.")),
                                    rx.list.item(rx.text("The borrower enters the code at the Smart Locker to ", rx.text.strong("retrieve the book"))),
                                    rx.list.item(rx.text("When returning the book, the borrower places it back into the Smart Locker, and the system", rx.text.strong(" notifies the owner.")))
                                ),
                                class_name="font-Roboto text-base text-[#182449]"
                            ),
                        )
                    )
                ),
                class_name="w-full h-1/5 items-start justify-start flex-col",
            ),
            class_name="w-4/5 mt-10",
        ),
        class_name="w-full h-1/5 items-center justify-center flex-col mt-48",
        id="faqs",
    )

def footer() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            rx.flex(
                rx.text("© 2024 SE-Library. All rights reserved.", class_name="text-[#FDFDFD] font-Roboto text-xs"),
                class_name="w-full h-full justify-center items-center",
            ),
            class_name="w-full bg-[#182449] h-[2rem] justify-center mt-8",
        ),
        rx.desktop_only(
            rx.flex(
                rx.flex(
                    rx.text("SELibrary", class_name="text-[#FDFDFD] font-Outfit text-3xl font-semibold"),
                    rx.flex(
                        rx.text("Contact", class_name="text-[#FDFDFD] font-Roboto text-lg font-semibold"),
                        rx.text("rachata.pho@se-library.org", class_name="text-[#FDFDFD] font-Roboto text-sm cursor-pointer"),
                        rx.text("sorasich.ler@se-library.org", class_name="text-[#FDFDFD] font-Roboto text-sm cursor-pointer"),
                        rx.text("phattadon.sor@se-library.org", class_name="text-[#FDFDFD] font-Roboto text-sm cursor-pointer"),
                        class_name="w-fit h-full flex-col justify-evenly"
                    ),
                    rx.flex(
                        APIProvider(
                            Map(
                                AdvancedMarker(),
                                style={"width": "80%", "height": "80%"},
                                gestureHandling="greedy",
                                controlled="true",
                            ),
                        ),
                        class_name="w-2/5 h-full flex-col justify-evenly"
                    ),
                    class_name="w-4/5 h-full items-center justify-evenly",
                ),
                class_name="w-full h-full justify-center",
            ),
            class_name="w-full h-[10rem] bg-[#182449] mt-40",
        ),
        class_name="w-full",
        id="contact",
    )


@rx.page(route="/", title="SELibrary")
def homepage() -> rx.Component:
    return rx.flex(
        navbar(),
        hero(),
        about(),
        faqs(),
        footer(),
        class_name="w-full h-full min-h-screen bg-[#FDFDFD] flex-col justify-start",
    )