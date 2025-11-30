"""
Основной файл телеграм-бота
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
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

# Хранение активных сессий обмена геолокацией
# Формат: {sender_id: receiver_id}
location_sharing_sessions = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        # Проверяем, что update.message существует
        if not update.message:
            logger.error("❌ update.message is None в команде /start")
            logger.error(f"Update: {update}")
            return
        
        user = update.message.from_user
        logger.info(f"📨 Получена команда /start от пользователя:")
        logger.info(f"   ID: {user.id}")
        logger.info(f"   Имя: {user.first_name} {user.last_name or ''}")
        logger.info(f"   Username: @{user.username or 'не указан'}")
        
        web_url = os.getenv('WEB_URL', 'https://your-username.github.io/FIT/')
        logger.info(f"🌐 WEB_URL: {web_url}")
        
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
        
        logger.info("📤 Отправка ответа пользователю...")
        sent_message = await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        logger.info(f"✅ Ответ на /start отправлен успешно (Message ID: {sent_message.message_id})")
    except Exception as e:
        logger.error(f"❌ Ошибка в обработчике /start: {e}", exc_info=True)
        logger.error(f"   Тип ошибки: {type(e).__name__}")
        if update.message:
            try:
                await update.message.reply_text(
                    'Произошла ошибка при обработке команды. Попробуйте позже.'
                )
            except Exception as send_error:
                logger.error(f"❌ Не удалось отправить сообщение об ошибке: {send_error}")


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
            '/menu - Открыть меню\n'
            '/my_id - Узнать свой ID\n'
            '/share_location - Поделиться геолокацией\n'
            '/stop_location - Остановить обмен геолокацией\n\n'
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


async def share_location_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для начала обмена геолокацией"""
    try:
        if not update.message:
            return
        
        user = update.message.from_user
        user_id = user.id
        
        # Проверяем, не делится ли уже пользователь геолокацией
        if user_id in location_sharing_sessions:
            receiver_id = location_sharing_sessions[user_id]
            await update.message.reply_text(
                f"⚠️ Вы уже делитесь геолокацией с пользователем (ID: {receiver_id})\n\n"
                f"Используйте /stop_location чтобы остановить обмен."
            )
            return
        
        # Получаем ID получателя из аргументов команды
        if context.args and len(context.args) > 0:
            try:
                receiver_id = int(context.args[0])
                
                # Проверяем, что получатель существует
                try:
                    receiver = await context.bot.get_chat(receiver_id)
                    receiver_name = receiver.first_name or f"ID: {receiver_id}"
                except:
                    await update.message.reply_text(
                        "❌ Не удалось найти получателя. Проверьте правильность ID."
                    )
                    return
                
                # Создаем сессию обмена
                location_sharing_sessions[user_id] = receiver_id
                
                # Создаем клавиатуру с кнопкой для отправки геолокации
                keyboard = [
                    [KeyboardButton("📍 Отправить мою геолокацию", request_location=True)],
                    [KeyboardButton("⏹ Остановить обмен")]
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
                
                await update.message.reply_text(
                    f"✅ Обмен геолокацией активирован!\n\n"
                    f"📤 Вы делитесь геолокацией с: {receiver_name}\n\n"
                    f"📍 Нажмите кнопку ниже, чтобы отправить вашу текущую геолокацию.\n"
                    f"⏹ Используйте /stop_location чтобы остановить обмен.",
                    reply_markup=reply_markup
                )
                
                # Уведомляем получателя
                try:
                    await context.bot.send_message(
                        receiver_id,
                        f"📍 <b>{user.first_name}</b> начал делиться с вами геолокацией.\n\n"
                        f"Вы будете получать обновления его местоположения.\n"
                        f"Используйте /stop_location чтобы остановить получение.",
                        parse_mode='HTML'
                    )
                except Exception as e:
                    logger.warning(f"Не удалось уведомить получателя {receiver_id}: {e}")
                
                logger.info(f"📍 Пользователь {user_id} начал делиться геолокацией с {receiver_id}")
                
            except ValueError:
                await update.message.reply_text(
                    "❌ Неверный формат ID получателя.\n\n"
                    "Использование: /share_location <ID_получателя>\n\n"
                    "Пример: /share_location 123456789"
                )
        else:
            await update.message.reply_text(
                "📍 <b>Обмен геолокацией</b>\n\n"
                "Использование: /share_location <ID_получателя>\n\n"
                "Пример: /share_location 123456789\n\n"
                "Чтобы узнать ID пользователя, попросите его написать боту @userinfobot",
                parse_mode='HTML'
            )
            
    except Exception as e:
        logger.error(f"Ошибка в share_location_command: {e}", exc_info=True)
        if update.message:
            await update.message.reply_text("Произошла ошибка. Попробуйте позже.")


async def my_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать свой ID"""
    try:
        if not update.message:
            return
        
        user = update.message.from_user
        user_id = user.id
        username = user.username or "не указан"
        name = f"{user.first_name} {user.last_name or ''}".strip()
        
        text = (
            f"🆔 <b>Ваша информация:</b>\n\n"
            f"ID: <code>{user_id}</code>\n"
            f"Имя: {name}\n"
            f"Username: @{username}\n\n"
            f"💡 <i>Поделитесь этим ID с тем, кто хочет делиться с вами геолокацией.</i>"
        )
        
        await update.message.reply_text(text, parse_mode='HTML')
        logger.info(f"🆔 Пользователь {user_id} запросил свой ID")
        
    except Exception as e:
        logger.error(f"Ошибка в my_id_command: {e}", exc_info=True)
        if update.message:
            await update.message.reply_text("Произошла ошибка. Попробуйте позже.")


async def stop_location_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Остановка обмена геолокацией"""
    try:
        if not update.message:
            return
        
        user_id = update.message.from_user.id
        
        if user_id in location_sharing_sessions:
            receiver_id = location_sharing_sessions[user_id]
            del location_sharing_sessions[user_id]
            
            # Убираем клавиатуру
            await update.message.reply_text(
                "⏹ Обмен геолокацией остановлен.",
                reply_markup=ReplyKeyboardRemove()
            )
            
            # Уведомляем получателя
            try:
                user_name = update.message.from_user.first_name
                await context.bot.send_message(
                    receiver_id,
                    f"⏹ <b>{user_name}</b> остановил обмен геолокацией.",
                    parse_mode='HTML'
                )
            except Exception as e:
                logger.warning(f"Не удалось уведомить получателя {receiver_id}: {e}")
            
            logger.info(f"⏹ Пользователь {user_id} остановил обмен геолокацией с {receiver_id}")
        else:
            # Проверяем, не является ли пользователь получателем
            sender_id = None
            for sid, rid in location_sharing_sessions.items():
                if rid == user_id:
                    sender_id = sid
                    break
            
            if sender_id:
                del location_sharing_sessions[sender_id]
                try:
                    sender_name = (await context.bot.get_chat(sender_id)).first_name
                    await update.message.reply_text(
                        f"⏹ Вы больше не получаете геолокацию от {sender_name}.",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    await context.bot.send_message(
                        sender_id,
                        f"⏹ Получатель остановил получение вашей геолокации.",
                        parse_mode='HTML'
                    )
                except Exception as e:
                    logger.warning(f"Ошибка при остановке получения: {e}")
            else:
                await update.message.reply_text(
                    "ℹ️ Вы не делитесь геолокацией и не получаете её.",
                    reply_markup=ReplyKeyboardRemove()
                )
                
    except Exception as e:
        logger.error(f"Ошибка в stop_location_command: {e}", exc_info=True)
        if update.message:
            await update.message.reply_text("Произошла ошибка. Попробуйте позже.")


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик получения геолокации"""
    try:
        if not update.message or not update.message.location:
            return
        
        sender_id = update.message.from_user.id
        location = update.message.location
        
        # Проверяем, есть ли активная сессия обмена
        if sender_id in location_sharing_sessions:
            receiver_id = location_sharing_sessions[sender_id]
            
            try:
                sender_name = update.message.from_user.first_name or "Пользователь"
                
                # Отправляем геолокацию получателю
                await context.bot.send_location(
                    receiver_id,
                    latitude=location.latitude,
                    longitude=location.longitude
                )
                
                # Отправляем текстовое сообщение с координатами
                await context.bot.send_message(
                    receiver_id,
                    f"📍 <b>{sender_name}</b> поделился геолокацией:\n\n"
                    f"Широта: {location.latitude}\n"
                    f"Долгота: {location.longitude}",
                    parse_mode='HTML'
                )
                
                # Подтверждаем отправителю
                await update.message.reply_text("✅ Геолокация отправлена!")
                
                logger.info(f"📍 Геолокация от {sender_id} отправлена {receiver_id}")
                
            except Exception as e:
                logger.error(f"Ошибка при отправке геолокации: {e}")
                await update.message.reply_text(
                    "❌ Не удалось отправить геолокацию. Возможно, получатель заблокировал бота."
                )
        else:
            await update.message.reply_text(
                "ℹ️ У вас нет активной сессии обмена геолокацией.\n"
                "Используйте /share_location чтобы начать обмен."
            )
            
    except Exception as e:
        logger.error(f"Ошибка в handle_location: {e}", exc_info=True)


async def handle_stop_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки 'Остановить обмен'"""
    if update.message and update.message.text == "⏹ Остановить обмен":
        await stop_location_command(update, context)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Эхо-обработчик для текстовых сообщений"""
    try:
        if update.message:
            # Проверяем, не является ли это кнопкой остановки
            if update.message.text == "⏹ Остановить обмен":
                await handle_stop_button(update, context)
            else:
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


async def post_init(application: Application) -> None:
    """Вызывается после инициализации бота"""
    bot_info = await application.bot.get_me()
    logger.info(f"Бот успешно подключен: @{bot_info.username} (ID: {bot_info.id})")
    logger.info(f"Имя бота: {bot_info.first_name}")
    logger.info("Бот готов к работе и ожидает команды...")

def main():
    """Запуск бота"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не установлен!")
        logger.error("Установите BOT_TOKEN в переменных окружения или в .env файле")
        return
    
    logger.info("=" * 50)
    logger.info("🚀 Запуск телеграм-бота...")
    logger.info(f"BOT_TOKEN установлен: {'✅ Да' if BOT_TOKEN else '❌ Нет'}")
    logger.info(f"WEB_URL: {os.getenv('WEB_URL', 'не установлен')}")
    
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
        
        # Регистрируем обработчики
        logger.info("📝 Регистрация обработчиков команд...")
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("my_id", my_id_command))
        application.add_handler(CommandHandler("share_location", share_location_command))
        application.add_handler(CommandHandler("stop_location", stop_location_command))
        
        # Обработчик геолокации (должен быть перед TEXT handler)
        application.add_handler(MessageHandler(filters.LOCATION, handle_location))
        
        # Обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        logger.info("✅ Обработчики зарегистрированы")
        
        # Регистрируем обработчик ошибок
        application.add_error_handler(error_handler)
        logger.info("✅ Обработчик ошибок зарегистрирован")
        
        # Запускаем бота
        logger.info("🔄 Запуск polling...")
        logger.info("=" * 50)
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True  # Игнорируем старые обновления при запуске
        )
    except Exception as e:
        logger.error(f"❌ Критическая ошибка при запуске бота: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()

