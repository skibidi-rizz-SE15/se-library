import reflex as rx
import os

config = rx.Config(
    app_name="se_library",
    db_url=os.environ.get("DATABASE_URL", "postgresql://postgres:admin@localhost/se_library"),
)