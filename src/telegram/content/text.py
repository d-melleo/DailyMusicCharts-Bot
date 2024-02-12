from aiogram.dispatcher import FSMContext
from textwrap import dedent
from types import ModuleType
from src.telegram import helper

def on_start(lang: ModuleType) -> str:
    text: str = dedent('''\
        {}
        
        {}
        {}
        
        {}
    ''').format(*lang.vocabulary['on_start'],
                '/language')
    return text


def prompt_find_song(lang: ModuleType) -> str:
    text: str = dedent('''\
        {}
        
        {}
    ''').format(*lang.vocabulary['prompt_find_song'])
    return text


async def downloading(lang: ModuleType, state: FSMContext) -> str:
    text: str = dedent('''\
        {} "{}"...
    ''').format(
        *lang.vocabulary['downloading'],
        *await helper.get_state_data(state, 'title')
        )
    return text


async def send_songs(lang: ModuleType, state: FSMContext) -> str:
    text: str = dedent('''\
        {} "{}".
    ''').format(
        *lang.vocabulary['send_songs'],
        *await helper.get_state_data(state, 'title')
        )
    return text


async def songs_not_found(lang: ModuleType, state: FSMContext) -> str:
    text: str = dedent('''\
        {} "{}".
    ''').format(
        *lang.vocabulary['songs_not_found'],
        *await helper.get_state_data(state, 'title')
        )
    return text


async def captcha(lang: ModuleType, qsize: int) -> str:
    text: str = dedent('''\
        {} ({})
    ''').format(
        *lang.vocabulary['captcha'],
        qsize
        )
    return text


async def language(lang: ModuleType) -> str:
    text: str = dedent('''\
        {}
    ''').format(
        *lang.vocabulary['language']
        )
    return text


async def set_language(lang: ModuleType, set_lang: str) -> str:
    text: str = dedent('''\
        {} {}
    ''').format(
        *lang.vocabulary['set_language'],
        lang.keyboard[set_lang]
        )
    return text