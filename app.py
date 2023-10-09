import asyncio
import logging

from aiohttp import web
from argparse import ArgumentParser
from handlers import LTHandlers
from common.utils import get_logger, load_json, set_up


def get_cmd_args() -> str:
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=str, help='Config path')
    args = parser.parse_args()
    return args.config


def create_web_app(logger: logging.Logger, app_config: dict) -> web.Application:
    lt_handdlers = LTHandlers(logger, app_config)
    for route in lt_handdlers.routes:
        logger.info(f"App route {route.path}")
    web_app = web.Application()
    web_app.add_routes(lt_handdlers.routes)
    return web_app


if __name__ == "__main__":
    config_path = get_cmd_args()
    config = load_json(config_path)

    set_up(config)

    _logger = get_logger(filename=config['logs_path'], level=config['log_level'])
    app = create_web_app(_logger, config)

    web.run_app(app, host=config['host'], port=config['port'], access_log=None)
