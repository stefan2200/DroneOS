import math
from mpu6050 import mpu6050
from time import sleep
class rotation:
    sensor = mpu6050(0x68)
    tilt_fw = 0
    tilt_lr = 0

    x = 0
    y = 0
    z = 0

    verbose = False

    active = True
    percision = 25

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    def pull(self):
        if self.active:
            x = []
            y = []
            z = []
            for index in range(0, self.percision):
                try:
                    accelerometer_data = self.sensor.get_accel_data()
                    x.append(accelerometer_data['x'] / 16384.0)
                    y.append(accelerometer_data['y'] / 16384.0)
                    z.append(accelerometer_data['z'] / 16384.0)
                except:
                    pass
            self.x = (sum(x) / len(x))
            self.y = (sum(y) / len(y))
            self.z = (sum(z) / len(z))
            self.get_rotation()
    def get_rotation(self):
        self.tilt_lr = self.get_x_rotation(self.x, self.y, self.z)
        self.tilt_fw = self.get_y_rotation(self.x, self.y, self.z)
        if self.verbose:
            print "X rotation: %s" % self.tilt_fw
            print "Y rotation: %s" % self.tilt_lr
