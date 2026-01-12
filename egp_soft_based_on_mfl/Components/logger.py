from logging import *
from datetime import date
from pathlib import Path

user_name = 'root'

def log__config():
    log_dir = Path(r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\backend_data\logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"log-{date.today()}.log"
    log_format = '{levelname} : Line no. {lineno} *** {name} *** {asctime} *** {message}'

    basicConfig(
        filename=log_file,
        level=DEBUG,
        filemode='a',
        format=log_format,
        style='{'
    )

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
