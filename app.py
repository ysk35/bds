from flask import Flask
from flask import request
import os
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

# generate instance
app = Flask(__name__)

# get environmental value from heroku
ACCESS_TOKEN = "g0sM8WGTf6pw+qNynFHG8A0w3es9+Xwb0dfYj7o60fok2+hSD2eqf4FmMIultNkOzU57RmkRQlRbzp6MZ2RLUuSR7dGGZ/qcfdJCO6meha31mPDaoj3ZS+Rok4/kd9QVuu14ut/ya6JrPAK8nIKFDwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "e5088dcddfd4d73a48b580ca70f23381"
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# endpoint
@app.route("/")
def test():
    return "<h1>It Works!</h1>"

# endpoint from linebot
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

# handle message from LINE
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text="test"))

if __name__ == "__main__":
  app.run()