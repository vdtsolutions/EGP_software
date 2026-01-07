from logging import *
from datetime import date
user_name = 'root'

def log__config():
    log_format = '{levelname} : Line no. {lineno} *** {name} *** {asctime} *** {message}'
    basicConfig(filename='./logs/log-' + str(date.today()) + '.log', level=DEBUG, filemode='a', format=log_format,
                style='{')

log__config()


def log_warning(msg):
    logger = getLogger(user_name)
    logger.warning(msg)

def log_critical(msg):
    logger = getLogger(user_name)
    logger.critical(msg)

def log_error(msg):
    logger = getLogger(user_name)
    logger.error(msg)

def log_info(msg):
    logger = getLogger(user_name)
    logger.info(msg)

def log_debug(msg):
    logger = getLogger(user_name)
    logger.debug(msg)
