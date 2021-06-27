import os


class EnvironmentService:

    @staticmethod
    def get_bot_token():
        return os.environ.get('bot_token')
