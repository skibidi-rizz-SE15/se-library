"""Base state for the application"""

import reflex as rx
from typing import Optional

from se_library.models import User

class BaseState(rx.State):
    """The base state for the app."""

    user: Optional[User] = None

    def logout(self):
        """Logout a user."""
        self.reset()
        return rx.redirect("/login")
    
    @rx.var(cache=True)
    def logged_in(self) -> bool:
        """Check if a user is logged in."""
        return self.user is not None

    async def check_login(self):
        """Check if a user is logged in."""
        if not self.logged_in:
            return rx.redirect("/login")
        