import reflex as rx

class HomePageState(rx.State):
    """homepage state."""

    ...

def navbar() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.text("SELibrary",
                    class_name="text-2xl font-bold text-black")
        )
    )


@rx.page(route="/")
def homepage() -> rx.Component:
    return rx.flex(
        navbar(),
    )