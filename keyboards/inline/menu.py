from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Inline tugmalarni yaratamiz
start_menu = InlineKeyboardMarkup(row_width=2)

buttons = [
    InlineKeyboardButton(text="📖 Kitob tahlili", callback_data="book_analysis"),
    InlineKeyboardButton(text="📚 Tavsiyalar", callback_data="recommend_books"),
    InlineKeyboardButton(text="ℹ️ Yordam", callback_data="help"),
    InlineKeyboardButton(text="💬 Suhbat", callback_data="chat"),
    InlineKeyboardButton(text="⭐ Fikr bildirish", callback_data="feedback"),
]

start_menu.add(*buttons)

