from aiogram.dispatcher.filters.state import StatesGroup, State

class RecommendBookState(StatesGroup):
    waiting_for_genre = State()
