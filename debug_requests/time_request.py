req_body = {
    "runConfig":
        {
            "scenario":
                [
                    "DETECTOR_640_V2",
                    "QA_V3",
                    "DESCRIPTOR_LARGE_V4",
                    "LIVENESS_LARGE_V4"
                ],
            "threadCount": 0,
            "imageResolution": "1280x720",
            "timeConfiguration":
                {
                    "testingTime": 60,
                    "standbyTime": 0,
                    "repeatCnt": 3
                }
        },
    "bioSdkExecutionTimes":
        [
            {"percentile95": 7109, "percentile50": 6967, "mean": 7106},
            {"percentile95": 6984, "percentile50": 6961, "mean": 6972},
            {"percentile95": 6988, "percentile50": 6954, "mean": 6960}],
    "batteryTemperatures":
        [
            {"percentile95": 0, "percentile50": 0, "mean": 0},
            {"percentile95": 0, "percentile50": 0, "mean": 0},
            {"percentile95": 0, "percentile50": 0, "mean": 0}],
    "cpuTemperatures":
        [
            {"percentile95": 0, "percentile50": 0, "mean": 0},
            {"percentile95": 0, "percentile50": 0, "mean": 0},
            {"percentile95": 0, "percentile50": 0, "mean": 0}
        ],
    "availableMbMemory":
        [
            {"percentile95": 313, "percentile50": 182, "mean": 316},
            {"percentile95": 189, "percentile50": 187, "mean": 186},
            {"percentile95": 189, "percentile50": 188, "mean": 188}
        ],
    "availableMemoryPercentages":
        [
            {"percentile95": 16, "percentile50": 9, "mean": 16},
            {"percentile95": 10, "percentile50": 10, "mean": 9},
            {"percentile95": 10, "percentile50": 10, "mean": 10}
        ],
    "deviceInfo":
        {
            "deviceModel": "P12",
            "coreNumbers": 4,
            "memoryThreshold": 226492416
        },
    "version": "1.12"
}


if __name__ == "__main__":
    import requests
    from pprint import pprint
    from time import perf_counter
    URL = 'http://0.0.0.0:8000/android_stress_test/add_result'
    start = perf_counter()
    response = requests.post(URL, json=req_body)
    print(f"Elapsed time >>> {round((perf_counter() - start) * 1000, 2)} ms")
    pprint(response.text)
