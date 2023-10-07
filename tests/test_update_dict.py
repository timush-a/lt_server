import logging
from common.save_results import SaveResult
from pytest import fixture


@fixture(scope="function")
def sr():
    return SaveResult(logging.getLogger('t'), '', '')


def test_empty_dict(sr):
    d = dict()
    sr._update_test_type_results(d, 1, 2, 3, result={'c': 3})
    assert d == {1: {2: {3: {'c': 3}}}}


def test_update_dict(sr):
    d = {1: {2: {3: {'c': 3}}}}
    sr._update_test_type_results(d, 1, 2, 3, result={'b': 3})
    assert d == {1: {2: {3: {'b': 3}}}}


def test_add_new_kv(sr):
    d = {1: {2: {3: {'b': 3}}}}
    sr._update_test_type_results(d, 4, result={'b': 3})
    assert {1: {2: {3: {'b': 3}}}, 4: {'b': 3}}
