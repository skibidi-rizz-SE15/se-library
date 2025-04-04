import reflex as rx

def borrowed_status(borrowed_amount, class_name:str ="") -> rx.Component:
    return rx.flex(
        rx.text("Borrowed", class_name="font-Montserrat text-sm"),
        rx.text(borrowed_amount, class_name="font-Valera text-xl font-semibold", color=rx.color("indigo", 10)),
        class_name=f"flex-col items-center w-full h-full {class_name}"
    )