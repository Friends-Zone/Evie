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
 - /addblacklist <trigger> : blacklists the trigger
 - /rmblacklist <trigger> : stop blacklisting a certain blacklist trigger
 - /listblacklist: list all active blacklist filters
 - /geturl: View the current blacklisted urls
 - /addurl <urls>: Add a domain to the blacklist. The bot will automatically parse the url.
 - /delurl <urls>: Remove urls from the blacklist.

**Example:**
 - /addblacklist the admins suck: This will remove "the admins suck" everytime some non-admin types it
 - /addurl bit.ly: This would delete any message containing url "bit.ly"
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
