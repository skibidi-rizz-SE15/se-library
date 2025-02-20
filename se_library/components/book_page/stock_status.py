import reflex as rx

def stock_status() -> rx.Component:
    return rx.flex(
        rx.text("Remaining", class_name="font-Montserrat text-sm"),
        rx.text("0/2", class_name="font-Valera text-xl font-semibold", color=rx.color_mode_cond(light=rx.color("indigo", 10), dark=rx.color("indigo", 9))),
        class_name="flex-col items-center w-full h-full"
    )