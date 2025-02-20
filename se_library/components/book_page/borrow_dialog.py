import reflex as rx

def borrow_dialog(dialog_btn: rx.Component) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(dialog_btn),
        rx.dialog.content(
            size="2",
            class_name="flex flex-col gap-4 w-[20rem] p-4"
        ),
    )