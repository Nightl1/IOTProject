import RPi.GPIO as GPIO
import time

class security_system():
    # if the can is openable
    openable = False
    
    # "passcode" system using two buttons:
    button0 = 16
    button1 = 20
    
    green_led = 19
    red_led = 26
    
    # this is the sequence that needs to be used to unlock:
    right_sequence = [0, 1, 0]
    
    # the sequence that the user is typing
    sequence = []
    
    # sometimes, when we press a button, it calls the callback twice.
    # as a walkaround, we check the time that went between the "calls"
    # and if it is smaller than 0.1, then we ignore the call.
    time_since_last_call = 1
    
    # once one of the buttons have been pressed, startrecording the sequence
    # if the sequence takes more than 5 seconds to execute, clear it
    # if the sequence is complete, check if it's the right one
    # if it is, set the "openable" to true
    # if it is not, keep it false
    # either way, clear sequance
    
    def __init__(self):
        self.time_since_last_call = time.time()
        self.setup()
    
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.green_led, GPIO.OUT)
        GPIO.setup(self.red_led, GPIO.OUT)
        
        GPIO.setup(self.button0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        GPIO.add_event_detect(self.button0, GPIO.RISING, callback=self.button0_callback)
        GPIO.add_event_detect(self.button1, GPIO.RISING, callback=self.button1_callback)
        
    def light_LED(self, led, seconds):
        GPIO.output(led, GPIO.HIGH)
        time.sleep(seconds)
        GPIO.output(led, GPIO.LOW)
    
    def button0_callback(self, channel):
        x = time.time() - self.time_since_last_call
        print(x)
        if x > 3:
            time_since_last_call = time.time()
            self.add_to_sequence(0)
    
    def button1_callback(self, channel):
        x = time.time() - self.time_since_last_call
        print(x)
        if x > 3:
            time_since_last_call = time.time()
            self.add_to_sequence(1)
    
    def add_to_sequence(self, x):
        # add to the sequence
        self.sequence.append(x)
        print("sequence: ", self.sequence)
        # if the sequence is the same lenght of the right one, check if the values are the same
        # if they are, unlock
        if(len(self.sequence) == len(self.right_sequence)):
            print("checking sequence...")
            is_right = True
            # looping through. If one element is wrong, remember it.
            for i in range(len(self.sequence)):
                if not (self.sequence[i] == self.right_sequence[i]):
                    is_right = False
                   
            # if the sequence is right, we open. Otherwise we don't
            if is_right:
                print("sequence is correct. Opening.")
                self.openable = True
                self.light_LED(self.green_led, 1)
            else:
                self.openable = False
                print("sequence is wrong. Not opening")
                self.light_LED(self.red_led, 1)
            
            self.sequence.clear()
            
    def get_openable(self):
        return self.openable
    
    def set_openable_false(self):
        self.openable = False