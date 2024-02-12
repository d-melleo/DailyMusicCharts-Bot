import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaAudio
from src.downloader.downloader import Downloader
from src.queues.sending import SendingQueue


# Get message id and chat id
def get_message_details(callback_query: types.CallbackQuery or types.Message) -> dict:
    # Get the details if type is CallbackQuery
    try:
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id
    # Get the details if type is Message
    except AttributeError:
        chat_id = callback_query.chat.id
        message_id = callback_query.message_id
        
    return {'chat_id': chat_id, 'message_id': message_id}


# Return values of keys
async def get_state_data(state: FSMContext, *keys: str) -> list:
    if type(state) is FSMContext:
        try:
            data: dict = await state.get_data()
            values = list(map(lambda x: data[x], keys))
            return values
        except KeyError:
            return None


async def download(commandHandler, title: str) -> list[str]:
    if not commandHandler.downloader:
        commandHandler.downloader = Downloader()
    songs: list[str] = await commandHandler.downloader.run(title)
    return songs


def convert_media(text: str, songs:list[str]) -> list[InputMediaAudio]:
    media_group: list = [InputMediaAudio(media=str(url)) for url in songs]
    # media_group[-1].caption = text
    return media_group


async def run_sender(commandHandler, media: list[str], callback_query: types.Message, state: FSMContext):
    sender = SendingQueue(commandHandler, media, callback_query, state)
    worker = asyncio.create_task(sender.run(), name="sending_queue")
    await worker


def captcha(callback_query: types.CallbackQuery) -> bool:
    if callback_query.data == "captcha_yes":
        return True
    elif callback_query.data == "captcha_no":
        return False