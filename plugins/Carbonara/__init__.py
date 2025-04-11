from traceback import format_exc
import io

from pyrogram.types import Message

from utils import *

from carbon import Carbon, CarbonOptions


DEFAULT_PHOTO_PARAMS = dict(
    background_color = [255, 255, 255, 1],
    drop_shadow = True,
    shadow_blur_radius_px = 68,
    shadow_offset_y_px = 20,
    export_size = 2,
    font_size_px = 14,
    font_family = 'hack',
    first_line_number = 1,
    line_height_percent = 1.33,
    show_line_numbers = True,
    show_window_controls = True,
    show_watermark = False,
    horizontal_padding_px = 56,
    vertical_padding_px = 56,
    adjust_width = True,
    theme = 'vscode',
    window_theme = 'none'
)

LOADING = f"{emoji(5821116867309210830, '⏳')} Загрузка..."



async def main(app: Client, mod: Module):


    if not await mod.db.get('params', None):
        await mod.db.set('params', DEFAULT_PHOTO_PARAMS)


    cb = Carbon()

    cmd = mod.cmd

    @cmd(['cb', 'carbon'])
    async def _cb(_, msg: Message):
        await msg.edit(LOADING)
        try:
            try: _, lang, code = msg.text.split(maxsplit=2)
            except ValueError:
                if r:=msg.reply_to_message:
                    if lang := get_args(msg.text):
                        code = getattr(msg.quote, 'text', None) or r.text or r.caption
                    else:
                        return await msg.edit(f"Используй " + code(f"{Config.PREFIX}{msg.command[0]}") + escape(" < язык / auto > < код / ответ >"))
                else:
                    return     await msg.edit(f"Используй " + code(f"{Config.PREFIX}{msg.command[0]}") + escape(" < язык / auto > < код / ответ >"))
                
            
            image = await cb.generate(CarbonOptions(code=code, language=lang.capitalize(), **await mod.db.get('params', dict())))
            await (msg.reply_to_message or msg).reply_photo(io.BytesIO(bytes(image)), quote=True, quote_text=msg.quote_text)
            
            await msg.delete()
        except Exception as e:
            await msg.edit(f"Произошла ошибка! {e}\n{await paste(format_exc())}")

    @cmd(['cbset'])
    async def _cbset(_, msg):
        args = get_args(msg.text)
        params = await mod.db.get('params', dict())
        if not args:
            t = 'параметр = текущее значение (значение по умолчанию)\n\n'
            for k, v in params.items():
                t += f"{code(k)} = {code(repr(v))}" + \
                    (f" ({code(repr(DEFAULT_PHOTO_PARAMS[k]))})\n" if v != DEFAULT_PHOTO_PARAMS[k] else "\n")
            return await msg.edit(t)
        args = args.split(maxsplit=1)
        if len(args) > 1:
            try:
                params[args[0]]
                params[args[0]] = eval(args[1])
            except KeyError:
                return await msg.edit("Такой параметр не найден!")
            except:
                return await msg.edit("Неверное значение!")
            else:
                await mod.db.set('params', params)
                return await msg.edit(f"Значение обновлено!\n{code(args[0])} = {code(repr(params[args[0]]))}")
        return await msg.edit("Неверный ввод!")

