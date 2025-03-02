import reflex as rx
from se_library.models import User
from se_library.states.base import BaseState

class ProfileState(rx.State):
    user: User = None


    @rx.event
    async def handle_on_load(self):
        self.user = await self.load_user()
        yield
        return

    async def load_user(self):
        base_state = await self.get_state(BaseState)
        return base_state.user