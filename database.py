import sqlite3
from typing import Dict, List

import config


class Database:
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Таблица для объявлений
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS advertisements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    price TEXT,
                    link TEXT NOT NULL,
                    image_url TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_new BOOLEAN DEFAULT TRUE,
                    hash TEXT UNIQUE
                )
            """)

            # Таблица для настроек пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER PRIMARY KEY,
                    notifications_enabled BOOLEAN DEFAULT TRUE,
                    min_price INTEGER DEFAULT 0,
                    max_price INTEGER DEFAULT 999999,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()

    def add_advertisement(self, ad_data: Dict) -> bool:
        """Добавление нового объявления в базу данных"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Создаем хеш для уникальности объявления
                ad_hash = f"{ad_data['site_name']}_{ad_data['title']}_{ad_data['link']}"

                cursor.execute(
                    """
                    INSERT OR IGNORE INTO advertisements 
                    (site_name, title, price, link, image_url, description, hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        ad_data["site_name"],
                        ad_data["title"],
                        ad_data.get("price", ""),
                        ad_data["link"],
                        ad_data.get("image_url", ""),
                        ad_data.get("description", ""),
                        ad_hash,
                    ),
                )

                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка при добавлении объявления: {e}")
            return False

    def get_new_advertisements(self, limit: int = 50) -> List[Dict]:
        """Получение новых объявлений"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM advertisements 
                WHERE is_new = TRUE 
                ORDER BY created_at DESC 
                LIMIT ?
            """,
                (limit,),
            )

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def mark_as_viewed(self, ad_id: int):
        """Отметить объявление как просмотренное"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE advertisements 
                SET is_new = FALSE 
                WHERE id = ?
            """,
                (ad_id,),
            )
            conn.commit()

    def get_advertisements_by_site(self, site_name: str, limit: int = 20) -> List[Dict]:
        """Получение объявлений по конкретному сайту"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM advertisements 
                WHERE site_name = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """,
                (site_name, limit),
            )

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def search_advertisements(self, query: str, limit: int = 20) -> List[Dict]:
        """Поиск объявлений по ключевому слову"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM advertisements 
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY created_at DESC 
                LIMIT ?
            """,
                (f"%{query}%", f"%{query}%", limit),
            )

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_statistics(self) -> Dict:
        """Получение статистики по объявлениям"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Общее количество объявлений
            cursor.execute("SELECT COUNT(*) FROM advertisements")
            total_ads = cursor.fetchone()[0]

            # Количество новых объявлений
            cursor.execute("SELECT COUNT(*) FROM advertisements WHERE is_new = TRUE")
            new_ads = cursor.fetchone()[0]

            # Количество объявлений по сайтам
            cursor.execute("""
                SELECT site_name, COUNT(*) as count 
                FROM advertisements 
                GROUP BY site_name
            """)
            site_stats = dict(cursor.fetchall())

            return {
                "total_ads": total_ads,
                "new_ads": new_ads,
                "site_stats": site_stats,
            }

    def cleanup_old_ads(self, days: int = 30):
        """Очистка старых объявлений"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM advertisements 
                WHERE created_at < datetime('now', '-{} days')
            """.format(days)
            )
            conn.commit()
