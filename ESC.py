import os
import time
import subprocess
import re
import sys
class ESC:
    freq_min = 1000
    freq_max = 1600
    pin = 0
    position_x = "a"
    position_y = "a"
    freq_current = 0
    fast_start = True

    def __init__(self, pin, position_x, position_y):
        self.pin = pin
        self.position_x = position_x
        self.position_y = position_y
        output = subprocess.Popen(['pigs', 'gpw', str(self.pin)], stdout=subprocess.PIPE).communicate()[0]
        if "GPIO is not in use" in output or "-r" in sys.argv:
            if self.fast_start:
                subprocess.Popen("pigs servo %d 2000 mils 2000 servo %d 1000 mils 2000" % (self.pin, self.pin), shell=True)
            else:
                os.system("pigs servo %d 2000 mils 2000 servo %d 1000 mils 2000" % (self.pin, self.pin))
        else:
            print "Pin %s is pwm, not setting up.." % self.pin

    def thrustperc(self, perc):
        minmax = self.freq_max - self.freq_min
        percstep = minmax / 100
        netforce = percstep * perc
        return netforce

    def move(self, perc):
        freq = int(self.thrustperc(perc))
        if freq > self.freq_max:
            freq = self.freq_max
        if freq < self.freq_min:
            freq = 0
        self.freq_current = freq
        subprocess.Popen("pigs servo %d %d" % (self.pin, freq), shell=True)

    def move_raw(self, freq):
        if freq > self.freq_max:
            freq = self.freq_max
        if freq < self.freq_min:
            freq = 0
        self.freq_current = freq
        os.system("pigs servo %d %d" % (self.pin, freq))

    def __del__(self):
        self.move(0)
