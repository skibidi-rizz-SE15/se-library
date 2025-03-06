from sqlmodel import Field, Relationship
from sqlalchemy import Enum as SqlalchemyEnum, Column, DateTime
import reflex as rx
from typing import Optional, List
from enum import Enum
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class GenreEnum(str, Enum):
    PROGRAMMING_LANGUAGES = "programming_languages"
    DESIGN_PATTERNS = "design_patterns"
    SOFTWARE_ARCHITECTURE = "software_architecture"
    DEVOPS = "devops"
    SOFTWARE_TESTING = "software_testing"
    PROJECT_MANAGEMENT = "project_management"
    USER_EXPERIENCE = "user_experience"
    SECURITY = "security"

class ConditionEnum(str, Enum):
    FACTORY_NEW = "factory_new"
    MINIMAL_WEAR = "minimal_wear"
    FIELD_TESTED = "field_tested"
    WELL_WORN = "well_worn"
    BATTLE_SCARRED = "battle_scarred"

class AvailabilityEnum(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    RESERVED = "reserved"

class BorrowStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    BORROWED = "borrowed"
    RETURNED = "returned"

class User(rx.Model, table=True):
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    password: str = Field(nullable=False)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

class BookAuthorLink(rx.Model, table=True):
    book_id: int = Field(foreign_key="book.id")
    author_id: int = Field(foreign_key="author.id")

class Author(rx.Model, table=True):
    name: str = Field(unique=True, nullable=False)

    books: List["Book"] = Relationship(back_populates="authors", link_model=BookAuthorLink)

class Publisher(rx.Model, table=True):
    name: str = Field(unique=True, nullable=False)

    books: List["Book"] = Relationship(back_populates="publisher")

class Book(rx.Model, table=True):
    title: str = Field(nullable=False)
    description: str
    isbn13: str = Field(unique=True, nullable=False)
    publisher_id: int = Field(foreign_key="publisher.id")
    cover_image_link: str = Field(unique=True, nullable=True)
    pages: int = Field(nullable=False)
    genre: GenreEnum = Field(
        sa_column=Column(SqlalchemyEnum(GenreEnum, name="genre_enum", create_constraint=True))
    )

    publisher: Optional["Publisher"] = Relationship(back_populates="books")
    authors: List["Author"] = Relationship(back_populates="books", link_model=BookAuthorLink)


class BookInventory(rx.Model, table=True):
    owner_id: int = Field(foreign_key="user.id", nullable=False)
    book_id: int = Field(foreign_key="book.id", nullable=False)
    condition: ConditionEnum = Field(
        sa_column=Column(SqlalchemyEnum(ConditionEnum, name="condition_enum", create_constraint=True))
    )
    availability: AvailabilityEnum = Field(
        sa_column=Column(SqlalchemyEnum(AvailabilityEnum, name="availability_enum", create_constraint=True))
    )

    owner: Optional["User"] = Relationship()
    book: Optional["Book"] = Relationship()

class BookTransaction(rx.Model, table=True):
    borrower_id: int = Field(foreign_key="user.id", nullable=False)
    book_inventory_id: int = Field(foreign_key="bookinventory.id", nullable=False)
    borrow_status: BorrowStatusEnum = Field(
        sa_column=Column(SqlalchemyEnum(BorrowStatusEnum, name="borrow_status_enum", create_constraint=True))
    )
    duration: int
    borrow_date: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    return_date: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    qr_code_image_link: str = Field(nullable=True)

    book_inventory: Optional["BookInventory"] = Relationship()
    borrower: Optional["User"] = Relationship()
