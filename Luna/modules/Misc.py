from Luna.events import register
from Luna import CMD_HELP
from Luna import tbot as bot
from Luna import tbot, abot, ubot
import io
import sys
import traceback
from telethon import custom, events, Button
import random
import time
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *
from telethon.errors import *
from Luna import *
import os
from Luna import SUDO_USERS, OWNER_ID, DEV_USERS, ubot
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from Luna import StartTime
from Luna.events import lunabot

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
gbanned = db.gban


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):          
        return True


def get_reason(id):
    return gbanned.find_one({"user": id})


TMP_DOWNLOAD_DIRECTORY = "./"
TEMP_DOWNLOAD_DIRECTORY = TMP_DOWNLOAD_DIRECTORY


@register(pattern="^/info(?: |$)(.*)")
async def who(event):

    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)

    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        event.edit("`Could not fetch info of that user.`")
        return

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )

        if not photo.startswith("http"):
            os.remove(photo)
        # await event.delete()

    except TypeError:
        await event.reply(caption, parse_mode="html")


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
            await event.reply(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, event):
    try:
        replied_user_profile_photos = await event.client(
            GetUserPhotosRequest(
                user_id=replied_user.user.id, offset=42, max_id=0, limit=80
            )
        )
        replied_user_profile_photos_count = (
            "Person needs help with uploading profile picture."
        )
        try:
            replied_user_profile_photos_count = replied_user_profile_photos.count
        except AttributeError as e:
            pass
        user_id = replied_user.user.id
        first_name = replied_user.user.first_name
        last_name = replied_user.user.last_name
        try:
            dc_id, location = get_input_location(replied_user.profile_photo)
        except Exception as e:
            dc_id = "Couldn't fetch DC ID!"
            location = str(e)
        user_id = replied_user.user.id
        first_name = replied_user.user.first_name
        last_name = replied_user.user.last_name
        username = replied_user.user.username
        user_bio = replied_user.about
        is_bot = replied_user.user.bot
        restricted = replied_user.user.restricted
        verified = replied_user.user.verified
        photo = await event.client.download_profile_photo(
            user_id, TEMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg", download_big=True
        )

        first_name = (
            first_name.replace("\u2060", "")
            if first_name
            else ("This User has no First Name")
        )
        last_name = (
            last_name.replace("\u2060", "")
            if last_name
            else ("This User has no Last Name")
        )
        username = f"@{username}" if username else "This User has no Username"
        user_bio = user_bio or "This User has no About"

        caption = "<b>USER INFO:</b> \n"
        caption += f"First Name: {first_name} \n"
        caption += f"Last Name: {last_name} \n"
        caption += f"Username: {username} \n"
        caption += f"Data Centre ID: {dc_id}\n"
        caption += f"Is Bot: {is_bot} \n"
        caption += f"Is Restricted: {restricted} \n"
        caption += f"Is Verified by Telegram: {verified} \n"
        caption += f"ID: <code>{user_id}</code> \n \n"
        caption += f"Bio: \n<code>{user_bio}</code> \n \n"

        users = gbanned.find({})
        for fuckers in users:
            gid = fuckers["user"]
        if user_id not in SUDO_USERS and user_id != OWNER_ID:
            if str(user_id) == str(gid):
                caption += "<b>Gbanned:</b> Yes\n"
                to_check = get_reason(id=user_id)
                bannerid = str(to_check["bannerid"])
                reason = str(to_check["reason"])
                caption += f"<b>Gbanned by: </b><code>{bannerid}</code>\n"
                caption += f"<b>Reason: </b><code>{reason}</code>\n\n"
            else:
                caption += "<b>Gbanned:</b> No\n\n"

        # caption += f"Common Chats with this user: {common_chat} \n\n"
        caption += "Permanent Link To Profile: "
        caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'

        if user_id in SUDO_USERS:
            caption += "\n\n<b>This person is one of my SUDO USERS\nHe can Gban/Ungban anyome, so mind it !</b>"

        if user_id == OWNER_ID:
            caption += (
                "\n\n<b>This person is my owner.\nHe is the reason why I am alive.</b>"
            )

        approved_userss = approved_users.find({})
        for ch in approved_userss:
            iid = ch["id"]
            userss = ch["user"]

        if event.chat_id == iid and str(user_id) == str(userss):
            caption += "\n\n<b>This person is approved in this chat.</b>"

        return photo, caption
    except Exception as e:
        print(e)


@register(pattern="^/chatid$")
async def chatidgetter(chat):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if chat.is_group:
        if await is_register_admin(chat.input_chat, chat.message.sender_id):
            pass
        elif chat.chat_id != iid or chat.sender_id != userss:
            return
    await chat.reply(f"Chat ID: `{str(chat.chat_id)}`")


@register(pattern="^/runs$")
async def runs(event):
    RUNIT = [
        "Now you see me, now you don't.",
        "ε=ε=ε=ε=┌(;￣▽￣)┘",
        "Get back here!",
        "REEEEEEEEEEEEEEEEEE!!!!!!!",
        "Look out for the wall!",
        "Don't leave me alone with them!!",
        "You've got company!",
        "Chotto matte!",
        "Yare yare daze",
        "*Naruto run activated*",
        "*Nezuko run activated*",
        "Hey take responsibilty for what you just did!",
        "May the odds be ever in your favour.",
        "Run everyone, they just dropped a bomb 💣💣",
        "And they disappeared forever, never to be seen again.",
        "Legend has it, they're still running.",
        "Hasta la vista, baby.",
        "Ah, what a waste. I liked that one.",
        "As The Doctor would say... RUN!",
    ]
    await event.reply(random.choice(RUNIT))


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list.pop()}, "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


@register(pattern="^/(ping|ping@Aniegrpbot)")
async def ping(event):
    import datetime

    start_time = datetime.datetime.now()
    message = await event.reply("Pinging_")
    end_time = datetime.datetime.now()
    pingtime = end_time - start_time
    telegram_ping = f"{str(round(pingtime.total_seconds(), 2))}s"
    uptime = get_readable_time((time.time() - StartTime))
    await message.edit(
        "PONG !\n"
        "<b>Time Taken:</b> <code>{}</code>\n"
        "<b>Service uptime:</b> <code>{}</code>".format(telegram_ping, uptime),
        parse_mode="html",
    )

@register(pattern="^/alive")
async def _(event):
    import datetime
    uptime = get_readable_time((time.time() - StartTime))
    ok = event.chat.title
    reply = "**I'm Up And Alive**\n\n"
    reply += f"**Awake Since:** {uptime}\n"
    reply += "**Telethon Ver:** 1.21.1\n"
    reply += "**Bot_Ver:** 2.0.1\n"
    reply += f"**Chat:** **-{ok}**"
    await tbot.send_message(event.chat_id, reply)


@register(pattern="^/phone (.*)")
async def _(event):
    import requests, json
    fone = event.pattern_match.group(1)
    number = fone if "+" in fone else f"+91{fone}"
    key = "fe65b94e78fc2e3234c1c6ed1b771abd"
    api = (
        "http://apilayer.net/api/validate?access_key="
        + key
        + "&number="
        + number
        + "&country_code=&format=1"
    )
    output = requests.get(api)
    content = output.text
    obj = json.loads(content)
    country_code = obj["country_code"]
    country_name = obj["country_name"]
    location = obj["location"]
    carrier = obj["carrier"]
    line_type = obj["line_type"]
    validornot = obj["valid"]
    reply = f"**Valid:** {str(validornot)}"
    reply += "\n**Phone number:** " + str(number)
    if country_code:
         reply += "\n**Country:** " + str(country_code)
    if country_name:
         reply += "\n**Country Name:** " + str(country_name)
    if location:
         reply += "\n**Location:** " + str(location)
    if carrier:
         reply += "\n**Carrier:** " + str(carrier)
    if line_type:
         reply += "\n**Device:** " + str(line_type)
    await event.reply(reply)

@register(pattern="^/sudolist")
async def _(event):
    if event.sender_id == OWNER_ID:
        pass
    elif event.sender_id not in SUDO_USERS and event.sender_id not in DEV_USERS:
        return
    replied_user = await tbot(GetFullUserRequest(OWNER_ID))
    h = replied_user.user.first_name
    reply = "**Owner 💞:**\n" + "• [{}](tg://user?id={})\n".format(h, OWNER_ID)
    k = SUDO_USERS
    reply += "**Sudo_Users 💫:**\n"
    for m in k:
         try:
            replied_user = await tbot(GetFullUserRequest(m))
            h = replied_user.user.first_name
            reply += f"{h}\n"
         except Exception:
            reply += f"`{m}`\n"
    d = DEV_USERS
    reply += "\n**DEV_USERS ⚔️:**\n"
    for v in d:
         try:
            replied_user = await tbot(GetFullUserRequest(v))
            g = replied_user.user.first_name
            reply += f"{g}\n"
         except Exception:
            pass
    await event.client.send_message(
                 event.chat_id, reply)

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /id: If replied to user's message gets that user's id otherwise get sender's id.
 - /info: Get userinfo
 - /who: Get full userinfo
 - /chatid: Get the current chat id.
 - /runs: Reply a random string from an array of replies.
 - /info: Get information about a user.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
