# 🚀 Развертывание бота на хостинге

## 📋 Варианты развертывания

### 1. Render (Рекомендуется - бесплатно)
### 2. Railway (Платно)
### 3. Heroku (Платно)
### 4. VPS сервер

---



## 🌐 Render (Рекомендуется - бесплатно)

### Шаг 1: Подготовка
1. Зарегистрируйтесь на [render.com](https://render.com)
2. Подключите GitHub аккаунт

### Шаг 2: Создание Web Service
1. Нажмите "New +"
2. Выберите "Web Service"
3. Подключите ваш репозиторий `jawa`

### Шаг 3: Настройка
- **Name**: `jawa-bot`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python render_start.py`

### Шаг 4: Переменные окружения
В разделе "Environment Variables" добавьте:
```env
TELEGRAM_TOKEN=ваш_токен_бота
ADMIN_USER_ID=ваш_telegram_id
```

### Шаг 5: Деплой
1. Нажмите "Create Web Service"
2. Дождитесь завершения деплоя
3. Ваш бот будет доступен по ссылке вида: `https://jawa-bot.onrender.com`

---

## 🚂 Railway (Платный вариант)

**⚠️ Внимание: Railway стал платным сервисом!**

### Шаг 1: Подготовка
1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Подключите GitHub аккаунт
3. **Потребуется кредитная карта для верификации**

### Шаг 2: Создание проекта
1. Нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Выберите ваш репозиторий `jawa`

### Шаг 3: Настройка переменных
В разделе "Variables" добавьте:
```env
TELEGRAM_TOKEN=ваш_токен_бота
ADMIN_USER_ID=ваш_telegram_id
```

### Шаг 4: Деплой
1. Railway автоматически определит Python проект
2. Нажмите "Deploy Now"
3. Дождитесь завершения деплоя

**💡 Рекомендуем использовать Render - он бесплатный!**

---

## 🎯 Heroku

### Шаг 1: Установка Heroku CLI
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# macOS
brew tap heroku/brew && brew install heroku
```

### Шаг 2: Логин
```bash
heroku login
```

### Шаг 3: Создание приложения
```bash
heroku create jawa-bot
```

### Шаг 4: Настройка переменных
```bash
heroku config:set TELEGRAM_TOKEN=ваш_токен_бота
heroku config:set ADMIN_USER_ID=ваш_telegram_id
```

### Шаг 5: Деплой
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

---

## 🖥️ VPS сервер

### Шаг 1: Аренда VPS
- **DigitalOcean** - от $5/месяц
- **Linode** - от $5/месяц
- **Vultr** - от $2.50/месяц

### Шаг 2: Подключение
```bash
ssh root@ваш_ip_адрес
```

### Шаг 3: Установка зависимостей
```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Python
apt install python3 python3-pip python3-venv -y

# Установка Git
apt install git -y
```

### Шаг 4: Клонирование проекта
```bash
git clone https://github.com/ваш_username/jawa.git
cd jawa
```

### Шаг 5: Настройка виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Шаг 6: Создание .env файла
```bash
nano .env
```
Добавьте:
```env
TELEGRAM_TOKEN=ваш_токен_бота
ADMIN_USER_ID=ваш_telegram_id
```

### Шаг 7: Запуск через systemd
```bash
nano /etc/systemd/system/jawa-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=Jawa CZ Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/jawa
Environment=PATH=/root/jawa/venv/bin
ExecStart=/root/jawa/venv/bin/python render_start.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Шаг 8: Запуск сервиса
```bash
systemctl daemon-reload
systemctl enable jawa-bot
systemctl start jawa-bot
systemctl status jawa-bot
```

---

## 🔧 Мониторинг и логи

### Railway/Render/Heroku
- Логи доступны в веб-интерфейсе
- Автоматический перезапуск при ошибках

### VPS
```bash
# Просмотр логов
journalctl -u jawa-bot -f

# Перезапуск сервиса
systemctl restart jawa-bot

# Статус сервиса
systemctl status jawa-bot
```

---

## 🚨 Важные моменты

1. **Токен бота** - храните в секрете
2. **Переменные окружения** - настройте на хостинге
3. **Мониторинг** - следите за логами
4. **Резервное копирование** - регулярно делайте бэкапы

---

## 🎉 После развертывания

Ваш бот будет работать 24/7 и будет доступен даже когда компьютер выключен!

**Удачного развертывания!** 🚀✨
