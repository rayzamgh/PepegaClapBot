import pandas
import requests
import ultah
import logging
import json 
import threading
import img
import resize
import tempfile
import os
from flask import Flask, request, abort
from requests.exceptions import HTTPError
from datetime import datetime

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, ImageMessage, TextMessage, TextSendMessage, DatetimePickerAction, 
    URIAction, ImageCarouselTemplate, ImageCarouselColumn, TemplateSendMessage,
    ImageSendMessage
)

staticurl = "https://pepegaclapbot.herokuapp.com/static/"
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

persistentdf = None

app = Flask(__name__)

line_bot_api = LineBotApi('/7Qy6IMQIXP7XiWH0yFZNaK8RPIx65oDz46hB/DMXjzmD/ONHKGgjYLmiEzLkbF7cLZTb7amrwwOzb6eLfcHYI25WwCVMYo/O74PWsrFtcbhykPW3rDRucDJU/A1dKy7lrWkoEylczCdqVrMPAsuwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6e865f08a26dba52f7c7c6b719a8290e')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    content = request.get_json()
    app.logger.info("Request body: " + body)
    print("Request content: " + json.dumps(content))

    # handle webhook body
    try:
        
        handler.handle(body, signature)
        
        curevent = content["events"][0]
        if curevent["type"] == "postback":
            to = getcallerid(curevent)

            #UPCOMING FEATURE
            #profile = line_bot_api.get_profile(to)

            datetext = curevent["postback"]["params"]["date"]

            dateparsed = datetime.strptime(datetext, '%Y-%m-%d')

            listultah = ultah.getultahcustom(persistentdf, dateparsed)
            
            if len(listultah) > 0:

                ultahtext = "Buat tanggal " + datetext + " yang ulang tahun adalah :\n\n"

                for x in listultah:
                    name = x[0]
                    nim  = x[1]

                    ultahtext = ultahtext + name + " nim " + str(nim) + "\n\n"
            else:

                ultahtext = "Tidak ada yang ultah di tanggal " + datetext
                
            line_bot_api.push_message(to, TextSendMessage(text=ultahtext))

    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=(ImageMessage))
def handle_content_message(event):

    print("CWD B4", os.getcwd())
    resize.cleartmp(static_tmp_path)
    print("CWD AFTER", os.getcwd())
    
    print("EVENT")
    print(event.message)
    print(event.message.type)
    print(event.message.id)

    temporary_image = event.message.id
    print("ImageID")
    print(temporary_image)
    message_content = line_bot_api.get_message_content(temporary_image)

    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    else:
        return

    # with open("static/" + "tempimg", 'wb') as fd:
    #     for chunk in message_content.iter_content():
    #         fd.write(chunk)
    #     tempfile_path = staticurl + "tempimg"
    #     print("PATHING", tempfile_path)
    # return

    print("STATIC TEMP")
    print(static_tmp_path)

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])

@handler.add(MessageEvent, message=(TextMessage))
def handle_message(event):

    print("CURRENT CWD", os.getcwd())

    TwitchList = [" Clap ", " KekW ", " Pog ", " Poggies ", " Pogu ", " Sadge ", " SadKek ", " WeirdChamp "]

    if event.message.type == "text":
        msg_from_user = event.message.text
        
        key = msg_from_user[:4]
        command = msg_from_user[5:]

        if len(msg_from_user) < 5:
            return

    ultahtext = ""

    if key == "!pog":
        if command[:6] == "editme":
            
            inpCommand = command.split('/')

            nim = inpCommand[1]
            name = inpCommand[2]

            image = img.editphotomanual(nim, "ultahoktober.png", name, "/tmp")
            
            image.save("static/" + "temporary","PNG")

            line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(staticurl + "temporary", staticurl + "temporary")
                )

        if command == "siapa ulang tahun hari ini":
            ultahtoday = ultah.getultahwho(persistentdf)

            ultahtext = "Selamat ulang tahun buat :\n\n"

            for x in ultahtoday:
                name = x[0]
                nim  = x[1]

                ultahtext = ultahtext + name + "nim " + str(nim) + "\n\n"

            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ultahtext))

        elif command[:7] == 'memepls':
            try:
                response = requests.get('https://meme-api.herokuapp.com/gimme/' + command[8:])
                response.raise_for_status()
                # access JSOn content
                jsonResponse = response.json()

                print("GOJALI")
                print(jsonResponse)
                print(jsonResponse["url"])

                if not(jsonResponse["nsfw"]):
                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(jsonResponse["url"], jsonResponse["url"])
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                    TextSendMessage(text="No porn >:("))

            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')

        elif command == 'pilih tanggal':
            image_carousel_template = ImageCarouselTemplate(columns=[
                ImageCarouselColumn(image_url='https://images.whooshkaa.com/podcasts/podcast_3271/podcast_media/9f1773-pad-logo.jpg',
                                    action=DatetimePickerAction(label='Date Pick',
                                                                data='date_postback',
                                                                mode='date'))
            ])

            template_message = TemplateSendMessage(
                alt_text='Pilih tanggal!', template=image_carousel_template)
            line_bot_api.reply_message(event.reply_token, template_message)
        
        elif command[:7] == 'editpls':

            carouselColumns = []
            alt_text = "Link buat yang gk bisa liat :\n"

            ultahtoday = ultah.getultahwho(persistentdf)

            for x in ultahtoday:
                name = x[0]
                nim  = str(x[1])

                images = img.editphoto(nim, "ultahoktober.png", name)

                imagenamelist = []

                for key, image in enumerate(images):
                    if key < 3:
                        imagename = nim + str(key) + ".PNG"
                        print("IMAGE CREATED : " + imagename)
                        imagenamelist.append(imagename)    
                        
                        if os.path.exists("static/" + imagename):
                            os.remove("static/" + imagename)            
                        
                        image.save("static/" + imagename,"PNG")

                print("IMAGE SENT : ", len(imagenamelist))

                for sends in imagenamelist:
                    alt_text += staticurl + sends + "\n"
                    carouselColumns.append(ImageCarouselColumn(image_url=staticurl + sends, action=URIAction(
                            label='Click Me!',
                            uri=staticurl + sends
                        )))

            template_message = TemplateSendMessage(alt_text=alt_text, template=ImageCarouselTemplate(columns=carouselColumns))

            line_bot_api.reply_message(event.reply_token, template_message)
    else:
        for subs in TwitchList:
            if (msg_from_user.find(subs) != -1):

                imagename = staticurl + "twitch/"+ subs.strip() + ".png"

                print("sending : ", imagename)

                line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(imagename, imagename)
                )

                break

                




def getcallerid(curevent):
    source = curevent["source"]
    if source["type"] == "user":
        return source["userId"]
    elif source["type"] == "group":
        return source["groupId"]
    elif source["type"] == "room":
        return source["roomId"]

def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    persistentdf = ultah.initdf()

    resize.clearstatic()

    seconddelay = 3600

    make_static_tmp_dir()

    threadwebhook = threading.Thread(target=ultah.thread_jamsepuluh,args=(line_bot_api,persistentdf,seconddelay))

    threadwebhook.start()
    
    app.run(host='0.0.0.0', port=port)
