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
from Chatbot import InterfaceWithTelegram
import telegram
import requests

# token from telegram bot
#TOKEN = '1474569647:AAH13gblvp4VBIhH3B9GeMBbuyFRdDprKr0'

#TELEGRAM BOT INFO:
TOKEN = '1447273538:AAHHUe6Tuga3PxCFjYByq3NuhcVt1VRkkNM'
username = 'virtual_dj_party_bot'
name = 'VirtualDJ'

# Flask url. Needs to be reachable via internet.  Tool ngrok is used for this
URL = 'https://f3506a76cd6b.ngrok.io/'
bot = telegram.Bot(TOKEN)

interface = InterfaceWithTelegram()

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    return "Hello World!"

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    try:
        s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
        return 'Webhook Set Correctly!'
    except:
        return 'Error Setting Webhook'

@app.route('/deletewebhook', methods=['GET', 'POST'])
def kill_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    try:
        s = bot.deleteWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
        return 'Webhook Deleted Correctly!'
    except:
        return 'Error Deleting Webhook'

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)
   chat_id = update.message.chat.id
   msg_id = update.message.message_id
   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()

   response = interface.process_text(text)

   # SEND RESPONSE TO TELEGRAM
   bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

   return 'ok'

if __name__ == '__main__':
    app.run()