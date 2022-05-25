from Luna import CMD_HELP
from Luna import tbot
import io
import os
import asyncio
from datetime import datetime

import requests
from telethon import types
from telethon.tl import functions
from Luna import REM_BG_API_KEY
from Luna import TEMP_DOWNLOAD_DIRECTORY
from Luna.events import bot as register

@register(pattern="^/rmbg")
async def _(event):
    if event.fwd_from:
        return
    if REM_BG_API_KEY is None:
        await event.reply("You need API token from remove.bg to use this plugin.")
        return False
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        k = await event.reply("Processing...")
        try:
            downloaded_file_name = await tbot.download_media(
                reply_message, TEMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await event.reply(str(e))
            return
        else:
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    else:
        HELP_STR = "use `/rmbg` as reply to a media"
        await event.reply(HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "rmbg.png"
            await tbot.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id,
            )
        await k.delete()
        end = datetime.now()
        ms = (end - start).seconds
        m = await event.reply(f"Background Removed in {ms} seconds")
        await asyncio.sleep(3)
        await m.delete()
    else:
        await event.reply(
            "remove.bg API returned Errors. Please report to @lunabotsupport\n`{}".format(
                output_file_name.content.decode("UTF-8")
            )
        )


def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /rmbg: Type in reply to a media to remove it's background
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
