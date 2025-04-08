import time, aiohttp
from pyrogram import types, enums
from utils import *



async def gpt4(prompt, model):
    url = "http://146.19.48.160:25701/generate"
    data = {
        "prompt": prompt,
        "model_name": model
    }
    headers = {"Content-Type": "application/json"}

    start_time = time.time()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()
                result = await response.json()
                response_time = time.time() - start_time

                return True, {
                    "answer": result.get('response'),
                    "time": f"{response_time:.2f}"
                }
    except aiohttp.ClientError as e:
        return False, f"<b>Произошла ошибка запроса</b>"
    except Exception as e:
        return False, f"<b>Произошла непредвиденная ошибка</b>"


async def main(app: Client, mod: Module):

    cmd = mod.cmd

    import aiohttp

    @cmd(['ai'])
    async def ai(_, msg: types.Message):
        await msg.edit("<b>Загрузка...</b>")
        try:
            _, text = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b>Вы не указали запрос!</b>")
            return

        if text in ["help", "h"]:
            result_text = """
<b>Информация и гайд по использованию модуля</b>

1. Есть несколько видов моделей:
 gpt4, 4turbo, gemini, llm3.1
 по умолчанию стоит gpt4
 .ai -model Запрос
 .ai -gemini Привет 

<i>Если у вас возникают проблемы с модулем пишите в лс: @vorsus</i>
""" 
            await msg.edit(result_text)
            return

        model = "llama-3-1-70b-versatile"
        if text.startswith(("-4turbo", "-gemini", "-llm3.1")):
            if text.startswith("-4turbo"):
                text = text[7:].strip()
                model = "gpt4-turbo"
            elif text.startswith("-gemini"):
                text = text[7:].strip()
                model = "gemini"
            elif text.startswith("-llm3.1"):
                text = text[7:].strip()
                model = "llama-3-1-70b-versatile"
            else:
                await msg.edit("Что то пошло не так")
                return 

        ok, result = await gpt4(text, model)
        if not ok:
            await msg.edit(result)
            return 
        result_text = (
            "**👨 Запрос:**\n"
            f"`{text}`\n\n"
            "**🤖 Ответ ИИ:**\n"
            f"{result['answer']}\n\n"
            f"Время ответа: `{result['time']}` секунд"
            )
        if len(result_text) > 4000:
            await msg.edit("<b>Отправка больших ответов в разработке</b>")
        await msg.edit(result_text, parse_mode=enums.ParseMode.MARKDOWN)
