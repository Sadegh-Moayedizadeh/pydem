import pytest


@pytest.fixture
def kaolinite_dict():
    di = {
        'type': 'kaolinite',
        'size_upper_bound': 3000,
        'size_lower_bound': 1000,
        'quantity': 100,
    }
    return di


@pytest.fixture
def quartz_dict():
    di = {
            'type': 'quartz',
            'size_upper_bound': 10000,
            'size_lower_bound': 8000,
            'quantity': 10,
    }
    return di

