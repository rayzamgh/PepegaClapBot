from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import numpy as np

img = Image.open(sys.argv[1]).convert("RGBA")
background = Image.open(sys.argv[2])
name = sys.argv[3]
nim = sys.argv[4]

size = (750,750)
img = img.resize(size, Image.ANTIALIAS)

background.paste(img, (150,200), img)
draw = ImageDraw.Draw(background)
font = ImageFont.truetype("calibri.ttf", 37)

x1 = 160
x2 = 735
y = 915

draw.text((x1-1,y-1), name, fill="white", font=font)
draw.text((x1+1,y-1), name, fill="white", font=font)
draw.text((x1-1,y+1), name, fill="white", font=font)
draw.text((x1+1,y+1), name, fill="white", font=font)

draw.text((x2-1,y-1), nim, fill="white", font=font)
draw.text((x2+1,y-1), nim, fill="white", font=font)
draw.text((x2-1,y+1), nim, fill="white", font=font)
draw.text((x2+1,y+1), nim, fill="white", font=font)

draw.text((x1,y), name, fill="black", font=font)
draw.text((x2,y), nim, fill="black", font=font)

background.save(nim + '.png', "PNG")