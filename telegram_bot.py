import asyncio
import logging
from datetime import datetime
from parser import AdvancedParser

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import config
from database import Database

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class JawaCzBot:
    def __init__(self):
        self.db = Database()
        self.parser = AdvancedParser()
        self.application = None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """
🏍️ *Добро пожаловать в бот для поиска мотоциклов Jawa и CZ!*

Я помогу вам найти актуальные объявления о продаже мотоциклов Jawa и CZ с различных сайтов.

*Доступные команды:*
• /search - Поиск объявлений
• /latest - Последние объявления
• /stats - Статистика
• /sites - Объявления по сайтам
• /help - Справка

        *Настроенные сайты:*
        • Куфар (Беларусь)
        • AV.by (Беларусь)
        • ABW.by (Беларусь)

Используйте /search для начала поиска!
        """

        keyboard = [
            [InlineKeyboardButton("🔍 Поиск", callback_data="search")],
            [InlineKeyboardButton("📰 Последние", callback_data="latest")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton("🌐 По сайтам", callback_data="sites")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
📖 *Справка по использованию бота*

*Основные команды:*
• `/start` - Главное меню
• `/search` - Поиск объявлений
• `/latest` - Последние объявления
• `/stats` - Статистика по объявлениям
• `/sites` - Объявления по конкретным сайтам

*Поиск:*
• Используйте `/search` для поиска по ключевым словам
• Бот автоматически ищет мотоциклы Jawa и CZ
• Можно указать конкретную модель (например, "Jawa 350")

*Уведомления:*
• Бот автоматически проверяет новые объявления каждые 30 минут
• Новые объявления помечаются как "новые"

        *Поддерживаемые сайты:*
        • Куфар (Беларусь) - auto.kufar.by
        • AV.by (Беларусь) - moto.av.by
        • ABW.by (Беларусь) - abw.by

*Примеры поиска:*
• Jawa 350
• CZ 175
• Чешский мотоцикл
• Jawa 500
        """

        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /search"""
        if not context.args:
            await update.message.reply_text(
                "🔍 *Поиск объявлений*\n\n"
                "Используйте команду с ключевым словом:\n"
                "`/search Jawa 350`\n"
                "`/search CZ 175`\n"
                "`/search чешский`",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        query = " ".join(context.args)
        await update.message.reply_text(
            f"🔍 Ищу объявления по запросу: *{query}*", parse_mode=ParseMode.MARKDOWN
        )

        # Выполняем поиск
        try:
            ads = self.parser.search_specific_model(query)

            if not ads:
                await update.message.reply_text(
                    "❌ По вашему запросу ничего не найдено."
                )
                return

            # Отправляем результаты
            await self._send_ads_results(
                update, ads, f"Результаты поиска по запросу: {query}"
            )

        except Exception as e:
            logger.error(f"Ошибка при поиске: {e}")
            await update.message.reply_text(
                "❌ Произошла ошибка при поиске. Попробуйте позже."
            )

    async def latest_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /latest"""
        await update.message.reply_text("📰 Получаю последние объявления...")

        try:
            # Получаем новые объявления из базы
            new_ads = self.db.get_new_advertisements(limit=20)

            if not new_ads:
                await update.message.reply_text("📭 Новых объявлений пока нет.")
                return

            await self._send_ads_results(update, new_ads, "📰 Последние объявления:")

        except Exception as e:
            logger.error(f"Ошибка при получении последних объявлений: {e}")
            await update.message.reply_text("❌ Произошла ошибка. Попробуйте позже.")

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /stats"""
        try:
            stats = self.db.get_statistics()

            stats_text = f"""
📊 *Статистика объявлений*

📈 *Общая статистика:*
• Всего объявлений: {stats['total_ads']}
• Новых объявлений: {stats['new_ads']}

🌐 *По сайтам:*
"""

            for site, count in stats["site_stats"].items():
                stats_text += f"• {site}: {count}\n"

            stats_text += (
                f"\n⏰ Последнее обновление: {datetime.now().strftime('%H:%M:%S')}"
            )

            await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

        except Exception as e:
            logger.error(f"Ошибка при получении статистики: {e}")
            await update.message.reply_text("❌ Ошибка при получении статистики.")

    async def sites_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /sites"""
        keyboard = []

        for site_key, site_config in config.PARSING_SITES.items():
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"🌐 {site_config['name']}", callback_data=f"site_{site_key}"
                    )
                ]
            )

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🌐 *Выберите сайт для просмотра объявлений:*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()

        if query.data == "search":
            # Создаем фейковый update для команды поиска
            fake_update = type("Update", (), {"message": query.message})()
            await self.search_command(fake_update, context)
        elif query.data == "latest":
            fake_update = type("Update", (), {"message": query.message})()
            await self.latest_command(fake_update, context)
        elif query.data == "stats":
            fake_update = type("Update", (), {"message": query.message})()
            await self.stats_command(fake_update, context)
        elif query.data == "sites":
            fake_update = type("Update", (), {"message": query.message})()
            await self.sites_command(fake_update, context)
        elif query.data.startswith("site_"):
            site_key = query.data.replace("site_", "")
            await self._show_site_ads(update, context, site_key)
        elif query.data.startswith("ad_"):
            ad_id = int(query.data.replace("ad_", ""))
            await self._show_ad_details(update, context, ad_id)

    async def _show_site_ads(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, site_key: str
    ):
        """Показать объявления с конкретного сайта"""
        try:
            site_ads = self.db.get_advertisements_by_site(
                config.PARSING_SITES[site_key]["name"], limit=15
            )

            if not site_ads:
                await update.callback_query.edit_message_text(
                    f"📭 На сайте {config.PARSING_SITES[site_key]['name']} пока нет объявлений."
                )
                return

            await self._send_ads_results(
                update,
                site_ads,
                f"🌐 Объявления с сайта {config.PARSING_SITES[site_key]['name']}:",
            )

        except Exception as e:
            logger.error(f"Ошибка при получении объявлений с сайта: {e}")
            await update.callback_query.edit_message_text(
                "❌ Ошибка при получении объявлений."
            )

    async def _show_ad_details(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, ad_id: int
    ):
        """Показать детали объявления"""
        try:
            # Получаем детали объявления
            ads = self.db.get_new_advertisements(limit=100)
            ad = next((ad for ad in ads if ad["id"] == ad_id), None)

            if not ad:
                await update.callback_query.answer("Объявление не найдено")
                return

            # Отмечаем как просмотренное
            self.db.mark_as_viewed(ad_id)

            # Формируем детальное сообщение
            details_text = f"""
🏍️ *{ad['title']}*

💰 Цена: {ad.get('price', 'Не указана')}
🌐 Сайт: {ad['site_name']}
🔗 [Ссылка на объявление]({ad['link']})
⏰ Добавлено: {ad['created_at']}
            """

            if ad.get("description"):
                details_text += f"\n📝 Описание:\n{ad['description']}"

            # Кнопка для возврата
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="latest")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.callback_query.edit_message_text(
                details_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )

        except Exception as e:
            logger.error(f"Ошибка при показе деталей объявления: {e}")
            await update.callback_query.answer("Ошибка при получении деталей")

    async def _send_ads_results(self, update: Update, ads: list, title: str):
        """Отправка результатов поиска объявлений"""
        if not ads:
            await update.message.reply_text("📭 Объявления не найдены.")
            return

        # Отправляем заголовок
        await update.message.reply_text(
            f"**{title}**\nНайдено: {len(ads)} объявлений",
            parse_mode=ParseMode.MARKDOWN,
        )

        # Отправляем объявления группами по 5
        for i in range(0, len(ads), 5):
            batch = ads[i : i + 5]
            await self._send_ads_batch(update, batch)
            
        # Добавляем отладочную информацию
        logger.info(f"Отправлено {len(ads)} объявлений для запроса: {title}")

    async def _send_ads_batch(self, update: Update, ads: list):
        """Отправка группы объявлений"""
        for ad in ads:
            try:
                # Формируем текст объявления
                ad_text = f"""
🏍️ *{ad['title']}*
💰 Цена: {ad.get('price', 'Не указана')}
🌐 Сайт: {ad['site_name']}
                """

                # Кнопка для просмотра деталей
                keyboard = [
                    [InlineKeyboardButton("📋 Детали", callback_data=f"ad_{ad['id']}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    ad_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
                )

                # Небольшая задержка между сообщениями
                await asyncio.sleep(0.5)
                
                # Добавляем отладочную информацию
                logger.info(f"Отправлено объявление: {ad.get('title', 'Без заголовка')}")

            except Exception as e:
                logger.error(f"Ошибка при отправке объявления: {e}")
                continue

    async def run_parsing(self):
        """Запуск автоматического парсинга"""
        while True:
            try:
                logger.info("Запуск автоматического парсинга...")

                # Парсим все сайты
                new_ads = self.parser.parse_all_sites()

                # Сохраняем в базу данных
                added_count = 0
                for ad in new_ads:
                    if self.db.add_advertisement(ad):
                        added_count += 1

                logger.info(
                    f"Парсинг завершен. Добавлено {added_count} новых объявлений."
                )

                # Ждем следующего цикла
                await asyncio.sleep(config.PARSING_INTERVAL * 60)

            except Exception as e:
                logger.error(f"Ошибка в автоматическом парсинге: {e}")
                await asyncio.sleep(300)  # Ждем 5 минут при ошибке

    def run(self):
        """Запуск бота"""
        # Создаем приложение
        self.application = Application.builder().token(config.TELEGRAM_TOKEN).build()

        # Добавляем обработчики команд
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("search", self.search_command))
        self.application.add_handler(CommandHandler("latest", self.latest_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("sites", self.sites_command))

        # Добавляем обработчик кнопок
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

        # Запускаем бота
        logger.info("Бот запущен!")
        self.application.run_polling()


if __name__ == "__main__":
    bot = JawaCzBot()
    bot.run()
