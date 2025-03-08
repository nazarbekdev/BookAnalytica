from aiogram.dispatcher.filters.state import State, StatesGroup

class BookAnalysisState(StatesGroup):
    waiting_for_book_text = State()
