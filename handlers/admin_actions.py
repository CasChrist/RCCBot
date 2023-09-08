from aiogram import types
from dispatcher import dp
from bot import BotDB

# Admin actions in a group goes here ...
@dp.message_handler(commands=['deleteall'])
async def delete_all_users(message: types.Message):
    BotDB.delete_all_users()

    await message.bot.send_message(message.from_user.id, "All users deleted!")

@dp.message_handler(commands=['abortdb'])
async def abort_db_connection(message: types.Message):
    BotDB.close()

    await message.reply("DB connection aborted.")

@dp.message_handler(commands=['showalltables'])
async def show_all_tables(message: types.Message):
    msg = BotDB.show_tables()
    await message.bot.send_message(message.from_user.id, msg)