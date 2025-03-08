import os
import requests
import logging
import asyncio
from keyboards.inline.menu import start_menu
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import CHANNEL
from utils.misc import subscription

logging.basicConfig(level=logging.INFO)

# Xabarlarni saqlash uchun vaqtinchalik dict
message_to_delete = {}

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    name = message.from_user.first_name

    url_post = os.getenv('CREATE_USER')
    url_get = os.getenv('USER_INFO')

    try:
        check_user = requests.get(f'{url_get}{user_id}')
        if check_user.status_code == 200:
            text = (f"Assalomu alaykum, hurmatli foydalanuvchi!\n\n"
                    "📚 Men <i><b>Book Analytica</b></i> botiman.\n\n"
                    "Sizga kitoblarni chuqur tahlil qilish, ularning mazmunini tushunishda yordam berish va qisqacha, aniq xulosalar taqdim etish imkoniyatiga egaman.\n")
    
            # Birinchi xabarni yuboramiz va message_id ni saqlaymiz
            welcome_msg = await message.answer(text, parse_mode='HTML')
            message_to_delete[user_id] = [welcome_msg.message_id]  # Saqlash
        else:
            data = {
                'name': name,
                'user_name': user_name,
                'telegram_id': user_id,
            }
            
            res = requests.post(url_post, data=data)
            if res.status_code == 200:
                # Ro'yxatdan o'tish xabari
                reg_msg = await message.answer(f"Assalomu alaykum {name}!\n Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
                message_to_delete[user_id] = [reg_msg.message_id]  # Saqlash
            else:
                error_msg = await message.answer("Ro'yxatdan o'tishda xatolik yuz berdi.")
                message_to_delete[user_id] = [error_msg.message_id]  # Saqlash

        check_sub_markup = InlineKeyboardMarkup()
        for channel in CHANNEL:
            try:
                chat = await bot.get_chat(channel)
                invite_link = await chat.export_invite_link()
                check_sub_markup.add(InlineKeyboardButton(
                    text=f"{chat.title}",
                    url=invite_link
                ))
            except Exception as e:
                logging.error(f"Kanal uchun havola olishda xatolik: {channel} - {e}")

        check_sub_markup.add(InlineKeyboardButton(
            text="✅ Obunani tekshirish",
            callback_data="check_subs"
        ))

        # Obuna tekshirish xabarini yuboramiz va message_id ni saqlaymiz
        sub_msg = await message.answer(
            "🤝 Hamkor kanalimizga a'zo bo'lib qo'ying!",
            reply_markup=check_sub_markup,
            disable_web_page_preview=True
        )
        message_to_delete[user_id].append(sub_msg.message_id)  # Saqlash

    except Exception as e:
        logging.exception("An error occurred: %s", str(e))

@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    try:
        result = ""
        all_subscribed = True

        for channel in CHANNEL:
            status = await subscription.check(user_id=user_id, channel=channel)
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()

            if status:
                result += f"✅ <a href='{invite_link}'><b>{chat.title}</b></a> kanaliga obuna bo'lgansiz!\n\n"
            else:
                result += f"❌ <a href='{invite_link}'><b>{chat.title}</b></a> kanaliga obuna bo'lmagansiz! Obuna bo'lish uchun <a href='{invite_link}'>bu yerga bosing</a>.\n\n"
                all_subscribed = False

        if all_subscribed:
            # Agar barcha kanallarga obuna bo'lsa, avvalgi xabarlarni o‘chiramiz
            if user_id in message_to_delete:
                for msg_id in message_to_delete[user_id]:
                    try:
                        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
                    except Exception as e:
                        logging.error(f"Xabarni o‘chirishda xatolik: {msg_id} - {e}")
                # O‘chirilgan xabarlarni ro‘yxatdan o‘chiramiz
                message_to_delete.pop(user_id, None)

            # Yangi xabarni yuboramiz
            success_msg = await call.message.answer(
                "🔍 Men sizga kitoblarni chuqur tushunishda yordam berish va ular bo‘yicha qisqacha, aniq xulosalar taqdim etish imkoniyatiga egaman.\n\nIltimos, quyidagi xizmatlardan birini tanlang!",
                reply_markup=start_menu
            )
        else:
            await call.message.answer(result, disable_web_page_preview=True)

    except Exception as e:
        logging.exception("An error occurred in subscription check: %s", str(e))