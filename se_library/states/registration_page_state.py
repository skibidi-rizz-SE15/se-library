import reflex as rx
import requests
import json
from typing import List
from enum import Enum
from ..models import Book, BookInventory, Publisher, Author, BookAuthorLink, ConditionEnum, AvailabilityEnum, GenreEnum, BOOK_REGISTRATION_LIMIT
from .base import BaseState
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

class BookPreviewDetails(rx.State):
    title: str = ""
    description: str = ""
    authors: List[str] = []
    publisher: str = ""
    cover_image_link: str = ""
    isbn13: str = ""
    pages: int = None

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

class BookRegistrationPageState(BookPreviewDetails):
    loading: bool = False
    book_exists: bool = None
    book_in_db: bool = None
    is_search: bool = False
    submit_loading: bool = False

    book_condition: ConditionEnum = None
    book_genre: GenreEnum = None

    @rx.var(cache=False)
    def get_formatted_condition(self) -> str:
        match self.book_condition:
            case ConditionEnum.FACTORY_NEW:
                return "Factory New"
            case ConditionEnum.MINIMAL_WEAR:
                return "Minimal Wear"
            case ConditionEnum.FIELD_TESTED:
                return "Field Tested"
            case ConditionEnum.WELL_WORN:
                return "Well Worn"
            case ConditionEnum.BATTLE_SCARRED:
                return "Battle Scarred"
            case _:
                return "Select Condition"
            
    @rx.var(cache=False)
    def get_formatted_genre(self) -> str:
        match self.book_genre:
            case GenreEnum.PROGRAMMING_LANGUAGES:
                return "Programming Languages"
            case GenreEnum.DESIGN_PATTERNS:
                return "Design Patterns"
            case GenreEnum.SOFTWARE_ARCHITECTURE:
                return "Software Architecture"
            case GenreEnum.DEVOPS:
                return "DevOps"
            case GenreEnum.SOFTWARE_TESTING:
                return "Software Testing"
            case GenreEnum.PROJECT_MANAGEMENT:
                return "Project Management"
            case GenreEnum.USER_EXPERIENCE:
                return "UX/UI"
            case GenreEnum.SECURITY:
                return "Security"
            case _:
                return "Select Genre"

    @rx.event
    def set_condition(self, selected_condition: ConditionEnum):
        if isinstance(selected_condition, str):
            selected_condition = ConditionEnum(selected_condition)
        self.book_condition = selected_condition

    @rx.event
    def set_genre(self, selected_genre: GenreEnum):
        if isinstance(selected_genre, str):
            selected_genre = GenreEnum(selected_genre)
        self.book_genre = selected_genre

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
                self.book_genre = existing_book.genre
                self.book_exists = True
                self.book_in_db = True
            else:
                self.book_in_db = False
                await self.fetch_isbndb()
        
    @rx.event
    async def handle_register_book(self, form_data: dict):
        if not self.book_genre:
            return
        dialog_state = await self.get_state(ConditionDialogState)
        self.submit_loading = True
        yield
        await asyncio.sleep(2)
        with rx.session() as session:
            existing_book = session.exec(
                Book.select().where(
                    Book.isbn13 == self.isbn13
                )
            ).first()

            if not existing_book:  
                existing_publisher = session.exec(
                    Publisher.select().where(
                        Publisher.name == self.publisher
                    )
                ).first() 
                publisher = None
                if not existing_publisher:
                    session.add(Publisher(
                        name=self.publisher
                    ))
                    publisher = session.exec(
                        Publisher.select().where(
                            Publisher.name == self.publisher
                        )
                    ).first()
                else:
                    publisher = existing_publisher

                session.add(Book(
                    title=self.title,
                    description=self.description,
                    isbn13=self.isbn13,
                    publisher_id=publisher.id,
                    cover_image_link=self.cover_image_link,
                    pages=self.pages,
                    genre=self.book_genre
                ))

                for author_name in self.authors:
                    existing_author = session.exec(
                        Author.select().where(
                            Author.name == author_name
                        )
                    ).first()
                    if not existing_author:
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
            has_multiple_copies = form_data["has_multiple_copies"] if "has_multiple_copies" in form_data else None
            # multiple books
            if has_multiple_copies:
                try:
                    quantities = []
                    total = 0
                    
                    for condition in ConditionEnum:
                        qty = form_data.get(f"{condition.value}", "0") 
                        try:
                            qty_int = int(qty) if qty else 0
                            if qty_int < 0:
                                self.submit_loading = False
                                yield rx.toast.error("Quantity cannot be negative", position="top-center")
                                return
                            total += qty_int
                            quantities.append((condition, qty_int))
                        except ValueError:
                            self.submit_loading = False
                            yield rx.toast.error(f"Invalid quantity for {condition.value}", position="top-center")
                            return
                    if total > BOOK_REGISTRATION_LIMIT:
                        self.submit_loading = False
                        yield rx.toast.error("Total quantity cannot exceed 50 books", position="top-center")
                        return
                    elif total <= 0:
                        self.submit_loading = False
                        yield rx.toast.error("Total quantity cannot be 0", position="top-center")
                        return
                    else:
                        for condition, quantity in quantities:
                            if quantity > 0:
                                for _ in range(quantity):
                                    session.add(BookInventory(
                                        book_id=new_book.id if not existing_book else existing_book.id,
                                        owner_id=user.id,
                                        condition=condition.value,
                                        availability=AvailabilityEnum.AVAILABLE,
                                    ))
                                    session.commit()
                    self.submit_loading = False
                    await dialog_state.reset_states()
                    yield rx.toast.success("Books Registered Successfully", position="top-center")
                    return
                except Exception as e:
                    print(f"Error adding book inventory: {e}")
                    self.submit_loading = False
                    yield rx.toast.error("Error adding book inventory", position="top-center")
                    return
            # single book
            else:
                try:
                    if not self.book_condition:
                        raise Exception("Condition is not selected")
                    session.add(BookInventory(
                        book_id=new_book.id if not existing_book else existing_book.id,
                        owner_id=user.id,
                        condition=self.book_condition,
                        availability=AvailabilityEnum.AVAILABLE,
                    ))
                    session.commit()
                except Exception as e:
                    print(f"Error adding book inventory: {e}")
                    self.submit_loading = False
                    yield rx.toast.error("Select the book condition!", position="top-center")
                    return
            self.submit_loading = False
            await dialog_state.reset_states()
            yield rx.toast.success("Book Registered Successfully", position="top-center")
            return
    
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
    is_dialog_open: bool = False
    has_multiple_copies: bool = False

    @rx.event
    async def reset_states(self):
        self.reset()
        book_registration_state = await self.get_state(BookRegistrationPageState)
        book_registration_state.book_condition = None
        book_registration_state.book_genre = None