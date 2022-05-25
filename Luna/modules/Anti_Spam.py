from Luna import CMD_HELP, OWNER_ID
from Luna.events import register
import os

k = 'News Py Files In Another Repo'
@register(pattern="^/teg ?(.*)")
async def sleepybot(time):
    if time.fwd_from:
        return
    if time.sender_id != OWNER_ID:
        return
    await time.reply("AntiSpam Py In App 2")

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /cleanbluetext <on/off/yes/no>: clean commands from non-admins after sending
 - /ignorecleanbluetext <word>: prevent auto cleaning of the command
 - /unignorecleanbluetext <word>: remove prevent auto cleaning of the command
 - /listcleanbluetext: list currently whitelisted commands
 - /profanity on/off: filters all explict/abusive words sent by non admins also filters explicit/porn images
 - /cleanservice on/off: cleans all service messages from telegram
 - /globalmode: let users only speak in english in your group (automatically deletes messages in other languages)
 - /addnsfw: Adds The Group to nsfw Watch List
 - /rmnsfw: Removes The Group From nsfw Watch List
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})


