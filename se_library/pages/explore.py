import reflex as rx

from ..components.navbar import navbar

def explore() -> rx.Component:
    return rx.flex(
        navbar(),
        class_name="flex flex-col h-screen w-screen bg-neutral-300",
    )