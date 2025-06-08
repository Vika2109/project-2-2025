import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

from config.settings import DATA_FILE, LANGUAGES

logger = logging.getLogger(__name__)

class JSONDatabase:
    def __init__(self, filename: str = DATA_FILE):
        self.filename = Path(filename)
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Загрузка данных из файла"""
        try:
            if self.filename.exists():
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {
                'favorites': {}, 
                'cache': {},
                'users': {},
                'stats': {
                    'total_users': 0,
                    'total_favorites': 0
                }
            }
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
            return {
                'favorites': {}, 
                'cache': {},
                'users': {},
                'stats': {
                    'total_users': 0,
                    'total_favorites': 0
                }
            }
    
    def _save_data(self) -> bool:
        """Сохранение данных в файл"""
        try:
            self.filename.parent.mkdir(exist_ok=True)
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения данных: {e}")
            return False
    
    def add_user(self, user_id: Union[int, str], language: str = 'ru') -> bool:
        """Добавление пользователя"""
        user_id = str(user_id)
        if user_id not in self.data['users']:
            self.data['users'][user_id] = {'language': language}
            self.data['stats']['total_users'] = len(self.data['users'])
            return self._save_data()
        return False
    
    def get_user_language(self, user_id: Union[int, str]) -> str:
        """Получение языка пользователя"""
        user_id = str(user_id)
        return self.data['users'].get(user_id, {}).get('language', 'ru')
    
    def set_user_language(self, user_id: Union[int, str], language: str) -> bool:
        """Установка языка пользователя"""
        user_id = str(user_id)
        if user_id in self.data['users']:
            self.data['users'][user_id]['language'] = language
            return self._save_data()
        return False
    
    def add_to_favorites(self, user_id: Union[int, str], book: Dict) -> bool:
        """Добавление книги в избранное"""
        try:
            user_id = str(user_id)
            if user_id not in self.data['favorites']:
                self.data['favorites'][user_id] = []
            
            book_data = {
                'book_id': book['id'],
                'title': book['volumeInfo']['title'],
                'author': ', '.join(book['volumeInfo'].get('authors', [LANGUAGES['ru']['book_author'].format('Неизвестен')])),
                'cover_url': book['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')
            }
            
            # Проверяем, нет ли уже такой книги
            if not any(b['book_id'] == book['id'] for b in self.data['favorites'][user_id]):
                self.data['favorites'][user_id].append(book_data)
                self.data['stats']['total_favorites'] = sum(len(v) for v in self.data['favorites'].values())
                self._save_data()
                logger.info(f"Книга добавлена в избранное для user_id {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Ошибка при добавлении в избранное: {e}")
            return False
    
    def get_favorites(self, user_id: Union[int, str]) -> List[Dict]:
        """Получение избранных книг пользователя"""
        user_id = str(user_id)
        return self.data['favorites'].get(user_id, [])
    
    def cache_books(self, genre: str, books: List[Dict]) -> bool:
        """Кэширование книг по жанру"""
        try:
            self.data['cache'][genre] = {
                'books': books,
                'timestamp': datetime.now().isoformat()
            }
            return self._save_data()
        except Exception as e:
            logger.error(f"Ошибка при кэшировании книг: {e}")
            return False
    
    def get_cached_books(self, genre: str) -> Optional[List[Dict]]:
        """Получение кэшированных книг"""
        cache = self.data['cache'].get(genre)
        if not cache:
            return None
        
        # Проверяем, не устарели ли данные (1 день)
        cache_time = datetime.fromisoformat(cache['timestamp'])
        if (datetime.now() - cache_time).days < 1:
            return cache['books']
        return None
    
    def clear_cache(self) -> bool:
        """Очистка кэша"""
        self.data['cache'] = {}
        return self._save_data()
    
    def get_stats(self) -> Dict:
        """Получение статистики"""
        return self.data['stats']
    
    def create_backup(self) -> bool:
        """Создание резервной копии"""
        try:
            backup_filename = self.filename.parent / f"{self.filename.stem}.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}{self.filename.suffix}"
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Ошибка создания резервной копии: {e}")
            return False
    