from Luna import CMD_HELP, OWNER_ID
from Luna.events import bot as register
import os

k = 'News Py Files In Another Repo'
@register(pattern="^/tem ?(.*)")
async def sleepybot(time):
    if time.fwd_from:
        return
    if time.sender_id != OWNER_ID:
        return
    await time.reply("Geopy Py In App 2")


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /gps <location>: Get gps location.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})

