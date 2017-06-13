import os
import time
import sys
os.system ("sudo pigpiod")
time.sleep(1)
import pigpio
import sensors
class motors:
    pi = pigpio.pi()

    pin_front_left = 17
    pin_front_right = 18
    pin_rear_left = 26
    pin_rear_right = 20

    current_fl = 0
    current_fr = 0
    current_rl = 0
    current_rr = 0

    gyro = sensors.rotation()

    lift_value = 1300

    min_value = 700
    test_value = 1300
    max_value = 1500

    gravity_norm = 1.04
    gravity_movement_down = 1.06
    gravity_movement_up = 0.98

    margin = 3

    def init(self):
        os.system("pigs servo %d 2000 mils 2000 servo %d 1000 mils 2000" % (self.pin_front_left, self.pin_front_left))
        time.sleep(1)
        print "init 1"
        os.system("pigs servo %d 2000 mils 2000 servo %d 1000 mils 2000" % (self.pin_front_right, self.pin_front_right))
        time.sleep(1)
        print "init 2"
        os.system("pigs servo %d 2000 mils 2000 servo %d 1000 mils 2000" % (self.pin_rear_left, self.pin_rear_left))
        time.sleep(1)
        print "init 3"
        os.system("pigs servo %d 2000 mils 2000 servo %d 1000 mils 2000" % (self.pin_rear_right, self.pin_rear_right))
        time.sleep(1)
        print "init done"
    def calibrate(self):
        self.gyro.pull()
        print "Default orientation: x%s y%s" % (self.gyro.tilt_fw, self.gyro.tilt_lr)
        time.sleep(2)
        print "Using vertical calibration [1]"
        self.setall(1100)
        cdatax = []
        cdatay = []
        secs = 5
        for x in range(0, secs):
            self.gyro.pull()
            cdatax.append(self.gyro.tilt_fw)
            cdatay.append(self.gyro.tilt_lr)
            time.sleep(1)
        self.setall(0)
        print "Step 1 done.. dropping data"
        time.sleep(1)
        print cdatax
        print cdatay
        avgx = sum(cdatax) / len(cdatax)
        avgy = sum(cdatay) / len(cdatay)
        if avgx > 10 or avgx < -10:
            print "[WARNING] Gyro x not stable.. reading %s" % avgx
        if avgy > 10 or avgy < -10:
            print "[WARNING] Gyro y not stable.. reading %s" % avgy
        print "Avarage: %s" % avgx
        print "Avarage: %s" %  avgy
        time.sleep(2)
        self.setall(1250)
        cdatax = []
        cdatay = []
        secs = 5
        for x in range(0, secs):
            self.gyro.pull()
            cdatax.append(self.gyro.tilt_fw)
            cdatay.append(self.gyro.tilt_lr)
            time.sleep(1)
        self.setall(0)
        print "Step 2 done.. dropping data"
        time.sleep(1)
        print cdatax
        print cdatay
        avgx = sum(cdatax) / len(cdatax)
        avgy = sum(cdatay) / len(cdatay)
        if avgx > 10 or avgx < -10:
            print "[WARNING] Gyro x not stable.. reading %s" % avgx
        if avgy > 10 or avgy < -10:
            print "[WARNING] Gyro y not stable.. reading %s" % avgy
        print "Avarage: %s" %  avgx
        print "Avarage: %s" %  avgy
        self.normx = avgx
        self.normy = avgy
        time.sleep(2)
    def lifttest(self):
        if not self.normx or not self.normy:
            print "Error reading calibration data, defaulting to x:0 y:0 "
            self.normx = 0
            self.normy = 0
        self.setall(1300)
        time.sleep(2)
        self.control()
        self.setall(1250)
        time.sleep(2)
    def control(self):
        for index in range(0, 5):
            gdata = self.gyro.pull()
            x = self.gyro.tilt_fw
            y = self.gyro.tilt_lr

            if abs(self.normx - x) > self.margin:
                if x < 0:
                    print "X too low, increasing forward speed with 10"
                    self.increase('f', 10)
                if x > 0:
                    print "X too high, increasing backward speed with 10"
                    self.increase('r', 10)
            if abs(self.normy - y) > self.margin:
                if y < 0:
                    print "Y too low, increasing left speed with 10"
                    self.increase('l', 10)
                if x > 0:
                    print "Y too high, increasing right speed with 10"
                    self.increase('r', 10)
            time.sleep(1)
    def ismoving(self):
        if self.gyro.z < self.gravity_movement_up:
            return abs(self.gyro.z - self.gravity_movement_up)
        if self.gyro.z > self.gravity_movement_down:
            return abs(self.gyro.z - self.gravity_movement_down)
        return False
    def increase(self, pos, amount):
        if pos is "f":
            old_fl = self.current_fl
            old_fr = self.current_fr
            self.setpin(c.pin_front_left, old_fl + amount)
            self.setpin(c.pin_front_right, old_fl + amount)

        if pos is "b":

            olf_rl = self.current_rl
            old_rr = self.current_rr
            self.setpin(c.pin_rear_left, olf_rl + amount)
            self.setpin(c.pin_rear_right, old_rr + amount)

        if pos is "r":

            olf_fr = self.current_fr
            old_rr = self.current_rr
            self.setpin(c.pin_front_right, olf_fr + amount)
            self.setpin(c.pin_rear_right, old_rr + amount)

        if pos is "l":
            old_fl = self.current_fl
            olf_rl = self.current_rl
            self.setpin(c.pin_front_left, old_fl + amount)
            self.setpin(c.pin_rear_left, olf_rl + amount)

        if pos is "a":
            old_fl = self.current_fl
            olf_rl = self.current_rl
            self.setpin(c.pin_front_left, old_fl + amount)
            self.setpin(c.pin_rear_left, olf_rl + amount)
            olf_fr = self.current_fr
            old_rr = self.current_rr
            self.setpin(c.pin_front_right, olf_fr + amount)
            self.setpin(c.pin_rear_right, old_rr + amount)
    def setall(self, inp):

        self.current_fl = inp
        self.current_fr = inp
        self.current_rl = inp
        self.current_rr = inp

        self.setpin(c.pin_front_left, inp)
        self.setpin(c.pin_front_right, inp)
        self.setpin(c.pin_rear_left, inp)
        self.setpin(c.pin_rear_right, inp)
    def setpin(self, pin, inp):

        if pin is 17:
            self.current_fl = inp

        if pin is 18:
            self.current_fr = inp

        if pin is 26:
            self.current_rl = inp

        if pin is 20:
            self.current_rr = inp

        if inp>self.max_value:
            inp = self.max_value
        if inp<self.min_value:
            inp = 0
        print "pigs servo %d %d" % (pin, inp)
        os.system("pigs servo %d %d" % (pin, inp))
time.sleep(5)
c = motors()
if "-acctest" in sys.argv:
    while(True):
        print c.ismoving()
        time.sleep(0.5)
if "-noinit" not in sys.argv:
        c.init()
else:
        time.sleep(3)
c.calibrate()
c.lifttest()
time.sleep(5)

c.setpin(c.pin_front_left, 0)
c.setpin(c.pin_front_right, 0)
c.setpin(c.pin_rear_left, 0)
c.setpin(c.pin_rear_right, 0)
