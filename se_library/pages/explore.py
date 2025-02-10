import reflex as rx

def explore() -> rx.Component:
    return rx.flex(
        rx.text("Coming Soon", class_name="text-5xl font-semibold text-[#253974]"),
        class_name="w-full h-full items-center justify-center flex-col",
    )