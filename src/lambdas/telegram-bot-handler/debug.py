import os
import time

from handler import lambda_handler

from flask import Flask, request
import telebot

TOKEN = os.environ.get('bot_token')
bot = telebot.TeleBot(TOKEN)

WEBHOOK_URL = 'https://{HOST}.ngrok.io'  # for local development
TARGET_PORT = 80
# for setting a webhook to API Gateway
# WEBHOOK_URL = 'https://{IG_HOST}.execute-api.eu-central-1.amazonaws.com/prod/handler'

server = Flask(__name__)


@server.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        event = {'body': request.json}
        lambda_handler(event=event, context={})
        return '', 200
    return '', 500


if __name__ == '__main__':
    print('Removing webhook...')
    bot.remove_webhook()
    time.sleep(1)
    print('Setting webhook')
    bot.set_webhook(url=WEBHOOK_URL)
    print('Starting debug server')
    server.run(host="0.0.0.0",
               port=os.environ.get('PORT', TARGET_PORT),
               debug=True)
