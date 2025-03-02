import reflex as rx
from se_library.models import User, BookTransaction, Book
from se_library.states.base import BaseState
from typing import List

class ProfileState(rx.State):
    user: User = None
    borrow_books: List[BookTransaction] = []


    @rx.event
    async def handle_on_load(self):
        self.user = await self.load_user()
        with rx.session() as session:
            self.borrow_books = await self.load_borrow_books(db=session)
            print(self.borrow_books[0].book_inventory.book.title)
        yield
        return

    async def load_user(self):
        base_state = await self.get_state(BaseState)
        return base_state.user
    
    async def load_borrow_books(self, db):
        return db.query(BookTransaction).filter(BookTransaction.borrower_id == self.user.id).all()