from sensors.util import TimeoutException
from sensors import GPS, TimeoutException
import pytest

def test_timeout_for_gps_taking_too_long(monkeypatch):
    def mock_gps_get_data_forever(self):
        while True:
            pass
    monkeypatch.setattr(GPS, "priv_get_GPS_data", mock_gps_get_data_forever)

    with pytest.raises(TimeoutException) as e_info:
        GPS().poll_sensor()