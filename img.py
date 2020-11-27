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

        size = (480,360)
        img = img.resize(size, Image.ANTIALIAS)

        left = 60
        top = 24
        right = 412
        bottom = 336
        
        img = img.crop((left, top, right, bottom)) 

        background.paste(img, (185,200), img)
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("App_data/Roboto-Regular.ttf", 18)

        x1 = int(185)
        x2 = int(185)
        y1  = int(1100 * 0.5)
        y2  = int(1150 * 0.5)

        draw.text((x1-1,y1-1), name, fill="white", font=font)
        draw.text((x1+1,y1-1), name, fill="white", font=font)
        draw.text((x1-1,y1+1), name, fill="white", font=font)
        draw.text((x1+1,y1+1), name, fill="white", font=font)

        draw.text((x2-1,y2-1), nim, fill="white", font=font)
        draw.text((x2+1,y2-1), nim, fill="white", font=font)
        draw.text((x2-1,y2+1), nim, fill="white", font=font)
        draw.text((x2+1,y2+1), nim, fill="white", font=font)

        draw.text((x1,y1), name, fill="black", font=font)
        draw.text((x2,y2), nim, fill="black", font=font)

        returns.append(background)
    
    return returns

def editphotomanual(nim, framename, name, imagefile):

    background = Image.open("App_data/" + framename)

    img = Image.open(imagefile).convert("RGBA")

    size = (480,360)
    img = img.resize(size, Image.ANTIALIAS)

    left = 60
    top = 24
    right = 412
    bottom = 336

    img = img.crop((left, top, right, bottom)) 

    background.paste(img, (185,200), img)
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("App_data/Roboto-Regular.ttf", 18)

    x1 = int(185)
    x2 = int(185)
    y1  = int(1100 * 0.5)
    y2  = int(1150 * 0.5)

    draw.text((x1-1,y1-1), name, fill="white", font=font)
    draw.text((x1+1,y1-1), name, fill="white", font=font)
    draw.text((x1-1,y1+1), name, fill="white", font=font)
    draw.text((x1+1,y1+1), name, fill="white", font=font)

    draw.text((x2-1,y2-1), nim, fill="white", font=font)
    draw.text((x2+1,y2-1), nim, fill="white", font=font)
    draw.text((x2-1,y2+1), nim, fill="white", font=font)
    draw.text((x2+1,y2+1), nim, fill="white", font=font)

    draw.text((x1,y1), name, fill="black", font=font)
    draw.text((x2,y2), nim, fill="black", font=font)

    return background

images = editphoto("13517071", "ultahoktober.png", "MARSA")

images[0].show()
