import reflex as rx

from ..components.navbar import navbar

@rx.page("/explore", title="Explore")
def explore() -> rx.Component:
    return rx.flex(
        navbar(),
        class_name="flex flex-col h-screen w-screen bg-neutral-300",
    )