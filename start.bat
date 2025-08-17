@echo off
chcp 65001 >nul
echo 🏍️ Telegram-бот для поиска мотоциклов Jawa и CZ
echo ================================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.8+
    pause
    exit /b 1
)

REM Проверяем наличие .env файла
if not exist ".env" (
    echo ❌ Файл .env не найден!
    echo 📝 Создайте файл .env на основе env_example.txt
    echo.
    echo Содержимое .env должно быть:
    echo TELEGRAM_TOKEN=ваш_токен_бота
    echo ADMIN_USER_ID=ваш_telegram_id
    echo.
    pause
    exit /b 1
)

REM Устанавливаем зависимости
echo 📦 Установка зависимостей...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей
    pause
    exit /b 1
)

echo.
echo ✅ Зависимости установлены
echo 🚀 Выберите действие:
echo.
echo 1. Запустить бота
echo 2. Протестировать парсер
echo 3. Протестировать белорусские сайты
echo.
echo 🇧🇾 Теперь только белорусские сайты - без блокировок!
echo.
set /p choice="Введите номер (1-3): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Запуск бота...
    python run_bot.py
) else if "%choice%"=="2" (
    echo.
    echo 🧪 Тестирование парсера...
    python test_parser.py
) else if "%choice%"=="3" (
    echo.
    echo 🇧🇾 Тестирование белорусских сайтов...
    python test_belarus_sites.py
) else (
    echo.
    echo ❌ Неверный выбор. Запускаю бота...
    python run_bot.py
)

pause
