import reflex as rx

class AuthState(rx.State):
    token: str = rx.LocalStorage(name="token")
    
    @rx.event
    def check_token(self):
        if not self.token:
            return rx.redirect("/login")
        yield