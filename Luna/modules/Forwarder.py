import logging
from Luna import tbot, CMD_HELP, OWNER_ID
from Luna.events import bot
import asyncio, os
from telethon import *
from telethon.tl import functions
from telethon.tl.types import *
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from telethon import TelegramClient, events
@bot(pattern="^/frwd")
async def frwder(event):
    if event.is_private:
        await event.reply("I work in groups!")
        return
    ok = await tbot(GetFullUserRequest(event.sender_id))
    txt = event.text.split(" ", maxsplit=2)
    try:
        chat = txt[1]
        msg = txt[2]
        if msg is None:
            await event.reply("No message provided!\n\nFormat - `/frwd <chat id/username> <message/reply to message>`")
            return
        if chat.startswith('@'):
            try:
                temp = await tbot.get_entity(chat)
                chat = temp.id
            except UsernameNotOccupiedError as e:
                await event.reply(str(e))
                return
        try:
            sent = await tbot.send_message(chat, msg)
            await sent.reply(f"Message from [{ok.user.first_name}](tg://user?id={event.sender_id})")
            temp = await event.reply("Done!")
            await asyncio.sleep(10)
            #await event.delete()
            await temp.delete()
        except Exception as e:
            await event.reply(f"Bot not in the group 🤔\n\n{str(e)}")
    except UsernameNotOccupiedError as e:
        await event.reply(str(e))
        return
    except Exception as e:
        await event.reply(f"Format - `/frwd <chat id/username> <message/reply to message>`\n\n{str(e)}")
        return

@bot(pattern="^/post ?(.*)")
async def post(event):
    if event.sender_id != OWNER_ID:
        return
    quew = event.pattern_match.group(1)
    chat = quew or -1001309757591
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message
    else:
        await event.reply('Master, Give some text to Post!')
        return
    try:
        await tbot.send_message(chat, text)
        await event.reply('Done!')
    except Exception:
        await event.reply('Failed to Post')
    


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /frwd <msg> <group>: Forwards the given msg to The Group
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
