from flask import Flask, request, abort
import pandas
import datetime
import ultah
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, DatetimePickerAction,
    ImageCarouselTemplate, ImageCarouselColumn, TemplateSendMessage
)

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
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_from_user = event.message.text
    
    if len(msg_from_user) < 5:
        return

    ultahtext = ""

    key = msg_from_user[:4]
    command = msg_from_user[5:]

    if key == "!pog":
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

        elif command == 'pilih tanggal':
            image_carousel_template = ImageCarouselTemplate(columns=[
                ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                    action=DatetimePickerAction(label='datetime',
                                                                data='datetime_postback',
                                                                mode='datetime')),
                ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                    action=DatetimePickerAction(label='date',
                                                                data='date_postback',
                                                                mode='date'))
            ])

            template_message = TemplateSendMessage(
                alt_text='ImageCarousel alt text', template=image_carousel_template)
            line_bot_api.reply_message(event.reply_token, template_message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    persistentdf = ultah.initdf()
    app.run(host='0.0.0.0', port=port)