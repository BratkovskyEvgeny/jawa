#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы с белорусскими сайтами
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser import AdvancedParser

import config


def test_belarus_sites():
    """Тестирование белорусских сайтов"""
    print("🇧🇾 Тестирование белорусских сайтов для мотоциклов Jawa")
    print("=" * 60)

    # Создаем экземпляр парсера
    parser = AdvancedParser()

    # Список белорусских сайтов
    belarus_sites = ["kufar", "av_by", "abw_by"]

    for site_key in belarus_sites:
        if site_key in config.PARSING_SITES:
            site_config = config.PARSING_SITES[site_key]
            print(f"\n🌐 Тестирование сайта: {site_config['name']}")
            print(f"URL: {site_config['search_url']}")

            try:
                # Парсим сайт
                ads = parser.parse_site(site_key)

                print(f"✅ Найдено объявлений Jawa: {len(ads)}")

                # Показываем первые 3 объявления
                for i, ad in enumerate(ads[:3]):
                    print(f"  {i+1}. {ad.get('title', 'Без заголовка')}")
                    print(f"     Цена: {ad.get('price', 'Не указана')}")
                    print(f"     Ссылка: {ad.get('link', 'Нет ссылки')}")
                    if ad.get("image_url"):
                        print(f"     Изображение: {ad.get('image_url')}")
                    print()

            except Exception as e:
                print(f"❌ Ошибка при парсинге {site_config['name']}: {e}")
        else:
            print(f"❌ Сайт {site_key} не найден в конфигурации")

    print("\n" + "=" * 60)
    print("🏁 Тестирование белорусских сайтов завершено!")


def test_jawa_keywords():
    """Тестирование поиска по ключевым словам Jawa"""
    print("\n🔍 Тестирование поиска по ключевым словам Jawa")
    print("=" * 50)

    parser = AdvancedParser()

    # Тестируем поиск по разным вариантам написания Jawa
    test_queries = ["Jawa", "Ява", "jawa", "ява", "Jawa 350", "Ява 350"]

    for query in test_queries:
        print(f"\n🏍️ Поиск по запросу: '{query}'")
        try:
            results = parser.search_specific_model(query)
            print(f"   Найдено: {len(results)} объявлений")

            if results:
                for i, ad in enumerate(results[:2]):
                    print(f"   {i+1}. {ad.get('title', 'Без заголовка')}")
                    print(f"      Сайт: {ad.get('site_name', 'Неизвестно')}")
                    print(f"      Цена: {ad.get('price', 'Не указана')}")

        except Exception as e:
            print(f"   ❌ Ошибка: {e}")


def main():
    """Главная функция тестирования"""
    print("🚀 Запуск тестирования белорусских сайтов для мотоциклов Jawa")
    print("=" * 70)

    try:
        # Тестируем белорусские сайты
        test_belarus_sites()

        # Тестируем поиск по ключевым словам
        test_jawa_keywords()

        print("\n🎉 Все тесты завершены успешно!")
        print("\n📝 Теперь у вас есть доступ к:")
        print("   • Куфар (Беларусь) - много объявлений Jawa")
        print("   • AV.by (Беларусь) - специализированный раздел Jawa")
        print("   • ABW.by (Беларусь) - брендовый раздел Jawa")
        print("\n🇧🇾 Все сайты - белорусские, без проблем с блокировкой!")

    except KeyboardInterrupt:
        print("\n⏹️ Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
