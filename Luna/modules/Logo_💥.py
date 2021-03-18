from Luna import CMD_HELP
from Luna.events import register
tmp = './'
from Luna import tbot, OWNER_ID
import os
from PIL import Image, ImageDraw, ImageFont

@register(pattern="^/logo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if "|" in quew:
     text, bg, font = quew.split("|")
     text = text.strip()
     bg = bg.strip()
     fnt = font.strip()
 else:
    text = quew
 if event.sender_id == OWNER_ID:
     pass
 else:
     if event.is_group:
       await event.reply('Currently This Module Only Works in my [PM](tg://user?id=1624337697)')
       return
     else:
       pass
 await event.reply('Processing! Pls Weit...')
 
# get an image
 if bg == None or bg == '2':
       base = Image.open('./Luna/resources/photo_2021-03-18_10-37-51.jpg').convert('RGBA')
 elif bg == '1':
       base = Image.open('./Luna/resources/IMG_20210316_204512_022.jpg').convert('RGBA')

# make a blank image for the text, initialized to transparent text color
 txt = Image.new('RGBA', base.size, (255,255,255,0))

# get a font
 if fnt == None or fnt == '2':
      font = ImageFont.truetype('./Luna/resources/Distort Me.otf', 160)
 elif fnt == '1'
      font = ImageFont.truetype('./Luna/resources/Vermin Vibes V.otf', 160)
# get a drawing context
 d = ImageDraw.Draw(txt)

# draw text, half opacity
 d.text((50,550), text, font=font, fill=(240,248,255,128))
# draw text, full opacity
 d.text((40,500), text, font=font, fill=(250,250,210,255), stroke_width=6, stroke_fill="black")

 out = Image.alpha_composite(base, txt)
 fname = 'lel.png'
 out.save(fname, "png")
 await tbot.send_file(event.chat_id, fname, caption="Made By Anie")
 if os.path.exists(fname2):
            os.remove(fname2)

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 In Beta!.
 - /logo <text>
Module Not Finished.!
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
