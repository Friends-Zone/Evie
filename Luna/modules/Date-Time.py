from Luna import CMD_HELP
import os
from Luna import tbot
import datetime
from typing import List

import requests
TIME_API_KEY = 'HW6LQCYX43HS'
from Luna.events import bot as register
from telethon import types
from telethon.tl import functions

def generate_time(to_find: str, findtype: List[str]) -> str:
    data = requests.get(
        f"http://api.timezonedb.com/v2.1/list-time-zone"
        f"?key={TIME_API_KEY}"
        f"&format=json"
        f"&fields=countryCode,countryName,zoneName,gmtOffset,timestamp,dst"
    ).json()

    for zone in data["zones"]:
        for eachtype in findtype:
            if to_find in zone[eachtype].lower():
                country_name = zone["countryName"]
                country_zone = zone["zoneName"]
                country_code = zone["countryCode"]

                daylight_saving = "Yes" if zone["dst"] == 1 else "No"
                date_fmt = r"%d-%m-%Y"
                time_fmt = r"%H:%M:%S"
                day_fmt = r"%A"
                gmt_offset = zone["gmtOffset"]
                timestamp = datetime.datetime.now(
                    datetime.timezone.utc
                ) + datetime.timedelta(seconds=gmt_offset)
                current_date = timestamp.strftime(date_fmt)
                current_time = timestamp.strftime(time_fmt)
                current_day = timestamp.strftime(day_fmt)

                break

    try:
        result = (
            f"<b>🌍Country :</b> <code>{country_name}</code>\n"
            f"<b>⏳Zone Name :</b> <code>{country_zone}</code>\n"
            f"<b>🗺Country Code :</b> <code>{country_code}</code>\n"
            f"<b>🌞Daylight saving :</b> <code>{daylight_saving}</code>\n"
            f"<b>🌅Day :</b> <code>{current_day}</code>\n"
            f"<b>⌚Current Time :</b> <code>{current_time}</code>\n"
            f"<b>📆Current Date :</b> <code>{current_date}</code>"
        )
    except BaseException:
        result = None

    return result


@register(pattern="^/datetime ?(.*)")
async def _(event):
    if event.fwd_from:
        return

    gay = event.pattern_match.group(1)

    try:
        query = gay
    except BaseException:
        await event.reply("Provide a country name/abbreviation/timezone to find.")
        return

    send_message = await event.reply(
        f"Finding timezone info for <b>{query}</b>", parse_mode="html"
    )

    query_timezone = query.lower()
    if len(query_timezone) == 2:
        result = generate_time(query_timezone, ["countryCode"])
    else:
        result = generate_time(query_timezone, ["zoneName", "countryName"])

    if not result:
        await send_message.edit(
            f"Timezone info not available for <b>{query}</b>", parse_mode="html"
        )
        return

    await send_message.edit(result, parse_mode="html")


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /datetime <timezone>: Get the present date and time information

**You can check out this [link](https://timezonedb.com/time-zones) for the available timezones**
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
