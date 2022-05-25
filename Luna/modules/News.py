from Luna import CMD_HELP, OWNER_ID
from Luna.events import bot as register
import os

k = 'News Py Files In Another Repo'
@register(pattern="^/testinglasicious ?(.*)")
async def sleepybot(time):
    if time.fwd_from:
        return
    if time.sender_id != OWNER_ID:
        return
    await time.reply("News Py In App 2")

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /news <country code> <LanguageCode>: Returns today's American News Headlines (ONLY WORKS IN PM)
**Example:**
 - /news US en: This will return news for US in english language.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
