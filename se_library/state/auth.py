import reflex as rx

class AuthState(rx.State):
    token: str = rx.LocalStorage(name="token")
    authenticated: bool = False
    
    @rx.event
    def check_token(self):
        self.authenticated = check_auth(self.token)
        if not self.authenticated:
            return rx.redirect("/login")

def check_auth(token):
    # Logic to check if token is valid need to be implemented
    if not token:
        return False
    return True