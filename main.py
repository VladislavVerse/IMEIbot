from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from utils import is_valid_imei
from dotenv import load_dotenv
import os
import time
import logging

# Загрузка переменных окружения из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Защита от спама
last_request_time = {}

# Клавиатура с кнопками
reply_keyboard = [["Проверить IMEI"]]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу проверить валидность IMEI устройства.\n"
        "Нажмите кнопку 'Проверить IMEI' или введите IMEI вручную.",
        reply_markup=markup
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Показать справку\n"
        "Введите IMEI устройства для проверки."
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    current_time = time.time()

    # Защита от спама (1 запрос в 5 секунд)
    if user_id in last_request_time and current_time - last_request_time[user_id] < 5:
        await update.message.reply_text("Пожалуйста, подождите перед следующим запросом.")
        return

    last_request_time[user_id] = current_time

    text = update.message.text.strip()
    if text == "Проверить IMEI":
        await update.message.reply_text("Введите IMEI устройства.", reply_markup=markup)
    elif is_valid_imei(text):
        await update.message.reply_text(f"IMEI {text} валиден.", reply_markup=markup)
    else:
        await update.message.reply_text(f"IMEI {text} невалиден.", reply_markup=markup)

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Запуск бота
def run_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Добавляем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Добавляем обработчик ошибок
    app.add_error_handler(error_handler)

    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    run_bot()