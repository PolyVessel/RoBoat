from sensors.util import time_limit, TimeoutException
from sensors.GPS import GPS
import os

def is_root():
    return os.geteuid() == 0

if __name__ == '__main__':
    # Requires root for setting time
    if not is_root():
        print("Please run as root")
        exit()

    GPS().update_system_clock()
    