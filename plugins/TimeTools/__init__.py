import time
import asyncio
from datetime import datetime

from pytimeparse2 import parse

from utils import *


__libs__ = ('pytz', 'pytz==2024.2'), ('timezonefinder', 'timezonefinder==6.5.2'), ('geopy', 'geopy==2.4.1')


helplist.add_module(
    HModule(
        __package__,
        description="Работа со временем\n\n* - примеры указания времени: 25s, 1d, 1h30m, 7d4s\n\nДля корректной работы включи уведомления у личного бота!",
        author='built-in (@RimMirK)',
        version='1.0.1'
    ).add_command(
        Command(['timer'], [Argument('время*'), Argument("Текст этикетки", False)], 'Завести таймер')
    ).add_command(
        Command(['timers'], [], 'Список таймеров')
    ).add_command(
        Command(['stoptimer'], [Argument('ID Таймера')], 'остановить таймер')
    ).add_command(
        Command(['gettime'], [Argument("Город")], 'Узнать время в городе')
    )
)

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

    import pytz
    from timezonefinder import TimezoneFinder
    from geopy.geocoders import Nominatim

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
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        timezone = pytz.timezone(timezone_str)
        current_time = datetime.now(timezone)
        utc_offset = pnum(current_time.utcoffset().total_seconds() / 3600)
        utc_offset = convert_to_time(utc_offset)
        str_time = current_time.strftime('%Y.%m.%d\xa0%H:%M')
        await msg.edit(f"<emoji id='5397782960512444700'>📌</emoji> Текущее время в городе {b(town)} {i(f'({timezone_str}, UTC{utc_offset})')}: {b(str_time)}")

        