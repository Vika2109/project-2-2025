from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from config.settings import GENRES, LANGUAGES


def get_genres_keyboard(user_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру с жанрами книг и кнопкой избранного
    """
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки для каждого жанра
    for genre in GENRES.keys():
        builder.button(text=genre, callback_data=f"genre_{genre}")
    
    # Кнопка избранного
    builder.button(
        text="⭐ Избранное" if lang == 'ru' else "⭐ Favorites", 
        callback_data="show_favorites"
    )
    
    # Распределение кнопок по 2 в ряд
    builder.adjust(2)
    return builder.as_markup()


def get_book_keyboard(user_id: int, lang: str = 'ru') -> ReplyKeyboardMarkup:
    """
    Создает reply-клавиатуру для взаимодействия с книгой
    """
    builder = ReplyKeyboardBuilder()
    
    # Тексты кнопок на разных языках
    buttons = [
        ("📄 Страницы", "📄 Pages"),
        ("📝 Описание", "📝 Description"),
        ("⭐ В избранное", "⭐ Add to favorites"),
        ("➡ Следующая", "➡ Next"),
        ("🎲 Новый жанр", "🎲 New genre")
    ]
    
    # Добавляем кнопки в соответствии с языком пользователя
    for ru_text, en_text in buttons:
        text = ru_text if lang == 'ru' else en_text
        builder.button(text=text)
    
    # Оптимальное расположение кнопок
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_admin_keyboard(user_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для админ-панели
    """
    builder = InlineKeyboardBuilder()
    
    # Тексты кнопок на разных языках
    buttons = [
        ("📊 Статистика", "📊 Statistics"),
        ("🗄️ Создать бэкап", "🗄️ Create backup"),
        ("🧹 Очистить кэш", "🧹 Clear cache"),
        ("🔙 Назад", "🔙 Back")
    ]
    
    # Добавляем кнопки в соответствии с языком пользователя
    for ru_text, en_text in buttons:
        text = ru_text if lang == 'ru' else en_text
        builder.button(
            text=text, 
            callback_data=f"admin_{ru_text.split()[0]}"
        )
    
    # Вертикальное расположение кнопок
    builder.adjust(1)
    return builder.as_markup()


def get_language_keyboard() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для выбора языка
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    builder.adjust(2)
    return builder.as_markup()


def get_back_to_genres_keyboard(user_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """
    Создает кнопку для возврата к выбору жанра
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="← К жанрам" if lang == 'ru' else "← To genres",
        callback_data="back_to_genres"
    )
    return builder.as_markup()                                                         