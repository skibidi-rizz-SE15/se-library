"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .pages.homepage import homepage
from dotenv import load_dotenv

load_dotenv()

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="indigo",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap",
        "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap"
    ]
)
app.add_page(homepage)