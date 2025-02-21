import reflex as rx

def borrow_dialog(dialog_btn: rx.Component, class_name:str ="") -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(dialog_btn),
        rx.dialog.content(
            size="2",
            class_name=f"flex flex-col gap-4 w-[20rem] p-4 {class_name}"
        ),
    )