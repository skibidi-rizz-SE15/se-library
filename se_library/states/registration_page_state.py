import reflex as rx
import requests
import json
from typing import List
from enum import Enum
from ..models import Book, BookInventory, Publisher, Author, BookAuthorLink, ConditionEnum, AvailabilityEnum
from .base import BaseState
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

BOOK_REGISTRATION_LIMIT = 50

class BookInfo(rx.State):
    title: str = ""
    description: str = ""
    authors: List[str] = []
    publisher: str = ""
    cover_image_link: str = ""
    isbn13: str = ""
    pages: int = None
    condition: ConditionEnum = None

    @rx.var(cache=False)
    def get_formatted_authors(self) -> str:
        return ", ".join(self.authors)

    @rx.event
    def set_isbn13_from_input(self, raw_isbn: str):
        isbn = raw_isbn.strip().replace(" ", "")
        isbn_length = len(isbn)
        match isbn_length:
            case 10:
                self.isbn13 = self.calculate_isbn13(isbn)
            case 13:
                self.isbn13 = isbn
            case _:
                self.isbn13 = ""

    def calculate_isbn13(self, isbn10):
        isbn13 = f"978{isbn10[:-1]}"
        check_sum = 0
        for i, char in enumerate(isbn13):
            num = int(char)
            check_sum += num * (3 if i % 2 != 0 else 1)
        check_num = check_sum % 10
        return isbn13 + str((10 - check_num) % 10)
    
class BookRegistrationPageState(BookInfo):
    loading: bool = False
    book_exists: bool = None
    is_search: bool = False
    book_condition: str = None
    submit_loading: bool = False

    @rx.event
    def set_new_condition(self, selected_condition: str):
        self.book_condition = selected_condition
        match selected_condition:
            case ConditionEnum.FACTORY_NEW:
                self.condition = ConditionEnum.FACTORY_NEW
            case ConditionEnum.MINIMAL_WEAR:
                self.condition = ConditionEnum.MINIMAL_WEAR
            case ConditionEnum.FIELD_TESTED:
                self.condition = ConditionEnum.FIELD_TESTED
            case ConditionEnum.WELL_WORN:
                self.condition = ConditionEnum.WELL_WORN
            case ConditionEnum.BATTLE_SCARRED:
                self.condition = ConditionEnum.BATTLE_SCARRED
            case  _:
                self.condition = None

    @rx.event
    async def handle_search(self, form_data: dict):
        self.loading = True
        self.is_search = True
        yield
        await asyncio.sleep(1)
        self.set_isbn13_from_input(form_data["raw_isbn"])
        await self.set_book_info()
        if self.book_exists:
            self.loading = False

    async def set_book_info(self):
        with rx.session() as session:
            existing_book = session.exec(
                Book.select().where(
                    Book.isbn13 == self.isbn13
                )
            ).first()

            if existing_book:
                self.title = existing_book.title
                self.cover_image_link = existing_book.cover_image_link
                self.description = existing_book.description
                self.publisher = existing_book.publisher.name
                self.authors = [author.name for author in existing_book.authors]
                self.pages = existing_book.pages
                self.book_exists = True
            else:
                await self.fetch_isbndb()
        
    @rx.event
    async def handle_register_book(self, form_data: dict):
        with rx.session() as session:
            existing_book = session.exec(
                Book.select().where(
                    Book.isbn13 == self.isbn13
                )
            ).first()

            if not existing_book:   
                session.add(Publisher(
                    name=self.publisher
                ))
                new_publisher = session.exec(
                    Publisher.select().where(
                        Publisher.name == self.publisher
                    )
                ).first()
                session.add(Book(
                    title=self.title,
                    description=self.description,
                    isbn13=self.isbn13,
                    publisher_id=new_publisher.id,
                    cover_image_link=self.cover_image_link,
                    pages=self.pages
                ))
                for author_name in self.authors:
                    session.add(Author(
                        name=author_name
                    ))
                session.commit()
                new_book = session.exec(
                    Book.select().where(
                        Book.isbn13 == self.isbn13
                    )
                ).first()
                new_authors = session.exec(
                    Author.select().where(
                        Author.name.in_(self.authors)     
                    )
                ).all()
                for new_author in new_authors:
                    session.add(BookAuthorLink(
                        book_id=new_book.id,
                        author_id=new_author.id
                    ))

            # add instance
            base_state = await self.get_state(BaseState)
            user = base_state.user
            print(user)
            has_multiple_books = form_data["has_multiple_books"] if "has_multiple_books" in form_data else None
            if has_multiple_books == "on":
                try:
                    quantities = []
                    total = 0
                    
                    for condition in ConditionEnum:
                        qty = form_data.get(f"{condition.value}", "0")
                        try:
                            qty_int = int(qty)
                            if qty_int < 0:
                                return rx.window_alert("Quantities cannot be negative")
                            total += qty_int
                            quantities.append((condition, qty_int))
                        except ValueError:
                            return rx.window_alert(f"Invalid quantity for {condition.value}")
                    if total > BOOK_REGISTRATION_LIMIT:
                        return rx.window_alert("Total quantity cannot exceed 50 books")
                    for condition, quantity in quantities:
                        if quantity > 0:
                            session.add(BookInventory(
                                book_id=new_book.id if not existing_book else existing_book.id,
                                owner_id=user.id,
                                condition=condition.value,
                                availability=AvailabilityEnum.AVAILABLE,
                            ))
                            session.commit()
                except Exception as e:
                    print(f"Error adding book inventory: {e}")
                    return rx.window_alert("Error adding book inventory")
            else:
                print(user)
                session.add(BookInventory(
                    book_id=new_book.id if not existing_book else existing_book.id,
                    owner_id=user.id,
                    condition=self.condition.value,
                    availability=AvailabilityEnum.AVAILABLE,
                ))
                session.commit()
            return rx.toast("Book Registered Successfully")
    
    async def fetch_isbndb(self) -> None:
        try:
            res = requests.get(f"https://api2.isbndb.com/book/{self.isbn13}", headers={
                "Host": "api2.isbndb.com",
                "User-Agent": "insomnia/5.12.4",
                "Authorization": os.getenv("ISBN_API_KEY"),
                "Accept": "*/*"
            })
            data = json.loads(res.content)

            if "book" in data:
                self.book_exists = True
                book = data["book"]
                self.title = book["title"]
                self.description = book["synopsis"].replace("<br/>", " ")
                self.authors = book["authors"]
                self.publisher = book["publisher"]
                self.cover_image_link = book["image"]
                self.isbn13 = book["isbn13"]
                self.pages = book["pages"]
        except Exception as e:
            print(f"Error fetching book info: {e}")
            self.book_exists = False
        finally:
            self.loading = False

    async def reset_states(self):
        self.reset()

class ConditionDialogState(rx.State):
    has_multiple_books: bool = False

    @rx.event
    def reset_states(self):
        self.reset()