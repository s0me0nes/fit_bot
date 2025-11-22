"""
Основной файл телеграм-бота
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
    web_url = os.getenv('WEB_URL', 'https://your-username.github.io/FIT/')
    
    # Создаем кнопку для открытия Mini App
    keyboard = [
        [InlineKeyboardButton(
            text="🍽️ Открыть меню",
            web_app=WebAppInfo(url=web_url)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        'Привет! Я телеграм-бот с меню.\n\n'
        'Нажмите кнопку ниже, чтобы открыть меню:',
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    web_url = os.getenv('WEB_URL', 'https://your-username.github.io/FIT/')
    
    keyboard = [
        [InlineKeyboardButton(
            text="🍽️ Открыть меню",
            web_app=WebAppInfo(url=web_url)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        'Доступные команды:\n'
        '/start - Начать работу\n'
        '/help - Показать эту справку\n'
        '/menu - Открыть меню\n\n'
        'Или нажмите кнопку ниже:',
        reply_markup=reply_markup
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Открывает меню через Mini App"""
    web_url = os.getenv('WEB_URL', 'https://your-username.github.io/FIT/')
    
    keyboard = [
        [InlineKeyboardButton(
            text="🍽️ Открыть меню",
            web_app=WebAppInfo(url=web_url)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        'Нажмите кнопку, чтобы открыть меню:',
        reply_markup=reply_markup
    )


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
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

