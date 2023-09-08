from aiogram import types
from dispatcher import dp
from bot import BotDB

# Personal actions go here (bot direct messages)
@dp.message_handler(is_owner=True, commands="ping", commands_prefix="!/")
async def cmd_ping_bot(message: types.Message):
    await message.reply("<b>👊 Up & Running!</b>\n\n")

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    # print(BotDB.user_exists(message.from_user.id))
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)

    await message.reply("Welcome!")


@dp.message_handler(commands = ['videos', 'lives'], commands_prefix = "!/")
async def record(message: types.Message) -> None:
    prefs = BotDB.get_preferences(message.from_user.id)
    if message.text == '/videos':

        if prefs[0]:
            BotDB.update_videos_preference(message.from_user.id, False)
            await message.reply("Вы отписались от уведомлений о новых видео!")
        
        else:
            BotDB.update_videos_preference(message.from_user.id, True)
            await message.reply("Вы подписались на уведомления о новых видео!")
    
    else:
        
        if prefs[1]:
            BotDB.update_livestreams_preference(message.from_user.id, False)
            await message.reply("Вы отписались от уведомлений о прямых трансляциях!")
        
        else:
            BotDB.update_livestreams_preference(message.from_user.id, True)
            await message.reply("Вы подписались на уведомления о прямых трансляциях!")


@dp.message_handler(commands = ['info'], commands_prefix= "!/")
async def info(message: types.Message) -> None:
    prefs = BotDB.get_preferences(message.from_user.id)
    username = message.from_user.username
    msg = "Уведомления пользователя @" + username + ":\n\n"

    if prefs[0]:
        msg += "Видео: ✅ Включено\n"
    else:
        msg += "Видео: ❌ Выключено\n"

    if prefs[1]:
        msg += "Прямые трансляции: ✅ Включено"
    else:
        msg += "Прямые трансляции: ❌ Выключено"
    
    await message.reply(msg)