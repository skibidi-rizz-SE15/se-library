import reflex as rx

def queue_status(class_name:str ="") -> rx.Component:
    return rx.flex(
        rx.text("In Queue", class_name="font-Montserrat text-sm"),
        rx.text("2", class_name="font-Valera text-xl font-semibold", color=rx.color("indigo", 10)),
        class_name=f"flex-col items-center w-full h-full {class_name}"
    )