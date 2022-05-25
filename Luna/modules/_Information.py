from Luna import tbot, OWNER_ID as owner, SUDO_USERS as sudo, DEV_USERS as dev
from Luna.events import register
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
import os

@register(pattern="^/u(?: |$)(.*)")
async def who(event):
    replied_user = await get_user(event)
    try:
        caption = await detail(replied_user, event)
    except AttributeError:
        event.edit("`Could not fetch info of that user.`")
        return
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    await event.reply(caption, parse_mode="html")

@register(pattern="^/id ?(.*)")
async def useridgetter(event):
    message = await event.get_reply_message()
    inp = event.pattern_match.group(1)
    if not message and not inp:
        await event.reply(f"Chat ID: `{str(event.chat_id)}`")
    if message:
        if not message.forward:
            user_id = message.sender.id
            name = message.sender.first_name
        else:
            user_id = message.forward.sender.id
            name = message.forward.sender.first_name
        await event.reply(f"User {name}'s id is `{user_id}`.")


async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await tbot(GetFullUserRequest(previous_message.sender_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.get_sender()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await tbot(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await tbot.get_entity(user)
            replied_user = await tbot(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.reply("I don't seem to have interacted with this user before - please forward a message from them to give me control! (like a voodoo doll, I need a piece of them to be able to execute certain commands...)")
            return None

    return replied_user

async def detail(replied_user, event):
    try:
        user_id = replied_user.user.id
        first_name = replied_user.user.first_name
        last_name = replied_user.user.last_name
        username = replied_user.user.username
        first_name = (
            first_name.replace("\u2060", "")
        )
        last_name = (
            last_name.replace("\u2060", "") if last_name else None
        )
        username = f"@{username}" if username else None

        caption = "<b>User Info:</b> \n"
        caption += f"ID: <code>{user_id}</code> \n"
        caption += f"First Name: {first_name} \n"
        if last_name:
          caption += f"Last Name: {last_name} \n"
        if username:
          caption += f"Username: {username} \n"
        caption += f'User link: <a href="tg://user?id={user_id}">link</a>'
        if user_id in sudo:
            caption += "\nStatus: <b>Sudo User</b>"
        if user_id in dev:
            caption += "\nStatus: <b>Dev User</b>"
        if user_id == owner:
            caption += "\nStatus: <b>Owner</b>"
        if user_id == 1624337697:
            caption += "\nStatus: <b>Itz Me</b>"
        return caption
    except Exception:
           print("lel")
