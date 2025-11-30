"""
Скрипт для проверки подключения бота к Telegram API
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения
env_paths = [
    Path(__file__).parent.parent / '.env',
    Path(__file__).parent / '.env',
    Path.cwd().parent / '.env',
    Path.cwd() / '.env',
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Загружен .env из: {env_path}")
        break
else:
    load_dotenv()
    print("⚠️  .env файл не найден, используем переменные окружения системы")

BOT_TOKEN = os.getenv('BOT_TOKEN', '')

if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не установлен!")
    print("\nУстановите BOT_TOKEN одним из способов:")
    print("1. Создайте файл .env в корне проекта или в папке bot/")
    print("2. Добавьте строку: BOT_TOKEN=ваш_токен")
    print("3. Или установите переменную окружения BOT_TOKEN")
    sys.exit(1)

print(f"\n🔍 Проверка подключения к Telegram API...")
print(f"Токен: {BOT_TOKEN[:10]}...{BOT_TOKEN[-5:]}")

try:
    import asyncio
    from telegram import Bot
    
    async def test_bot():
        bot = Bot(token=BOT_TOKEN)
        bot_info = await bot.get_me()
        
        print("\n✅ Бот успешно подключен!")
        print(f"   Имя: {bot_info.first_name}")
        print(f"   Username: @{bot_info.username}")
        print(f"   ID: {bot_info.id}")
        print(f"   Может присоединяться к группам: {bot_info.can_join_groups}")
        print(f"   Может читать сообщения групп: {bot_info.can_read_all_group_messages}")
        
        print("\n✅ Все проверки пройдены! Бот готов к работе.")
        print("\n💡 Запустите бота командой: python main.py")
    
    asyncio.run(test_bot())
    
except ImportError:
    print("\n❌ ОШИБКА: Не установлена библиотека python-telegram-bot")
    print("Установите её командой: pip install python-telegram-bot")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ ОШИБКА при подключении к Telegram API:")
    print(f"   {type(e).__name__}: {e}")
    print("\nВозможные причины:")
    print("1. Неверный BOT_TOKEN")
    print("2. Проблемы с интернет-соединением")
    print("3. Telegram API временно недоступен")
    sys.exit(1)

