from pip import main
import serial 


def main():
   ser = serial.Serial('/dev/tty0', baudrate=9600, timeout=1, stopbits=serial.STOPBITS_ONE)
   ser.write(0xC3C3C3)
   print(ser.read(8))

if __name__ == "__main__":
   main()