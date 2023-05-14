import json
import aiohttp
import config
from create_bot import bot
from cashews import cache
import sqlite3

conn = sqlite3.connect('database.db')
cache.setup("mem://", size=1024)

user_state = {}
condition_dict = {
    'clear': ['ясно', '☀️'],
    'partly-cloudy': ['малооблачно', '🌤'],
    'cloudy': ['облачно с прояснениями', '⛅️'],
    'overcast': ['пасмурно', '🌥'],
    'drizzle': ['морось', '🌦'],
    'light-rain': ['небольшой дождь', '🌦'],
    'rain': ['дождь', '🌧'],
    'moderate-rain': ['умеренно сильный дождь', '🌧'],
    'heavy-rain': ['сильный дождь', '🌧'],
    'continuous-heavy-rain': ['длительный сильный дождь', '🌧'],
    'showers': ['ливень', '🌧'],
    'wet-snow': ['дождь со снегом', '🌨'],
    'light-snow': ['небольшой снег', '🌨'],
    'snow': ['снег', '❄️'],
    'snow-showers': ['снегопад', '❄️'],
    'hail': ['град', '🌨'],
    'thunderstorm': ['гроза', '🌩'],
    'thunderstorm-with-rain': ['дождь с грозой', '⛈'],
    'thunderstorm-with-hail': ['гроза с градом', '🌩']
}
good_weather = ['clear', 'partly-cloudy', 'cloudy', 'overcast', 'drizzle']
bad_weather = ['light-rain', 'rain', 'moderate-rain', 'heavy-rain',
               'continuous-heavy-rain', 'showers', 'wet-snow', 'light-snow',
               'snow', 'snow-showers', 'hail', 'thunderstorm', 'thunderstorm-with-rain',
               'thunderstorm-with-hail']


@cache(ttl='1h')
async def get_weather(user_id, lat, lon) -> dict:
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&lang=ru_RU"
    headers = {
        "X-Yandex-API-Key": config.weather_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
            else:
                print(f"Ошибка запроса: {response.status}")
                data = {}
    # with open('dump2.json', 'w',  encoding="utf-8") as file:
    #     json.dump(data, file,indent=3,ensure_ascii=False )
    # data = json.load(file)
    return data


def text_render(state, weather):
    date_texts = ['Сегодня', 'Завтра', 'Послезавтра']

    city = weather['geo_object']['locality']['name']
    date = weather['forecasts'][state]['date']
    morning = weather['forecasts'][state]['parts']['morning']
    day = weather['forecasts'][state]['parts']['day']
    evening = weather['forecasts'][state]['parts']['evening']

    if state <= 2:
        date_text = date_texts[state]
    else:
        date_text = 'Прогноз на'

    if state == 0:
        fact = weather['fact']
        now_text = f"{condition_dict[fact['condition']][1]}Сейчас {fact['temp']}°C {condition_dict[fact['condition']][0]}\nВетер {fact['wind_speed']}м/с\n"
        date_text, date = '', ''
    else:
        now_text = ''

    text = f'''
{city}
{date_text} {date}
{now_text}
{condition_dict[morning['condition']][1]}Утром: {morning['temp_avg']}°C {condition_dict[morning['condition']][0]}
{condition_dict[day['condition']][1]}Днём: {day['temp_avg']}°C {condition_dict[day['condition']][0]}
{condition_dict[evening['condition']][1]}Вечером: {evening['temp_avg']}°C {condition_dict[evening['condition']][0]}
'''
    return text


def user_info_update(user_id, lat, lon):
    cur = conn.execute("SELECT * FROM main_1 WHERE id = ?", (user_id,))
    row = cur.fetchone()
    print(row)
    if row:
        sql = "UPDATE main_1 SET lat = ?, lon = ? WHERE id = ?"
        data = (lat, lon, user_id)
    else:
        sql = "INSERT INTO main_1 (id, lat, lon) VALUES (?, ?, ?)"
        data = (user_id, lat, lon)
    conn.execute(sql, data)
    conn.commit()


def user_info_get(user_id):
    cur = conn.execute("SELECT * FROM main_1 WHERE id = ?", (user_id,))
    row = cur.fetchone()
    return row
