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
                "iterations": 10
        },
    "bioSdkExecutionTimes":
        [
            {"percentile95": 7055, "percentile50": 6917, "mean": 6951}
        ],
    "batteryTemperatures":
        [
            {"percentile95": 0, "percentile50": 0, "mean": 0}
        ],
    "cpuTemperatures":
        [
            {"percentile95": 0, "percentile50": 0, "mean": 0}
        ],
    "availableMbMemory":
        [
            {"percentile95": 198, "percentile50": 196, "mean": 209}
        ],
    "availableMemoryPercentages":
        [
            {"percentile95": 10, "percentile50": 10, "mean": 10}
        ],
    "deviceInfo":
        {"deviceModel": "P12", "coreNumbers": 4, "memoryThreshold": 226492416},
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
