from aiogram.fsm.state import State, StatesGroup

class BookStates(StatesGroup):
    waiting_for_book_choice = State()
    waiting_for_genre = State()