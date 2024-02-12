from aiogram import types
from aiogram.dispatcher import FSMContext
from src.telegram.states import conversation


async def user_input(*args):
    await conversation.Conversation.user_input.set()


async def downloading(callback_query: types.Message, state: FSMContext):
    await state.update_data(title=callback_query.text)
    await conversation.Conversation.downloading.set()


async def sending(state: FSMContext):
    await conversation.Conversation.sending.set()


async def conversation_finished(state: FSMContext):
    await state.finish()


async def captcha(*args):
    await conversation.Conversation.captcha.set()


async def captcha_answer(state: FSMContext, answer: bool):
    if answer: await conversation.Conversation.sending.set()
    else: await state.finish()


async def language(state: FSMContext):
    if state:
        await state.finish()
    await conversation.Conversation.language.set()