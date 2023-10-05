from logging import Logger
from aiohttp import web


class LTHandlers:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.routes = [
            web.post('/result', self.handler)
        ]

    async def parse_request(self, request_body: dict):
        try:
            config = request_body['runConfig']
            timings = request_body['bioSdkExecutionTimes']
            battery_temperature = request_body['batteryTemperatures']
            cpu_temperature = request_body['cpuTemperatures']
            available_ram = request_body['availableMbMemory']
            available_ram_percent = request_body['availableMemoryPercentages']
            device_info = request_body['deviceInfo']
            version = request_body['version']
        except KeyError as e:
            self.logger.exception(e)

    async def parse_test_run_config(self, test_run_config: dict):
        try:
            test_pipeline = sorted(test_run_config['scenario'])
            threads_count = test_run_config['threadCount']
            image_size = test_run_config['imageResolution']
            if test_run_config.get('iterations'):
                iterations = test_run_config['iterations']
            else:
                time_config = test_run_config['timeConfiguration']
                test_time = time_config['testingTime']
                standy_time = time_config['standbyTime']
                repeat_count = time_config['repeatCnt']

        except KeyError as e:
            self.logger.exception(e)

    async def handler(self, request: web.Request) -> web.Response:
        return web.Response(status=200, body={"Error": "OK"})
