import time
from math import pi, isnan

class PID:
    esc_l = None
    esc_r = None
    timePrev = 0
    ctime = 0

    totalangle = 0
    pid_p = 0
    pid_i = 0

    pid_d = 0
    kp = 15.44
    ki = 1.00
    kd = 0.005

    PID = 0
    previous_error = 0

    # percentage
    throttle = 1300

    desired_angle = 0

    def __init__(self, escl, escr):
        self.time = self.gettime()
        self.timePrev = self.time
        self.esc_l = escl
        self.esc_r = escr

    def gettime(self):
        return time.time() * 1000

    def loop(self):
        self.ctime = self.gettime()
        itntime = (self.ctime - self.timePrev)
        elapsedTime =  itntime / 1000
        error = self.totalangle - self.desired_angle

        self.pid_p = self.kp * error
        if (-3 < error < 3):
            self.pid_i = self.pid_i + (self.ki * error)

        self.pid_d = self.kd * ((error - self.previous_error) / elapsedTime)
        self.PID = self.pid_p + self.pid_i + self.pid_d
        if (self.PID < -1000):
            self.PID = -1000
        if (self.PID > 1000):
            self.PID = 1000

        pwmLeft = self.throttle + self.PID
        pwmRight = self.throttle - self.PID

        if (pwmRight < 1000):
            pwmRight = 1000
        if (pwmRight > 2000):
            pwmRight = 2000
        if (pwmLeft < 1000):
            pwmLeft = 1000
        if (pwmLeft > 2000):
            pwmLeft = 2000
        escdata = {}
        for esc in self.esc_l:
            escdata[esc] = pwmLeft
        for esc in self.esc_r:
            escdata[esc] = pwmRight

        self.previous_error = error
        return escdata

