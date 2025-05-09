import reflex as rx
from se_library.states.auth import AuthState

class LoginForm(AuthState):

    is_login_form: bool = True

    @rx.event
    def handle_switch_login_and_register(self):
        self.email = ""
        self.password = ""
        self.username = ""
        self.is_login_form = not self.is_login_form
        yield

def login_form() -> rx.Component:
    return rx.flex(
        rx.mobile_only(
            rx.flex(
                rx.text("SELibrary", class_name="text-5xl font-semibold text-[#253974]"),
                rx.vstack(
                    rx.cond(
                        # not AuthState.is_login_form
                        ~LoginForm.is_login_form,
                        rx.fragment(
                            rx.text("Username", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                            rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", value=AuthState.username, on_change=AuthState.set_username),
                        ),
                    ),
                    rx.text("Email", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", type="email", value=AuthState.email, on_change=AuthState.set_email),
                    rx.text("Password", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", type="password", value=AuthState.password, on_change=AuthState.set_password),
                    rx.cond(
                        LoginForm.is_login_form,
                        rx.box(
                            rx.button("Login", class_name="w-full h-10 bg-[#253974] text-white rounded-lg", on_click=AuthState.login),
                            rx.text("Don't have an account?",rx.text.strong(" Sign up",class_name="italic", on_click=LoginForm.handle_switch_login_and_register ), class_name="text-sm text-neutral-500 mt-5"),
                            class_name="w-full h-1/2 flex flex-col items-center justify-center",
                        ),
                        rx.box(
                            rx.button("Register", class_name="w-full h-10 bg-[#253974] text-white rounded-lg", on_click=AuthState.signup),
                            rx.text("Already have an account?",rx.text.strong(" Login",class_name="italic", on_click=LoginForm.handle_switch_login_and_register ), class_name="text-sm text-neutral-500 mt-5"),
                            class_name="w-full h-2/5 flex flex-col items-center justify-center",
                        ),
                    ),
                    class_name="w-full h-3/4 mt-2",
                ),
                class_name="w-full h-full items-center flex-col",
            ),
            class_name="min-w-[25rem] w-4/5 h-2/3 bg-[#FDFDFD] rounded-lg shadow-lg p-4",
        ),
        rx.tablet_and_desktop(
            rx.flex(
                rx.text("SELibrary", class_name="text-5xl font-semibold text-[#253974]"),
                rx.vstack(
                    rx.cond(
                        # not LoginForm.is_login_form
                        ~LoginForm.is_login_form,
                        rx.fragment(
                            rx.text("Username", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                            rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", value=AuthState.username, on_change=AuthState.set_username),
                        ), 
                    ),
                    rx.text("Email", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", type="email", value=AuthState.email, on_change=AuthState.set_email),
                    rx.text("Password", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974] mt-4"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", type="password", value=AuthState.password, on_change=AuthState.set_password),
                    rx.cond(
                        LoginForm.is_login_form,
                        rx.box(
                            rx.button("Login", class_name="px-8 py-2 bg-[#253974] text-white rounded-lg cursor-pointer", on_click=AuthState.login),
                            rx.text("Don't have an account?", rx.text.strong(" Sign up", class_name="italic cursor-pointer", on_click=LoginForm.handle_switch_login_and_register), class_name="text-sm text-neutral-500 mt-2"),
                            class_name="mt-8 mx-auto flex flex-col items-center justify-center",
                        ),
                        rx.box(
                            rx.button("Register", class_name="px-8 py-2 bg-[#253974] text-white rounded-lg cursor-pointer", on_click=AuthState.signup),
                            rx.text("Already have an account?", rx.text.strong(" Sign in", class_name="italic cursor-pointer", on_click=LoginForm.handle_switch_login_and_register), class_name="text-sm text-neutral-500 mt-2"),
                            class_name="mt-8 mx-auto flex flex-col items-center justify-center",
                        ),
                    ),
                    class_name="w-[max(10rem,60%)] mt-4",
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