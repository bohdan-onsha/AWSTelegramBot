import logging
import os
from sys import stdout

_name_to_level = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}

logger = logging.getLogger('aws-bot')
logger.propagate = False
console_handler = logging.StreamHandler(stream=stdout)
console_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
logger.addHandler(console_handler)

try:
    log_level = _name_to_level.get(os.environ['log_level'])
except KeyError as e:
    log_level = logging.DEBUG
logger.setLevel(log_level)
logging.captureWarnings(True)


def get_logger(log_name, level=log_level):
    """
    :param level:   CRITICAL = 50
                    ERROR = 40
                    WARNING = 30
                    INFO = 20
                    DEBUG = 10
                    NOTSET = 0
    :type log_name: str
    :type level: int
    """
    module_logger = logger.getChild(log_name)
    if level:
        module_logger.setLevel(level)
    return module_logger
