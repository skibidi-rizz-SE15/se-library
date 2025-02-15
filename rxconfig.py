import reflex as rx
import os

config = rx.Config(
    app_name="se_library",
    db_url=os.environ.get("DATABASE_URL", "postgresql://rachatapondee@localhost:5432/se_library"),
    tailwind={
        "theme": {
            "extend": {
                "fontFamily": {
                    "Outfit": ['Outfit', 'sans-serif'],
                    "Roboto": ['Roboto', 'sans-serif'],
                    "Varela": ['Varela', 'sans-serif'],
                },
            },
        }
    },  # tailwindcss configuration
)