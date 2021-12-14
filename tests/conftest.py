import numpy as np
import pytest

from generation.particles import Kaolinite, Quartz


@pytest.fixture
def kaolinite_dict():
    di = {
        "type": "kaolinite",
        "size_upper_bound": 3000,
        "size_lower_bound": 1000,
        "quantity": 100,
    }
    return di


@pytest.fixture
def quartz_dict():
    di = {
        "type": "quartz",
        "size_upper_bound": 10000,
        "size_lower_bound": 8000,
        "quantity": 10,
    }
    return di


@pytest.fixture
def base_kaolinite_particle():
    k = Kaolinite(
        x=50000, y=50000, length=2000, thickness=2, inclination=0, hierarchy=1
    )
    return k


@pytest.fixture
def base_quartz_particle():
    q = Quartz(x=80000, y=80000, length=9000, hierarchy=0)
    return q


@pytest.fixture
def intersecting_kaolinite_with_kaolinite():
    k = Kaolinite(
        x=50500,
        y=50500,
        length=2000,
        thickness=2,
        inclination=np.math.pi / 2,
        hierarchy=1,
    )
    return k


@pytest.fixture
def intersecting_kaolinite_with_quartz():
    k = Kaolinite(
        x=85000, y=80000, length=2000, thickness=2, inclination=0, hierarchy=1
    )
    return k


@pytest.fixture
def intersecting_quartz_with_quartz():
    q = Quartz(x=88500, y=80000, length=9000, hierarchy=0)
    return q
