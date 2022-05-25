from sys import argv, exit
from Luna import tbot
from Luna import TOKEN

import Luna.events

try:
    tbot.start(bot_token=TOKEN)
except Exception:
    print("Bot Token Invalid")
    exit(1)

if len(argv) in {1, 3, 4}:
    tbot.run_until_disconnected()

else:
    tbot.disconnect()
