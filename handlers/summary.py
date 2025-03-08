from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from states.book_analysis import BookAnalysisState
from ai import analyze_book_summary
from keyboards.inline.menu import start_menu


def register_handlers_summary(dp: Dispatcher):
    dp.register_callback_query_handler(book_analysis_callback, Text(equals="book_analysis"))
    dp.register_message_handler(analyze_book, state=BookAnalysisState.waiting_for_book_text)

async def book_analysis_callback(call: types.CallbackQuery):
    await call.message.answer("📖 Kitob nomini yoki qisqacha mazmunini kiriting:\n\nBekor qilish uchun: /cannel")
    await BookAnalysisState.waiting_for_book_text.set()

async def analyze_book(message: Message, state: FSMContext):
    book_text = message.text
    if book_text == '/cannel':
            await message.answer("Sizga kitoblarni tushunishda va qisqacha xulosalar berishda yordam beraman.\nQuyidagi tugmalardan foydalanib xizmatlardan foydalanishingiz mumkin.", reply_markup=start_menu)
    else:
        # response = analyze_book_summary(book_text)  # AI modelga yuboramiz
        # await message.answer(response, reply_markup=start_menu)
        await message.answer('Ishlayapti...', reply_markup=start_menu)
    await state.finish()
