from sensors.util import TimeoutException
from sensors import GPS, GPSNoSignal
from datetime import datetime, timezone

import pytest
import types

@pytest.mark.slow
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

    assert GPS().poll_sensor().current_time_utc == expected_date_time

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

def test_gps_other_data(monkeypatch):
    def mock_gps_get_gps_data_other_data(self):
        data = types.SimpleNamespace()
        data.lon = 123.12932
        data.lat = 456.21954
        data.headMot = 29.2384
        data.numSV = 15
        data.gSpeed = 2382
        data.sAcc = 152
        data.hAcc = 325
        data.headAcc = 452

        # Just random data to appease datetime()
        data.year = 2000
        data.month = 1
        data.day = 1
        data.hour = 1
        data.min = 1
        data.sec = 1

        return data

    monkeypatch.setattr(GPS, "priv_get_GPS_data", mock_gps_get_gps_data_other_data)

    gps_data =  GPS().poll_sensor();

    assert gps_data.lon     == 123.12932
    assert gps_data.lat     == 456.21954
    assert gps_data.headMot == 29.2384
    assert gps_data.numSV   == 15
    assert gps_data.gSpeed  == 2382
    assert gps_data.sAcc    == 152
    assert gps_data.hAcc    == 325
    assert gps_data.headAcc == 452

def test_value_error(monkeypatch):
    def mock_gps_value_error(self):
        raise ValueError()
    
    monkeypatch.setattr(GPS, "priv_get_GPS_data", mock_gps_value_error)

    with pytest.raises(ValueError) as e_info:
        GPS().poll_sensor()

def test_io_error(monkeypatch):
    def mock_gps_io_error(self):
        raise IOError()
    
    monkeypatch.setattr(GPS, "priv_get_GPS_data", mock_gps_io_error)

    with pytest.raises(IOError) as e_info:
        GPS().poll_sensor()