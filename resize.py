import os
from PIL import Image

def compress_images(directory=False, quality=30):
    # 1. If there is a directory then change into it, else perform the next operations inside of the 
    # current working directory:
    if directory:
        os.chdir(directory)

    # 2. Extract all of the .png and .jpeg files:
    files = os.listdir()

    # 3. Extract all of the images:
    images = [file for file in files if file.endswith(('JPG', 'PNG'))]

    # 4. Loop over every image:
    for image in images:

        # 5. Open every image:
        img = Image.open(image)

        # 5. Compress every image and save it with a new name:
        img.save("BOTRDY_"+image, optimize=True, quality=quality)

        print("Done ", image)

def clearstatic():
    os.chdir("static")

    files = os.listdir()

    images = [file for file in files if file.endswith(('JPG', 'PNG'))]

    for image in images:
        print("Removed : ", image.path)
        os.remove(image.path)