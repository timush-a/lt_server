import json
import asyncio
from typing import Union
from logging import Logger
from concurrent.futures import ThreadPoolExecutor
from common.save_results import SaveResult, SaveException
from common.test_types import TestRunResult, TestRunIteraionsConfig, TestRunTimeConfig
from common.errors import JSON_ERROR, SAVE_ERROR, NO_ERROR
from aiohttp import web


class LTHandlers:
    # TODO
    #  Сохранять результаты в csv с датой в общюю директорию
    #  Возможность загружать последние файлы из этой директории
    #  Сохранение типов тестов в отдельный json
    #  Добавление новых результатов в этой json
    #  Получение на фронте возможности посмотреть типы тестов и выбрать девайсы и версии
    #  Сравнение результатов в виде графиков и csv
    def __init__(self, logger: Logger, config: dict):
        self.loop = None
        self.logger = logger
        self.save_result = SaveResult(logger, config['json_save_path'], config['csv_save_path'])
        self.pool = ThreadPoolExecutor(max_workers=int(config['max_workers']))
        base_route = '/android_stress_test'
        self.routes = [
            web.post(f'{base_route}/add_result', self.add_result),
            web.post(f'{base_route}/compare', self.compare),
            web.get(f'{base_route}/view_results', self.view),
            web.get(f'{base_route}/download_csv', self.compare)
        ]

    async def add_result(self, request: web.Request) -> web.Response:
        request_body = await request.json()
        try:
            run_config = self.get_run_config(request_body)
            result = self.get_test_run_result(request_body)
        except Exception as e:
            self.logger.exception(e)
            return self.compile_response(*JSON_ERROR)
        else:
            try:
                if not self.loop:
                    self.loop = asyncio.get_running_loop()
                await self.loop.run_in_executor(self.pool, self.save_result.save_result_csv, run_config, result)
                await self.loop.run_in_executor(self.pool, self.save_result.save_result_json, run_config, result)
            except SaveException as e:
                self.logger.exception(e)
                return self.compile_response(*SAVE_ERROR)
        return self.compile_response(*NO_ERROR)

    async def compare(self, request: web.Request) -> web.Response:
        pass

    async def view(self, request: web.Request) -> web.Response:
        pass

    async def download(self, request: web.Request) -> web.Response:
        pass

    @staticmethod
    def get_run_config(request_body: dict) -> Union[TestRunIteraionsConfig, TestRunTimeConfig]:
        run_config = request_body['runConfig']
        test_pipeline = sorted(run_config['scenario'])
        threads_count = run_config['threadCount']
        image_size = run_config['imageResolution']
        if run_config.get('iterations'):
            return TestRunIteraionsConfig(test_pipeline, threads_count, image_size, run_config['iterations'])
        if run_config.get('timeConfiguration'):
            time_config = run_config['timeConfiguration']
            test_time = time_config['testingTime']
            standy_time = time_config['standbyTime']
            repeat_count = time_config['repeatCnt']
            return TestRunTimeConfig(test_pipeline, threads_count, image_size, test_time, standy_time, repeat_count)
        else:
            raise Exception('Invalid test type')

    @staticmethod
    def get_test_run_result(request_body: dict) -> TestRunResult:
        return TestRunResult(
            timings=request_body['bioSdkExecutionTimes'],
            battery_temperature=request_body['batteryTemperatures'],
            cpu_temperature=request_body['cpuTemperatures'],
            available_ram=request_body['availableMbMemory'],
            available_ram_percent=request_body['availableMemoryPercentages'],
            device_model=request_body['deviceInfo']['deviceModel'],
            version=request_body['version']
        )

    @staticmethod
    def compile_response(status: int, body: dict) -> web.json_response:
        return web.json_response(body, status=status, dumps=json.dumps, content_type="application/json")
