from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from services.database import JSONDatabase
from services.api_client import get_books
from keyboards.builders import (
    get_genres_keyboard,
    get_book_keyboard,
    get_admin_keyboard,
    get_language_keyboard
)
from states.book_states import BookStates
from config.settings import LANGUAGES, GENRES, ADMIN_IDS
from utils.translator import translate_description

router = Router()
db = JSONDatabase()

async def show_current_book(message: Message, state: FSMContext):
    """Показ текущей книги"""
    data = await state.get_data()
    books = data.get("books", [])
    current_index = data.get("current_index", 0)
    
    if not books or current_index >= len(books):
        lang = db.get_user_language(message.from_user.id)
        await message.answer(LANGUAGES[lang]["no_books"])
        return

    book = books[current_index]
    info = book["volumeInfo"]
    lang = db.get_user_language(message.from_user.id)
    
    title = info.get("title", "Без названия" if lang == 'ru' else "No title")
    authors = ", ".join(info.get("authors", ["Неизвестен"] if lang == 'ru' else ["Unknown"]))
    cover_url = info.get('imageLinks', {}).get('thumbnail', '')
    
    if cover_url:
        await message.answer_photo(
            photo=cover_url,
            caption=f"{LANGUAGES[lang]['book_title'].format(title)}\n{LANGUAGES[lang]['book_author'].format(authors)}",
            parse_mode="HTML",
            reply_markup=get_book_keyboard(message.from_user.id, lang)
        )
    else:
        await message.answer(
            f"{LANGUAGES[lang]['book_title'].format(title)}\n{LANGUAGES[lang]['book_author'].format(authors)}",
            parse_mode="HTML",
            reply_markup=get_book_keyboard(message.from_user.id, lang)
        )

@router.callback_query(F.data.startswith("genre_"))
async def process_genre(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора жанра"""
    genre = callback.data.split('_')[1]
    genre_query = GENRES[genre]
    lang = db.get_user_language(callback.from_user.id)
    
    await callback.message.answer(LANGUAGES[lang]["searching"].format(genre))
    books = await get_books(genre_query, genre)
    
    if not books:
        await callback.message.answer(LANGUAGES[lang]["no_books"])
        return
    
    await state.set_data({
        "books": books,
        "current_index": 0
    })
    await show_current_book(callback.message, state)
    await state.set_state(BookStates.waiting_for_book_choice)

@router.message(
    F.text.in_(["➡ Следующая", "➡ Next"]), 
    BookStates.waiting_for_book_choice
)
async def next_book_handler(message: Message, state: FSMContext):
    """Обработка кнопки следующей книги"""
    data = await state.get_data()
    current_index = data["current_index"]
    books = data["books"]
    
    new_index = (current_index + 1) % len(books)
    await state.update_data(current_index=new_index)
    await show_current_book(message, state)

@router.message(
    F.text.in_(["📄 Страницы", "📄 Pages"]), 
    BookStates.waiting_for_book_choice
)
async def show_pages_handler(message: Message, state: FSMContext):
    """Обработка кнопки показа страниц"""
    data = await state.get_data()
    book = data["books"][data["current_index"]]
    info = book["volumeInfo"]
    lang = db.get_user_language(message.from_user.id)
    
    pages = info.get("pageCount", "Не указано" if lang == 'ru' else "Not specified")
    await message.answer(LANGUAGES[lang]["pages"].format(pages))

@router.message(
    F.text.in_(["📝 Описание", "📝 Description"]), 
    BookStates.waiting_for_book_choice
)
async def show_description_handler(message: Message, state: FSMContext):
    """Обработка кнопки показа описания"""
    data = await state.get_data()
    book = data["books"][data["current_index"]]
    info = book["volumeInfo"]
    lang = db.get_user_language(message.from_user.id)
    
    description = info.get("description", LANGUAGES[lang]["no_description"])
    msg = LANGUAGES[lang]["description"].format(description[:500] + ("..." if len(description) > 500 else ""))
    
    if lang == 'ru' and description and len(description) > 10:
        translated = await translate_description(description)
        if translated:
            msg += LANGUAGES[lang]["translated_description"].format(translated[:500] + ("..." if len(translated) > 500 else ""))
    
    await message.answer(msg)

@router.message(
    F.text.in_(["⭐ В избранное", "⭐ Add to favorites"]), 
    BookStates.waiting_for_book_choice
)
async def add_to_favorites_handler(message: Message, state: FSMContext):
    """Обработка добавления в избранное"""
    data = await state.get_data()
    book = data["books"][data["current_index"]]
    lang = db.get_user_language(message.from_user.id)
    
    if db.add_to_favorites(message.from_user.id, book):
        await message.answer(LANGUAGES[lang]["added_to_favorites"])
    else:
        await message.answer(LANGUAGES[lang]["already_in_favorites"])

@router.message(
    F.text.in_(["🎲 Новый жанр", "🎲 New genre"]), 
    BookStates.waiting_for_book_choice
)
async def new_genre_handler(message: Message, state: FSMContext):
    """Обработка кнопки нового жанра"""
    lang = db.get_user_language(message.from_user.id)
    await state.clear()
    await message.answer(
        LANGUAGES[lang]["choose_genre"],
        reply_markup=get_genres_keyboard(message.from_user.id, lang)
    )

@router.callback_query(F.data == "show_favorites")
async def show_favorites_handler(callback: CallbackQuery):
    """Обработка кнопки избранного"""
    lang = db.get_user_language(callback.from_user.id)
    favorites = db.get_favorites(callback.from_user.id)
    
    if not favorites:
        await callback.message.answer(LANGUAGES[lang]["favorites_empty"])
        return
    
    for book in favorites:
        if book['cover_url']:
            await callback.message.answer_photo(
                photo=book['cover_url'],
                caption=f"{LANGUAGES[lang]['book_title'].format(book['title'])}\n{LANGUAGES[lang]['book_author'].format(book['author'])}",
                parse_mode="HTML"
            )
        else:
            await callback.message.answer(
                f"{LANGUAGES[lang]['book_title'].format(book['title'])}\n{LANGUAGES[lang]['book_author'].format(book['author'])}",
                parse_mode="HTML"
            )

@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    """Обработка смены языка"""
    language = callback.data.split('_')[1]
    db.set_user_language(callback.from_user.id, language)
    lang = db.get_user_language(callback.from_user.id)
    
    await callback.message.edit_text(
        LANGUAGES[lang]["start"],
        reply_markup=get_genres_keyboard(callback.from_user.id, lang)
    )

@router.callback_query(F.data.startswith("admin_"))
async def admin_actions(callback: CallbackQuery):
    """Обработка действий администратора"""
    if callback.from_user.id not in ADMIN_IDS:
        return
    
    action = callback.data.split('_')[1]
    lang = db.get_user_language(callback.from_user.id)
    
    if action == "📊":
        stats = db.get_stats()
        text = (
            f"{LANGUAGES[lang]['stats']}\n"
            f"{LANGUAGES[lang]['total_users'].format(stats['total_users'])}\n"
            f"{LANGUAGES[lang]['total_favorites'].format(stats['total_favorites'])}"
        )
        await callback.message.answer(text)
    
    elif action == "🗄️":
        if db.create_backup():
            await callback.message.answer(LANGUAGES[lang]["backup_created"])
        else:
            await callback.message.answer("❌ Ошибка создания бэкапа / Backup error")
    
    elif action == "🧹":
        if db.clear_cache():
            await callback.message.answer(LANGUAGES[lang]["cache_cleared"])
        else:
            await callback.message.answer("❌ Ошибка очистки кэша / Cache clearing error")
    
    elif action == "🔙":
        await callback.message.edit_text(
            LANGUAGES[lang]["start"],
            reply_markup=get_genres_keyboard(callback.from_user.id, lang)
        )                                                        