import reflex as rx
import requests
import json
from typing import List
from enum import Enum
from ..models import Book, BookInventory, Publisher, Author, BookAuthorLink
from dotenv import load_dotenv
import os

load_dotenv()

class ConditionEnum(Enum):
    FACTORY_NEW = "factory_new"
    MINIMAL_WEAR = "minimal_wear"
    FIELD_TESTED = "field_tested"
    WELL_WORN = "well_worn"
    BATTLE_SCARRED = "battle_scarred"

class BookInfo(rx.State):
    title: str = ""
    description: str = ""
    authors: List[str] = []
    publisher: str = ""
    cover_image_link: str = ""
    isbn: str = ""
    isbn13: str = ""
    language: str = ""
    date: str = ""
    pages: int = None
    edition: str = ""
    is_found_in_db: bool = False
    condition: ConditionEnum = None

    @rx.var(cache=False)
    def get_formatted_authors(self) -> str:
        return ", ".join(self.authors)

    @rx.event
    def set_formatted_isbn(self, raw_isbn: str):
        self.isbn = raw_isbn.strip().replace(" ", "")
    
class BookRegistrationPageState(BookInfo):
    loading: bool = False
    book_exists: bool = None
    
    @rx.event
    async def handle_search(self, form_data: dict):
        self.loading = True
        self.set_formatted_isbn(form_data["raw_isbn"])
        await self.set_book_info()
        if self.book_exists:
            self.loading = False

    async def set_book_info(self):
        with rx.session() as session:
            existing_book = session.exec(
                Book.select().where(
                    Book.isbn == self.isbn
                )
            ).first()

            if existing_book:
                self.title = existing_book.title
                self.description = existing_book.description
                self.publisher = existing_book.publisher.name
                self.authors = [author.name for author in existing_book.authors]
                self.book_exists = True
                self.is_found_in_db = True
            else:
                await self.fetch_isbndb()
        
    @rx.event
    async def handle_register_book(self):
        with rx.session() as session:
            existing_book = session.exec(
                Book.select().where(
                    Book.isbn == self.isbn
                )
            ).first()
            if not existing_book:   
                session.add(Publisher(
                    name=self.publisher
                ))
                new_publisher = session.exec(
                    Publisher.select().where(
                        Publisher.name == self.name
                    )
                ).first()
                session.add(Book(
                    title=self.title,
                    description=self.description,
                    isbn=self.isbn,
                    publisher_id=new_publisher.id
                ))
                for author_name in self.authors:
                    session.add(Author(
                        name=author_name
                    ))
                new_book = session.exec(
                    Book.select().where(
                        Book.isbn == self.isbn
                    )
                ).first()
                new_authors = session.exec(
                    Author.select().where(
                        Author.name in self.authors     
                    )
                ).all()
                for new_author in new_authors:
                    session.add(BookAuthorLink(
                        book_id=new_book.id,
                        author_id=new_author.id
                    ))
                # add instance
    
    async def fetch_isbndb(self) -> None:
        try:
            res = requests.get(f"https://api2.isbndb.com/book/{self.isbn}", headers={
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
                self.isbn = book["isbn"]
                self.language = book["language"]
                self.date = book["date_published"]
                self.pages = book["pages"]
                self.edition = book["edition"]
                self.is_found_in_db = False
        except Exception as e:
            print(f"Error fetching book info: {e}")
            self.book_exists = False
        finally:
            self.loading = False


