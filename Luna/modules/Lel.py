from Luna import SUDO_USERS as k
from Luna import DEV_USERS as l
from Luna import OWNER_ID
from Luna.events import register
@register(pattern="^/staffs")
async def _(event):
   reply = "**Owner💥:**\n"
   reply += f"{OWNER_ID}\n"
   p = list(k)
   reply += "**Sudo Users 🔥:**\n"
   for m in p:
        user_id = int(m)
        try:
            reply += "• [{}](tg://user?id={})\n".format(m, m)
        except Exception:
            pass
   n = list(l)
   reply += "**Dev Users 🤖:**\n"
   for f in n:
        user_id = int(f)
        try:
            reply += "• [{}](tg://user?id={})\n".format(f, f)
        except Exception:
            pass
   reply += "• [{}](tg://user?id={})\n".format(OWNER_ID, OWNER_ID)
   await event.client.send_message(
                event.chat_id, reply)
