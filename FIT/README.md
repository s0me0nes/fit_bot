# Telegram Bot с Веб-сайтом

Проект состоит из двух частей:
- **bot/** - Код телеграм-бота
- **backend/** - Код веб-сайта/бэкенда

## 🚀 Быстрый старт

### Локальная разработка

1. **Установите зависимости для бота:**
```bash
cd bot
pip install -r requirements.txt
```

2. **Установите зависимости для бэкенда:**
```bash
cd ../backend
pip install -r requirements.txt
```

3. **Создайте файл `.env` в корне проекта:**
```env
BOT_TOKEN=ваш_токен_бота_от_BotFather
WEB_URL=http://localhost:8000
PORT=8000
```

4. **Запустите бэкенд:**
```bash
cd backend
python main.py
```

5. **В другом терминале запустите бота:**
```bash
cd bot
python main.py
```

## 📦 Деплой

### Вариант 1: Railway.app (Рекомендуется)

1. **Создайте аккаунт на [Railway.app](https://railway.app)**

2. **Установите Railway CLI:**
```bash
npm i -g @railway/cli
railway login
```

3. **Создайте два сервиса в Railway:**
   - Один для бота (`bot/`)
   - Один для бэкенда (`backend/`)

4. **Для каждого сервиса:**
   - Подключите GitHub репозиторий
   - Укажите корневую папку (`bot/` или `backend/`)
   - Добавьте переменные окружения:
     - Для бота: `BOT_TOKEN`, `WEB_URL` (URL вашего бэкенда)
     - Для бэкенда: `PORT` (Railway автоматически установит)

5. **Railway автоматически определит Python и установит зависимости**

### Вариант 2: Render.com

1. **Создайте аккаунт на [Render.com](https://render.com)**

2. **Для бэкенда:**
   - Создайте новый "Web Service"
   - Подключите GitHub репозиторий
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Environment Variables: `PORT=8000`

3. **Для бота:**
   - Создайте новый "Background Worker"
   - Root Directory: `bot`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Environment Variables: `BOT_TOKEN=...`, `WEB_URL=...` (URL вашего бэкенда)

### Вариант 3: VPS (DigitalOcean, Hetzner и т.д.)

1. **Подключитесь к серверу по SSH**

2. **Установите Python и зависимости:**
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

3. **Клонируйте репозиторий:**
```bash
git clone <ваш_репозиторий>
cd FIT
```

4. **Установите зависимости:**
```bash
cd backend && pip3 install -r requirements.txt
cd ../bot && pip3 install -r requirements.txt
```

5. **Создайте systemd сервисы для автозапуска:**

**`/etc/systemd/system/telegram-bot.service`:**
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/FIT/bot
Environment="BOT_TOKEN=your_token"
Environment="WEB_URL=https://your-domain.com"
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
User=your_user
WorkingDirectory=/path/to/FIT/backend
Environment="PORT=8000"
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

6. **Запустите сервисы:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot web-backend
sudo systemctl start telegram-bot web-backend
```

7. **Настройте Nginx для бэкенда (опционально):**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔧 Настройка

### Получение токена бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям
4. Скопируйте полученный токен в переменную `BOT_TOKEN`

## 📝 Структура проекта

```
FIT/
├── bot/
│   ├── main.py          # Основной файл бота
│   └── requirements.txt # Зависимости бота
├── backend/
│   ├── main.py          # FastAPI приложение
│   └── requirements.txt # Зависимости бэкенда
├── .gitignore
└── README.md
```

## 🛠 Технологии

- **Bot**: Python + python-telegram-bot
- **Backend**: Python + FastAPI
- **Deployment**: Railway/Render/VPS

## 📚 Дополнительные ресурсы

- [Документация python-telegram-bot](https://python-telegram-bot.org/)
- [Документация FastAPI](https://fastapi.tiangolo.com/)
- [Railway Documentation](https://docs.railway.app/)

