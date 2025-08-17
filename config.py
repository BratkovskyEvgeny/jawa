import os

from dotenv import load_dotenv

load_dotenv()

# Конфигурация Telegram бота
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", 0))

# Сайты для парсинга мотоциклов Jawa и CZ
PARSING_SITES = {
    "kufar_jawa": {
        "name": "Куфар - Jawa (Беларусь)",
        "base_url": "https://auto.kufar.by",
        "search_url": "https://auto.kufar.by/l/motocikl?brn=264&cur=BYR&ot=1&query=%D1%8F%D0%B2%D0%B0&sort=lst.d",
        "selectors": {
            "items": "article[data-testid='listing-item']",
            "title": "h3[data-testid='listing-title']",
            "price": "span[data-testid='listing-price']",
            "link": "a[data-testid='listing-link']",
            "image": "img[data-testid='listing-image']",
        },
    },
    "kufar_cezet": {
        "name": "Куфар - Cezet (Беларусь)",
        "base_url": "https://auto.kufar.by",
        "search_url": "https://auto.kufar.by/l/motocikl-cezet?cur=BYR&ot=1&query=%D1%8F%D0%B2%D0%B0&sort=lst.d",
        "selectors": {
            "items": "article[data-testid='listing-item']",
            "title": "h3[data-testid='listing-title']",
            "price": "span[data-testid='listing-price']",
            "link": "a[data-testid='listing-link']",
            "image": "img[data-testid='listing-image']",
        },
    },
    "av_by_jawa": {
        "name": "AV.by - Jawa (Беларусь)",
        "base_url": "https://moto.av.by",
        "search_url": "https://moto.av.by/bike/jawa",
        "selectors": {
            "items": ".listing-item",
            "title": ".listing-item__title",
            "price": ".listing-item__price",
            "link": ".listing-item__title a",
            "image": ".listing-item__image img",
        },
    },
    "av_by_cezet": {
        "name": "AV.by - Cezet (Беларусь)",
        "base_url": "https://moto.av.by",
        "search_url": "https://moto.av.by/bike/cezet",
        "selectors": {
            "items": ".listing-item",
            "title": ".listing-item__title",
            "price": ".listing-item__price",
            "link": ".listing-item__title a",
            "image": ".listing-item__image img",
        },
    },
    "abw_by": {
        "name": "abw.by (Беларусь)",
        "base_url": "https://abw.by",
        "search_url": "https://abw.by/moto/brand_jawa",
        "selectors": {
            "items": ".catalog-item",
            "title": ".catalog-item__title",
            "price": ".catalog-item__price",
            "link": ".catalog-item__title a",
            "image": ".catalog-item__image img",
        },
    },
}

# Ключевые слова для поиска мотоциклов Jawa и CZ
SEARCH_KEYWORDS = [
    "jawa",
    "cz",
    "чехословакия",
    "чешский",
    "мотоцикл jawa",
    "мотоцикл cz",
    "jawa 350",
    "jawa 250",
    "cz 175",
    "cz 250",
    "jawa 500",
    "cz 500",
    "ява",
    "ява 350",
    "ява 250",
    "ява 500",
    "jawa 634",
    "jawa 638",
    "jawa 360",
    "ява 634",
    "ява 638",
    "ява 360",
]

# Настройки парсинга
PARSING_INTERVAL = 30  # минуты
MAX_ITEMS_PER_SITE = 20
REQUEST_DELAY = 2  # секунды между запросами

# Настройки базы данных
DATABASE_PATH = "motorcycle_ads.db"
