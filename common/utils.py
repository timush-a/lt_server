import logging
import json


def get_logger(name='app', level=logging.INFO, filename: str = 'logs.txt'):
    # TODO
    return logging.Logger(name, level)


def load_config(config_path: str) -> dict:
    return json.load(open(config_path))
