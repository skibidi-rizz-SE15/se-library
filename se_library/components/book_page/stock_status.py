import reflex as rx

def stock_status(remaining: int=0, actual: int=0, class_name:str ="") -> rx.Component:
    return rx.flex(
        rx.text("Remaining", class_name="font-Montserrat text-sm"),
        rx.text(f"{remaining}/{actual}", class_name="font-Valera text-xl font-semibold", color=rx.color_mode_cond(light=rx.color("indigo", 10), dark=rx.color("indigo", 9))),
        class_name=f"flex-col items-center w-full h-full {class_name}"
    )