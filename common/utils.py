import os
import json
import logging
import logging.handlers
from datetime import datetime


def set_up(config: dict):
    """
    If necessary, creates directories before launching
    :param config: app config
    :return:
    """
    for directory in config['save_path'], config['json_save_path'], config['csv_save_path']:
        if not os.path.exists(directory):
            os.mkdir(directory)


def get_logger(name='app', level=logging.INFO, filename: str = 'logs.txt') -> logging.Logger:
    """
    Create logger
    :param name: logger name
    :param level: default level
    :param filename: path to save logs
    :return:
    """
    logger = logging.Logger(name, level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.handlers.RotatingFileHandler(filename)
    file_handler.setFormatter(formatter)

    stream_handler.setLevel(level)
    file_handler.setLevel(level)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


def load_json(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def get_datetime():
    return datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
