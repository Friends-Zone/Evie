import wikipedia
from Luna import *
from wikipedia.exceptions import DisambiguationError, PageError
from telethon import *
from telethon.tl import *
from Luna.events import bot as register

@register(pattern="^/wiki ?(.*)")
async def _(event):
    
    input_str = event.pattern_match.group(1)
    if not input_str:
        await event.reply("Please provide some input.")
        return
    res = ""
    search = input_str
    try:
        res = wikipedia.summary(search)
    except DisambiguationError as e:
        await event.reply(
            "Disambiguated pages found! Adjust your query accordingly.\n<i>{}</i>".format(
                e
            ),
            parse_mode="html",
        )
    except PageError as e:
        await event.reply(f"<code>{e}</code>", parse_mode="html")
    if res:
        result = f"<b>{search}</b>\n\n"
        result += f"<i>{res}</i>\n"
        result += f"""<a href="https://en.wikipedia.org/wiki/{search.replace(" ", "%20")}">Read more...</a>"""
        if len(result) > 4000:
            with open("result.txt", "w") as f:
                f.write(f"{result}")
            with open("result.txt", "rb") as f:
                await tbot.send_file(
                    chat_id=event.chat_id,
                    file=f,
                    filename=f.name,
                    reply_to=event,
                    parse_mode="html",
                )
        else:
            await event.reply(result, parse_mode="html", link_preview=False)


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /wiki <search>: Find results for search in wikipedia and return it.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
