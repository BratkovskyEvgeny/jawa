import logging
import threading
import time
from parser import AdvancedParser

import schedule

import config
from database import Database

logger = logging.getLogger(__name__)


class ParsingScheduler:
    def __init__(self):
        self.db = Database()
        self.parser = AdvancedParser()
        self.is_running = False
        self.thread = None

    def start_scheduler(self):
        """Запуск планировщика в отдельном потоке"""
        if self.is_running:
            logger.info("Планировщик уже запущен")
            return

        self.is_running = True

        # Настраиваем расписание
        schedule.every(config.PARSING_INTERVAL).minutes.do(self.run_parsing)

        # Запускаем планировщик в отдельном потоке
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()

        logger.info(
            f"Планировщик запущен. Парсинг каждые {config.PARSING_INTERVAL} минут"
        )

    def stop_scheduler(self):
        """Остановка планировщика"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Планировщик остановлен")

    def _run_scheduler(self):
        """Основной цикл планировщика"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Проверяем каждую минуту
            except Exception as e:
                logger.error(f"Ошибка в планировщике: {e}")
                time.sleep(300)  # Ждем 5 минут при ошибке

    def run_parsing(self):
        """Выполнение парсинга всех сайтов"""
        try:
            logger.info("🔄 Запуск автоматического парсинга...")

            # Парсим все сайты
            new_ads = self.parser.parse_all_sites()

            # Сохраняем в базу данных
            added_count = 0
            for ad in new_ads:
                if self.db.add_advertisement(ad):
                    added_count += 1

            logger.info(
                f"✅ Парсинг завершен. Добавлено {added_count} новых объявлений"
            )

            # Очищаем старые объявления (старше 30 дней)
            self.db.cleanup_old_ads(days=30)

        except Exception as e:
            logger.error(f"❌ Ошибка при автоматическом парсинге: {e}")

    def run_parsing_now(self):
        """Запуск парсинга немедленно"""
        logger.info("🚀 Запуск немедленного парсинга...")
        self.run_parsing()

    def get_next_run_time(self):
        """Получение времени следующего запуска"""
        jobs = schedule.get_jobs()
        if jobs:
            return jobs[0].next_run
        return None

    def get_schedule_info(self):
        """Получение информации о расписании"""
        jobs = schedule.get_jobs()
        info = {
            "is_running": self.is_running,
            "next_run": self.get_next_run_time(),
            "interval_minutes": config.PARSING_INTERVAL,
            "total_jobs": len(jobs),
        }
        return info


def main():
    """Тестирование планировщика"""
    scheduler = ParsingScheduler()

    try:
        # Запускаем планировщик
        scheduler.start_scheduler()

        # Запускаем немедленный парсинг
        scheduler.run_parsing_now()

        # Держим программу запущенной
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
        scheduler.stop_scheduler()
        logger.info("Программа завершена")


if __name__ == "__main__":
    main()
