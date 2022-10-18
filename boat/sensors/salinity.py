# Driver class for the salinity sensor
# datasheet can be found here https://atlas-scientific.com/files/EC_EZO_Datasheet.pdf


from msilib.schema import SelfReg
import serial

PORT = "/dev/ttyO2"
PROBE_TYPE = "1.0" #sensitivity of the probe being used.

class Salinity:

    serial_port = None
    last_reading = 0

    def __init__(self) -> None:
        try:
            self.serial_port = serial.Serial(port = PORT, baudrate=9600, 
                        timeout=1, stopbits=serial.STOPBITS_ONE, 
                        parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)

            self.serial_port.write(b"K," + PROBE_TYPE + "\r")

        except Exception as e:
            print("Error opening serial port")
            print(e)
            return
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Salinity, cls).__new__(cls)
        return cls.instance

    def __del__(self):
        """Closes serial port when done"""
        try:
            self.serial_port.close()
        except Exception as e:
            pass #Expected for Unit tests
    
    def poll_sensor(self):
        if self.serial_port is None:
            print("Serial port not initialized, sending 0")
            return 0
        waiting = self.serial_port.in_waiting()
        if waiting > 0:
            bytes = self.serial_port.read(waiting)
            all_data = bytes.decode("ascii")
            all_data.split("\r")
            #EC,TDS,SAL,SG (1 sec) <cr>
            self.last_reading = int(all_data[-1].split(",")[2])
        return self.last_reading
          
    # this routine should only be run when a new sensor is used.
    def calibrate(self):
        print("Calibrating salinity sensor...")
        input("make sensor dry and press enter")
        self.serial_port.write(bytes("Cal,dry\r", "ascii"))
        print(self.serial_port.readunitl(b"\r").decode("ascii"))
        input("put sensor into distilled water and press enter")
        self.serial_port.write(bytes("Cal,low,0\r", "ascii"))
        print(self.serial_port.readunitl(b"\r").decode("ascii"))
        ppm = input("put sensor into solution and enter ppm")
        self.serial_port.write(bytes("Cal,high," + ppm + "\r", "ascii"))
        print(self.serial_port.readunitl(b"\r").decode("ascii"))
        print("Calibration complete")


