import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from src.telegram import helper
from utils.loader import bot
from types import ModuleType
from src.telegram.content import markup
from src.telegram.content import text
import yarl


######################### ON START #########################
async def on_start(callback_query: types.Message, lang: ModuleType) -> types.Message:
    # Send a message on bot start
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = text.on_start(lang),
        reply_markup = markup.on_start(lang)
    )
    return message


async def prompt_find_song(callback_query: types.CallbackQuery, lang: ModuleType) -> types.Message:
    # Prompt to find a song
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = text.prompt_find_song(lang)
    )
    return message


async def downloading(callback_query: types.Message, lang: ModuleType, state: FSMContext) -> types.Message:
    # Aknowlegde the searching has started
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.downloading(lang, state)
    )
    return message


async def send_songs(callback_query: types.Message, lang: ModuleType, songs: list[str], state: FSMContext) -> types.Message:
    # Send audio
    message = await bot.send_media_group(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        media=helper.convert_media(text=await text.send_songs(lang, state), songs=songs),
    )
    return message


async def songs_not_found(callback_query: types.Message, lang: ModuleType, state: FSMContext) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.songs_not_found(lang, state)
    )
    return message


async def captcha(callback_query: types.Message, lang: ModuleType, qsize: int) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.captcha(lang, qsize),
        reply_markup = markup.captcha(lang)
    )
    return message


async def language(callback_query: types.Message, lang: ModuleType) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.language(lang),
        reply_markup = markup.language(lang)
    )
    return message


async def set_language(callback_query: types.Message, lang: ModuleType) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.set_language(lang, callback_query.data)
    )
    return message