from enum import Enum
from dataclasses import dataclass
from typing import List


class TestType(Enum):
    ITERAIONS = 1
    TIME = 2


@dataclass
class TestRunResult:
    timings: List[dict]
    battery_temperature: List[dict]
    cpu_temperature: List[dict]
    available_ram: List[dict]
    available_ram_percent: List[dict]
    device_model: str
    version: str


@dataclass
class TestRunIteraionsConfig:
    test_type = TestType.ITERAIONS
    test_pipeline: List[str]
    threads_count: int
    image_size: str
    iterations: int


@dataclass
class TestRunTimeConfig:
    test_type = TestType.TIME
    test_pipeline: List[str]
    threads_count: int
    image_size: str
    test_time: int
    standy_time: int
    repeat_count: int
