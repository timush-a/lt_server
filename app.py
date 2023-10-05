from aiohttp import web
from argparse import ArgumentParser
from handlers import LTHandlers
from common.utils import get_logger, load_config


def get_cmd_args():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=str, help='Config path')
    args = parser.parse_args()
    return args.config


def create_app(logger) -> web.Application:
    lt_handdlers = LTHandlers(logger)
    app = web.Application()
    app.add_routes(lt_handdlers.routes)
    return app


if __name__ == "__main__":
    config_path = get_cmd_args()
    config = load_config(config_path)
    _logger = get_logger(filename=config['logs_path'])
    app = create_app(_logger)
    web.run_app(app, host=config['host'], port=config['port'], access_log=None)
