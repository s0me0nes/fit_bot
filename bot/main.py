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

# Настройка логирования (сначала, чтобы можно было использовать logger)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения из .env файла
# Пробуем несколько путей
env_paths = [
    Path(__file__).parent.parent / '.env',  # В корне проекта
    Path(__file__).parent / '.env',  # В папке bot
    Path.cwd().parent / '.env',  # Родительская папка от текущей
    Path.cwd() / '.env',  # Текущая папка
]

env_loaded = False
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        env_loaded = True
        logger.info(f"Загружен .env из: {env_path}")
        break

if not env_loaded:
    # Пробуем загрузить без указания пути (из текущей директории)
    load_dotenv()
    logger.warning(".env файл не найден, используем переменные окружения системы")

# Токен бота (получаем из переменных окружения)
BOT_TOKEN = os.getenv('BOT_TOKEN', '')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        # Проверяем, что update.message существует
        if not update.message:
            logger.error("update.message is None в команде /start")
            return
        
        logger.info(f"Получена команда /start от пользователя {update.message.from_user.id}")
        
        web_url = os.getenv('WEB_URL', 'https://your-username.github.io/FIT/')
        
        # Создаем красивое меню с тремя кнопками
        keyboard = [
            [InlineKeyboardButton(
                text="🌐 Открыть сайт",
                web_app=WebAppInfo(url=web_url)
            )],
            [InlineKeyboardButton(
                text="📞 Связь для заказа",
                url="https://t.me/MariaZeynalova"
            )],
            [InlineKeyboardButton(
                text="🚚 Связь с курьером",
                url="https://t.me/Nill_Kafri"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = (
            "👋 Добро пожаловать!\n\n"
            "Выберите нужный раздел:\n\n"
            "🌐 <b>Открыть сайт</b> - просмотр меню и оформление заказа\n"
            "📞 <b>Связь для заказа</b> - связь с менеджером\n"
            "🚚 <b>Связь с курьером</b> - связь с курьером"
        )
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        logger.info("Ответ на /start отправлен успешно")
    except Exception as e:
        logger.error(f"Ошибка в обработчике /start: {e}", exc_info=True)
        if update.message:
            try:
                await update.message.reply_text(
                    'Произошла ошибка при обработке команды. Попробуйте позже.'
                )
            except:
                pass


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    try:
        if not update.message:
            logger.error("update.message is None в команде /help")
            return
        
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
    except Exception as e:
        logger.error(f"Ошибка в обработчике /help: {e}", exc_info=True)


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Открывает меню через Mini App"""
    try:
        if not update.message:
            logger.error("update.message is None в команде /menu")
            return
        
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
    except Exception as e:
        logger.error(f"Ошибка в обработчике /menu: {e}", exc_info=True)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Эхо-обработчик для текстовых сообщений"""
    try:
        if update.message:
            await update.message.reply_text(update.message.text)
    except Exception as e:
        logger.error(f"Ошибка в обработчике echo: {e}", exc_info=True)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка при обработке обновления: {context.error}", exc_info=True)
    if update and update.message:
        try:
            await update.message.reply_text(
                'Произошла ошибка. Попробуйте позже или используйте /help для справки.'
            )
        except:
            pass


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
    
    # Регистрируем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    logger.info("Бот запущен...")
    logger.info(f"BOT_TOKEN установлен: {'Да' if BOT_TOKEN else 'Нет'}")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

