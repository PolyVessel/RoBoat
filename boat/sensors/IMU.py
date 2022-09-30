import rcpy
import rcpy.mpu9250 as mpu9250

class IMU:

    initialized = False

    # Singleton Pattern (we only have 1 IMU)
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IMU, cls).__new__(cls)
        return cls.instance

    def init(self):
        mpu9250.initialize(enable_magnetometer=True)
        self.initialized = True

    def poll_sensor(self):
        if rcpy.get_state() != rcpy.RUNNING:
            rcpy.run()

        if rcpy.get_state == rcpy.RUNNING:
            temp = mpu9250.read_imu_temp()
            data = mpu9250.read()

            print("Data: {}\n\nTemp: {}".format(data, temp))

        else:
            # Add more robust logs here
            print("RCPY is not RUNNING, even though we set it to run")