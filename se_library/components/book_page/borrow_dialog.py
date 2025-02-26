import reflex as rx

def borrow_dialog(dialog_btn: rx.Component, class_name:str ="") -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(dialog_btn),
        rx.dialog.content(
            rx.dialog.title(rx.text("Borrow Details", class_name="font-semibold font-Valera text-center text-lg")),
            rx.form(
                rx.flex(
                    rx.text("Select condition", class_name="font-semibold font-Valera"),
                    rx.select(
                        ["Factory New", "Minimal Wear", "Field Tested", "Well Worn", "Battle Scarred"],
                        class_name="w-[50%] p-2"
                    ),
                    class_name="flex flex-col gap-2 w-full mb-4"
                ),
                rx.button("Borrow", class_name="w-full text-white rounded-md p-2"),
            ),
            size="2",
            class_name=f"flex flex-col gap-4 w-[20rem] p-4 {class_name}"
        ),
    )