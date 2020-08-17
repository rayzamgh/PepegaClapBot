import pandas as pd
from datetime import datetime
from pandas import Timestamp

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