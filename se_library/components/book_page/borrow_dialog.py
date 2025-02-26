import reflex as rx

def borrow_dialog(available_condition: list[str], state, dialog_btn: rx.Component, class_name:str ="") -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(dialog_btn),
        rx.dialog.content(
            rx.dialog.title(rx.text("Borrow Details", class_name="font-semibold font-Valera text-center text-lg")),
            rx.form(
                rx.flex(
                    rx.text("Select condition", class_name="font-semibold font-Valera"),
                    rx.select(
                        available_condition,
                        name="condition",
                        disabled=state.is_submitted,
                        class_name="w-[50%] p-2"
                    ),
                    rx.cond(
                        state.is_error,
                        rx.text(state.error_message, class_name="text-red-500 text-sm")
                    ),
                    class_name="flex flex-col gap-2 w-full mb-4"
                ),
                rx.flex(
                    rx.button("Borrow", type="submit", class_name="w-full text-white rounded-md p-2", loading=state.is_submitted),
                    rx.button("Cancel", color_scheme="red", type="button", class_name="w-full text-white rounded-md p-2", on_click=state.reset_states, disabled=state.is_submitted),
                    class_name="flex flex-col gap-2 w-full"
                ),
                on_submit=state.handle_on_submit,
            ),
            size="2",
            class_name=f"flex flex-col gap-4 w-[20rem] p-4 {class_name}"
        ),
        open=state.is_open,
    )