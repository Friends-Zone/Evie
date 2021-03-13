from Luna import tbot
from Luna import CMD_HELP
from Luna.events import register
from telethon import *
from telethon.tl import functions
import os
import subprocess


@register(pattern="^/camscanner$")
async def asciiart(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Reply To A Image Plox..")
        return
    directory = "./"
    test = os.listdir(directory)
    for item in test:
        if item.endswith(".jpg"):
            os.remove(os.path.join(directory, item))
        elif item.endswith(".png"):
            os.remove(os.path.join(directory, item))
        elif item.endswith(".jpeg"):
            os.remove(os.path.join(directory, item))
    reply_msg = await event.get_reply_message()
    downloaded_file_name = await tbot.download_media(reply_msg, "./")
    let = f"{downloaded_file_name}"
    subprocess.run(["python", "scan.py", "--image", let])
    await tbot.send_file(event.chat_id, "./scanned.jpg")
    os.remove(f"{downloaded_file_name}")
    os.remove("./scanned.jpg")


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /camscanner: Reply to a image to scan and improve it's clarity.

**Instructions**
▪️The image should be a page with some written text on it (screenshots aren't permitted)
▪️The image should contain the page with four corners clearly visible
▪️The background should be somewhat darker than the page
▪️The image should contain only the page with no other objects like pencil, eraser etc. beside it(within the image)

**PRO TIP**
You can simply draw a border(a black square) around the portion you want to scan for better efficiency and edge detection
If you are still messed up send `/helpcamscanner` in pm for the tutorial !
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})