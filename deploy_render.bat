@echo off
chcp 65001 >nul
echo 🌐 Развертывание бота на Render
echo ================================
echo.

echo 📋 Инструкция по развертыванию:
echo.
echo 1. Зарегистрируйтесь на https://render.com
echo 2. Подключите GitHub аккаунт
echo 3. Нажмите "New +"
echo 4. Выберите "Web Service"
echo 5. Подключите ваш репозиторий jawa
echo 6. В разделе Environment Variables добавьте:
echo    TELEGRAM_TOKEN=ваш_токен_бота
echo    ADMIN_USER_ID=ваш_telegram_id
echo 7. Нажмите "Create Web Service"
echo.

echo 📁 Файлы для развертывания готовы:
echo ✅ Procfile
echo ✅ runtime.txt
echo ✅ render_start.py
echo ✅ web_server.py
echo ✅ requirements.txt
echo.

echo 🌐 После деплоя ваш бот будет доступен 24/7!
echo.

pause
