import time
import asyncio
from datetime import datetime

from pytimeparse2 import parse

from utils import *

import requests
from zoneinfo import ZoneInfo
from geopy.geocoders import Nominatim


async def worker(app, mod):
    while True:
        timers: list[dict] = await mod.db.get('timers', [])
        for timer in timers:
            if timer['time'] <= time.time():
                await app.bot.send_message(app.me.id, f"⏰ Таймер на {b(sec_to_str(timer['during']))}!\n\n" + timer.get('text', ''))
                timers.remove(timer)
                await mod.db.set('timers', timers)
        await asyncio.sleep(1)


async def main(app: Client, mod: Module):


    cmd = mod.cmd

    mod.add_task(worker(app, mod))

    @cmd(['timers'])
    async def _timers(app: Client, msg):
        timers: list[dict] = await mod.db.get('timers', [])
        o = b("Активные таймеры:\n\n")
        for timer in timers:
            o += f"🪪 ID: {code(timer['id'])}\n"
            o += f"⏰ Длительность: {b(sec_to_str(timer['during']))}\n"
            o += f"⏱ Осталось: {b(sec_to_str( timer['time'] - time.time() ))}\n"
            o += b("🪧 Текст этикетки: ") + timer.get('text', '-') + "\n"
            o += code('··················') + "\n"
        
        await msg.edit(o)


    @cmd(['timer'])
    async def _timer(app: Client, msg):
        if len(msg.command) == 1:
            return await msg.edit(f"<emoji id='5240241223632954241'>🚫</emoji> Неверный ввод данных!")
        
        text = msg.text.split(maxsplit=2)[-1] if len(msg.command) > 2 else ""
        str_time = msg.command[1]
        sec_time = parse(str_time)
        if sec_time is None:
            return await msg.edit(f"<emoji id='5240241223632954241'>🚫</emoji> Неверный ввод данных!")
        timers: list[dict] = await mod.db.get('timers', [])
        timer = {}
        timer['time'] = time.time() + sec_time
        timer['during'] = sec_time
        if len(timers) == 0:
            timer['id'] = 1
        else:
            timer['id'] = timers[-1]['id'] + 1
        if text:
            timer['text'] = text
        timers.append(timer)
        await mod.db.set('timers', timers)
        await msg.edit(
            f"<emoji id='5413704112220949842'>⏰</emoji> Таймер {timer['id']} успешно установлен на {b(sec_to_str(sec_time))}\n"
            + ((b("Текст этикетки: ") + text) if text else '')
        )


    @cmd(['stoptimer'])
    async def _stoptimer(app, msg):
        if len(msg.command) != 2:
            return await msg.edit(f"<emoji id='5240241223632954241'>🚫</emoji> Неверный ввод данных!")

        try: timer_id = int(msg.command[1])
        except ValueError: return await msg.edit(f"<emoji id='5240241223632954241'>🚫</emoji> Неверный ввод данных!\nВведи число!")
        
        timers = await mod.db.get('timers', [])
        
        success = False
        
        for timer in timers:
            if timer['id'] == timer_id:
                timers.remove(timer)
                success = True
                break
        
        if success:
            await mod.db.set('timers', timers)
            return await msg.edit(f"<emoji id='5206607081334906820'>✅</emoji> Таймер {b(timer_id)} успешно удален!")
        return await msg.edit(f"<emoji id='5210952531676504517'>❌</emoji> Таймер {b(timer_id)} не найден!")

    def convert_to_time(number):
        sign = '+' if number >= 0 else '-'
        abs_number = abs(number)

        hours = int(abs_number)
        minutes = round((abs_number - hours) * 60)

        return f"{sign}{hours}:{minutes:02d}" if minutes else f"{sign}{hours}"

    @cmd(['gettime'])
    async def _gettime(app, msg):
        if len(msg.command) == 1:
            return await msg.edit(f"<emoji id='5240241223632954241'>🚫</emoji> Неверный ввод данных!")

        await msg.edit("<emoji id='5231012545799666522'>🔍</emoji> Ищу Ваш город...")

        town = msg.text.split(maxsplit=1)[1]

        geolocator = Nominatim(user_agent="timezone_finder")
        location = geolocator.geocode(town)

        if location is None:
            return await msg.edit(f"<emoji id='5210952531676504517'>❌</emoji> Город {b(town)} не найден!")

        username = "RimTUB"
        geo_url = f"http://api.geonames.org/searchJSON?q={town}&maxRows=1&username={username}"
        geo_res = requests.get(geo_url).json()

        if not geo_res["geonames"]:
            return await msg.edit(f"<emoji id='5210952531676504517'>❌</emoji> Город {b(town)} не найден!")

        lat = geo_res["geonames"][0]["lat"]
        lon = geo_res["geonames"][0]["lng"]

        # Получаем таймзону
        tz_url = f"http://api.geonames.org/timezoneJSON?lat={lat}&lng={lon}&username={username}"
        tz_res = requests.get(tz_url).json()

        timezone_str = tz_res.get("timezoneId")
        if not timezone_str:
            return await msg.edit(f"<emoji id='5210952531676504517'>❌</emoji> Не удалось найти таймзону для города {b(town)}!")

        now = datetime.now(ZoneInfo(timezone_str))
        utc_offset = now.utcoffset().total_seconds() / 3600
        utc_offset = f"+{int(utc_offset):02d}:00" if utc_offset >= 0 else f"-{int(abs(utc_offset)):02d}:00"
        str_time = now.strftime('%Y.%m.%d\xa0%H:%M')

        await msg.edit(f"<emoji id='5397782960512444700'>📌</emoji> Текущее время в городе {b(town)} {i(f'({timezone_str}, UTC{utc_offset})')}: {b(str_time)}")
