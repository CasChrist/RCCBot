from aiogram import types
from dispatcher import dp
from bot import BotDB

# Admin actions in a group goes here ...
@dp.message_handler(is_admin=True, commands=['refresh'])
async def check_videos(message: types.Message):
    command = message.text.split(' ')
    command.pop(0)
    

@dp.message_handler(is_owner=True, commands=['deleteall'])
async def delete_all_users(message: types.Message):
    BotDB.delete_all_users()

    await message.bot.send_message(message.from_user.id, "All users deleted!")

@dp.message_handler(is_owner=True, commands=['abortdb'])
async def abort_db_connection(message: types.Message):
    BotDB.close()

    await message.reply("DB connection aborted.")

@dp.message_handler(is_admin=True, commands=['showalltables'])
async def show_all_tables(message: types.Message):
    msg = BotDB.show_tables()
    await message.bot.send_message(message.from_user.id, msg)

@dp.message_handler(is_admin=True, commands="ping", commands_prefix="!/")
async def cmd_ping_bot(message: types.Message):
    await message.reply("<b>👊 Up & Running!</b>\n\n")

@dp.message_handler(is_owner=True, commands=['addusers']) # change to is_admin
async def add_users(message: types.Message):
    ids = message.text.split(' ')
    ids.pop(0)
    total_users = len(ids)
    forbidden, cleared_ids = [], []

    for id in range(len(ids)):
        try:
            ids[id] = int(ids[id])
        except ValueError:
            forbidden.append(ids[id])
            ids[id] = None
    
    if len(forbidden) > 0:
        cleared_ids = [id for id in ids if type(id) == int]
    else:
        cleared_ids = ids
    del ids

    if len(cleared_ids) < 1 and len(forbidden) > 0:
            msg0 = f"❌ <b>Failed to add user(s) you've entered to the database.</b>\n\nProbably, the entered value(s) not of type <i>INTEGER</i> or something else might've come in the way."
            await message.bot.send_message(message.from_user.id, msg0)
            raise ValueError("No user ID has been provided!")
    elif len(cleared_ids) < 1:
        await message.reply("<b>⚙️ Usage: /addusers (user_id1) [user_id2] [user_id3] [...]</b>\n\n<i>Adds 1 or more users to the database. User ID should be of type</i> <code>INTEGER</code><i>. At least 1 user ID to be provided to the input.</i>")
        raise ValueError("No user ID has been provided!")
    for id in range(len(cleared_ids)):
        BotDB.add_user(cleared_ids[id])
    if len(forbidden) > 0:
        final_msg1 = f"⚠️ <b>Successfully added only {len(cleared_ids)} user(s) out of {total_users} to the database. "
        final_msg2 = f"The following {len(forbidden)} user(s) failed to add:</b>\n"
        final_msg3 = ""
        for i in range(len(forbidden)):
            final_msg3 += f"<b>{i+1}.</b> {forbidden[i]}\n"
        final_msg4 = "\nProbably, the entered values aren't of type <i>INTEGER</i> or something else might've come in the way."
        await message.bot.send_message(message.from_user.id, final_msg1 + final_msg2 + final_msg3 + final_msg4)
    else:
        await message.bot.send_message(message.from_user.id, f"✅ <b>{len(cleared_ids)} user(s) added to the database!</b>")