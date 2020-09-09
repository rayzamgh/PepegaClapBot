import pandas as pd
import pytz 
import json 
import img
import logging
import threading
import time
import os
from app import staticurl
from datetime import datetime
from pandas import Timestamp
from linebot.models import (
    TextSendMessage, ImageSendMessage
)
def initdf():
    dateparse = lambda x: datetime.strptime(x.replace(" AM", ""), '%m/%d/%Y %H:%M')

    df = pd.read_csv("App_data/ultahall.csv",parse_dates=['DTSTART', 'DTEND'], date_parser=dateparse)

    df.drop(['DUE', 'DTEND', 'ATTENDEE','LOCATION','PRIORITY','URL','CALENDAR','UID','ORGANIZER','DURATION'], axis=1, inplace=True)

    df.rename(columns={"SUMMARY": "NIM", "DTSTART": "DATE", "NOTES": "NAME"}, inplace=True)

    return df

def getultahwho(df):
    datenow = datetime.today()

    listultah = []

    for _, row in df.iterrows():
        curDate = Timestamp.to_pydatetime((row["DATE"]))
        if (curDate.date() == datenow.date()):
            listultah.append([row["NAME"], row["NIM"]])

    return listultah

def getultahcustom(df, customdate):

    listultah = []

    for _, row in df.iterrows():
        curDate = Timestamp.to_pydatetime((row["DATE"]))
        if (curDate.date() == customdate.date()):
            listultah.append([row["NAME"], row["NIM"]])

    return listultah

def getbandunghourtime():
    IST = pytz.timezone('Asia/Bangkok') 
    pog = datetime.now(IST)
    return(pog.hour)

def getbandungdate():
    IST = pytz.timezone('Asia/Bangkok') 
    pog = datetime.now(IST)
    return(pog.date())

def thread_jamsepuluh(line_bot_api, persistentdf, delay):
    while True:
        if((getbandunghourtime() == 22) or (getbandunghourtime() == 11)):
            
            to = "C8e5b62fcae0399f19a31367fb32bded2"

            datetext = getbandungdate().strftime('%Y-%m-%d')

            dateparsed = datetime.strptime(datetext, '%Y-%m-%d')

            listultah = getultahcustom(persistentdf, dateparsed)
                
            if len(listultah) > 0:

                ultahtext = "Buat tanggal " + datetext + " yang ulang tahun adalah :\n\n"

                for x in listultah:
                    name = x[0]
                    nim  = str(x[1])

                    ultahtext = ultahtext + name + "nim " + nim + "\n\n"

                    images = img.editphoto(nim, "ultahseptember.png", name)

                    imagenamelist = []

                    for key, image in enumerate(images):
                        imagename = nim + str(key) + ".PNG"
                        imagenamelist.append(imagename)
                        
                        if os.path.exists("static/" + imagename):
                            os.remove("static/" + imagename)
                        
                        image.save("static/" + imagename,"PNG")

                    for sends in imagenamelist:
                        line_bot_api.push_message(
                            to,
                            ImageSendMessage(staticurl + sends, staticurl + sends)
                        )


            else:

                ultahtext = "Tidak ada yang ultah di tanggal " + datetext

            ultahtext = ultahtext + ", callbythread"

            line_bot_api.push_message(to, TextSendMessage(text=ultahtext))
        else:
            print("the hour is :" + str(getbandunghourtime()))
        time.sleep(delay)
