import re
import time
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import config


class MotorcycleParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def parse_site(self, site_key: str) -> List[Dict]:
        """Парсинг конкретного сайта"""
        site_config = config.PARSING_SITES.get(site_key)
        if not site_config:
            print(f"Конфигурация для сайта {site_key} не найдена")
            return []

        try:
            print(f"Парсинг сайта: {site_config['name']}")

            # Получаем HTML страницы
            response = self.session.get(site_config["search_url"], timeout=30)
            response.raise_for_status()

            # Парсим HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Извлекаем объявления
            ads = self._extract_ads(soup, site_config)

            # Фильтруем по ключевым словам Jawa и CZ
            filtered_ads = self._filter_jawa_cz_ads(ads)

            print(
                f"Найдено {len(filtered_ads)} объявлений Jawa/CZ на {site_config['name']}"
            )

            # Добавляем информацию о сайте
            for ad in filtered_ads:
                ad["site_name"] = site_config["name"]
                ad["site_key"] = site_key

            return filtered_ads

        except Exception as e:
            print(f"Ошибка при парсинге {site_config['name']}: {e}")
            return []

    def _extract_ads(self, soup: BeautifulSoup, site_config: Dict) -> List[Dict]:
        """Извлечение объявлений с HTML страницы"""
        ads = []
        selectors = site_config["selectors"]

        # Находим все элементы объявлений
        ad_elements = soup.select(selectors["items"])

        for element in ad_elements[: config.MAX_ITEMS_PER_SITE]:
            try:
                ad = {}

                # Заголовок
                title_elem = element.select_one(selectors["title"])
                if title_elem:
                    ad["title"] = title_elem.get_text(strip=True)

                # Цена
                price_elem = element.select_one(selectors["price"])
                if price_elem:
                    ad["price"] = price_elem.get_text(strip=True)

                # Ссылка
                link_elem = element.select_one(selectors["link"])
                if link_elem:
                    link = link_elem.get("href", "")
                    if link:
                        ad["link"] = urljoin(site_config["base_url"], link)

                # Изображение
                img_elem = element.select_one(selectors["image"])
                if img_elem:
                    img_src = img_elem.get("src") or img_elem.get("data-src")
                    if img_src:
                        ad["image_url"] = urljoin(site_config["base_url"], img_src)

                # Описание (если есть)
                desc_elem = element.select_one("p, .description, .desc")
                if desc_elem:
                    ad["description"] = desc_elem.get_text(strip=True)

                # Проверяем, что у нас есть минимум данных
                if ad.get("title") and ad.get("link"):
                    ads.append(ad)

            except Exception as e:
                print(f"Ошибка при извлечении объявления: {e}")
                continue

        return ads

    def _filter_jawa_cz_ads(self, ads: List[Dict]) -> List[Dict]:
        """Фильтрация объявлений по ключевым словам Jawa и CZ"""
        filtered_ads = []

        for ad in ads:
            title = ad.get("title", "").lower()
            description = ad.get("description", "").lower()

            # Расширенные ключевые слова для лучшего поиска
            jawa_keywords = [
                "jawa",
                "ява",
                "cezet",
                "чезет",
                "cz",
                "чехословакия",
                "чешский",
            ]

            # Проверяем наличие ключевых слов
            for keyword in jawa_keywords:
                if keyword in title or keyword in description:
                    filtered_ads.append(ad)
                    break

            # Также проверяем по основным ключевым словам из конфига
            for keyword in config.SEARCH_KEYWORDS:
                if keyword.lower() in title or keyword.lower() in description:
                    if ad not in filtered_ads:  # Избегаем дублирования
                        filtered_ads.append(ad)
                    break

        return filtered_ads

    def parse_all_sites(self) -> List[Dict]:
        """Парсинг всех настроенных сайтов"""
        all_ads = []

        for site_key in config.PARSING_SITES.keys():
            try:
                print(f"Парсинг сайта: {config.PARSING_SITES[site_key]['name']}")
                site_ads = self.parse_site(site_key)
                all_ads.extend(site_ads)
                print(
                    f"Найдено {len(site_ads)} объявлений Jawa/CZ на {config.PARSING_SITES[site_key]['name']}"
                )

                # Задержка между запросами к разным сайтам
                if (
                    site_key != list(config.PARSING_SITES.keys())[-1]
                ):  # Не ждем после последнего сайта
                    time.sleep(config.REQUEST_DELAY)

            except Exception as e:
                print(
                    f"Ошибка при парсинге {config.PARSING_SITES[site_key]['name']}: {e}"
                )
                continue

        return all_ads

    def search_specific_model(self, model: str) -> List[Dict]:
        """Поиск конкретной модели мотоцикла"""
        all_ads = self.parse_all_sites()

        # Фильтруем по ключевым словам Jawa и CZ
        model_ads = []
        model_lower = model.lower()

        # Расширенные ключевые слова для поиска
        jawa_keywords = ["jawa", "ява", "cezet", "чезет", "cz"]

        for ad in all_ads:
            title = ad.get("title", "").lower()
            description = ad.get("description", "").lower()

            # Проверяем точное совпадение модели
            if model_lower in title or model_lower in description:
                model_ads.append(ad)
                continue

            # Проверяем по ключевым словам Jawa/CZ
            for keyword in jawa_keywords:
                if keyword in title or keyword in description:
                    model_ads.append(ad)
                    break

        return model_ads


class AdvancedParser(MotorcycleParser):
    """Расширенный парсер с дополнительными возможностями"""

    def __init__(self):
        super().__init__()
        self.session.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def parse_with_retry(self, site_key: str, max_retries: int = 3) -> List[Dict]:
        """Парсинг с повторными попытками при ошибках"""
        for attempt in range(max_retries):
            try:
                return self.parse_site(site_key)
            except Exception as e:
                print(f"Попытка {attempt + 1} для {site_key} не удалась: {e}")
                if attempt < max_retries - 1:
                    time.sleep(config.REQUEST_DELAY * (attempt + 1))
                else:
                    print(f"Все попытки для {site_key} исчерпаны")
                    return []

    def get_ad_details(self, ad_url: str) -> Optional[Dict]:
        """Получение детальной информации об объявлении"""
        try:
            response = self.session.get(ad_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            details = {}

            # Извлекаем дополнительные детали
            # Год выпуска
            year_pattern = r"\b(19[5-9]\d|20[0-2]\d)\b"
            text_content = soup.get_text()
            year_match = re.search(year_pattern, text_content)
            if year_match:
                details["year"] = year_match.group(1)

            # Пробег
            mileage_pattern = r"(\d+)\s*(км|тыс\.?\s*км|тысяч\s*км)"
            mileage_match = re.search(mileage_pattern, text_content, re.IGNORECASE)
            if mileage_match:
                details["mileage"] = (
                    mileage_match.group(1) + " " + mileage_match.group(2)
                )

            # Состояние
            condition_keywords = [
                "отличное",
                "хорошее",
                "удовлетворительное",
                "требует ремонта",
            ]
            for keyword in condition_keywords:
                if keyword in text_content.lower():
                    details["condition"] = keyword
                    break

            return details

        except Exception as e:
            print(f"Ошибка при получении деталей объявления {ad_url}: {e}")
            return None
