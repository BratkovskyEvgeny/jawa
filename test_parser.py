#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы парсера
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser import AdvancedParser
from database import Database
import config

def test_parser():
    """Тестирование парсера"""
    print("🧪 Тестирование парсера мотоциклов Jawa и CZ")
    print("=" * 50)
    
    # Создаем экземпляр парсера
    parser = AdvancedParser()
    
    # Тестируем парсинг каждого сайта
    for site_key, site_config in config.PARSING_SITES.items():
        print(f"\n🌐 Тестирование сайта: {site_config['name']}")
        print(f"URL: {site_config['search_url']}")
        
        try:
            # Парсим сайт
            ads = parser.parse_site(site_key)
            
            print(f"✅ Найдено объявлений: {len(ads)}")
            
            # Показываем первые 3 объявления
            for i, ad in enumerate(ads[:3]):
                print(f"  {i+1}. {ad.get('title', 'Без заголовка')}")
                print(f"     Цена: {ad.get('price', 'Не указана')}")
                print(f"     Ссылка: {ad.get('link', 'Нет ссылки')}")
                print()
                
        except Exception as e:
            print(f"❌ Ошибка при парсинге {site_config['name']}: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Тестирование завершено!")

def test_database():
    """Тестирование базы данных"""
    print("\n💾 Тестирование базы данных")
    print("=" * 30)
    
    try:
        # Создаем экземпляр БД
        db = Database()
        print("✅ База данных инициализирована")
        
        # Получаем статистику
        stats = db.get_statistics()
        print(f"📊 Статистика: {stats}")
        
        # Тестируем поиск
        search_results = db.search_advertisements("jawa", limit=5)
        print(f"🔍 Результаты поиска 'jawa': {len(search_results)} объявлений")
        
    except Exception as e:
        print(f"❌ Ошибка при работе с БД: {e}")

def test_search():
    """Тестирование поиска конкретных моделей"""
    print("\n🔍 Тестирование поиска конкретных моделей")
    print("=" * 40)
    
    parser = AdvancedParser()
    
    test_models = ["Jawa 350", "CZ 175", "Jawa 250", "CZ 250"]
    
    for model in test_models:
        print(f"\n🏍️ Поиск модели: {model}")
        try:
            results = parser.search_specific_model(model)
            print(f"   Найдено: {len(results)} объявлений")
            
            if results:
                for i, ad in enumerate(results[:2]):
                    print(f"   {i+1}. {ad.get('title', 'Без заголовка')}")
                    print(f"      Сайт: {ad.get('site_name', 'Неизвестно')}")
                    
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

def main():
    """Главная функция тестирования"""
    print("🚀 Запуск тестирования Telegram-бота для мотоциклов Jawa и CZ")
    print("=" * 70)
    
    try:
        # Тестируем парсер
        test_parser()
        
        # Тестируем базу данных
        test_database()
        
        # Тестируем поиск
        test_search()
        
        print("\n🎉 Все тесты завершены успешно!")
        print("\n📝 Для запуска бота используйте: python telegram_bot.py")
        
    except KeyboardInterrupt:
        print("\n⏹️ Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
