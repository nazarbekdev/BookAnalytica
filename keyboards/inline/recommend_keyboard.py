from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

genre_keyboard = InlineKeyboardMarkup(row_width=2)
genres = [
    "Fantastika", "Tarixiy", "Detektiv", "Ilmiy-ommabop", "Falsafa", "O'zbek adabiyoti", "↩️ Ortga qaytish"
]

buttons = [InlineKeyboardButton(text=genre, callback_data=genre) for genre in genres]
genre_keyboard.add(*buttons)
