import reflex as rx
import os

config = rx.Config(
    app_name="se_library",
    db_url=os.environ.get("DATABASE_URL", "[YOUR_LOCAL_DB_URL]"),
    tailwind={
        "theme": {
            "extend": {
                "fontFamily": {
                    "Outfit": ['Outfit', 'sans-serif'],
                    "Roboto": ['Roboto', 'sans-serif'],
                },
            },
        }
    },  # tailwindcss configuration
)