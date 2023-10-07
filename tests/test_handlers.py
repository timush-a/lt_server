import asyncio
import logging
from json import dumps
from copy import deepcopy

from aiohttp.test_utils import make_mocked_request
from aiohttp import StreamReader, base_protocol
from pytest import fixture, mark

from handlers import LTHandlers
from common.utils import load_json
from debug_requests.time_request import req_body as time_req_body
from debug_requests.iterations_request import req_body as iter_req_body


def get_mocker_request(method: str, route: str, body: dict):
    loop = asyncio.get_event_loop()
    reader = StreamReader(base_protocol.BaseProtocol(loop=loop), 1024)
    reader.feed_data(dumps(body).encode())
    reader.feed_eof()
    return make_mocked_request(method, route, payload=reader)


@fixture(scope="class")
def get_handlers():
    return LTHandlers(logger=logging.getLogger('t'), config=load_json('../configs/base_config.json'))


class TestHandlers:
    # TODO
    #  check csv, json files
    #  check another test types
    #  check update data
    add_result_route = '/android_stress_test/add_result'

    @mark.asyncio
    async def test_add_result_invalid_run_config(self, get_handlers):
        req_body = {"runConfig": {"scenario": ["LIVENESS_LARGE_V4"], "threadCount": 0,
                                  "imageResolution": "1280x720", "iterations": 10}}
        request = get_mocker_request('POST', self.add_result_route, req_body)
        response = await get_handlers.add_result(request)
        assert response.status == 409
        assert response.body == dumps({"Error": "Json parse error"}).encode()

    @mark.asyncio
    async def test_add_result_invalid_result(self, get_handlers):
        req_body = deepcopy(time_req_body)
        del req_body['bioSdkExecutionTimes']
        request = get_mocker_request('POST', self.add_result_route, req_body)
        response = await get_handlers.add_result(request)
        assert response.status == 409
        assert response.body == dumps({"Error": "Json parse error"}).encode()

    @mark.asyncio
    async def test_add_result_save_error(self, get_handlers):
        req_body = deepcopy(time_req_body)
        del req_body['bioSdkExecutionTimes'][0]['percentile95']
        request = get_mocker_request('POST', self.add_result_route, req_body)
        response = await get_handlers.add_result(request)
        assert response.status == 409
        assert response.body == dumps({"Error": "Json parse error"}).encode()
