from Luna import tbot
from Luna.events import register
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from Luna import CMD_HELP
from telethon.tl import types
from telethon.tl.types import *
from telethon.tl import functions
import os
async def can_del(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.delete_messages
    )

@register(pattern="^/purge$")
async def purge_messages(event):
    if event.sender_id is None:
        return

    if not await can_del(message=event):
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return
    message_id = reply_msg.id
    delete_to = event.message.id

    messages = [event.reply_to_msg_id]
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == 100:
            try:
                await tbot.delete_messages(event.chat_id, messages)
                messages = []
            except MessageDeleteForbiddenError:
                await event.reply("I can't delete messages that are too old")
                return
    try:
        await tbot.delete_messages(event.chat_id, messages)
    except MessageDeleteForbiddenError:
        await event.reply("I can't delete messages that are too old")
        return

    text = "Purged Successfully !"
    await event.respond(text, parse_mode="markdown")


@register(pattern="^/del$")
async def delete_messages(event):
    if event.sender_id is None:
        return

    if not await can_del(message=event):
        return

    message = await event.get_reply_message()
    if not message:
        await event.reply("What you want to delete?")
        return
    chat = await event.get_input_chat()
    del_message = [message, event.message]
    try:
        await tbot.delete_messages(chat, del_message)
    except MessageDeleteForbiddenError:
        await event.reply("I can't delete messages that are too old")
        return

__help__ = """
 - /purge: deletes all messages from the message you replied to
 - /del: deletes the message replied to
"""
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
