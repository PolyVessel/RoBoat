import os
from ublox_gps import UbloxGps
import serial
from datetime import datetime, timezone

# TODO: Will wait forever if no GPS is connected
class GPS:
    gps = None
    serial_port = None

    # Singleton Pattern (we only have 1 GPS module)
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GPS, cls).__new__(cls)
        return cls.instance

    def init(self):
        # Connect GPS module to GPS UART
        self.serial_port = serial.Serial('/dev/ttyS2', baudrate=9600, timeout=1, stopbits=serial.STOPBITS_ONE,
                                  parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)
        self.gps = UbloxGps(self.serial_port)

    def poll_sensor(self):
        """Polls the GPS for sensor data, initializing the GPS if needed.
        More data in https://cdn.sparkfun.com/assets/0/9/4/3/5/u-blox8-M8_ReceiverDescrProtSpec__UBX-13003221__Public.pdf

        Returns Dictionary:
          "lat"  -> Latitude in Deg
          "lon" -> Longitude in Deg
          "current_time_utc" -> Python datetime obj of current time in UTC
          "headMot" -> Heading of Motion in deg
          "numSV" -> Number of Satellites used in Solution,
          "gSpeed": Ground Speed in mm/s (2D)
          "sAcc": Speed Accuracy in mm/s
          "hAcc": Horizontal Accuracy in mm
          "headAcc": Accuracy of Heading in deg
        """


        # Init if not already
        if self.gps is None or self.serial_port is None:
            self.init()

        try:
            gps_data = self.gps.geo_coords()

            current_date_time = datetime(gps_data.year, gps_data.month, gps_data.day,
                                         hour=gps_data.hour, minute=gps_data.min, second=gps_data.sec,
                                         tzinfo=timezone.utc)

            ret_data = {
                "current_time_utc": current_date_time,
                "lon": gps_data.lon,
                "lat": gps_data.lat,
                "headMot": gps_data.headMot,
                "numSV": gps_data.numSV,
                "gSpeed": gps_data.gSpeed,
                "sAcc": gps_data.sAcc,
                "hAcc": gps_data.hAcc,
                "headAcc": gps_data.headAcc

            }
            return ret_data
        except (ValueError, IOError) as err:
            # TODO: Do a smarter log here
            print(err)
            return None

    #TODO: Requires root Privledges, add a check into main program that this is called as root
    def update_system_clock(self):
        """Accurate to ~1s, because GPS Library only gives precision
        up to seconds."""

        gps_data = self.poll_sensor()
        time_data = gps_data["current_time_utc"]

        # convert time_data to a form the date -u command will accept: "20140401 17:32:04"
        gps_utc = "{:04d}{:02d}{:02d} {:02d}:{:02d}:{:02d}".format(time_data.year, time_data.month, time_data.day, time_data.hour, time_data.minute, time_data.second)
        os.system('sudo date -u --set="{}"'.format(gps_utc))


    def __del__(self):
        """Closes serial port when done"""
        self.serial_port.close()


if __name__ == '__main__':
    print(GPS().poll_sensor())
