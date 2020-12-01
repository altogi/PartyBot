# ------------------------------------------------------------------------------------------
# This app establishes a Python Flask server which connects to a Telegram Chatbot. 
# It receives messages sent to the Virtual DJ Chatbot
# It sends messages sent to the Virtual DJ Chatbot
# 
# Addtional tools needed:
#  - ngrok. Creates a open port on your laptop so that the web app is reachable from the internet
# 
# Steps:
# 0. Install ngrok
# 1. Open Flask port with ngrok ./ngrok http 5000
# 2. Paste ngrok HTTPS URL and assign it to Python variable URL
# 3. run "python3 app.py" to establish Flask server
# 3. Call [URL]/setwebhook to receive the messages that were sent to the Telegram 
# 4. Close webhook [URL]/deletewebhook (TBD)
# 
# 
# https://www.toptal.com/python/telegram-bot-tutorial-python
# https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html
# ------------------------------------------------------------------------------------------


from flask import Flask, request
import telegram
import requests

# token from telegram bot
TOKEN = '1474569647:AAH13gblvp4VBIhH3B9GeMBbuyFRdDprKr0'
# Flask url. Needs to be reachable via internet.  Tool ngrok is used for this
URL = 'https://b9511b8e6068.ngrok.io/'
bot = telegram.Bot(TOKEN)


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    return "Hello World!"


@app.route('/test', methods=['POST'])
def receive_message_test():
    return "In test!"


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    print("In set webhook")
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/deletewebhook', methods=['GET', 'POST'])
def kill_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.deleteWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook deleted ok"
    else:
        return "webhook deleted failed"


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)

   # SEND TEXT TO WATSON and get response
   # response = SendTextToWatson(text) # obviously dummy method

   # SEND RESPONSE TO TELEGRAM
   #bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id) # works

   # GET BE DELETED

   if "kids" in text:
       # print the the message
       message = "Group 8 for sure my lord"
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=message, reply_to_message_id=msg_id)
   else:
       message = "Could you repeat please?"
       bot.sendMessage(chat_id=chat_id, text=message, reply_to_message_id=msg_id)

   return 'ok'

if __name__ == '__main__':
    app.run()