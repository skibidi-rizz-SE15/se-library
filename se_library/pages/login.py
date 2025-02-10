import reflex as rx

@rx.page("/login", title="Login")
def login_page():
    return rx.flex(
        rx.text("Coming soon...", class_name="text-8xl"),
        class_name="flex flex-col items-center justify-center h-screen w-screen"
    )