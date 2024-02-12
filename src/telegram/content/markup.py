from aiogram.types import \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from types import ModuleType


def on_start(lang: ModuleType) -> InlineKeyboardMarkup:
    keyboardStart = InlineKeyboardMarkup(row_width=1)
    keyboardStart.add(InlineKeyboardButton(text=lang.keyboard['on_start'], callback_data='on_start'))
    return keyboardStart

def captcha(lang: ModuleType) -> InlineKeyboardMarkup:
    keyboardCaptcha = InlineKeyboardMarkup(row_width=2)
    keyboardCaptcha.add(InlineKeyboardButton(text=lang.keyboard['captcha_yes'], callback_data='captcha_yes'))
    keyboardCaptcha.insert(InlineKeyboardButton(text=lang.keyboard['captcha_no'], callback_data='captcha_no'))
    return keyboardCaptcha

def language(lang: ModuleType) -> InlineKeyboardMarkup:
    keyboardLang = InlineKeyboardMarkup(row_width=1)
    keyboardLang.add(InlineKeyboardButton(text=lang.keyboard['en'], callback_data='en'))
    keyboardLang.add(InlineKeyboardButton(text=lang.keyboard['ua'], callback_data='ua'))
    return keyboardLang