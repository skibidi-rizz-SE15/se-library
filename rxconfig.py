import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="se_library",
    db_url=os.environ.get("DATABASE_URL"),
    tailwind={
        "theme": {
            "extend": {
                "fontFamily": {
                    "Outfit": ['Outfit', 'sans-serif'],
                    "Roboto": ['Roboto', 'sans-serif'],
                    "Varela": ['Varela', 'sans-serif'],
                    "Montserrat": ['Montserrat', 'sans-serif'],
                    
                },
            },
        }
    },  # tailwindcss configuration
)