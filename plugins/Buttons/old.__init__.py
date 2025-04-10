from pyrogram.types import Message as M
from telebot.types import (
    CallbackQuery as C,
    InlineKeyboardMarkup as IM, InlineKeyboardButton as IB
)

from utils import *


async def main(app: Client, mod: Module):

    cmd = mod.cmd

    def get_rm(app: Client, rm_id):
        match rm_id:
            case 'menu':
                return IM(
                ).add(IB("нажми меня", callback_data=format_callback(app, click))
                ).add(IB("Числа",      callback_data=format_callback(app, show_numbers)))
            case 'numbers':
                rm = IM()
                rm.add(*[
                        IB(str(i), callback_data=format_callback(app, click_numbers, False, i))
                        for i in range(16)
                    ], row_width=4
                ).add(
                    IB("Назад", callback_data=format_callback(app, menu, False))
                )
                return rm
            case 'to_menu':
                return IM().add(IB('В меню', callback_data=format_callback(app, menu)))
            
    async def click(app: Client, c: C):
        await app.bot.edit_message_text("Нажал!", reply_markup=get_rm(app, 'to_menu'), inline_message_id=c.inline_message_id)

    async def show_numbers(app: Client, c: C):
        await app.bot.edit_message_text("Выбери число", reply_markup=get_rm(app, 'numbers'), inline_message_id=c.inline_message_id)        

    async def click_numbers(app: Client, c: C, num):
        await app.bot.answer_callback_query(c.id, f"Ты выбрал {num}!", True)

    async def menu(app: Client, c):
        await app.bot.edit_message_text("Меню.", reply_markup=get_rm(app, 'menu'), inline_message_id=c.inline_message_id)
    
    
    @cmd(["test"])
    async def _test(app: Client, msg: M):
        await create_buttons(app, msg.chat.id, format_callback(app, menu))
        await msg.delete()