#!/bin/bash

echo "🏍️ Telegram-бот для поиска мотоциклов Jawa и CZ"
echo "================================================"
echo

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден! Установите Python 3.8+"
    exit 1
fi

# Проверяем версию Python
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Требуется Python 3.8+, у вас $python_version"
    exit 1
fi

echo "✅ Python $python_version найден"

# Проверяем наличие .env файла
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Создайте файл .env на основе env_example.txt"
    echo
    echo "Содержимое .env должно быть:"
    echo "TELEGRAM_TOKEN=ваш_токен_бота"
    echo "ADMIN_USER_ID=ваш_telegram_id"
    echo
    exit 1
fi

echo "✅ Файл .env найден"

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Ошибка при установке зависимостей"
    exit 1
fi

echo
echo "✅ Зависимости установлены"
echo "🚀 Запуск бота..."
echo

# Запускаем бота
python3 run_bot.py
