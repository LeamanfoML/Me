import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import Config
from services.scheduler import Scheduler
from database import db
import asyncio

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(bot)
scheduler = None

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🔄 Обновить сейчас"))
    keyboard.add(types.KeyboardButton("⚙️ Настройки"))
    
    await message.reply(
        "🤖 Добро пожаловать в бота арбитража NFT!\n\n"
        "Я автоматически отслеживаю выгодные сделки между:\n"
        "• Portals Market\n• Tonnel Relayer Bot\n\n"
        "Используйте кнопки ниже для управления:",
        reply_markup=keyboard
    )

@dp.message_handler(text="🔄 Обновить сейчас")
async def manual_update(message: types.Message):
    # Проверка прав доступа
    if message.from_user.id != Config.ADMIN_CHAT_ID:
        return await message.reply("❌ Доступ запрещен!")
    
    await message.reply("⏳ Запускаю обновление данных...")
    await scheduler.update_data()
    await message.reply("✅ Данные успешно обновлены!")

@dp.message_handler(text="⚙️ Настройки")
async def show_settings(message: types.Message):
    # Реализация меню настроек
    pass

async def on_startup(dp):
    global scheduler
    scheduler = Scheduler(bot)
    asyncio.create_task(scheduler.start())
    await bot.send_message(
        chat_id=Config.ADMIN_CHAT_ID,
        text="🤖 Бот арбитража NFT запущен!\n"
             f"⏱ Автообновление каждые {Config.UPDATE_INTERVAL} сек"
    )

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
