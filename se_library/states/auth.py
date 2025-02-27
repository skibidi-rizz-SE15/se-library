"""The authentication state."""
import reflex as rx
from sqlmodel import select

from .base import BaseState, User

class AuthState(BaseState):
    """The authentication state for sign up and login page."""

    email: str
    password: str
    username: str

    def login(self):
        """Log in a user."""
        with rx.session() as session:
            user = session.exec(
                User.select().where(
                    User.email == self.email
                )
            ).first()
            if not user or not user.verify_password(self.password):
                return rx.window_alert("Invalid username or password.")
            self.user = user
            return rx.redirect("/explore")
        
    def signup(self):
        """Sign up a user."""
        with rx.session() as session:
            if not all([self.email, self.password, self.username]):
                return rx.window_alert("Please fill in all fields.")
            
            if session.exec(select(User).where(User.email == self.email)).first():
                return rx.window_alert("Email already exists.")
            
            new_user = User(
                email=self.email, 
                username=self.username,
                password=User.hash_password(self.password)
            )
            session.add(new_user)
            session.commit()
            self.user = session.exec(select(User).where(User.email == self.email)).first()
            return rx.redirect("/explore")