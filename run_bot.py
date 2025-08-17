#!/usr/bin/env python3
"""
Главный файл для запуска Telegram-бота с планировщиком
"""

import asyncio
import threading
import logging
import signal
import sys
from telegram_bot import JawaCzBot
from scheduler import ParsingScheduler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BotRunner:
    def __init__(self):
        self.bot = None
        self.scheduler = None
        self.is_running = False
        
    def setup_signal_handlers(self):
        """Настройка обработчиков сигналов для graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Получен сигнал {signum}, завершаем работу...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def start_scheduler(self):
        """Запуск планировщика в отдельном потоке"""
        try:
            self.scheduler = ParsingScheduler()
            self.scheduler.start_scheduler()
            logger.info("✅ Планировщик запущен успешно")
            
            # Запускаем немедленный парсинг
            self.scheduler.run_parsing_now()
            
        except Exception as e:
            logger.error(f"❌ Ошибка при запуске планировщика: {e}")
    
    def start_bot(self):
        """Запуск Telegram-бота"""
        try:
            self.bot = JawaCzBot()
            logger.info("✅ Telegram-бот инициализирован")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при инициализации бота: {e}")
            raise
    
    def run(self):
        """Основной цикл запуска"""
        try:
            logger.info("🚀 Запуск Telegram-бота для мотоциклов Jawa и CZ")
            
            # Настраиваем обработчики сигналов
            self.setup_signal_handlers()
            
            # Запускаем планировщик
            self.start_scheduler()
            
            # Запускаем бота
            self.start_bot()
            
            self.is_running = True
            logger.info("🎉 Бот успешно запущен и готов к работе!")
            
            # Запускаем бота
            self.bot.run()
            
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки от пользователя")
            self.shutdown()
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}")
            self.shutdown()
            raise
    
    def shutdown(self):
        """Graceful shutdown"""
        if not self.is_running:
            return
            
        logger.info("🔄 Завершение работы...")
        
        try:
            # Останавливаем планировщик
            if self.scheduler:
                self.scheduler.stop_scheduler()
                logger.info("✅ Планировщик остановлен")
            
            # Останавливаем бота
            if self.bot and self.bot.application:
                self.bot.application.stop()
                logger.info("✅ Telegram-бот остановлен")
                
        except Exception as e:
            logger.error(f"Ошибка при остановке: {e}")
        
        self.is_running = False
        logger.info("🏁 Работа завершена")

def main():
    """Главная функция"""
    print("🏍️ Telegram-бот для поиска мотоциклов Jawa и CZ")
    print("=" * 50)
    
    # Проверяем наличие необходимых файлов
    required_files = ['.env', 'config.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Отсутствуют необходимые файлы: {', '.join(missing_files)}")
        print("📝 Создайте файл .env на основе env_example.txt")
        return
    
    # Запускаем бота
    runner = BotRunner()
    
    try:
        runner.run()
    except Exception as e:
        print(f"💥 Ошибка запуска: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import os
    main()
