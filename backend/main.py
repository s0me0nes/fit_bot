"""
FastAPI бэкенд для веб-сайта
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
import os
import json

# Загружаем переменные окружения из .env файла
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

app = FastAPI(title="Telegram Bot Web Backend")

# Модели данных
class Review(BaseModel):
    name: str
    handle: str
    city: str
    avatar: str
    rating: int
    text: str

class ReviewDelete(BaseModel):
    index: int
    username: str  # Для проверки прав администратора

# Хранение отзывов (в продакшене лучше использовать БД)
REVIEWS_FILE = Path(__file__).parent.parent / "reviews.json"

# Базовые отзывы
DEFAULT_REVIEWS = [
    {
        "name": "Алина К.",
        "handle": "@healthy_alina",
        "city": "Саратов",
        "avatar": "images/photo1.jpg",
        "rating": 5,
        "text": "Заказываю уже третий месяц. Всегда ощущение домашней еды: свежие продукты, аккуратная упаковка и очень понятное расписание доставок."
    },
    {
        "name": "Михаил Т.",
        "handle": "@mikhail_fit",
        "city": "Энгельс",
        "avatar": "images/photo2.jpg",
        "rating": 5,
        "text": "Приятно, что можно подобрать меню под тренировочный план. Ребята гибко меняют блюда, если предупреждать заранее, и всегда вовремя привозят."
    },
    {
        "name": "Виктория С.",
        "handle": "@vika_wellness",
        "city": "Саратов",
        "avatar": "images/photo3.jpeg",
        "rating": 4,
        "text": "Люблю разнообразие в рационе. Здесь каждую неделю новое меню и при этом стабильный вкус. Оценка 4 только потому, что хочется ещё больше десертов 😊"
    },
    {
        "name": "Илья П.",
        "handle": "@ilya_runner",
        "city": "Саратов",
        "avatar": "images/photo4.jpg",
        "rating": 5,
        "text": "Поддерживаю форму для марафонов и ценю продуманное БЖУ. Ребята присылают полную информацию по каждому блюду — удобно контролировать результат."
    }
]

def load_reviews():
    """Загружает отзывы из файла или возвращает базовые"""
    if REVIEWS_FILE.exists():
        try:
            with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
                reviews = json.load(f)
                if reviews:
                    return reviews
        except Exception as e:
            print(f"Ошибка при загрузке отзывов: {e}")
    return DEFAULT_REVIEWS.copy()

def save_reviews(reviews: List[dict]):
    """Сохраняет отзывы в файл"""
    try:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении отзывов: {e}")
        return False

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

@app.get("/api/reviews")
async def get_reviews():
    """Получить все отзывы"""
    reviews = load_reviews()
    return {"reviews": reviews}

@app.post("/api/reviews")
async def add_review(review: Review):
    """Добавить новый отзыв"""
    reviews = load_reviews()
    review_dict = review.dict()
    reviews.insert(0, review_dict)  # Добавляем в начало
    if save_reviews(reviews):
        return {"status": "success", "message": "Отзыв добавлен"}
    else:
        raise HTTPException(status_code=500, detail="Ошибка при сохранении отзыва")

@app.delete("/api/reviews/{review_index}")
async def delete_review(review_index: int, username: Optional[str] = None):
    """Удалить отзыв по индексу (только для администратора)"""
    # Проверка прав администратора
    if username != "Nill_Kafri":
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления отзыва")
    
    reviews = load_reviews()
    
    if review_index < 0 or review_index >= len(reviews):
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    deleted_review = reviews.pop(review_index)
    
    if save_reviews(reviews):
        return {
            "status": "success",
            "message": "Отзыв удален",
            "deleted_review": deleted_review
        }
    else:
        raise HTTPException(status_code=500, detail="Ошибка при сохранении изменений")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

