import reflex as rx
from se_library.states.profile_state import ProfileState

from ..components.navbar import navbar_desktop, navbar_mobile_tablet
from ..components.profile_dashboard import profile_dashboard

@rx.page("/profile", title="Profile", on_load=ProfileState.handle_on_load)
def profile() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            rx.flex(
                navbar_mobile_tablet(),
                class_name="w-svw h-svh"
            ),
        ),
        rx.desktop_only(
            rx.flex(
                navbar_desktop(),
                profile_dashboard(state=ProfileState),
                class_name="flex flex-col h-screen w-screen bg-neutral-300",
            ),
        ),
    )