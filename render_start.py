#!/usr/bin/env python3
"""
Запуск бота на Render с веб-сервером
"""

import os
import threading
import time

from scheduler import ParsingScheduler
from telegram_bot import JawaCzBot
from web_server import app


def start_bot():
    """Запуск Telegram бота"""
    try:
        print("🔄 Инициализация Telegram бота...")
        bot = JawaCzBot()
        print("✅ Telegram-бот инициализирован")
        print("🚀 Запуск бота...")
        bot.run()
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        import traceback
        traceback.print_exc()


def start_scheduler():
    """Запуск планировщика"""
    try:
        scheduler = ParsingScheduler()
        scheduler.start_scheduler()
        print("✅ Планировщик запущен")

        # Запускаем немедленный парсинг
        scheduler.run_parsing_now()

        # Держим планировщик запущенным
        while True:
            time.sleep(60)
    except Exception as e:
        print(f"❌ Ошибка при запуске планировщика: {e}")


def main():
    """Главная функция"""
    print("🚀 Запуск Jawa CZ Bot на Render")
    
    # Проверяем переменные окружения
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("❌ ОШИБКА: TELEGRAM_TOKEN не установлен!")
        return
    
    admin_id = os.environ.get("ADMIN_USER_ID")
    if not admin_id:
        print("❌ ОШИБКА: ADMIN_USER_ID не установлен!")
        return
    
    print(f"✅ TELEGRAM_TOKEN: {'*' * len(token)}")
    print(f"✅ ADMIN_USER_ID: {admin_id}")

    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    print("✅ Планировщик запущен в отдельном потоке")

    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    print("✅ Бот запущен в отдельном потоке")

    # Запускаем веб-сервер в основном потоке
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Веб-сервер запущен на порту {port}")
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
