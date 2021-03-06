import os
from PIL import Image

def compress_images(directory=False, quality=30):
    oldpath = os.getcwd()
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

    os.chdir(oldpath)

def delete_copy(directory=False, quality=30):
    oldpath = os.getcwd()
    # 1. If there is a directory then change into it, else perform the next operations inside of the 
    # current working directory:
    if directory:
        os.chdir(directory)

    # 2. Extract all of the .png and .jpeg files:
    files = os.listdir()

    # 3. Extract all of the images:
    images4 = [file for file in files if file.endswith(('(4).JPG'))]
    images5 = [file for file in files if file.endswith(('(5).JPG'))]
    images6 = [file for file in files if file.endswith(('(6).JPG'))]
    images7 = [file for file in files if file.endswith(('(7).JPG'))]

    images = images4 + images5 + images6 + images7

    # 4. Loop over every image:
    for image in images:

        os.remove(image)

        print("Removed ", image)

    os.chdir(oldpath)

def clearstatic():
    print("STARTING STATIC FILE CLEANUP")

    os.chdir("static")

    files = os.listdir()

    images = [file for file in files if file.endswith(('JPG', 'PNG'))]

    print("FOUND NUMBER OF FILES TO CLEAR : " + str(len(images)))

    for image in images:
        print("Removed : ", image.path)
        os.remove(image.path)

    os.chdir("..")

def cleartmp(path):
    oldpath = os.getcwd()

    print("CURRENTLY IN : ", oldpath)

    os.chdir('static/tmp')

    print("STARTING TEMP FILE CLEANUP IN : ", os.getcwd())

    files = os.listdir()

    images = [file for file in files if (file.endswith(('JPG', 'PNG', 'jpg', 'png')) or file.startswith(('temporary')))]

    print("FOUND TEMP OF FILES TO CLEAR  : " + str(len(images)))
    print("FOUND TEMP OF FILES NON IMAGE : " + str(len(files)))

    for file in files:
        print("FILE: ", file)

    for image in images:
        print("Removed : ", image)
        os.remove(image)

    os.chdir("..")
    os.chdir("..")
