
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Включаем логирование, чтобы видеть ошибки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- ВАЖНЫЕ ПЕРЕМЕННЫЕ ---
# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на реальный токен вашего бота
BOT_TOKEN = "8282443190:AAESG9behz4_m3pbYDCaCOFBj7wXmxiWMd8"

# !!! ВАЖНО: Это временный URL. Замените его на реальный URL вашего Web App, когда он будет готов.
# Для теста можно использовать любой сайт, например, от Google.
WEB_APP_URL = "https://me-seven-nu.vercel.app/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Эта функция вызывается по команде /start.
    Она отправляет приветственное сообщение и кнопку для открытия Web App.
    """
    # Создаем объект WebAppInfo, который указывает на ваше веб-приложение
    web_app_info = WebAppInfo(url=WEB_APP_URL)

    # Создаем inline-кнопку, которая будет открывать наше веб-приложение
    keyboard = [
        [InlineKeyboardButton("🚀 Открыть Аниме-хаб", web_app=web_app_info)]
    ]

    # Создаем разметку с этой кнопкой
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Получаем имя пользователя для персонального приветствия
    user_name = update.effective_user.first_name

    # Отправляем сообщение пользователю
    await update.message.reply_text(
        f"👋 Привет, {user_name}!\n\n"
        "Добро пожаловать в Аниме-хаб. Здесь ты можешь найти и отслеживать свои любимые аниме и мангу.\n\n"
        "Нажми на кнопку ниже, чтобы начать!",
        reply_markup=reply_markup
    )


def main() -> None:
    """Основная функция для запуска бота."""
    # Создаем приложение и передаем ему токен бота
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота. Он будет работать, пока вы его не остановите (Ctrl-C)
    logger.info("Бот запущен...")
    application.run_polling()
    logger.info("Бот остановлен.")


if __name__ == "__main__":
    main()
