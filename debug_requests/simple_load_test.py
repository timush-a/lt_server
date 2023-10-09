import json
import aiohttp


async def send_request(url: str, body: dict):
    async with aiohttp.ClientSession() as session:
        response = await session.post(url, data=json.dumps(body))
        body = await response.json()
        await asyncio.sleep(1)
        return response.status, body


if __name__ == "__main__":
    import asyncio
    from time_request import req_body
    URL = 'http://0.0.0.0:8000/android_stress_test/add_result'
    tasks = list()
    for _ in range(1):
        req_body['version'] = str(_)
        tasks.append(send_request(URL, req_body))

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(asyncio.gather(*tasks))
    http_error_codes = [a[0] for a in result if a is not None]
    print(f"OK {len([_ for _ in http_error_codes if _ == 200])}")
    print(f"ERROR {len([_ for _ in http_error_codes if _ == 409])}")
