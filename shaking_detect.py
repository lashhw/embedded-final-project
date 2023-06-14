import time
import smbus
import numpy as np

from imusensor.MPU9250 import MPU9250


class ShakingDetector:
    def __init__(self):
        self.address = 0x68
        self.bus = smbus.SMBus(1)
        self.imu = MPU9250.MPU9250(self.bus, self.address)
        self.imu.begin()
        self.imu.loadCalibDataFromFile("./calibration/calib.json")
        self.prev_accel = np.array(self.imu.AccelVals)
        self.irregular_times = 0

    def detect(self, q):
        """
        1. Read the acceleration data
        2. Compute the difference between the current acceleration and the previous acceleration
        3. Compute the norm of the difference
        4. If the norm is greater than a threshold, then we consider it as a collision
        """
        self.imu.readSensor()
        self.imu.computeOrientation()

        cur_accel = np.array(self.imu.AccelVals)

        accel_diff = cur_accel - self.prev_accel
        delta_accel = np.sqrt(np.sum(np.power(accel_diff, 2)))

        # print(f"Accel x: {imu.AccelVals[0]} ; Accel y : {imu.AccelVals[1]} ; Accel z : {imu.AccelVals[2]}")
        if delta_accel > 15:
            self.irregular_times += 1
            print(f"delta acceleration: {delta_accel}")
        else:
            self.irregular_times = 0

        if self.irregular_times >= 1:
            q.put_nowait(["shaking"])

            # print(f"roll: {imu.roll} ; pitch : {imu.pitch} ; yaw : {imu.yaw}")
        time.sleep(0.1)
        self.prev_accel = cur_accel


def shaking_detect_loop(q):
    sd = ShakingDetector()
    while True:
        sd.detect(q)


if __name__ == "__main__":
    detector = ShakingDetector()
    while True:
        detector.detect()
