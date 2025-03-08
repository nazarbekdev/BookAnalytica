from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp, bot
from keyboards.inline.menu import start_menu
from dotenv import load_dotenv
import html
import os

load_dotenv()

ADMIN_ID = os.getenv('ADMINS')
CHANNEL_ID = "@kitoblar_haqida_fikrlar"

# Ma'lumotlarni saqlash uchun vaqtinchalik "bazamiz" (dikt)
feedback_storage = {}

class FeedbackState(StatesGroup):
    waiting_for_book_name = State()
    waiting_for_genre = State()
    waiting_for_author = State()
    waiting_for_summary = State()
    waiting_for_lessons = State()

@dp.callback_query_handler(lambda call: call.data == "feedback")
async def start_feedback(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("📖 Sevimli kitobingiz nomini yozing:")
    await FeedbackState.waiting_for_book_name.set()

@dp.message_handler(state=FeedbackState.waiting_for_book_name)
async def process_book_name(message: types.Message, state: FSMContext):
    if message.text == '↩️ Ortga qaytish':
        await message.answer("🔍 Men sizga kitoblarni chuqur tushunishda yordam berish va ular bo‘yicha qisqacha, aniq xulosalar taqdim etish imkoniyatiga egaman.\n\nIltimos, quyidagi xizmatlardan birini tanlang!",
                reply_markup=start_menu)
        await state.finish()
    else:
        await state.update_data(book_name=message.text)
        await message.answer("📚 Kitob janrini yozing:")
        await FeedbackState.waiting_for_genre.set()

@dp.message_handler(state=FeedbackState.waiting_for_genre)
async def process_genre(message: types.Message, state: FSMContext):
    if message.text == '↩️ Ortga qaytish':
        await message.answer("🔍 Men sizga kitoblarni chuqur tushunishda yordam berish va ular bo‘yicha qisqacha, aniq xulosalar taqdim etish imkoniyatiga egaman.\n\nIltimos, quyidagi xizmatlardan birini tanlang!",
                reply_markup=start_menu)
        await state.finish()
    else:
        await state.update_data(genre=message.text)
        await message.answer("✍️ Muallifning ismini yozing:")
        await FeedbackState.waiting_for_author.set()

@dp.message_handler(state=FeedbackState.waiting_for_author)
async def process_author(message: types.Message, state: FSMContext):
    if message.text == '↩️ Ortga qaytish':
        await message.answer("🔍 Men sizga kitoblarni chuqur tushunishda yordam berish va ular bo‘yicha qisqacha, aniq xulosalar taqdim etish imkoniyatiga egaman.\n\nIltimos, quyidagi xizmatlardan birini tanlang!",
                reply_markup=start_menu)
        await state.finish()
    else:
        await state.update_data(author=message.text)
        await message.answer("📖 Kitobdagi asosiy voqealarni qisqacha yozing:")
        await FeedbackState.waiting_for_summary.set()

@dp.message_handler(state=FeedbackState.waiting_for_summary)
async def process_summary(message: types.Message, state: FSMContext):
    if message.text == '↩️ Ortga qaytish':
        await message.answer("🔍 Men sizga kitoblarni chuqur tushunishda yordam berish va ular bo‘yicha qisqacha, aniq xulosalar taqdim etish imkoniyatiga egaman.\n\nIltimos, quyidagi xizmatlardan birini tanlang!",
                reply_markup=start_menu)
        await state.finish()
    else:
        await state.update_data(summary=message.text)
        await message.answer("📌 Ushbu kitobdan olgan foydali saboqlaringizni yozing:")
        await FeedbackState.waiting_for_lessons.set()

@dp.message_handler(state=FeedbackState.waiting_for_lessons)
async def process_lessons(message: types.Message, state: FSMContext):
    if message.text == '↩️ Ortga qaytish':
        await message.answer("🔍 Men sizga kitoblarni chuqur tushunishda yordam berish va ular bo‘yicha qisqacha, aniq xulosalar taqdim etish imkoniyatiga egaman.\n\nIltimos, quyidagi xizmatlardan birini tanlang!",
                reply_markup=start_menu)
        await state.finish()
    else:
        data = await state.get_data()
        data['lessons'] = message.text
        user_id = message.from_user.id
        
    feedback_text = f"📖 <b>Kitob nomi:</b> {html.escape(data['book_name'])}\n" \
                    f"📚 <b>Janri:</b> {html.escape(data['genre'])}\n" \
                    f"✍️ <b>Muallif:</b> {html.escape(data['author'])}\n" \
                    f"📖 <b>Asosiy voqealar:</b> {html.escape(data['summary'])}\n" \
                    f"📌 <b>Foydali saboqlar:</b> {html.escape(data['lessons'])}\n" \
                    f"👤 <b>Fikr bildiruvchi:</b> @{html.escape(message.from_user.username or message.from_user.full_name)}"

    # Ma'lumotlarni feedback_storage ga saqlash
    feedback_storage[user_id] = data

    try:
        admin_message = await bot.send_message(
            ADMIN_ID,
            f"📩 <b>Yangi fikr keldi!</b>\n\n{feedback_text}\n\n✅ Qabul qilish uchun pastdagi tugmani bosing.",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"accept_feedback:{user_id}")
            ),
            parse_mode='HTML'
        )
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
        return

    await message.answer("✅ Fikringiz adminga yuborildi. Tasdiqlangach, kanalga joylanadi.")
    await message.answer("📢 Kitoblar haqida fikrlarni shu kanaldan o‘qishingiz mumkin: 🔗 @kitoblar_haqida_fikrlar")
    await state.finish()

@dp.callback_query_handler(lambda call: call.data.startswith("accept_feedback"))
async def accept_feedback(call: types.CallbackQuery):
    user_id = int(call.data.split(":")[1]) 

    # Foydalanuvchi haqida qo‘shimcha ma’lumot olish
    try:
        user = await bot.get_chat(user_id)
        username = user.username or user.full_name or "Anonim"
    except Exception as e:
        await call.message.edit_text(f"❌ Foydalanuvchi ma'lumotlarini olishda xato: {str(e)}")
        return

    # Saqlangan ma'lumotlarni olish
    data = feedback_storage.get(user_id)

    if not data:
        await call.message.edit_text("❌ Fikr topilmadi yoki ma'lumotlar allaqachon o'chib ketgan.")
        return

    feedback_text = f"📩 <b>Yangi fikr!</b>\n\n" \
                    f"📖 <b>Kitob nomi:</b> {html.escape(data.get('book_name', 'Noma’lum'))}\n" \
                    f"📚 <b>Janri:</b> {html.escape(data.get('genre', 'Noma’lum'))}\n" \
                    f"✍️ <b>Muallif:</b> {html.escape(data.get('author', 'Noma’lum'))}\n" \
                    f"📖 <b>Asosiy voqealar:</b> {html.escape(data.get('summary', 'Noma’lum'))}\n" \
                    f"📌 <b>Foydali saboqlar:</b> {html.escape(data.get('lessons', 'Noma’lum'))}\n" \
                    f"👤 <b>Fikr bildiruvchi:</b> @{html.escape(username)}"

    try:
        await bot.send_message(CHANNEL_ID, feedback_text, parse_mode='HTML')
        await call.message.edit_text("✅ Fikr kanalga joylandi.")

        feedback_storage.pop(user_id, None)
        
    except Exception as e:
        await call.message.edit_text(f"❌ Xatolik yuz berdi: {str(e)}")
        