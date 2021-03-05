from Luna import SUDO_USERS, tbot, OWNER_ID, DEV_USERS
from telethon.tl.types import ChatBannedRights
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from pymongo import MongoClient
from Luna import MONGO_DB_URI
import asyncio
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


def get_reason(id):
    return gbanned.find_one({"user": id})

chat = -1001356773955
@tbot.on(events.NewMessage(pattern="^/gban (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.sender_id == OWNER_ID:
        pass
    else:
        return
    quew = event.pattern_match.group(1)
    if event.reply_to_msg_id:
       reply_message = await event.get_reply_message()
       k = reply_message.sender_id
       cid = k
       if quew:
           reason = quew
       else:
           reason = "None"
       user = reply_message.sender.first_name
    if not event.reply_to_msg_id:
        if "|" in quew:
          iid, reasonn = quew.split("|")
        cid = iid.strip()
        reason = reasonn.strip()   
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
    if not reason:
        await event.reply("Need a reason for gban.")
        return
    chats = gbanned.find({})

    if r_sender_id == OWNER_ID:
        await event.reply("Fool, how can I gban my master ?")
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
            await event.client.send_message(
                chat,
                "**GLOBAL BAN UPDATE**\n\n**PERMALINK:** `{}` \n**UPDATER:** `{}`**\nREASON:** `{}`".format(
                    r_sender_id, cd, reason
                ),
            )
            return

    gbanned.insert_one(
        {"bannerid": event.sender_id, "user": r_sender_id, "reason": reason}
    )
    await event.client.send_message(
        chat,
        "**Global Ban**\n**Originated from: {}**\n\n**Sudo Admin:** [{}](tg://user?id={})\n**User:** [{}](tg://user?id={})\n**ID:** [{}](tg://user?id={})\n**Reason:** `{}`".format(
            place, cd, event.sender_id, user, r_sender_id, r_sender_id, r_sender_id, reason
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
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    else:
        return

    quew = event.pattern_match.group(1)
    if event.reply_to_msg_id:
       reply_message = await event.get_reply_message()
       k = reply_message.sender_id
       cid = k
       if quew:
           reason = quew
       else:
           reason = "None"
       user = reply_message.sender.first_name
    if not event.reply_to_msg_id:
        if "|" in quew:
          iid, reasonn = quew.split("|")
        cid = iid.strip()
        reason = reasonn.strip()   
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
    if not reason:
        await event.reply("Need a reason for ungban.")
        return
    chats = gbanned.find({})

    if r_sender_id == OWNER_ID:
        await event.reply("Fool, how can I ungban my master ?")
        return
    if r_sender_id in SUDO_USERS:
        await event.reply("Hey that's a sudo user idiot.")
        return
    k=event.sender
    fname=k.first_name
    X=k.last_name
    cd = (f"{fname}-{X}") 
    for c in chats:
        if r_sender_id == c["user"]:
            to_check = get_reason(id=r_sender_id)
            gbanned.delete_one({"user": r_sender_id})
            await event.client.send_message(
                chat,
                "**REMOVAL OF GLOBAL BAN**\n\n**USER:** {}\n**PERMALINK:** [user](tg://user?id={})\n**REMOVER:** `{}`\n**REASON:** `{}`".format(
                    user, r_sender_id, cd, reason
                ),
            )
            await event.reply("Ungbanned Successfully !")
            return
    await event.reply("Is that user even gbanned ?")


@tbot.on(events.ChatAction())
async def join_ban(event):
    if event.is_private: 
        return 
    if event.chat_id == int(-1001158277850):
        return
    if event.chat_id == int(-1001342790946):
        return
    pass
    user = event.user_id
    chats = gbanned.find({})
    for c in chats:
        if user == c["user"]:
            if event.user_joined:
                try:
                    to_check = get_reason(id=user)
                    reason = to_check["reason"]
                    bannerid = to_check["bannerid"]
                    await tbot(EditBannedRequest(event.chat_id, user, BANNED_RIGHTS))
                    await event.reply(
                        "This user is gbanned and has been removed !\n\n**Gbanned By**: `{}`\n**Reason**: `{}`".format(
                            cd, reason
                        )
                    )
                except Exception as e:
                    print(e)
                    return


@tbot.on(events.NewMessage(pattern=None))
async def type_ban(event):
    if event.is_private: 
        return 
    if event.chat_id == int(-1001158277850):
        return
    if event.chat_id == int(-1001342790946):
        return
    pass
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
                        cd, reason
                    )
                )
            except Exception:
                return
