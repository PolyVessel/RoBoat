from sensors.util import TimeoutException, time_limit
from time import sleep
import pytest

def takes_1_second():
    sleep(1)


def test_going_over_time_limit():
    with pytest.raises(TimeoutException) as e_info:
        with time_limit(0.5):
            takes_1_second()

def test_under_time_limit():
    try:
        with time_limit(5):
            takes_1_second()
        assert True
    except TimeoutException as e:
        assert False, "Time limit raised exception when it should not have"