from Luna import SUDO_USERS, tbot, OWNER_ID, DEV_USERS, BOT_ID
from telethon.tl.types import ChatBannedRights
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from pymongo import MongoClient
from Luna import MONGO_DB_URI
import asyncio
from datetime import datetime
import pytz
from telethon.tl.functions.users import GetFullUserRequest
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
gbanned = db.gban

IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)

def get_reason(id):
    return gbanned.find_one({"user": id})

chat = -1001309757591
@tbot.on(events.NewMessage(pattern="^/gban ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if (
        event.sender_id != OWNER_ID
        and event.sender_id not in SUDO_USERS
        and event.sender_id not in DEV_USERS
    ):
        return
    quew = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        k = reply_message.sender_id
        cid = k
        reason = "None" if quew is None else quew
        user = reply_message.sender.first_name
    if not event.reply_to_msg_id:
        if "|" in quew:
          iid, reasonn = quew.split("|")
          cid = iid.strip()
          reason = reasonn.strip()
        else:
          cid = quew
          reason = None
        if cid.isnumeric():
           cid = int(cid)
        entity = await tbot.get_input_entity(cid)
        r_sender_id = entity.user_id
        k = r_sender_id
        replied_user = await tbot(GetFullUserRequest(k))
        user = replied_user.user.first_name
    entity = await tbot.get_input_entity(cid)
    try:
        r_sender_id = entity.user_id
    except Exception:
        await event.reply("Couldn't fetch that user.")
        return
    chats = gbanned.find({})
    if r_sender_id == OWNER_ID:
        k = await tbot.send_file(event.chat_id, file='CAADBQADFAIAAjUy2FRA5ZOSuDMchgI')
        await event.reply(f"Char Chavanni godhe pe\n{event.sender.first_name} Mere Lode Pe!.")
        await k.edit('test')
        return
    elif r_sender_id in SUDO_USERS:
        await tbot.send_message(event.chat_id, file='CAADAQAD2wEAAkVfBy8Mh2GQNhOIIAI')
        return
    elif r_sender_id in DEV_USERS:
        await event.reply("This Person is a Dev, Sorry!")
        return
    elif r_sender_id == BOT_ID:
        await event.reply("Another one bits the dust! banned a betichod!")
        return
    k=event.sender
    fname=k.first_name
    X=k.last_name
    cd = (f"{fname}-{X}")
    origin = event.chat_id
    ok = event.chat.title
    place = (f"{ok} {origin}")
    for c in chats:
        if r_sender_id == c["user"]:
            to_check = get_reason(id=r_sender_id)
            gbanned.update_one(
                {
                    "_id": to_check["_id"],
                    "bannerid": to_check["bannerid"],
                    "user": to_check["user"],
                    "reason": to_check["reason"],
                },
                {"$set": {"reason": reason, "bannerid": event.sender_id}},
            )
            await event.reply(
                "This user is already gbanned, I am updating the reason of the gban with your reason."
            )
            pic = datetime.now(IST)
            tym = pic.strftime('%H:%M:%S')
            await event.client.send_message(
                chat,
                "**Global Ban Update**\n**Originated from: {}**\n\n**Sudo Admin:** [{}](tg://user?id={})\n**User:** [{}](tg://user?id={})\n**ID:** `{}`\n**New Reason:** {}\n**Event Time:** **{}**".format(
                    place, cd, event.sender_id, user, r_sender_id, r_sender_id, reason, tym
                ),
            )
            return

    gbanned.insert_one(
        {"bannerid": event.sender_id, "user": r_sender_id, "reason": reason}
    )
    op = datetime.now(IST)
    tym = op.strftime('%H:%M:%S')
    if reason:
      await event.client.send_message(
        chat,
        "**Global Ban**\n**Originated from: {}**\n\n**Sudo Admin:** [{}](tg://user?id={})\n**User:** [{}](tg://user?id={})\n**ID:** `{}`\n**Reason:** {}\n**Event Time:** **{}**".format(
            place, cd, event.sender_id, user, r_sender_id, r_sender_id, reason, tym
        ),
      )
    else:
      await event.client.send_message(
        chat,
        "**Global Ban**\n**Originated from: {}**\n\n**Sudo Admin:** [{}](tg://user?id={})\n**User:** [{}](tg://user?id={})\n**ID:** `{}`\n**Event Time:** **{}**".format(
            place, cd, event.sender_id, user, r_sender_id, r_sender_id, tym
        ),
      )
    k = await event.reply("Initiating Global Ban.!")
    await asyncio.sleep(6)
    await k.delete()
    await event.reply("Gban Completed")

@tbot.on(events.NewMessage(pattern="^/ungban (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if (
        event.sender_id != OWNER_ID
        and event.sender_id not in SUDO_USERS
        and event.sender_id not in DEV_USERS
    ):
        return
    quew = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        k = reply_message.sender_id
        cid = k
        reason = "None" if quew is None else quew
        user = reply_message.sender.first_name
    if not event.reply_to_msg_id:
        if "|" in quew:
          iid, reasonn = quew.split("|")
          cid = iid.strip()
          reason = reasonn.strip()
        else:
           cid = quew
           reason = None
        if cid.isnumeric():
           cid = int(cid)
        entity = await tbot.get_input_entity(cid)
        r_sender_id = entity.user_id
        k = r_sender_id
        replied_user = await tbot(GetFullUserRequest(k))
        user = replied_user.user.first_name
    entity = await tbot.get_input_entity(cid)
    try:
        r_sender_id = entity.user_id
    except Exception:
        await event.reply("Couldn't fetch that user.")
        return
    chats = gbanned.find({})

    if r_sender_id == OWNER_ID:
        await event.reply("Don't Play With my Master !")
        return
    elif r_sender_id in SUDO_USERS:
        await event.reply("Don't Do Sudo War Mc!")
        return
    elif r_sender_id in DEV_USERS:
        await event.reply("This Person is a Dev, Sorry!")
        return
    elif r_sender_id == BOT_ID:
        await event.reply("Nada")
        return
    k=event.sender
    fname=k.first_name
    X=k.last_name
    cd = (f"{fname}-{X}")
    origin = event.chat_id
    ok = event.chat.title
    place = (f"{ok} {origin}")
    abe = datetime.now(IST)
    tym = abe.strftime('%H:%M:%S')
    for c in chats:
        if r_sender_id == c["user"]:
            to_check = get_reason(id=r_sender_id)
            gbanned.delete_one({"user": r_sender_id})
            if reason:
              await event.client.send_message(
                chat,
                "**Removal of Global Ban**\n**Originated from: {}**\n\n**Sudo Admin:** [{}](tg://user?id={})\n**User:** [{}](tg://user?id={})\n**ID:** `{}`\n**Reason:** {}\n**Event Time:** **{}**".format(
                    place, cd, event.sender_id, user, r_sender_id, r_sender_id, reason, tym
                ),
               )
            else:
               await event.client.send_message(
                chat,
                "**Removal of Global Ban**\n**Originated from: {}**\n\n**Sudo Admin:** [{}](tg://user?id={})\n**User:** [{}](tg://user?id={})\n**ID:** `{}`\n**Event Time:** **{}**".format(
                    place, cd, event.sender_id, user, r_sender_id, r_sender_id, tym
                ),
               )
            k = await event.reply("Initiating Removal Of Global Ban.!")
            await asyncio.sleep(6)
            await k.delete()
            await event.reply("Global Ungban Completed.")
            return
    await event.reply("Is that user even gbanned ?")


@tbot.on(events.ChatAction())
async def join_ban(event):
    if event.is_private: 
        return
    if event.chat_id == -1001486931338:
        return
    user = event.user_id
    if user == OWNER_ID:
       await client.send_file(event.chat_id, file='AgADBQADEqwxG4Le2Fbjy1e1eAudcxGbD290AAvLSQMAAQI')

@tbot.on(events.NewMessage(pattern=None))
async def type_ban(event):
    if event.is_private: 
        return
    chats = gbanned.find({})
    for c in chats:
        if event.sender_id == c["user"]:
            try:
                to_check = get_reason(id=event.sender_id)
                reason = to_check["reason"]
                bannerid = to_check["bannerid"]
                await tbot(
                    EditBannedRequest(event.chat_id, event.sender_id, BANNED_RIGHTS)
                )
                await event.reply(
                    "This user is gbanned and has been removed !\n\n**Gbanned By**: `{}`\n**Reason**: `{}`".format(
                        bannerid, reason
                    )
                )
            except Exception:
                return
@tbot.on(events.ChatAction())
async def join_ban(event):
    if event.is_private:
        return
    chat = event.chat_id
    k = event.user_id
    gey = event.user_id
    for c in chats:
       if gey == c["user"]:
              try:
                to_check = get_reason(id=event.sender_id)
                reason = to_check["reason"]
                bannerid = to_check["bannerid"]
                await tbot(
                    EditBannedRequest(event.chat_id, event.sender_id, BANNED_RIGHTS)
                )
                await event.reply(
                    "This user is gbanned and has been removed !\n\n**Gbanned By**: `{}`\n**Reason**: `{}`".format(
                        bannerid, reason
                    )
                )
              except Exception:
                return

from Luna.modules.sql.mute_sql import is_muted, mute, unmute
from telethon import events

@register(pattern="^/gmute ?(.*)")
async def gmute(event):
    if (
        event.sender_id != OWNER_ID
        and event.sender_id not in DEV_USERS
        and event.sender_id not in SUDO_USERS
    ):
        return
    reply = await event.get_reply_message()
    userid = reply.sender_id
    if userid == OWNER_ID:
        await event.reply("I can Act on my master")
        return
    elif userid == BOT_ID:
         await event.reply("Ya I'm not gonna mute myself;")
         return
    elif userid in SUDO_USERS:
         await event.reply("I Won't mute my Sudo User!")
         return
    elif userid in DEV_USERS:
         await event.reply("Nope Can't mute my Dev")
         return
    if is_muted(userid, "gmute"):
        return await event.reply("This user is already gmuted")
    try:
        mute(userid, "gmute")
    except Exception as e:
        await event.reply("Error occured!\nError is " + str(e))
    else:
        await event.reply("Successfully gmuted that person")

@register(pattern="^/ungmute ?(.*)")
async def ungmute(event):
    if (
        event.sender_id != OWNER_ID
        and event.sender_id not in DEV_USERS
        and event.sender_id not in SUDO_USERS
    ):
        return
    reply = await event.get_reply_message()
    userid = reply.sender_id
    if userid == OWNER_ID:
        await event.reply("I can Act on my master")
        return
    elif userid == BOT_ID:
         await event.reply("Ya I'm not gonna ungmute myself;")
         return
    elif userid in SUDO_USERS:
         await event.reply("I Won't. my Sudo User!")
         return
    elif userid in DEV_USERS:
         await event.reply("Nope Can't. my Dev!")
         return
    if not is_muted(userid, "gmute"):
        return await event.reply("This user is not gmuted")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await event.reply("Error occured!\nError is " + str(e))
    else:
        await event.reply("Successfully ungmuted that person")


@tbot.on(events.NewMessage(pattern=None))
async def lel(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()



