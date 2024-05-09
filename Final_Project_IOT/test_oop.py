# distance module connetions:
# VCC: 5v
# Trig: GPIO 5
# Echo: GPIO 6
# Gnd: Ground

# led bar connections:
# -: ground
# +: 3.3v
# DCKI: GPIO 24
# DI: GPIO 23

# Buttons connections:
# -: ground
# +: 3.3v
# blue S: GPIO 16
# red S: GPIO 20

# Buzzer connections:
# -: Ground
# +: 3.3v
# S: GPIO 18

# LED connectons:
# shorts: ground
# green long: resistor + GPIO 19
# red long: resistor + GPIO 26

import led_bar_object
import distance_module_object
import security_sequence
import RPi.GPIO as GPIO

class interactions:
    module = distance_module_object.distance_module() # the distance module object
    bar = led_bar_object.led_bar() # the led bar object
    security = security_sequence.security_system() # The security System

    opened = False

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)

    # reverses the percentage (0% is 100%)
    def flip_percentage(self, x):
        return 100 - x

    def act(self):
        try:
            dist = self.module.check_distance()
            print("distance: ", dist)
            if(dist > 1):
                self.opened = True
                dist = 1
            else:
                if(self.opened):
                    self.security.set_openable_false()
                self.opened = False
            self.bar.set_percentage(self.flip_percentage(dist * 100))
        
            if(not self.security.get_openable() and self.opened):
                GPIO.output(18, GPIO.HIGH)
            else:
                GPIO.output(18, GPIO.LOW)
        
            if(not self.opened):
                GPIO.output(18, GPIO.LOW)
            
        except KeyboardInterrupt:
            GPIO.cleanup()
            exit()
