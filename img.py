from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import os
import numpy as np

def editphoto(nim, framename, name):
    #ultahseptember.png

    returns = []

    fullname = "BOTRDY_" + nim

    files = os.listdir("App_data/UNIX")

    images = [file for file in files if file.startswith(fullname)]

    for image in images:

        background = Image.open("App_data/" + framename)
        
        img = Image.open("App_data/UNIX/" + image).convert("RGBA")

        size = (1225,855)
        img = img.resize(size, Image.ANTIALIAS)

        left = 100
        top = 0
        right = 1025
        bottom = 855
        
        img = img.crop((left, top, right, bottom)) 

        background.paste(img, (540,660), img)
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("App_data/Roboto-Regular.ttf", 37)

        x1 = 475
        x2 = 1350
        y = 1600

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

        returns.append(background)
    
    return returns

images = editphoto("13517071", "ultahseptember.png", "MARSA")

images[0].show()
        