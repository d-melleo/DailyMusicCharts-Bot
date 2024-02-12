import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from src.downloader.downloader import Downloader
from src.telegram.handlers import send_message, update_state
from src.telegram.states import conversation
from src.telegram import helper
from src.userdata import database
from utils.mongo import CLIENT
from src.queues import captcha


class CommandHandler:
    def __init__(self, dp: Dispatcher, user: database.UserData):
        self.user: database.UserData = user
        self.downloader: Downloader = None
        
        ##################### REGISTER HANDLERS #####################
        dp.register_callback_query_handler(self.prompt_find_song, lambda x: x.data == "on_start", state="*" or None)
        dp.register_message_handler(self.language, commands=["language"], state="*")
        dp.register_message_handler(self.user_input, content_types=types.ContentTypes.TEXT, regexp='^(?!/).*', state=conversation.Conversation.user_input)
        dp.register_callback_query_handler(self.captcha_answer, lambda x: x.data in ['captcha_yes', 'captcha_no'], state=conversation.Conversation.captcha)
        dp.register_callback_query_handler(self.set_language, lambda x: x.data in ['en', 'ua'], state=conversation.Conversation.language)
    
    
    async def on_start(self, callback_query: types.Message, state: FSMContext):
        message: types.Message = await send_message.on_start(callback_query, self.user.language)
    
    
    # @dp.callback_query_handler(lambda x: x.data == "on_start")
    async def prompt_find_song(self, callback_query: types.CallbackQuery, state: FSMContext):
        await update_state.user_input()
        message: types.Message = await send_message.prompt_find_song(callback_query, self.user.language)
    
    
    # @dp.message_handler(content_types=types.ContentTypes.TEXT, state=conversation.Conversation.user_input)
    async def user_input(self, callback_query: types.Message, state: FSMContext):
        await update_state.downloading(callback_query, state)
        message: types.Message = await send_message.downloading(callback_query, self.user.language, state)
        
        songs: list[str] = await helper.download(self, callback_query.text)
        
        
        if songs:
            print(f'\n{self.user.username} | {callback_query.text}\n{songs}\n')
            await helper.run_sender(self, songs, callback_query, state)
        else:
            await send_message.songs_not_found(callback_query, self.user.language, state)
        
        self.user.update_search_history(callback_query.text)
        await update_state.conversation_finished(state)
        await self.prompt_find_song(callback_query, state)
    
    
    async def send_songs(self, callback_query: types.Message, songs: list[str], state: FSMContext):
        await update_state.sending(state)
        message: types.Message = await send_message.send_songs(callback_query, self.user.language, songs, state)
    
    
    async def captcha(self, callback_query: types.Message, qsize: int) -> bool:
        await update_state.captcha()
        await send_message.captcha(callback_query, self.user.language, qsize)
        answer: bool = asyncio.create_task(captcha.run())
        return await answer
    
    
    # @dp.callback_query_handler(lambda x: x.data in ['captcha_yes', 'captcha_no'], state=conversation.Conversation.captcha)
    async def captcha_answer(self, callback_query: types.CallbackQuery, state: FSMContext):
        answer: bool = helper.captcha(callback_query)
        await update_state.captcha_answer(state, answer)
        await captcha.queue.put(answer)
    
    
    # @dp.callback_query_handler(lambda x: x.data == "language", state="*")
    async def language(self, callback_query: types.CallbackQuery, state: FSMContext):
        await update_state.language(state)
        await send_message.language(callback_query, self.user.language)
    
    
    # @dp.callback_query_handler(lambda x: x.data in ['en', 'ua'], state=conversation.Conversation.language)
    async def set_language(self, callback_query: types.CallbackQuery, state: FSMContext):
        self.user.update_language(callback_query.data)
        await send_message.set_language(callback_query, self.user.language)
        await update_state.conversation_finished(state)
        await self.prompt_find_song(callback_query, state)