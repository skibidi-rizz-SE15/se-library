import reflex as rx
from ..models import User
from ..state.auth import AuthState
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class LoginForm(rx.State):
    email: str = ""
    password: str = ""
    name: str = ""

    is_login_form: bool = True
    error_message: str = ""
    
    def create_access_token(self, user_id: int) -> str:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now() + expires_delta
        
        to_encode = {
            "sub": str(user_id),
            "exp": expire
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @rx.event
    def handle_switch_login_and_register(self):
        self.email = ""
        self.password = ""
        self.name = ""
        self.error_message = ""
        self.is_login_form = not self.is_login_form
        yield

    @rx.event
    async def handle_login(self):
        """Handle user login."""
        try:
            with rx.session() as session:
                user = session.exec(
                    User.select().where(
                        User.email == self.email
                    )
                ).first()
                
                if not user or not user.verify_password(self.password):
                    self.error_message = "Invalid email or password"
                    return
                
                access_token = self.create_access_token(user.id)
                # Save token in local storage
                yield AuthState.set_token(access_token)
                
                # Clear form and redirect
                self.email = ""
                self.password = ""
                self.error_message = ""
                yield rx.redirect("/explore")
                
        except Exception as e:
            self.error_message = "An error occurred during login"
            print(f"Login error: {str(e)}")

    @rx.event
    async def handle_register(self):
        """Handle user registration."""
        try:
            if not all([self.name, self.email, self.password]):
                self.error_message = "All fields are required"
                return

            with rx.session() as session:
                existing_user = session.exec(
                    User.select().where(
                        User.email == self.email
                    )
                ).first()

                if existing_user:
                    self.error_message = "Email already registered"
                    return

                new_user = User(
                    name=self.name,
                    email=self.email,
                    password=User.hash_password(self.password)
                )
                
                session.add(new_user)
                session.commit()
                session.refresh(new_user)

                access_token = self.create_access_token(new_user.id)
                # Save token in local storage
                yield AuthState.set_token(access_token)

                self.email = ""
                self.password = ""
                self.name = ""
                self.error_message = ""
                yield rx.redirect("/explore")

        except IntegrityError:
            self.error_message = "Email already registered"
            session.rollback()
        except Exception as e:
            self.error_message = "An error occurred during registration"
            print(f"Registration error: {str(e)}")
            session.rollback()

def login_form() -> rx.Component:
    return rx.flex(
        rx.mobile_and_tablet(
            rx.flex(
                rx.text("SELibrary", class_name="text-5xl font-semibold text-[#253974]"),
                rx.vstack(
                    rx.cond(
                        # not LoginForm.is_login_form
                        ~LoginForm.is_login_form,
                        rx.fragment(
                            rx.text("Username", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                            rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", value=LoginForm.name, on_change=LoginForm.set_name),
                        ),
                    ),
                    rx.text("Email", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", type="email", value=LoginForm.email, on_change=LoginForm.set_email),
                    rx.text("Password", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", type="password", value=LoginForm.password, on_change=LoginForm.set_password),
                    rx.cond(
                        LoginForm.is_login_form,
                        rx.box(
                            rx.button("Login", class_name="w-full h-10 bg-[#253974] text-white rounded-lg", on_click=LoginForm.handle_login),
                            rx.text("Don't have an account?",rx.text.strong(" Sign up",class_name="italic", on_click=LoginForm.handle_switch_login_and_register ), class_name="text-sm text-neutral-500 mt-5"),
                            class_name="w-full h-1/2 flex flex-col items-center justify-center",
                        ),
                        rx.box(
                            rx.button("Register", class_name="w-full h-10 bg-[#253974] text-white rounded-lg", on_click=LoginForm.handle_register),
                            rx.text("Already have an account?",rx.text.strong(" Login",class_name="italic", on_click=LoginForm.handle_switch_login_and_register ), class_name="text-sm text-neutral-500 mt-5"),
                            class_name="w-full h-2/5 flex flex-col items-center justify-center",
                        ),
                    ),
                    class_name="w-full h-3/4 mt-2",
                ),
                class_name="w-full h-full items-center flex-col",
            ),
            class_name="w-4/5 h-2/3 bg-[#FDFDFD] rounded-lg shadow-lg p-4",
        ),
        rx.desktop_only(
            rx.flex(
                rx.text("SELibrary", class_name="text-5xl font-semibold text-[#253974]"),
                rx.vstack(
                    rx.cond(
                        # not LoginForm.is_login_form
                        ~LoginForm.is_login_form,
                        rx.fragment(
                            rx.text("Username", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                            rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", value=LoginForm.name, on_change=LoginForm.set_name),
                        ), 
                    ),
                    rx.text("Email", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974]"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", type="email", value=LoginForm.email, on_change=LoginForm.set_email),
                    rx.text("Password", rx.text.span("*", color="red"), class_name="text-lg font-semibold text-[#253974] mt-4"),
                    rx.input(class_name="w-full h-10 border-2 border-[#253974] rounded-lg p-2", type="password", value=LoginForm.password, on_change=LoginForm.set_password),
                    rx.cond(
                        LoginForm.is_login_form,
                        rx.box(
                            rx.button("Login", class_name="px-8 py-2 bg-[#253974] text-white rounded-lg", on_click=LoginForm.handle_login),
                            rx.text("Don't have an account?", rx.text.strong(" Sign up", class_name="italic", on_click=LoginForm.handle_switch_login_and_register), class_name="text-sm text-neutral-500 mt-2"),
                            class_name="mt-8 mx-auto flex flex-col items-center justify-center",
                        ),
                        rx.box(
                            rx.button("Register", class_name="px-8 py-2 bg-[#253974] text-white rounded-lg", on_click=LoginForm.handle_register),
                            rx.text("Already have an account?", rx.text.strong(" Sign in", class_name="italic", on_click=LoginForm.handle_switch_login_and_register), class_name="text-sm text-neutral-500 mt-2"),
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