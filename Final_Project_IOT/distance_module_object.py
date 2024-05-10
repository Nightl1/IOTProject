import RPi.GPIO as GPIO
import time

# connections:
# VCC to 3.3v
# trig to GPIO 4 (pin 29)
# Echo to GPIO 6 (pin 31)
# GND to ground

class distance_module():
    Tr = 5 # The pin number of the input end of the ultrasonic module
    Ec = 6 # Pin number of the output end of the ultrasonic module
    
    def __init__(self):
        self.setup()
    
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Tr, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Ec, GPIO.IN)
        
    def check_distance(self):     
        # Set the input terminal of the module to high level
        # and send out an initial sound wave
        GPIO.output(self.Tr, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.Tr, GPIO.LOW)
        
        # timout
        max_time = 2
    
        t1 = time.time() # time when the initial sound wave was emitted
        
        loops = 0
        # stall the code untill the sound signal comes back
        while not GPIO.input(self.Ec) and not (time.time() - t1 > max_time):
            loops += 1
            pass
        
        self.loops = 0
        while GPIO.input(self.Ec) and not (time.time() - t1 > max_time):
            loops += 1
            pass
    
        t2 = time.time() # the time when the return soud wave was captured
        return round((t2-t1)*343/2, 3) # calculate the distance