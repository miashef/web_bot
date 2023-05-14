from aiogram import F, Router
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder


def inline_keyboard_builder(state):
    keyboard = InlineKeyboardBuilder()
    if state >= 1:
        keyboard.button(text="Назад", callback_data="day_back")
    if state < 6:
        keyboard.button(text="Далее", callback_data="day_next")
    keyboard.adjust(2)
    return keyboard.as_markup()
