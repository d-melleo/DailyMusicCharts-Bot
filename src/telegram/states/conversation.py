from aiogram.dispatcher.filters.state import State, StatesGroup


class Conversation(StatesGroup):
    user_input = State()
    downloading = State()
    sending = State()
    sending = State()
    captcha = State()
    language = State()