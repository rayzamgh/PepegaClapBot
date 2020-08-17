from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import numpy as np

img = Image.open(sys.argv[1]).convert("RGBA")
background = Image.open(sys.argv[2])


size = (750,750)
img = img.resize(size, Image.ANTIALIAS)

background.paste(img, (150,200), img)
draw = ImageDraw.Draw(background)
font = ImageFont.truetype("C:\ASMAN.TTF", 37)
draw.text((160,915), "Abiyu", (255,255,255), font=font)
draw.text((760,915), "13511222", (255,255,255), font=font)
background.save('test.png', "PNG")

#test.paste(img, (0,0), img)
#test.paste(background, (0,0), background)
#background.save('result.png', "PNG")
#img.save('test.png', "PNG")
#test.save('test.png', "PNG")