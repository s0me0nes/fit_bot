"""
Основной файл телеграм-бота
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные окружения из .env файла
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота (получаем из переменных окружения)
BOT_TOKEN = os.getenv('BOT_TOKEN', '')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        'Привет! Я телеграм-бот с веб-сайтом.\n'
        'Используй /help для списка команд.'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        'Доступные команды:\n'
        '/start - Начать работу\n'
        '/help - Показать эту справку\n'
        '/web - Получить ссылку на веб-сайт'
    )


async def web_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет ссылку на веб-сайт"""
    web_url = os.getenv('WEB_URL', 'http://localhost:8000')
    await update.message.reply_text(f'🌐 Веб-сайт: {web_url}')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Эхо-обработчик для текстовых сообщений"""
    await update.message.reply_text(update.message.text)


def main():
    """Запуск бота"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не установлен!")
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("web", web_link))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

