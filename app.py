from flask import Flask
from flask import request
import os
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (FollowEvent, MessageEvent, TextMessage, TextSendMessage,)
from UserModel import User
from AttendanceModel import Attendance
from setting import session
import datetime

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
  messageText = event.message.text.split("\n")
  user = session.query(User).\
    filter(User.line_user_id == event.source.user_id).\
    first()
  if (not user.name and not user.student_number) or user.is_temporary == True:
    if user.is_confirm == False:
      if not messageText[1]:
        replyText = "2行で以下のような形式で回答してください\n例:\n1行目：74○○○○○\n2行目：理科大太郎"
      else:
        user.is_confirm = True
        user.student_number = messageText[0]
        user.name = messageText[1]
        user.is_temporary = True
        session.commit()
        replyText = "学籍番号：" + messageText[0] + "\n名前：" + messageText[1] + "\nでよろしいでしょうか？\n「はい」又は「いいえ」で答えてください"
    elif user.is_confirm == True:
      if event.message.text == "はい":
        user.is_temporary = False
        session.commit()
        replyText = "登録しました"
      elif event.message.text == "いいえ":
        replyText = "以下のような形式で送信してください\n例:\n1行目：74○○○○○\n2行目：理科大太郎"
        user.is_confirm = False
        user.student_number = None
        user.name = None
        session.commit()
      else:
        replyText = "「はい」又は「いいえ」で答えてください"
  else:
    if event.message.text == "出席":
      dt_now = datetime.datetime.now()
      dt_now_ar = dt_now.strftime('%Y/%m/%d')
      attendance = session.query(Attendance).\
        filter(Attendance.user_id == user.id, Attendance.date == dt_now_ar).\
        first()
      if not attendance:
        session.add(Attendance(user_id = user.id, name = user.name, date = dt_now_ar))
        session.commit()
        replyText = "出席登録が完了しました"
      else:
        replyText = "出席登録が完了しています"
    else:
      replyText = "出席登録以外の情報は送信しないでください"

  # print(event.message.text)
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=replyText))

@handler.add(FollowEvent)# FollowEventをimportするのを忘れずに！
def follow_message(event):# event: LineMessagingAPIで定義されるリクエストボディ
  if event.type == "follow":# フォロー時のみメッセージを送信
    line_bot_api.reply_message(
      event.reply_token,# イベントの応答に用いるトークン
      TextSendMessage(text="フォローありがとうございます！"))

  session.add(User(line_user_id = event.source.user_id, is_confirm = False))
  session.commit()

if __name__ == "__main__":
  app.run()