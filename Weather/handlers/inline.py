from aiogram import F, Router, types
from aiogram.filters import Text
import json
import gui
from methods import get_weather, text_render, user_state, user_info_get

router = Router()


@router.callback_query(Text(startswith='day'))
async def test(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user = user_info_get(user_id)
    if not user:
        await callback.message.edit_text('Не удалось получить данные пользователя, отправьте заново вашу геолокацию')
    weather = await get_weather(user_id, user[1], user[2])
    await callback.answer()

    try:
        if callback.data == "day_next":
            user_state[user_id] += 1
            state = user_state[user_id]

        elif callback.data == "day_back":
            user_state[user_id] -= 1
            state = user_state[user_id]
    except Exception as e:
        print(e)
        state = 0
        user_state.update({user_id: 0})

    text = text_render(state, weather)
    await callback.message.edit_text(text, reply_markup=gui.inline_keyboard_builder(state))
