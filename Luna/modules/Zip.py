from datetime import datetime
from Luna import CMD_HELP
from telethon.tl.types import DocumentAttributeVideo
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from Luna import tbot
import os
import time
import zipfile
from telethon import types
from telethon.tl import functions
from Luna import TEMP_DOWNLOAD_DIRECTORY
from Luna.events import bot as register


@register(pattern="^/zip")
async def _(event):
    if event.fwd_from:
        return


    if not event.is_reply:
        await event.reply("Reply to a file to compress it.")
        return

    mone = await event.reply("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await tbot.download_media(
                reply_message, TEMP_DOWNLOAD_DIRECTORY
            )
            directory_name = downloaded_file_name
        except Exception as e:
            await mone.reply(str(e))
    zipfile.ZipFile(f"{directory_name}.zip", "w", zipfile.ZIP_DEFLATED).write(
        directory_name
    )

    await tbot.send_file(
        event.chat_id,
        f"{directory_name}.zip",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
    )


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))


extracted = f"{TEMP_DOWNLOAD_DIRECTORY}extracted/"
thumb_image_path = f"{TEMP_DOWNLOAD_DIRECTORY}/thumb_image.jpg"
if not os.path.isdir(extracted):
    os.makedirs(extracted)


@register(pattern="^/unzip")
async def _(event):
    if event.fwd_from:
        return



    mone = await event.reply("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await tbot.download_media(
                reply_message, TEMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await mone.reply(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds

        with zipfile.ZipFile(downloaded_file_name, "r") as zip_ref:
            zip_ref.extractall(extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        await event.reply("Unzipping now")
        for single_file in filename:
            if os.path.exists(single_file):
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ]
                try:
                    await tbot.send_file(
                        event.chat_id,
                        single_file,
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=document_attributes,
                    )
                except Exception as e:
                    await tbot.send_message(
                        event.chat_id,
                        f"{caption_rts} caused `{str(e)}`",
                        reply_to=event.message.id,
                    )

                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /zip: reply to a telegram file to compress it in .zip format
 - /unzip: reply to a telegram file to decompress it from the .zip format
"""


CMD_HELP.update({file_helpo: [file_helpo, __help__]})
