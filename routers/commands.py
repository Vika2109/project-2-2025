from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.database import JSONDatabase
from keyboards.builders import get_genres_keyboard, get_language_keyboard, get_admin_keyboard
from config.settings import LANGUAGES, ADMIN_IDS

router = Router()
db = JSONDatabase()

@router.message(Command("start", "help"))
async def start(message: types.Message):
    """Обработка команд /start и /help"""
    db.add_user(message.from_user.id)
    lang = db.get_user_language(message.from_user.id)
    await message.answer(
        LANGUAGES[lang]["start"],
        reply_markup=get_genres_keyboard(message.from_user.id, lang)
    )

@router.message(Command("favorites"))
async def show_favorites_cmd(message: types.Message):
    """Обработка команды /favorites - показ избранных книг"""
    lang = db.get_user_language(message.from_user.id)
    favorites = db.get_favorites(message.from_user.id)
    
    if not favorites:
        await message.answer(LANGUAGES[lang]["favorites_empty"])
        return
    
    for book in favorites:
        if book['cover_url']:
            await message.answer_photo(
                photo=book['cover_url'],
                caption=f"{LANGUAGES[lang]['book_title'].format(book['title'])}\n{LANGUAGES[lang]['book_author'].format(book['author'])}",
                parse_mode="HTML"
            )
        else:
            await message.answer(
                f"{LANGUAGES[lang]['book_title'].format(book['title'])}\n{LANGUAGES[lang]['book_author'].format(book['author'])}",
                parse_mode="HTML"
            )

@router.message(Command("language"))
async def change_language(message: types.Message):
    """Обработка команды /language - смена языка интерфейса"""
    await message.answer(
        "Выберите язык / Choose language:",
        reply_markup=get_language_keyboard()
    )

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    """Обработка команды /admin - доступ к админ-панели"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    lang = db.get_user_language(message.from_user.id)
    await message.answer(
        LANGUAGES[lang]["admin_panel"],
        reply_markup=get_admin_keyboard(message.from_user.id, lang)
    )        