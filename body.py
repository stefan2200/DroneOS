from ESC import ESC
from Positon import rotation
import os
import time
from Pid import PID
import threading

class body:
    gyro = rotation()
    esc_setup = {
        'esc_1': {'pin': 17, 'position_x': 'f', 'position_y': 'l'},
        'esc_2': {'pin': 18, 'position_x': 'f', 'position_y': 'r'},
        'esc_3': {'pin': 26, 'position_x': 'r', 'position_y': 'l'},
        'esc_4': {'pin': 20, 'position_x': 'r', 'position_y': 'r'}
        }
    escs = {}
    groups = {}
    ignore_warnings = True

    speed = 1150
    movement = ""

    fwangle = 0
    lrwangle = 0
    gyrox_static = 0
    gyroy_static = 0
    gyro_tilt = 0
    gyro_roll = 0

    def __init__(self):
        print "Starting DroneOS"
        os.system("sudo pigpiod")
        time.sleep(5)

    def moveto(self, to):
        if to is "a":
            self.fwangle = self.gyrox_static
            self.lrwangle = self.gyroy_static
            self.movement = 'a'
        if to is "f":
            self.fwangle = 10
            self.lrwangle = self.gyroy_static
            self.movement = 'f'
        if to is "b":
            self.fwangle = -10
            self.lrwangle = self.gyroy_static
            self.movement = 'b'
        if to is "l":
            self.fwangle =  self.gyrox_static
            self.lrwangle = 10
            self.movement = 'l'
        if to is "l":
            self.fwangle =  self.gyrox_static
            self.lrwangle = 10
            self.movement = 'r'

    def run(self):

        pid_roll = PID(['esc_4'], ['esc_3'])
        # pid_tilt = PID()

        pid_roll.desired_angle = 0

        pid_tilt = PID(['esc_1'], ['esc_2'])
        # pid_tilt = PID()

        pid_roll.desired_angle = 6
        #print "Starting simulation"
        #thread1 = Simulation(self)
        # thread.start_new_thread(self.move, ())
        counter = 0
        # counter is for testing purposes :)
        while(counter < 100):
            print "Movement: %s desired_roll %s desired tilt %s" % (self.movement, self.lrwangle, self.fwangle)
            if self.movement is not "a":
                pid_roll.desired_angle = self.lrwangle
                pid_tilt.desired_angle = self.fwangle
            self.gyro_run()
            pid_roll.totalangle = self.gyro_roll
            pid_roll.throttle = self.speed
            pid_tilt.totalangle = self.gyro_tilt
            pid_tilt.throttle = self.speed
            powers = pid_roll.loop()
            powers2 = pid_tilt.loop()
            total = self.mdict(powers2, powers)
            for x in total:
                self.escs[x].move_raw(total[x])
            self.printspeeds()

            counter += 1

    def printspeeds(self):
        s = """
                  %0.2f
                 *  %s
                 *
        %s ********* %s   %0.2f
                 *
                 * %s
        """ % (self.gyro_roll, int(self.escs['esc_1'].freq_current), int(self.escs['esc_3'].freq_current), int(self.escs['esc_4'].freq_current), self.gyro_tilt, int(self.escs['esc_2'].freq_current))
        print s

    def setup_groups(self):
        for x in self.esc_setup:
            xdata = self.esc_setup[x]
            e = ESC(xdata['pin'], xdata['position_x'], xdata['position_y'])
            self.escs[x] = e
        time.sleep(7)

    def mdict(self, m1, m2):
        for x in m2:
            if x not in m1:
                m1[x] = m2[x]
        return m1

    def gyro_run(self):
        self.gyro.pull()
        self.gyro_tilt = self.gyro.tilt_fw
        self.gyro_roll = self.gyro.tilt_lr
        print "%s tilt %s roll" % (self.gyro.tilt_fw, self.gyro.tilt_lr)

    def gyro_default(self):
        self.gyro.pull()
        print "Default calibration: %s tilt %s roll" % (self.gyro.tilt_fw, self.gyro.tilt_lr)
        print "I'm starting with %d groups controlling %d ESCs" % (len(self.groups), len(self.escs))
        self.gyrox_static = self.gyro.tilt_fw
        self.gyroy_static = self.gyro.tilt_lr

class Simulation (threading.Thread):
   def __init__(self, core):
      threading.Thread.__init__(self)
      self.core = core
   def run(self):
      print "Starting " + self.name
      simulation = {'a': 7, 'f': 3, 'a': 5, 'r': 2, 'a': 10}
      for x in simulation:
          print "Move %s for %d seconds" % (x, simulation[x])
          self.core.moveto(x)
          time.sleep(simulation[x])
      print "Exiting " + self.name
