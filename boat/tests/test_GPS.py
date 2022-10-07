from sensors.util import TimeoutException
from sensors import GPS, GPSNoSignal
from datetime import datetime, timezone

import pytest
import types

def test_timeout_for_gps_taking_too_long(monkeypatch):
    def mock_gps_get_data_forever(self):
        while True:
            pass
    monkeypatch.setattr(GPS, "priv_get_GPS_data", mock_gps_get_data_forever)

    with pytest.raises(TimeoutException) as e_info:
        GPS().poll_sensor()

def test_gps_date_time_parse(monkeypatch):
    def mock_gps_get_gps_data_return_time(self):
        data = types.SimpleNamespace()
        data.year = 2022
        data.month = 2
        data.day = 8
        data.hour = 16
        data.min = 34
        data.sec = 25

        data.lon = 0
        data.lat = 0
        data.headMot = 0
        data.numSV = 1 # So it is seen as "valid"
        data.gSpeed = 0
        data.sAcc = 0
        data.hAcc = 0
        data.headAcc = 0
        return data

    monkeypatch.setattr(GPS, "priv_get_GPS_data", mock_gps_get_gps_data_return_time)

    expected_date_time = datetime(2022, 2, 8, 16, 34, 25, tzinfo=timezone.utc)

    assert GPS().poll_sensor()["current_time_utc"] == expected_date_time

def test_gps_no_signal(monkeypatch):
    def mock_gps_get_gps_data_return_no_sat(self):
        data = types.SimpleNamespace()
        data.numSV = 0 # So it is seen as "invalid"

        # Just random data to appease datetime()
        data.year = 2000
        data.month = 1
        data.day = 1
        data.hour = 1
        data.min = 1
        data.sec = 1
        data.lon = 0
        data.lat = 0
        data.headMot = 0
        data.gSpeed = 0
        data.sAcc = 0
        data.hAcc = 0
        data.headAcc = 0
        return data

    monkeypatch.setattr(GPS, "priv_get_GPS_data", mock_gps_get_gps_data_return_no_sat)

    with pytest.raises(GPSNoSignal) as e_info:
            GPS().poll_sensor()