from helpers.exception import AwbBotException

RESPONSE_OK_CODE = 200
RESPONSE_INTERNAL_SERVER_ERROR = 500


def build_response(content, code=200):
    if code == RESPONSE_OK_CODE:
        return {
            'code': code,
            'body': content
        }
    raise AwbBotException(
        code=code,
        content=content
    )
