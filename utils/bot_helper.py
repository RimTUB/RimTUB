from typing import Any, List, Optional, Union


from utils.misc import _objects
from pyrogram import filters
from pyrogram.types import InlineQuery,  InlineQueryResultArticle, InputTextMessageContent, CallbackQuery
from pyrogram.types import InlineKeyboardMarkup as Buttons, InlineKeyboardButton as Button


__all__ = [
    'Button',
    'Buttons',
    '_load_bot_helper_handlers',
    'C',
]



class Button(Button):
    extra_data: dict
    extra_data_id: str

    def __init__(
        self,
        text: str,
        callback_data: Optional[Union[str, bytes]] = None,
        url: Optional[str] = None,
        copy_text: str = None,
        extra_data: Optional[dict] = None
    ):
        super().__init__(
            text=text,
            callback_data=callback_data,
            url=url,
            copy_text=copy_text
        )
        self.extra_data = extra_data if extra_data is not None else dict()
        self.extra_data_id = ''

class Buttons(Buttons):
    """An inline keyboard that appears right next to the message it belongs to.

    Parameters:
        inline_keyboard (List of List of :obj:`~pyrogram.types.InlineKeyboardButton`):
            List of button rows, each represented by a List of InlineKeyboardButton objects.
    """
    inline_keyboard: List[List[Button]]

    def __init__(self, inline_keyboard: List[List[Button]], general_extra_data: Optional[dict] = None):

        super().__init__(inline_keyboard)

        if general_extra_data:
            for row in self.inline_keyboard:
                for button in row:
                    if button.callback_data:
                        button.extra_data.update(general_extra_data)


class C(CallbackQuery):
    extra_data: Any
    original_data: str
    original_callback: CallbackQuery


def _load_bot_helper_handlers(bot):

    @bot.on_inline_query(filters.create(lambda _, __, i: i.query.startswith('iqm:')))
    async def _all_inline(_, i: InlineQuery):
        bot.logger.debug(f'got inline query. {i}')
        _, id = i.query.split(':')
        data = _objects.get(id)
        if data:
            await bot.answer_inline_query(i.id, [
                InlineQueryResultArticle('1', InputTextMessageContent(data['text'], bot.parse_mode, **data.get('input_text_message_content_params', {})), id='0', reply_markup=data.get('buttons'))
            ])
