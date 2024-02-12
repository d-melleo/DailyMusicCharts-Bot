import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from src.userdata import database
from src.telegram.handlers import command_handler
from utils.loader import dp
from utils.mongo import CLIENT



@dp.message_handler(commands=["start"], state="*")
async def init_start(callback_query: types.Message, state: FSMContext):
    USER = database.UserData(CLIENT, callback_query)
    ch = command_handler.CommandHandler(dp, USER)
    await ch.on_start(callback_query, state)


if __name__ == "__main__":
    asyncio.run(dp.start_polling())