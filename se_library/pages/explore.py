import reflex as rx

from ..components.navbar import navbar_desktop, navbar_mobile_tablet

@rx.page("/explore", title="Explore")
def explore() -> rx.Component:
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
                class_name="flex flex-col h-screen w-screen bg-neutral-300",
            ),
        ),
    )