from aiogram import executor

from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import handlers
import logging
from handlers.summary import register_handlers_summary


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    
    # INFO level loglarni chiqarish
    logging.basicConfig(level=logging.INFO)
    
    # Barcha handlerlarni yuklash
    register_handlers_summary(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    