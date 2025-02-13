import reflex as rx

def borrow_list_content() -> rx.Component:
    return rx.flex(
        rx.text("Borrowed books will be shown here.", class_name="text-gray-600 p-4"),
        class_name="p-4"
    )

def lent_books_content() -> rx.Component:
    return rx.flex(
        rx.text("Lent books will be shown here.", class_name="text-gray-600 p-4"),
        class_name="p-4"
    )

def profile_dashboard() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("circle-user-round", size=80, class_name="text-gray-700"),
            rx.text("User Name", class_name="text-2xl font-semibold text-[#253974]"),
            class_name="w-full items-center space-x-4 p-6 bg-white shadow rounded-md"
        ),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Borrow List", value="borrow_list", class_name="px-4 py-2 font-semibold"),
                rx.tabs.trigger("Lent Books", value="lent_books", class_name="px-4 py-2 font-semibold"),
                class_name="border-b border-gray-300"
            ),
            rx.tabs.content(
                borrow_list_content(),
                value="borrow_list"
            ),
            rx.tabs.content(
                lent_books_content(),
                value="lent_books"
            ),
            default_value="borrow_list",
            class_name="w-full"
        ),
        class_name="flex-col w-full h-full bg-[#dadada] max-w-4xl mx-auto p-4"
    )
