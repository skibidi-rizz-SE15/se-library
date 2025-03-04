import reflex as rx
from se_library.states.action_pages.approve_state import ApproveState

@rx.page("/approve", on_load=ApproveState.handle_approve)
def approve_page():
    return rx.text("Approve Page")