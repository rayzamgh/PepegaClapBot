import os 
import pandas as pd  

arr = os.listdir()

#"16519039"

data = pd.read_csv("nim.csv") 
data.rename(columns={"NIM": "nimbaru", "NIM TPB": "nimlama"}, inplace = True)
print(data.head())

nimbaru = data['nimbaru'].tolist()
nimlama = data['nimlama'].tolist()

res = dict(zip(nimlama, nimbaru)) 

#print ("Resultant dictionary is : " +  str(res)) 

for x in arr:
    if (x.startswith('BOTRDY_16519')):
        curnim = int(x[7:15])
        print(curnim , " : ", res[curnim])

        if x.lower().endswith('.png'):
            print(x, "BOTRDY_" + str(res[curnim]) + '.png')
            os.rename(x, "BOTRDY_" + str(res[curnim]) + '.png')

        if x.lower().endswith('.jpg'):
            print(x, "BOTRDY_" + str(res[curnim]) + '.jpg')
            os.rename(x, "BOTRDY_" + str(res[curnim]) + '.jpg')
    