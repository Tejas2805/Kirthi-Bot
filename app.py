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


messages = { "02": "ok",
             "03": "ok23",
             "04": "04",
             "05": "ok",
             "06": "ok23",
             "07": "04",
             "08": "ok",
             "09": "ok23",
             "10": "04",
             "11": "ok",
             "12": "ok23",
             "13": "04",
             "14": "ok",
             "15": "ok23",
             "16": "04",
             "17": "ok",
             "18": "ok23",
             "19": "04",
             "20": "ok",
             "21": "ok23",
             "22": "04",
             "23": "ok",
             "24": "final" }

guesses = { "02": { "name": "Rutwick", "x": "GUESSED" },
            "03": { "name": "Rutwick", "x": "GUESSED" },
            "04": { "name": "Rutwick", "x": "GUESSED" },
            "05": { "name": "Rutwick", "x": "GUESSED" },
            "06": { "name": "Rutwick", "x": "GUESSED" },
            "07": { "name": "Rutwick", "x": "GUESSED" },
            "08": { "name": "Rutwick", "x": "GUESSED" },
            "09": { "name": "Rutwick", "x": "GUESSED" },
            "10": { "name": "Rutwick", "x": "GUESSED" },
            "11": { "name": "Rutwick", "x": "GUESSED" },
            "12": { "name": "Rutwick", "x": "GUESSED" },
            "13": { "name": "Rutwick", "x": "GUESSED" },
            "14": { "name": "Rutwick", "x": "GUESSED" },
            "15": { "name": "Rutwick", "x": "GUESSED" },
            "16": { "name": "Rutwick", "x": "GUESSED" },
            "17": { "name": "Rutwick", "x": "GUESSED" },
            "18": { "name": "Rutwick", "x": "GUESSED" },
            "19": { "name": "Rutwick", "x": "GUESSED" },
            "20": { "name": "Rutwick", "x": "GUESSED" },
            "21": { "name": "Rutwick", "x": "GUESSED" },
            "22": { "name": "Rutwick", "x": "GUESSED" },
            "23": { "name": "Rutwick", "x": "GUESSED" },
            "24": { "name": "Rutwick", "x": "GUESSED" },
            }


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    updater = Updater('1689944976:AAGJyxSIFGkXehTNjO0YB8ylwY6K3qO9fLQ')  # API key
    dp = updater.dispatcher

    print("Update: " + str(update))

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    #text = update.message.text.encode('utf-8').decode()
    text = update.message.text
    print(update.message.text)
    print()
    print("got text message :", text)

    if text == "None":
        print("NONE RECEIVED")
        response = get_response("Validation", update)
    else:
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
    user_first_name = update.message.from_user.first_name
    print(update)
    message = "Hi {} !\n\n".format(user_first_name)
    if update.message.chat.username == "kirthi099":
        return "Hi Kirthi!\n\n Welcome to your birthday countdown tracker! You can access today's message using /message."
    every_message = message + "This is a countdown tracker for Kirthi's birthday. \n\n"
    every_message = every_message + "You can access today's message using /message ."

    return every_message

def guess(update, msg):
    if len(msg) != 3:
        return "Enter 2 things: Name and X with the guess command."
    name = msg[1]
    x = msg[2]
    today = datetime.now()
    pacific_tzinfo = pytz.timezone("Asia/Singapore")
    pacific_time = today.astimezone(pacific_tzinfo)
    d1 = pacific_time.strftime("%d/%m/%Y %H:%M:%S")
    d1 = d1.split("/")

    if guesses[d1[0]]["name"] == name and guesses[d1[0]]["x"] == x:
        return "Hurray! It's correct."
    return "Wrong answer!"


def message_day(update):
    today = datetime.now()
    pacific_tzinfo = pytz.timezone("Asia/Singapore")
    pacific_time = today.astimezone(pacific_tzinfo)
    d1 = pacific_time.strftime("%d/%m/%Y %H:%M:%S")
    d1 = d1.split("/")
    message = messages[d1[0]]
    return message


def get_response(msg, update):
    msg_list = msg.split(' ')

    if msg == "/start":
        return start_info(update)
    elif msg == "/message":
        return message_day(update)
    elif msg == "Validation":
        return "Successfully validated"
    elif msg_list[0] == "/guess":
        return guess(update, msg_list)
    else:
        return "Such a command doesn't exist."
