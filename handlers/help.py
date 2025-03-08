from loader import dp
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from keyboards.inline.menu import start_menu


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam"
            )

    await message.answer("\n".join(text))


@dp.callback_query_handler(lambda call: call.data == "help")
async def show_help(call: types.CallbackQuery):
    await call.answer()
    
    help_text = (
        "ℹ️ <b>Yordam</b>\n\n"
        "Ushbu bot quyidagi imkoniyatlarni taqdim etadi:\n\n"
        "📖 <b>Kitob tahlili</b> – Siz kiritgan kitob haqida qisqacha tahlil beradi.\n"
        "📚 <b>Tavsiyalar</b> – Qiziqishlaringizga mos kitoblarni tavsiya qiladi.\n"
        "💬 <b>Suhbat</b> – O'zingiz qiziqqan kitob haqida umumiy suhbat qilishingiz mumkin.\n"
        "⭐ <b>Fikr bildirish</b> – Sevimli kitobingiz haqida fikr qoldirishingiz mumkin.\n\n"
        "Qo‘shimcha savollaringiz bo‘lsa, admin bilan bog‘lanishingiz mumkin.\n"
        "Admin: @mr_uzdev"
    )
    
    await call.message.edit_text(help_text, parse_mode="HTML", reply_markup=start_menu)


@dp.message_handler(commands=['cannel'])
async def cannel(message: types.Message):
    await message.answer("Sizga kitoblarni tushunishda va qisqacha xulosalar berishda yordam beraman.", reply_markup=start_menu)


@dp.message_handler(lambda message: message.text == '↩️ Ortga qaytish')
async def cannel(message: types.Message):
    await message.answer("Sizga kitoblarni tushunishda va qisqacha xulosalar berishda yordam beraman.", reply_markup=start_menu)
    