from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Oddiy tugmalar uchun keyboard yaratamiz
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# Tugmalarni qo‘shamiz
keyboard.add(KeyboardButton(text="↩️ Ortga qaytish"))
