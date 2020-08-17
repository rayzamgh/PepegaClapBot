from flask import Flask, request, abort

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

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)