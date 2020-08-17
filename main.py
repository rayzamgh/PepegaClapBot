from flask import Flask, request, abort
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import numpy as np

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def generate_image(name, nim, background, img):
    img = Image.open(sys.argv[1]).convert("RGBA")
    background = Image.open(sys.argv[2])
    name = sys.argv[3]
    nim = sys.argv[4]

    size = (750,750)
    img = img.resize(size, Image.ANTIALIAS)

    background.paste(img, (150,200), img)
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("calibri.ttf", 37)

    x1 = 160
    x2 = 735
    y = 915

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

    background.save(nim + '.png', "PNG")

if __name__ == "__main__":
    app.run()

