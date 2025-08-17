@echo off
chcp 65001 >nul
echo 🔄 Обновление pip...
echo.

python.exe -m pip install --upgrade pip

echo.
echo ✅ Обновление завершено!
pause
