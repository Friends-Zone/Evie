from Luna import CMD_HELP
import os
from Luna import tbot
from telethon.tl import types
from Luna import *

from Luna.modules.sql.notes_sql import (
    add_note,
    get_all_notes,
    get_notes,
    remove_note)

from telethon import events
from telethon.tl import functions


async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (isinstance(
        p, types.ChannelParticipantAdmin) and p.admin_rights.change_info)


@tbot.on(events.NewMessage(pattern=r"\#(\S+)"))
async def on_note(event):
    name = event.pattern_match.group(1)
    note = get_notes(event.chat_id, name)
    message_id = event.reply_to_msg_id or event.sender_id
    if note is None:
        return
    await event.reply(note.reply, reply_to=message_id)


@register(pattern="^/save(?: |$)(.*)")
async def _(event):
    if (
        event.is_group
        and not await can_change_info(message=event)
        or not event.is_group
    ):
        return
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        note = msg.text
        add_note(
            event.chat_id,
            name,
            note,
        )
        await event.reply(
            "Note **{name}** saved successfully. Get it with #{name}".format(name=name)
        )
    else:
        await event.reply("Reply to a message with /addnote keyword to save the note")


@register(pattern="^/notes$")
async def on_note_list(event):
    if not event.is_group:
        return
    all_notes = get_all_notes(event.chat_id)
    OUT_STR = "**Available notes:**\n"
    if len(all_notes) > 0:
        for a_note in all_notes:
            OUT_STR += f"➤ #{a_note.keyword} \n"
    else:
        OUT_STR = "No notes. Start Saving using /addnote"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "notes.text"
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available notes",
                reply_to=event,
            )
    else:
        await event.reply(OUT_STR)


@register(pattern="^/rmnote (.*)")
async def on_note_delete(event):
    if (
        event.is_group
        and not await can_change_info(message=event)
        or not event.is_group
    ):
        return
    name = event.pattern_match.group(1)
    remove_note(event.chat_id, name)
    await event.reply(f"Note **{name}** deleted successfully")

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
**Admin Only**
 - /save <word>: Type in reply to a message to save that message to the note called "word"
 - /rmnote <word>: delete the note called "word"

**Admin+Non-Admin**
 - /notes: List all notes in the chat
 - #<word> : get the note registered to that word
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
