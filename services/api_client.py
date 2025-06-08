import asyncio
import requests
from config.settings import GOOGLE_BOOKS_API_KEY
from services.database import JSONDatabase
import logging

logger = logging.getLogger(__name__)

db = JSONDatabase()

async def get_books(genre_query, genre_name):
    cached = db.get_cached_books(genre_name)
    if cached:
        return cached
    
    url = f"https://www.googleapis.com/books/v1/volumes?q={genre_query}&key={GOOGLE_BOOKS_API_KEY}&maxResults=40"
    try:
        response = await asyncio.to_thread(requests.get, url, timeout=10)
        data = response.json()
        
        if not data.get("items"):
            return None
        
        books = [book for book in data["items"] if book['volumeInfo'].get('imageLinks', {}).get('thumbnail')]
        if books:
            db.cache_books(genre_name, books)
        return books
        
    except Exception as e:
        logger.error(f"Ошибка при запросе к Google Books: {e}")
        return None