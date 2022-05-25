from Luna import CMD_HELP
import os
from Luna import tbot
import math
import requests
import json

from telethon import types
from telethon.tl import functions
from Luna.events import bot as register


@register(pattern="^/simplify (.*)")
async def _(event):
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/simplify/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/factor (.*)")
async def _(event):
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/factor/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/derive (.*)")
async def _(event):
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/derive/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/integrate (.*)")
async def _(event):
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/integrate/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/zeroes (.*)")
async def _(event):
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/zeroes/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/tangent (.*)")
async def _(event):
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/tangent/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/area (.*)")
async def _(event):
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/area/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/cos (.*)")
async def _(event):
    args = int(event.pattern_match.group(1))
    await event.reply(str(math.cos(args)))


@register(pattern="^/sin (.*)")
async def _(event):
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.sin(args)))


@register(pattern="^/tan (.*)")
async def _(event):
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.tan(args)))


@register(pattern="^/arccos (.*)")
async def _(event):
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.acos(args)))


@register(pattern="^/arcsin (.*)")
async def _(event):
    
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.asin(args)))


@register(pattern="^/arctan (.*)")
async def _(event):
    
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.atan(args)))


@register(pattern="^/abs (.*)")
async def _(event):
    
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.fabs(args)))


@register(pattern="^/log (.*)")
async def _(event):
    
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.log(args)))

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
Solves complex math problems using https://newton.now.sh
 - /simplify: Simplify `/simplify 2^2+2(2)`
 - /factor: Factor `/factor x^2 + 2x`
 - /derive: Derive `/derive x^2+2x`
 - /integrate: Integrate `/integrate x^2+2x`
 - /zeroes: Find 0's `/zeroes x^2+2x`
 - /tangent: Find Tangent `/tangent 2lx^3`
 - /area: Area Under Curve `/area 2:4lx^3`
 - /cos: Cosine `/cos 0`
 - /sin: Sine `/sin 0`
 - /tan: Tangent `/tan 0`
 - /arccos: Inverse Cosine `/arccos 1`
 - /arcsin: Inverse Sine `/arcsin 0`
 - /arctan: Inverse Tangent `/arctan 0`
 - /abs: Absolute Value `/abs -1`
 - /log: Logarithm `/log 28`

_Keep in mind_: To find the tangent line of a function at a certain x value, send the request as c|f(x) where c is the given x value and f(x) is the function expression, the separator is a vertical bar '|'. See the table above for an example request.
To find the area under a function, send the request as c:d|f(x) where c is the starting x value, d is the ending x value, and f(x) is the function under which you want the curve between the two x values.
To compute fractions, enter expressions as numerator(over)denominator. For example, to process 2/4 you must send in your expression as 2(over)4. The result expression will be in standard math notation (1/2, 3/4) .
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
