import os
import csv
import json
import logging
from typing import List, Tuple, Union
from . utils import load_json, get_datetime
from . test_types import TestType, TestRunResult, TestRunTimeConfig, TestRunIteraionsConfig


class SaveException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class SaveResult:
    def __init__(self, logger: logging.Logger, json_save_path: str, csv_save_path: str):
        self.logger = logger
        self.json_save_path = json_save_path
        self.csv_save_path = csv_save_path

    def save_result_json(self, run_cfg: Union[TestRunTimeConfig, TestRunIteraionsConfig],
                         test_result: TestRunResult) -> None:
        try:
            filename = f"{get_test_filename(run_cfg)}.json"
            file_path = os.path.join(self.json_save_path, filename)
            if not os.path.exists(file_path):
                data = {}
            else:
                data = load_json(file_path)
            device_model, sdk_version, measurements = self.get_json_data_to_write(test_result)
            self._update_test_type_results(data, device_model, sdk_version, result=measurements)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.exception(e)
            raise SaveException("Error saving the json file")

    def save_result_csv(self, run_cfg: Union[TestRunIteraionsConfig, TestRunTimeConfig],
                        test_result: TestRunResult) -> None:
        try:
            filename = get_test_filename(run_cfg)
            measurements = (
                (test_result.timings, 'Time (ms)'),
                (test_result.battery_temperature, 'Battery temp.'),
                (test_result.cpu_temperature, 'CPU temp.'),
                (test_result.available_ram, 'Free RAM'),
                (test_result.available_ram_percent, 'Free RAM %')
            )
            file_path = os.path.join(self.csv_save_path, f"{get_datetime()}__{filename}")
            self._write_to_csv(file_path, measurements)

        except Exception as e:
            self.logger.exception(e)
            raise SaveException("Error saving the csv file")

    @staticmethod
    def _write_to_csv(filename: str, measurements: Tuple) -> None:
        with open(f'{filename}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Item', 'Mean', 'Percentile 50', 'Percentile 95'])
            for data, item in measurements:
                if len(data) == 1:
                    writer.writerow([item, data[0]['mean'], data[0]['percentile50'], data[0]['percentile95']])
                else:
                    for number, _ in enumerate(data, start=1):
                        writer.writerow(
                            [f"{number} run. {item}", _['mean'], _['percentile50'], _['percentile95']]
                        )

    def _update_test_type_results(self, dictionary: dict, *keys: Union[str, int, tuple], result: dict) -> None:
        try:
            for key in keys:
                if key == keys[-1]:
                    dictionary[key] = result
                if not dictionary.get(key):
                    dictionary[key] = dict()
                    dictionary = dictionary[key]
                else:
                    dictionary = dictionary[key]
        except Exception as e:
            self.logger.exception(e)
            raise SaveException("Error updating test results")

    @staticmethod
    def get_json_data_to_write(test_result: TestRunResult) -> Tuple[str, str, dict]:
        data = (
            test_result.device_model,
            test_result.version,
            {
                'time': test_result.timings,
                'battery_temp': test_result.battery_temperature,
                'cpu_temp': test_result.cpu_temperature,
                'free_ram': test_result.available_ram,
                'free_ram_percent': test_result.available_ram_percent
            }
        )
        return data


def get_test_filename(run_cfg: Union[TestRunIteraionsConfig, TestRunTimeConfig]):
    if run_cfg.test_type == TestType.TIME:
        return f"time_{run_cfg.test_time}__standby_{run_cfg.standy_time}" \
               f"__repeats_{run_cfg.repeat_count}__{'__'.join(sorted(run_cfg.test_pipeline))}" \
               f"__threads_{run_cfg.threads_count}__resolution_{run_cfg.image_size}"
    if run_cfg.test_type == TestType.ITERAIONS:
        return f"iterations_{run_cfg.iterations}__{'__'.join(sorted(run_cfg.test_pipeline))}" \
               f"__threads_{run_cfg.threads_count}__resolution_{run_cfg.image_size}"
    else:
        raise SaveException('Invalid test type')


def get_filenames(dir_path: str) -> List[str]:
    return [os.path.join(dir_path, filename) for filename in os.listdir(dir_path)]
