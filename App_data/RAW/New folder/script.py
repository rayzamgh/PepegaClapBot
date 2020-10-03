import os 

arr = os.listdir()

#"16519039"

for x in arr:
    if not(x.startswith('BOTRDY')):
        if x.lower().endswith('.png'):
            os.rename(x, "BOTRDY_" + x[:8] + '.png')

        if x.lower().endswith('.jpg'):
            os.rename(x, "BOTRDY_" + x[:8] + '.jpg')
    