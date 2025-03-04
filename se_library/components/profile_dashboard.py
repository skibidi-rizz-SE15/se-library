from typing import Dict, Tuple
import reflex as rx
from se_library.models import ConditionEnum
from se_library.states.profile_state import ProfileState, BookDetails, TransactionDetails

def borrowed_books_grid() -> rx.Component:
    return rx.grid(
        rx.foreach(
            ProfileState.borrowed_transactions,
            borrow_item
        ),
        class_name="grid-cols-[repeat(auto-fill,minmax(17rem,1fr))] gap-4 p-4"
    )

def borrow_item(transaction: TransactionDetails) -> rx.Component:
    return rx.grid(
        book_image(image=transaction.book_inventory_details.book_details.cover_image_link, class_name="w-full"),
        book_details(
            book=transaction.book_inventory_details.book_details, 
            available_on=transaction.borrow_date, 
            return_within=transaction.return_date,
            condition=transaction.book_inventory_details.condition,
            status=transaction.borrow_status
        ),
        class_name="grid-cols-[2fr_3fr] items-start h-fit gap-4"
    )

def book_image(image: str, class_name: str="") -> rx.Component:
    return rx.image(
        src=f"{image}",
        class_name=f"rounded-md shadow-lg {class_name}"
    )

def book_details(book: BookDetails, available_on: str, return_within: str, condition: str, status: str) -> rx.Component:
    return rx.flex(
        rx.text(f"{book.title}", title=book.title, class_name="font-semibold text-[0.9rem] text-ellipsis line-clamp-3 font-Valera"),
        rx.text(f"By: {book.authors}", class_name="text-gray-500 text-[0.8rem]"),
        rx.text(f"Condition: {condition}", class_name="text-gray-500 text-[0.8rem]"),
        rx.text(f"Status: {status}", class_name="text-gray-500 text-[0.8rem]"),
        rx.text(f"Available on {available_on}", class_name="text-gray-500 text-[0.8rem] mt-4 font-semibold"),
        rx.text(f"Return within {return_within}", class_name="text-gray-500 text-[0.8rem] font-semibold"),
        class_name="flex-col leading-5 gap-2"
    )

def lent_books_grid() -> rx.Component:
    return rx.grid(
        rx.foreach(
            ProfileState.lent_transactions,
            lent_item
        ),
        class_name="grid-cols-[repeat(auto-fill,minmax(17rem,1fr))] gap-4 p-4"
    )

def lent_item(transaction: Tuple[BookDetails, Dict[ConditionEnum, int]]) -> rx.Component:
    book_details = transaction[0]
    condition_quantities = transaction[1]
    fn_quantity = condition_quantities[ConditionEnum.FACTORY_NEW]
    mw_quantity = condition_quantities[ConditionEnum.MINIMAL_WEAR]
    ft_quantity = condition_quantities[ConditionEnum.FIELD_TESTED]
    ww_quantity = condition_quantities[ConditionEnum.WELL_WORN]
    bs_quantity = condition_quantities[ConditionEnum.BATTLE_SCARRED]
    total_quantity = fn_quantity + mw_quantity + ft_quantity + ww_quantity + bs_quantity

    return rx.grid(
        book_image(image=book_details.cover_image_link, class_name="w-full"),
        rx.flex(
            rx.text(f"{book_details.title}", title=book_details.title, class_name="font-semibold text-[0.9rem] text-ellipsis line-clamp-3 font-Valera"),
            rx.text(f"By: {book_details.authors}", class_name="text-gray-500 text-[0.8rem]"),
            rx.flex(
                rx.text(f"Total: {total_quantity} copies", class_name="text-gray-500 text-[0.8rem]"),
                rx.text("?", class_name="cursor-pointer peer px-2 rounded-full text-white bg-blue-400 hover:bg-blue-300"),
                rx.grid(
                    rx.text("Factory New:"),
                    rx.text(fn_quantity),
                    rx.text("Minimal Wear:"),
                    rx.text(mw_quantity),
                    rx.text("Field Tested:"),
                    rx.text(ft_quantity),
                    rx.text("Well Worn:"),
                    rx.text(ww_quantity),
                    rx.text("Battle Scarred:"),
                    rx.text(bs_quantity),
                    class_name=(
                        "absolute right-0 bottom-full "
                        "grid grid-cols-[max-content_1fr] items-center gap-2 "
                        "bg-black text-[#FFFFFF] border text-[0.8rem] p-2 rounded-lg "
                        "opacity-0 peer-hover:opacity-100 transition-opacity duration-200 pointer-events-none"
                    )
                ),
                class_name="relative items-center gap-2 w-fit"
            ),
            class_name="flex-col leading-5 gap-2"
        ),
        class_name="grid-cols-[2fr_3fr] items-start mx-auto h-fit gap-4"
    )

def borrow_approval_content() -> rx.Component:
    return rx.grid(
        rx.foreach(
            ProfileState.pending_approvals,
            borrow_approval_item
        ),
        class_name="gap-4 p-4"
    )

def borrow_approval_item(transaction: TransactionDetails) -> rx.Component:
    book = transaction.book_inventory_details.book_details
    condition = transaction.book_inventory_details.condition
    img_src = transaction.book_inventory_details.book_details.cover_image_link
    approval_rate = transaction.approval_rate

    return rx.flex(
        book_image(img_src, class_name="h-[5rem] w-auto"),
        rx.text(f"{book.title}", title=book.title, class_name="font-semibold text-[0.9rem] text-ellipsis line-clamp-3 font-Valera"),
        rx.text(f"Condition: {condition}", class_name="text-gray-500 text-[0.8rem]"),
        rx.text(f"Borrowed by {transaction.borrower}", class_name="text-gray-500 text-[0.8rem] font-semibold"),
        rx.text(f"{approval_rate * 100}% approval rate", class_name="text-gray-500 text-[0.8rem]"),
        rx.button("Approve"),
        rx.button("Reject"),
        class_name="leading-5 items-center gap-2"
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
                lent_books_grid(),
                value="lent_books"
            ),
            rx.tabs.content(
                borrow_approval_content(),
                value="borrow_approval"
            ),
            default_value="borrow_list",
            class_name="  w-full"
        ),
        background_color=rx.color_mode_cond(light=rx.color("indigo", 2), dark=rx.color("indigo", 1)),
        class_name="h-max min-h-full flex-col w-full max-w-4xl mx-auto p-4"
    )