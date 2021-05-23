import logging
import telegram
from flask import Flask, request
from telegram.ext import Updater
from datetime import datetime
import pytz

from credentials import bot_token, URL

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    updater = Updater('1689944976:AAGJyxSIFGkXehTNjO0YB8ylwY6K3qO9fLQ')  # API key
    dp = updater.dispatcher

    print("Update: " + str(update))

    text = update.message.text
    if text is None:
        print("NONE RECEIVED")
        response = get_response("Validation", update)
    else:
        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        #text = update.message.text.encode('utf-8').decode()
        text = update.message.text
        print(update.message.text)
        print()
        response = get_response(text, update)
    if response != "no_response":
        bot.sendMessage(chat_id=chat_id, text=response, parse_mode=telegram.ParseMode.MARKDOWN)
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)


def start_info(update):

    print(update)
    if update.message.chat.username == "Soumil99" or update.message.chat.username == "kirthi099" or update.message.chat.username == "tejas2805":
        return "Hello Kirthi Rachakonda! We have been expecting you.\n\nThe world is faced with a large threat and you are the only who can possibly save us. We just saw your mettle in the selection challenge and believe you are ready for this journey. During your journey your friends might be your comrade in arms or your enemy. But at the end of it, it will all be worth it.\n\nHope you are ready for the next challenge. Put the answer in the bot and get your next challenge.\n\nVenture On!"
    else:
        return "Sorry but you are not the chosen warrior."

def puzzle_answer(msg):
    if msg == "Friends become our chosen family.":
        return "This was just the start. There is still a long way to go. Hope you enjoyed your first challenge.\n\nNext challenge at 1:30 PM SGT / 11 AM IST."
    elif msg == "Varun":
        return "Looks like we made the right by selecting you. But are you ready for next challenge?.\n\nNext challenge at 5:00 PM SGT / 2:30 PM IST."
    elif msg == "blueflower":
        return "You just cracked another one. Keep it going.\n\nNext challenge at 9:00 PM SGT / 6:30 PM IST."
    elif msg == "22":
        return "You are almost there but now is the time for the toughest one ever. The world's faith depends on you.\n\nNext challenge at 11:30 PM SGT / 9 PM IST."
    else:
        return "That is not the answer. Please don't be cheeky. "


def get_response(msg, update):

    if msg == "/start":
        return start_info(update)
    elif msg == "/puzzle_answer":
        return puzzle_answer(msg)
    elif msg == "Validation":
        return "Successfully validated"
    else:
        return "Such a command doesn't exist."
