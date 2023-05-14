from aiogram import F, Router
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from create_bot import bot
from methods import get_weather, user_state, text_render, user_info_update

router = Router()
from gui import inline_keyboard_builder


@router.message(Command(commands=['start', '']))
async def start(message: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.row(
        types.KeyboardButton(text='Отправить местоположение', request_location=True)
    )
    await message.answer('Отправьте свое местоположение, чтобы бот определил ваш город',
                         reply_markup=kb.as_markup(resize_keyboard=True))


@router.message(F.location)
async def location(message: types.Message):
    await message.delete()
    lat = message.location.latitude
    lon = message.location.longitude
    state = 0
    user_info_update(message.from_user.id, lat, lon)
    weather = await get_weather(message.from_user.id, lat, lon)
    user_state.update({message.from_user.id: state})

    text = text_render(state, weather)

    await message.answer(text, reply_markup=inline_keyboard_builder(state))
