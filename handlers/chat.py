from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ai import chat_books
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp
from keyboards.inline.menu import start_menu
from keyboards.inline.back import keyboard

class ChatState(StatesGroup):
    waiting_for_question = State()
    
    
@dp.callback_query_handler(lambda call: call.data == "chat")
async def start_chat(call: types.CallbackQuery, state: FSMContext):
    """Foydalanuvchidan kitob haqida savol berishni so‘raydi."""
    await call.message.answer(
        "📖 Kitob haqida qanday savolingiz bor? Menga yozing.",
        )

    await ChatState.waiting_for_question.set()


@dp.message_handler(state=ChatState.waiting_for_question)
async def process_question(message: types.Message, state: FSMContext):
    """Foydalanuvchi kitob haqida savol berganda AI dan javob olib, qaytaradi."""
    if message.text == '↩️ Ortga qaytish':
        await message.answer("Sizga kitoblarni tushunishda va qisqacha xulosalar berishda yordam beraman.\nQuyidagi tugmalardan foydalanib xizmatlardan foydalanishingiz mumkin.", reply_markup=start_menu)
        await message.answer(
            "ha",
            reply_markup=None
        )
        await state.finish()  # Holatni tugatish
    else:
        msg = await message.answer('Biroz kuting...')
        # ai_response = chat_books(message.text)
        ai_response = 'Ishlayapti...'

    await message.answer(f"{ai_response}")
    await msg.delete()
    await message.answer("Yana savolingiz bormi?", reply_markup=keyboard)
