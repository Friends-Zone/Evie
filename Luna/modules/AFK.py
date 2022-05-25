import os
from Luna import tbot, CMD_HELP
from Luna.modules.sql import afk_sql as sql
from telethon.tl.functions.users import GetFullUserRequest
import time
from telethon import types
from telethon.tl import functions
from Luna.events import register
from telethon import events
import random
options = [
                "{} is here!",
                "{} is back!",
                "{} is now in the chat!",
                "{} is awake!",
                "{} is back online!",
                "{} is finally here!",
                "Welcome back! {}",
                "Where is {}?\nIn the chat!",
            ]
nub = random.choice(options)


@register(pattern=r"(.*?)")
async def _(event):
    sender = await event.get_sender()
    if event.text.startswith("/afk"):
        cmd = event.text[len("/afk ") :]
        reason = cmd if cmd is not None else ""
        fname = sender.first_name
        # print(reason)
        start_time = fname
        sql.set_afk(sender.id, reason, start_time)
        await event.reply(f"{fname} is now AFK !", parse_mode="markdown")
        return
    if event.text.startswith("Brb"):
        cmd = event.text[len("Brb ") :]
        reason = cmd if cmd is not None else ""
        fname = sender.first_name
        # print(reason)
        start_time = fname
        sql.set_afk(sender.id, reason, start_time)
        await event.reply(f"{fname} is now AFK !", parse_mode="markdown")
        return
    if event.text.startswith("brb"):
        cmd = event.text[len("brb ") :]
        reason = cmd if cmd is not None else ""
        fname = sender.first_name
        first_name = fname
        # print(reason)
        start_time = fname
        sql.set_afk(sender.id, reason, start_time)
        await event.reply(f"{fname} is now AFK !", parse_mode="markdown")
        return

    if sql.is_afk(sender.id):
        if res := sql.rm_afk(sender.id):
            firstname = sender.first_name
            loda = nub.format(firstname)
            text = f"{loda}"
            await event.reply(text, parse_mode="markdown")
        

@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    sender = event.sender_id
    msg = str(event.text)
    global let
    global userid
    userid = None
    let = None
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        userid = reply.sender_id
    else:
        try:
            for (ent, txt) in event.get_entities_text():
                if ent.offset != 0:
                    break
                if not isinstance(
                    ent, types.MessageEntityMention
                ) and not isinstance(ent, types.MessageEntityMentionName):
                    return
                c = txt
                a = c.split()[0]
                let = await tbot.get_input_entity(a)
                userid = let.user_id
        except Exception:
            return

    if not userid:
        return
    if sender == userid:
        return

    if not event.is_group:
        return

    if sql.is_afk(userid):
        user = sql.check_afk_status(userid)
        final = user.start_time
        res = (
            "{} is AFK !\nReason: {}".format(final, user.reason)
            if user.reason
            else f"{final} is AFK !"
        )

        await event.reply(res, parse_mode="markdown")
    userid = ""  # after execution
    let = ""  # after execution


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /afk <reason>: mark yourself as AFK(Away From Keyboard)
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
