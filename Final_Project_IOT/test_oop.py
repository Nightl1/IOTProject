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
    percentage = 0

    opened = False # true if the can is opened
    unothorized_entry = False # true if the can was opened without authorization

    # GPIO setup for the buzzer
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)

    # reverses the percentage (0% is 100%)
    def flip_percentage(self, x):
        return 100 - x

    # method that checks the distance, set the percentage, and buzz the buzzer upon unothorized entry
    def act(self):
        try:
            # gets the distance from the distance module
            dist = self.module.check_distance() 
            print("distance: ", dist)
            
            # if the distance is greater than 1, the can is considered opened.
            # we set the distance to 1 (100%) to avoid issues later in the code.
            # we rearm the security system once the can gets closed again.
            if(dist > 1):
                self.opened = True
                dist = 1
            else:
                if(self.opened):
                    self.security.set_openable_false()
                self.opened = False
                
            # turns the distance into a percentage and flips the percentage
            # (closer to the sensor is a higher persentage)
            self.percentage = self.flip_percentage(dist * 100)
            self.bar.set_percentage(self.percentage)
        
            # sounds the buzzer upon unothorized entry
            if(not self.security.get_openable() and self.opened):
                GPIO.output(18, GPIO.HIGH)
                self.unothorized_entry = True
            else:
                GPIO.output(18, GPIO.LOW)
                unothorized_entry = False
            if(not self.opened):
                GPIO.output(18, GPIO.LOW)
                unothorized_entry = False
            
        except KeyboardInterrupt:
            GPIO.cleanup()
            exit()
          
    # returns the current percentage for the UI
    def get_percentage(self):
        return self.percentage
    
    def get_authorization(self):
        print(self.unothorized_entry)
        return self.unothorized_entry
    
    def close(self):
        GPIO.cleanup()
