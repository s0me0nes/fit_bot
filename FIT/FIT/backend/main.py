"""
FastAPI бэкенд для веб-сайта
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

app = FastAPI(title="Telegram Bot Web Backend")

# Настройка CORS (если нужно)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы (если будут)
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Главная страница"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Telegram Bot Web</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            p {
                color: #666;
                font-size: 1.2em;
                line-height: 1.6;
                margin-bottom: 30px;
            }
            .btn {
                display: inline-block;
                padding: 15px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                transition: transform 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Bot Web</h1>
            <p>Добро пожаловать на веб-сайт телеграм-бота!</p>
            <p>Этот сайт работает внутри вашего телеграм-бота.</p>
            <a href="https://t.me/your_bot_username" class="btn">Открыть бота в Telegram</a>
        </div>
    </body>
    </html>
    """


@app.get("/api/health")
async def health():
    """Проверка здоровья API"""
    return {"status": "ok", "message": "Backend is running"}


@app.get("/api/info")
async def info():
    """Информация о бэкенде"""
    return {
        "name": "Telegram Bot Backend",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

