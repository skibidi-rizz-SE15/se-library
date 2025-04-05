import reflex as rx
from se_library.states.profile_state import ProfileState

from ..components.navbar import navbar_desktop, navbar_mobile_tablet
from ..components.profile_dashboard import profile_dashboard

@rx.page("/profile", title="Profile", on_load=ProfileState.handle_on_load)
def profile() -> rx.Component:
    return rx.flex(
        # desktop version
        rx.flex(
            navbar_desktop(),
            rx.flex(
                profile_dashboard(),
                class_name="overflow-y-auto grow"
            ),
            class_name="flex flex-col h-screen w-screen",
        ),
    )