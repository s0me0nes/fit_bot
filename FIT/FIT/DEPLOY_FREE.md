# 🆓 Бесплатный деплой через GitHub

## Вариант 1: GitHub Pages + Fly.io (Рекомендуется)

### Преимущества:
- ✅ GitHub Pages - полностью бесплатно, без ограничений
- ✅ Fly.io - бесплатный тариф (3 shared-cpu-1x VM), не засыпает
- ✅ Автоматический деплой через GitHub Actions
- ✅ Все через GitHub

### Шаг 1: Настройте GitHub Pages

1. В вашем GitHub репозитории:
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / `docs`
   - Folder: `/docs`
   - Save

2. Ваш сайт будет доступен по адресу:
   `https://ваш-username.github.io/FIT/`

### Шаг 2: Деплой на Fly.io (бесплатно)

1. **Установите Fly CLI:**
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

2. **Войдите в Fly.io:**
```bash
fly auth login
```

3. **Создайте приложение для бэкенда:**
```bash
cd backend
fly launch --name telegram-bot-backend
# Выберите регион (например: fra - Frankfurt)
# Не создавайте Postgres (нажмите N)
```

4. **Добавьте переменные окружения:**
```bash
fly secrets set PORT=8000
```

5. **Деплой:**
```bash
fly deploy
```

6. **Создайте приложение для бота:**
```bash
cd ../bot
fly launch --name telegram-bot
# Выберите регион (тот же, что и бэкенд)
```

7. **Добавьте переменные окружения для бота:**
```bash
fly secrets set BOT_TOKEN=ваш_токен
fly secrets set WEB_URL=https://telegram-bot-backend.fly.dev
```

8. **Деплой бота:**
```bash
fly deploy
```

### Шаг 3: Обновите URL в GitHub Pages

В файле `docs/index.html` замените:
```javascript
const API_URL = 'https://your-backend.fly.dev';
```
на ваш реальный URL бэкенда.

---

## Вариант 2: PythonAnywhere (Проще, но ограничения)

### Преимущества:
- ✅ Полностью бесплатно
- ✅ Простая настройка
- ✅ Не нужно устанавливать CLI

### Недостатки:
- ⚠️ Ограничение: 1 веб-приложение на бесплатном аккаунте
- ⚠️ Нужно обновлять вручную (или через GitHub)

### Инструкция:

1. Зарегистрируйтесь на [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Для бэкенда:**
   - Web → Add a new web app
   - Выберите Manual configuration → Python 3.10
   - В Files загрузите код из папки `backend/`
   - В Web → WSGI configuration file добавьте:
   ```python
   import sys
   path = '/home/ваш_username/telegram-bot-backend'
   if path not in sys.path:
       sys.path.append(path)
   
   from main import app
   application = app
   ```
   - В Web → Environment variables добавьте: `PORT=8000`

3. **Для бота:**
   - Tasks → Add a new task
   - Command: `cd /home/ваш_username/telegram-bot && python3 main.py`
   - Schedule: Always (или по расписанию)
   - Environment variables: `BOT_TOKEN`, `WEB_URL`

---

## Вариант 3: Replit (Очень просто)

### Преимущества:
- ✅ Полностью бесплатно
- ✅ Встроенный редактор
- ✅ Автоматический деплой из GitHub

### Недостатки:
- ⚠️ Засыпает после неактивности
- ⚠️ Медленный старт

### Инструкция:

1. Зайдите на [replit.com](https://replit.com)
2. Import from GitHub → выберите ваш репозиторий
3. Создайте два Repl:
   - Один для `backend/`
   - Один для `bot/`
4. В каждом Repl добавьте Secrets (Environment Variables)
5. Replit автоматически задеплоит при push в GitHub

---

## 🎯 Рекомендация

**Используйте Fly.io** - это лучший бесплатный вариант:
- Не засыпает
- Быстрый
- Автоматический деплой через GitHub Actions
- 3 бесплатных VM (достаточно для бота и бэкенда)

---

## 📝 Настройка GitHub Actions для Fly.io

Создайте `.github/workflows/fly-deploy.yml`:

```yaml
name: Deploy to Fly.io

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'
      - 'bot/**'

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, 'backend') || contains(github.event.head_commit.modified, 'backend')
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --config backend/fly.toml
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}

  deploy-bot:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, 'bot') || contains(github.event.head_commit.modified, 'bot')
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --config bot/fly.toml
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

Добавьте `FLY_API_TOKEN` в GitHub Secrets (получите через `fly auth token`).

