import logging
import telegram
from flask import Flask, request
from telegram.ext import Updater

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
    print("Update.callback_query: " + str(update.callback_query))

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

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
    name = msg[1]
    x = msg[2]

    message = name + " " + x
    return message


def message_day(update):
    return "Message of the day shown here."


def get_response(msg, update):
    msg_list = msg.split(' ')

    if msg == "/start":
        return start_info(update)
    elif msg == "/message":
        return message_day(update)
    elif msg_list[0] == "/guess":
        return guess(update, msg_list)
    else:
        return "Such a command doesn't exist."
