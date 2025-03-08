from aiogram import types
from aiogram.dispatcher import FSMContext
from states.recommend_state import RecommendBookState
from keyboards.inline.recommend_keyboard import genre_keyboard
from ai import recommend_books
from keyboards.inline.menu import start_menu
from loader import dp  # Bot dispatcher

@dp.callback_query_handler(lambda call: call.data == "recommend_books")
async def ask_for_genre(call: types.CallbackQuery, state: FSMContext):
    """Foydalanuvchidan kitob janrini so‘raydi."""
    await call.answer()
    message = await call.message.answer(
        "📚 Qaysi janrda kitob tavsiyasi kerak?\nQuyidagilardan birini tanlang:",
        reply_markup=genre_keyboard
    )
    await state.update_data(question_message=message.message_id)  # Xabar ID ni saqlaymiz
    await RecommendBookState.waiting_for_genre.set()

@dp.callback_query_handler(state=RecommendBookState.waiting_for_genre)
async def process_genre(call: types.CallbackQuery, state: FSMContext):
    """Foydalanuvchi janr tanlasa, AI modelga so‘rov jo‘natadi."""
    genre = call.data
    await call.answer()

    # Inline tugmalar va savol xabarini o‘chirish
    user_data = await state.get_data()
    question_message_id = user_data.get("question_message")
    if question_message_id:
        try:
            await call.message.bot.delete_message(call.message.chat.id, question_message_id)
        except Exception as e:
            print(f"Xabarni o‘chirishda xatolik: {e}")

    msg = await call.message.answer("⏳ Kitob tavsiyalari tayyorlanmoqda...")
    if genre == '↩️ Ortga qaytish':
            await call.message.answer("Sizga kitoblarni tushunishda va qisqacha xulosalar berishda yordam beraman.\nQuyidagi tugmalardan foydalanib xizmatlardan foydalanishingiz mumkin.", reply_markup=start_menu)
    else:
        # recommendations = recommend_books(genre)  # AI modeldan javob olamiz
        # await call.message.answer(recommendations, parse_mode="Markdown", reply_markup=start_menu)

        await call.message.answer("Ishlayapti...")
    
    # "Tayyorlanmoqda..." xabarini o‘chirish
    try:
        await msg.delete()
    except Exception as e:
        print(f"Xabarni o‘chirishda xatolik: {e}")

    await state.finish()
