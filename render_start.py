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
        bot = JawaCzBot()
        print("✅ Telegram-бот инициализирован")
        bot.run()
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")


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

    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    # Запускаем веб-сервер в основном потоке
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Веб-сервер запущен на порту {port}")
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
