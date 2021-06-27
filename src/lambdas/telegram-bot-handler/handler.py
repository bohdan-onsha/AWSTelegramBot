import os

from telebot import TeleBot, types

from helpers.log_helper import get_logger
from services import ServiceProvider
from services.abstract_lambda import AbstractLambda
from services.environment_service import EnvironmentService

_LOG = get_logger('telegram-bot-handler')

token = os.environ.get('bot_token')

PARAM_UPDATE_ID = 'update_id'


class TelegramBotHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        if not event.get(PARAM_UPDATE_ID):
            return f'Invalid input, \'{PARAM_UPDATE_ID}\' param is missing.'

    def __init__(self, environment_service: EnvironmentService):
        self.environment_service = environment_service
        self.bot = TeleBot(token=token, threaded=False)

        @self.bot.message_handler(func=lambda msg: True)
        def reply(message):
            self.bot.reply_to(message=message, text=message.text)

    def handle_request(self, event, context):
        _LOG.info(f'Event: {event}')
        update = types.Update.de_json(event)
        _LOG.info(f'Updates to process: {update}')
        self.bot.process_new_updates([update])
        _LOG.info(f'Updates has been processed')


API_HANDLER = TelegramBotHandler(
    environment_service=ServiceProvider().environment_service())


def lambda_handler(event, context):
    return API_HANDLER.lambda_handler(event=event, context=context)
