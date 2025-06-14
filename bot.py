import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Отправь, пожалуйста, чек об оплате курса (фото).")

@dp.message(F.photo)
async def handle_photo(message: Message):
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=f"Новый чек от @{message.from_user.username or 'не указано'} (id: {message.from_user.id})"
    )
    await message.answer("Спасибо! Чек отправлен на проверку. Ответ придёт в течение 4 часов.")

@dp.message(F.reply_to_message, F.text.in_(['✅', '❌']))
async def admin_reply(message: Message):
    caption = message.reply_to_message.caption
    if caption and 'id: ' in caption:
        try:
            user_id_text = caption.split('id: ')[-1].strip().rstrip(')')
            user_id = int(user_id_text)
            if message.text == '✅':
                await bot.send_message(user_id, "✅ Оплата подтверждена! Вот ссылка на курс: https://t.me/+tU_u4LCb7UliNmRi")
            else:
                await bot.send_message(user_id, "❌ Платёж не подтверждён. Проверь чек и попробуй снова.")
        except Exception as e:
            await message.reply(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
