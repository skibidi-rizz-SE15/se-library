import reflex as rx
from se_library.states.action_pages.confirm_state import ConfirmState

@rx.page("/confirm", on_load=ConfirmState.handle_confirming)
def confirm_page() -> rx.Component:
    return rx.fragment(
        rx.cond(
            ConfirmState.confirming,
            rx.flex(
                loading_scene(),
                class_name="w-screen h-screen"
            ),
            rx.flex(
                rx.cond(
                    ConfirmState.is_success,
                    message_box(True),
                    message_box(False),
                )
            )
        )
    )

def loading_scene():
    return rx.flex(
        rx.spinner(),
        rx.text("Approving...", class_name="text-lg font-bold ml-2"),
        class_name="w-full h-full justify-center items-center"
    )

def message_box(result: bool):
    return rx.card(
        rx.cond(
            result,
            rx.flex(
                rx.icon("check", color="green", size=64),
                rx.text("Success!", class_name="text-[2rem] font-bold font-sans"),
                rx.cond(
                    ConfirmState.is_borrower,
                    rx.text("You have been confirmed the return of the book. Thank you for your action", class_name="text-base text-center"),
                    rx.text("You have been confirmed the book is ready. Thank you for your action", class_name="text-base text-center"),
                ),
                rx.button("Back to Homepage", class_name="bg-blue-500 text-white py-6 px-4 rounded-md mt-4 text-lg font-bold"),
                class_name="w-full h-full justify-center items-center flex-col space-y-4",
            ),
            rx.flex(
                rx.icon("x", color="red", size=64),
                rx.text("Error!", class_name="text-[2rem] font-bold font-sans"),
                rx.text("There's some unexpected error happening", class_name="text-base text-center"),
                rx.button("Back to Homepage", class_name="bg-blue-500 text-white py-6 px-4 rounded-md mt-4 text-lg font-bold"),
                class_name="w-full h-full justify-center items-center flex-col space-y-4",
            ),
        ),
        class_name="w-2/5 p-10 min-h-1/2 m-auto shadow-lg"
    )