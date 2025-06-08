import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

# Конфигурация
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
DATA_FILE = BASE_DIR / 'storage' / 'books_data.json'

# Локализация
LANGUAGES = {
    "ru": {
        "start": "📚 Я - книжный бот! Выбери жанр или посмотри избранное:",
        "favorites_empty": "В избранном пока ничего нет",
        "searching": "🔍 Ищу книги в жанре {}...",
        "no_books": "Книги не найдены 😢 Попробуйте другой жанр.",
        "pages": "📄 Страниц: {}",
        "description": "📝 {}",
        "no_description": "Описание отсутствует",
        "added_to_favorites": "✅ Книга добавлена в избранное!",
        "already_in_favorites": "❌ Эта книга уже в избранном",
        "choose_genre": "Выбери жанр:",
        "unknown_command": "Используй кнопки для навигации",
        "admin_panel": "🔐 Админ-панель",
        "stats": "📊 Статистика:",
        "total_users": "👥 Всего пользователей: {}",
        "total_favorites": "⭐ Всего избранных книг: {}",
        "book_title": "📖 <b>{}</b>",
        "book_author": "👤 {}",
        "translated_description": "\n\n🇷🇺 Перевод описания:\n{}",
        "backup_created": "✅ Резервная копия создана",
        "cache_cleared": "✅ Кэш очищен",
    },
    "en": {
        "start": "📚 I'm a book bot! Choose a genre or view favorites:",
        "favorites_empty": "No favorites yet",
         "searching": "🔍 Searching for {} books...",
        "no_books": "No books found 😢 Try another genre.",
        "pages": "📄 Pages: {}",
        "description": "📝 {}",
        "no_description": "No description available",
        "added_to_favorites": "✅ Book added to favorites!",
        "already_in_favorites": "❌ This book is already in favorites",
        "choose_genre": "Choose genre:",
        "unknown_command": "Use buttons for navigation",
        "admin_panel": "🔐 Admin panel",
        "stats": "📊 Statistics:",
        "total_users": "👥 Total users: {}",
        "total_favorites": "⭐ Total favorites: {}",
        "book_title": "📖 <b>{}</b>",
        "book_author": "👤 {}",
        "translated_description": "\n\n🇷🇺 Russian translation:\n{}",
        "backup_created": "✅ Backup created",
        "cache_cleared": "✅ Cache cleared",
    }
}

# Список жанров
GENRES = {
    "Фэнтези": "subject:fantasy",
    "Научная фантастика": "subject:science fiction",
    "Детектив": "subject:detective",
    "Романтика": "subject:romance",
    "Ужасы": "subject:horror",
    "Биография": "subject:biography",
    "Триллер": "subject:thriller",
    "Поэзия": "subject:poetry"
}