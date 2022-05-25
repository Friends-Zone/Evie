
from Luna import tbot, OWNER_ID, SUDO_USERS, DEV_USERS
from Luna.events import register

@register(pattern="^/echo ?(.*)")
async def echo(event):
  if event.fwd_from:
        return
  if (event.sender_id != OWNER_ID and event.sender_id not in SUDO_USERS
      and event.sender_id not in DEV_USERS):
    return
  if event.reply_to_msg_id:
          await event.delete()
          previous_message = await event.get_reply_message()
          k = await tbot.send_message(
                event.chat_id,
                previous_message
             )
  else:
          ok = event.pattern_match.group(1)
          await event.delete()
          await tbot.send_message(event.chat_id, ok)

