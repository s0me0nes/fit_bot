# 🚀 Инструкция по деплою

## Railway.app (Самый простой способ)

### Шаг 1: Подготовка
1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Подключите ваш GitHub репозиторий

### Шаг 2: Деплой бэкенда
1. Нажмите "New Project" → "Deploy from GitHub repo"
2. Выберите ваш репозиторий
3. В настройках проекта:
   - **Root Directory**: `backend`
   - **Start Command**: `python main.py`
4. В разделе "Variables" добавьте:
   - `PORT` = `8000` (Railway автоматически установит, но можно указать явно)
5. Railway автоматически даст вам URL (например: `https://your-app.railway.app`)
6. **Скопируйте этот URL** - он понадобится для бота

### Шаг 3: Деплой бота
1. В том же проекте нажмите "New Service" → "GitHub Repo"
2. Выберите тот же репозиторий
3. В настройках:
   - **Root Directory**: `bot`
   - **Start Command**: `python main.py`
4. В разделе "Variables" добавьте:
   - `BOT_TOKEN` = ваш токен от BotFather
   - `WEB_URL` = URL вашего бэкенда (из шага 2)

### Готово! 🎉
Оба сервиса запущены и работают.

---

## Render.com (Альтернатива)

### Бэкенд
1. Создайте новый **Web Service**
2. Подключите GitHub репозиторий
3. Настройки:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Environment Variables**: `PORT=8000`

### Бот
1. Создайте новый **Background Worker**
2. Подключите тот же репозиторий
3. Настройки:
   - **Root Directory**: `bot`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Environment Variables**: 
     - `BOT_TOKEN=ваш_токен`
     - `WEB_URL=url_вашего_бэкенда`

---

## VPS (Полный контроль)

### Установка зависимостей
```bash
sudo apt update
sudo apt install python3 python3-pip git nginx
```

### Клонирование и настройка
```bash
git clone <ваш_репозиторий>
cd FIT

# Установка зависимостей
cd backend && pip3 install -r requirements.txt
cd ../bot && pip3 install -r requirements.txt
```

### Создание systemd сервисов

**`/etc/systemd/system/telegram-bot.service`:**
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/FIT/bot
Environment="BOT_TOKEN=ваш_токен"
Environment="WEB_URL=https://ваш-домен.com"
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**`/etc/systemd/system/web-backend.service`:**
```ini
[Unit]
Description=Web Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/FIT/backend
Environment="PORT=8000"
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Запуск
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot web-backend
sudo systemctl start telegram-bot web-backend
sudo systemctl status telegram-bot web-backend
```

### Nginx конфигурация (опционально)
```nginx
server {
    listen 80;
    server_name ваш-домен.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔑 Получение токена бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в переменную `BOT_TOKEN`

---

## ✅ Проверка работы

1. **Бэкенд**: Откройте URL в браузере - должна загрузиться страница
2. **Бот**: Откройте бота в Telegram и отправьте `/start`

---

## 🐛 Решение проблем

### Бот не отвечает
- Проверьте, что `BOT_TOKEN` правильный
- Проверьте логи в Railway/Render
- Убедитесь, что бот запущен

### Бэкенд не доступен
- Проверьте, что порт указан правильно
- Проверьте логи
- Убедитесь, что сервис запущен

### Ошибки при деплое
- Проверьте, что все зависимости в `requirements.txt`
- Убедитесь, что Root Directory указан правильно
- Проверьте логи сборки

