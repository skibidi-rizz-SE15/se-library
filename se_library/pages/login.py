import reflex as rx

class LoginForm(rx.State):
    email: str = ""
    password: str = ""
    name: str = ""

    is_registered: bool = False

    @rx.event
    def handle_change_login_to_register(self):
        self.is_registered = not self.is_registered

    @rx.event
    def handle_login(self):
        print(f"Email: {self.email}, Password: {self.password}")
        return rx.redirect("/explore")
    
    @rx.event
    def handle_register(self):
        print(f"Name: {self.name}, Email: {self.email}, Password: {self.password}")
        return rx.redirect("/explore")

def login_form() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            rx.cond(
                LoginForm.is_registered,
                rx.flex(
                    rx.text("SELibrary", class_name="text-5xl font-semibold text-[#253974]"),
                    rx.vstack(
                        rx.text("Name", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                        rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", value=LoginForm.name, on_change=LoginForm.set_name),
                        rx.text("Email", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                        rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", value=LoginForm.email, on_change=LoginForm.set_email),
                        rx.text("Password", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                        rx.input(type="password", class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", value=LoginForm.password, on_change=LoginForm.set_password),
                        rx.box(
                            rx.button("Register", class_name="w-full h-10 bg-[#253974] text-white rounded-lg", on_click=LoginForm.handle_register),
                            rx.text("have an account?",rx.text.strong(" Sign up",class_name="italic", on_click=LoginForm.handle_change_login_to_register ), class_name="text-sm text-neutral-500 mt-5"),
                            class_name="w-full h-2/5 flex flex-col items-center justify-center",
                        ),
                        class_name="w-full h-3/4 mt-2",
                    ),
                    class_name="w-full h-full items-center flex-col",
                ),
                rx.flex(
                    rx.text("SELibrary", class_name="text-5xl font-semibold text-[#253974]"),
                    rx.vstack(
                        rx.text("Email", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                        rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", value=LoginForm.email, on_change=LoginForm.set_email),
                        rx.text("Password", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                        rx.input(type="password", class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", value=LoginForm.password, on_change=LoginForm.set_password),
                        rx.box(
                            rx.button("Login", class_name="w-full h-10 bg-[#253974] text-white rounded-lg", on_click=LoginForm.handle_login),
                            rx.text("Don't have an account?",rx.text.strong(" Sign up",class_name="italic", on_click=LoginForm.handle_change_login_to_register ), class_name="text-sm text-neutral-500 mt-5"),
                            class_name="w-full h-1/2 flex flex-col items-center justify-center",
                        ),
                        class_name="w-full h-3/4",
                    ),
                    class_name="w-full h-full items-center flex-col justify-evenly",
                ),
            ),
            class_name="w-4/5 h-2/3 bg-[#FDFDFD] rounded-lg shadow-lg p-4",
        ),
        rx.desktop_only(
            rx.flex(
                rx.text("SELibrary", class_name="text-5xl font-semibold text-[#253974]"),
                rx.vstack(
                    rx.text("Email", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2"),
                    rx.text("Password", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974] mt-4"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2"),
                    rx.box(
                        rx.button("Login", class_name="px-8 py-2 bg-[#253974] text-white rounded-lg"),
                        rx.text("Don't have an account?", rx.text.strong(" Sign up", class_name="italic"), class_name="text-sm text-neutral-500 mt-2"),
                        class_name="mt-8 mx-auto flex flex-col items-center justify-center",
                    ),
                    class_name="w-[max(10rem,60%)]",
                ),
                class_name="min-w-[30rem] w-[min(80%,60rem)] h-2/3 rounded-lg shadow-lg bg-[#FDFDFD] border-[#253974] border-[0.5rem] flex flex-col items-center justify-evenly p-8",
            ),
            class_name="contents",
        ),
        class_name="w-full h-full justify-center items-center bg-[#FDFDFD]",
    )

@rx.page("/login", title="Login")
def login_page():
    return rx.flex(
        login_form(),
        class_name="flex flex-col items-center justify-center h-screen w-screen bg-[#253974]"
    )