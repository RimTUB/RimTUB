from utils import *


async def main(app: Client, mod: Module):

    cmd = mod.cmd
    group = mod.get_group()

    # делаем функцию для кнопок
    # функцию - потому что эта клавиатура будет использоваться несколько раз 
    def main_buttons(general_extra_data: dict = None):
        # Зачем тут этот параметр - узнаешь позже 
        
        if not general_extra_data:
            general_extra_data = {}
        
        
        # Общая extra_data. Будет передана каждой кнопке в клавиатуре
        general_extra_data.update(
            name = mod.name
        ) 
        # как пример просто передал название модуля
        
        return Buttons([
            [ # первый ряд
                Button('Hello!!!!!', callback_data='hello'), # первая кнопка
                Button('copy me', copy_text='copied!') # вторая кнопка
            ],
            [ # второй ряд кнопок
                Button('RimMirK', url='t.me/RimMirK')
            ],
            [   # для каждой кнопки где есть callback_data можно указать extra_data (dict).
                # Эти данные будут передаваться обработчику.
                # Эти данные доступны только для юб. В callback_data они не видны.
                # Передавать можно все что угодно. Все данные хранятся в формате pickle.
                # Данные живут 3 дня, после чего удаляются.
                # Изменить время жизни можно в конфиге, DEFAULT_STORAGE_FILES_TTL.
                #                                                 vvvvvvvvvvvvvvvvvvvvvvv
                Button('Private button', callback_data='private', extra_data={'secret': 8}),
                Button('Public button',  callback_data='public'),
            ],
            [
                Button('Edit text', callback_data='edit_text'),
                Button('Edit buttons', callback_data='edit_buttons')
            ],
            [
                Button("Page", callback_data='page')
            ],
            [
                Button("Close", callback_data='close')
            ]
        #  передаю общую екстра дату
        ], general_extra_data=general_extra_data)


    

    @cmd('butest')
    async def _butest(_, msg):

        # Отправляем кнопочки методом send_buttons
        await mod.send_buttons(msg.chat.id, 'Держи кнопки!', main_buttons())

        # кнопки отправляются как новое сообщение,
        # поэтому сообщение с командой надо удалить
        await msg.delete()


    # создаем обработчик на callback_data=='hello'
    # желательно указывать group, для корректной работы,
    # но это НЕ Обязательно
    @mod.callback('hello', group=group, is_private=False) # делаем кнопку публичной
    async def _hello(c: C):
        # отвечаем на нажатие окошком
        await c.answer("Hi!", True)
        # True значит что ответ будет в виде окна
        # Если False то будет просто всплывающая надпись. (по умолчанию)


    # создаем обработчик на callback_data=='private'
    @mod.callback('private', group=group)
    async def _private(c: C):
        # часто надо запретить другим пользователям тыкать на наши кнопки. Вот как это сделать:

        if c.from_user.id != app.me.id: # проверяем, совпадает ли ид клиента с ид чела кто жмет на кнопку
            return await c.answer("It's not your button!", True)
        
        # а вот и наша extra_data. Как видишь, все передалось, причем в колбек дате этого секрета нет.
        await c.answer(f"Hi, owner! Your secret is {c.extra_data.get('secret')}\n"
                       f"By the way, it is a {c.extra_data.get('name')} module)")
    

    @mod.callback('public', group=group)
    async def _public(c: C):
        text = c.from_user.full_name + (f" (@{c.from_user.username})" if c.from_user.username else '')
        text += ' кликнул на кнопку!'
        
        # Bot API не дает информацию о сообщении при использовании inline режима.
        # Но RimTUB дает доступ к нему через extra_data['message']
        await app.send_message(c.extra_data['message'].chat.id, text)

        # Кстати, тут нет ответа на кнопку. Вообще тг требует на них отвечать.
        # Но в данном случае отвечать не обязательно, RimTUB ответит сам за тебя :)
        

    @mod.callback('edit_text', group=group)
    async def _edit_text(c: C):
        # попробуем изменить текст сообщения

        # сразу сформируем измененный текст
        
        # т.к. в c.extra_data['message'] хранится изначальный текст сообщения
        # (который мы передавали в send_buttons) нам надо его обновить (получить новый)
        
        msg: M = c.extra_data['message'] # для удобства, сохраню его в типизированную переменную
        
        try:
            new_msg = await app.get_messages(msg.chat.id, msg.id)
        except:
            mod.logger.error('Can\'t get message', exc_info=True)
            await c.answer("Упс! Произошла ошибка! Подробности в консоли")
            return
            
        
        text = new_msg.text + "\nEdited!"

        # И еще: когда изменяешь текст, тг,
        # не пойми зачем удаляет кнопки,
        # так что их надо опять сгенерировать
        # и присоединить к сообщению.
        # Возможно в следующих обновлениях
        # я исправлю это неудобство, а пока так

        # При обновлении кнопок, для того чтобы был доступ к сообщения,
        # нужно в general_extra_data передать прежнюю екстра дату
        # Именно для этого мы и делали параметр в main_buttons

        # получаем наши кнопки заново
        buttons = main_buttons(c.extra_data)

        # если не пользуемся send_buttons, а передаем кнопки сразу напрямую, 
        # надо обязательно использовать mod.prepare_buttons
        buttons = await mod.prepare_buttons(buttons)

        # изменяем сообщение методом edit_message_text.
        # Не забываем присоединить кнопки
        await c.edit_message_text(text, reply_markup=buttons)




    @mod.callback('edit_buttons', group=group)
    async def _edit_buttons(c: C):

        # теперь попробуем заменить клавиатуру

        # В этот раз попробуем передать данные через колбек дату.
        # в некоторых случаях правильней будет так, чем через extra_data

        # генерируем сетку чисел (в кнопках, понятное дело)
        # кстати тут кнопки делаем прям в обработчике,
        # потому что эти кнопки используются только тут и больше нигде.
        buttons = Buttons([ 
            *[
                [ # эти страшные генераторы - это просто генерация сетки чисел.
                    Button( # вся суть вот тут |
                        str(i * 4 + j), #      V
                        callback_data=f'number:{i*4+j}',
                        # число вставляем сразу в колбек дату.
                        # Разделитель советую ':', но можно выбрать любой другой
                    ) for j in range(4)
                ]
                for i in range(4)
            ],
            [Button('Back', callback_data='back')]
        ], general_extra_data=c.extra_data)
        # не забываем передать екстра дату дальше

        # изменяем кнопки методом edit_message_reply_markup.
        # Не забываем про prepare_buttons.
        # Без этого кнопки не будут работать никак
        await c.edit_message_reply_markup(await mod.prepare_buttons(buttons))


    # обработчик уже нужен на startswith
    @mod.callback(startswith='number', group=group, is_private=False)
    async def _number(c: C):

        # выбераем из колбек даты наше число
        number = c.data.split(':')[-1]

        # и выводим пользователю
        await c.answer(number)


    # другой пример изменения кнопок (без генерации)
    @mod.callback('page')
    async def _page(c: C):
        text = "Thanks for using RimTUB ❤️"
        buttons = Buttons([ # новые кнопки
            [
                Button(f"My id: {app.me.id}", copy_text=f'{app.me.id}')
            ],
            [
                Button('RimTUB Developer', url='https://t.me/RimMirK')
            ],
            [
                Button('RimTUB Channel', url='https://t.me/RimTUB'),
                Button('Chat', url='https://t.me/RimTUB_chat')
            ],
            [
                Button('return back', callback_data='back')
            ]
        ], general_extra_data=c.extra_data)
        await c.edit_message_text(text, reply_markup=await mod.prepare_buttons(buttons))


    # тут покажу как хендлерить все остальные кнопки
    @mod.callback(group=group, is_private=True)
    async def _all(c: C):
        # проверяем колбек дату вручную
        if c.data == 'back':

            # меняем клаву назад, на главные кнопки, опять же, не забываем про екстра дату
            await c.edit_message_reply_markup(
                await mod.prepare_buttons(main_buttons(c.extra_data))
            )
            
        elif c.data == 'close':
            msg = c.extra_data['message']
            await app.delete_messages(msg.chat.id, msg.id)
