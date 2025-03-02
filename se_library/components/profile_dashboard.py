import reflex as rx
from se_library.states.profile_state import ProfileState, BookDetails, TransactionDetails

def borrowed_books_grid() -> rx.Component:
    return rx.grid(
        rx.foreach(
            ProfileState.borrowed_transactions,
            borrow_item
        ),
        # borrow_item(ProfileState.borrowed_transactions[0].book_inventory_details.book_details, ProfileState.borrowed_transactions[0].borrow_date),
        class_name="grid-cols-[repeat(auto-fill,minmax(17rem,1fr))] gap-4 p-4"
    )

def borrow_item(transaction: TransactionDetails) -> rx.Component:
    print(transaction)
    return rx.grid(
        book_image(image=transaction.book_inventory_details.book_details.cover_image_link),
        book_details(book=transaction.book_inventory_details.book_details, available_on=transaction.borrow_date, return_within=transaction.return_date),
        class_name="grid-cols-[2fr_3fr] mx-auto h-fit gap-4"
    )

def book_image(image: str) -> rx.Component:
    return rx.image(
        src=f"{image}",
        class_name="rounded-md shadow-lg w-full"
    )

def book_details(book: BookDetails, available_on: str, return_within: str) -> rx.Component:
    return rx.flex(
        rx.text(f"{book.title}", title=book.title, class_name="font-semibold text-[0.9rem] text-ellipsis line-clamp-3 font-Valera"),
        rx.text(f"By: {book.authors}", class_name="text-gray-500 text-[0.8rem]"),
        rx.text(f"Available on {available_on}", class_name="text-gray-500 text-[0.8rem] mt-4 font-semibold"),
        rx.text(f"Return within {return_within}", class_name="text-gray-500 text-[0.8rem] font-semibold"),
        class_name="flex-col leading-5 gap-2"
    )

def lent_books_contents() -> rx.Component:
    return rx.fragment(
        rx.text("Lent books will be shown here.", class_name="text-gray-600 p-4"),
        class_name="p-4"
    )

def lent_item() -> rx.Component:
    return rx.flex(

    )

def borrow_approval_contents() -> rx.Component:
    return rx.fragment(
        
    )

def profile_dashboard() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("circle-user-round", size=80, class_name="text-gray-700"),
            rx.text(f"{ProfileState.user.username}", class_name="text-2xl font-semibold text-[#253974]"),
            class_name="w-full items-center space-x-4 p-6 bg-white shadow rounded-md"
        ),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Borrow List", value="borrow_list", class_name="px-4 py-2 font-semibold cursor-pointer"),
                rx.tabs.trigger("Lent Books", value="lent_books", class_name="px-4 py-2 font-semibold cursor-pointer"),
                rx.tabs.trigger("Borrow Approval", value="borrow_approval", class_name="px-4 py-2 font-semibold cursor-pointer"),
                class_name="border-b border-gray-300"
            ),
            rx.tabs.content(
                borrowed_books_grid(),
                value="borrow_list"
            ),
            rx.tabs.content(
                lent_books_contents(),
                value="lent_books"
            ),
            rx.tabs.content(
                lent_books_contents(),
                value="borrow_approval"
            ),
            default_value="borrow_list",
            class_name="w-full"
        ),
        background_color=rx.color_mode_cond(light=rx.color("indigo", 2), dark=rx.color("indigo", 1)),
        class_name="h-full flex-col w-full max-w-4xl mx-auto p-4"
    )