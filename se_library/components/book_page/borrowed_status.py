import reflex as rx

def borrowed_status() -> rx.Component:
    return rx.flex(
        rx.text("Borrowed", class_name="font-Montserrat text-sm"),
        rx.text("2", class_name="font-Valera text-xl font-semibold", color=rx.color_mode_cond(light=rx.color("indigo", 10), dark=rx.color("indigo",9))),
        class_name="flex-col items-center w-full h-full"
    )