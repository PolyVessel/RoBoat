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
        mpu9250.initialize(enable_dmp = True, dmp_sample_rate = 4, enable_magnetometer=True)
        self.initialized = True

    def poll_sensor(self):
        if not self.initialized:
            self.init()

        imu_data = mpu9250.read()
        temp = mpu9250.read_imu_temp()

        data = {
            "heading": imu_data["head"],
            "accel": imu_data["accel"],
            "gyro": imu_data["gyro"],
            "mag": imu_data["mag"],
            "tb": imu_data["tb"],
            "temp": temp,
        }

        return data

if __name__ == "__main__":
    rcpy.set_state(rcpy.RUNNING)
    print(IMU().poll_sensor())
