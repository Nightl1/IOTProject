import RPi.GPIO as GPIO
import time
import math

# connections:
# - to ground
# + to 3.3v
# DCKI to GPIO 23 (pin 16)
# DI to GPIO 24 (pin 18)

class led_bar:
    DATA_Pin = 23
    CLK_Pin  = 24
  
    CmdMode  = 0x0000  # Work on 8-bit mode
    ON       = 0x00ff  # 8-byte 1 data
    SHUT     = 0x0000  # 8-byte 0 data
 
    #s_clk_flag
    s_clk_flag = 0
    
    percentage_values = {
        0: 0x0000,
        10: 0x0001,
        20: 0x0003,
        30: 0x0007,
        40: 0x000f,
        50: 0x001f,
        60: 0x003f,
        70: 0x007f,
        80: 0x00ff,
        90: 0x01ff,
        100: 0x03ff
        }
    
    def __init__(self):
        self.setup()

    def send16bitData(self, data):
        self.s_clk_flag
        for i in range(0, 16):
            if data & 0x8000:
                GPIO.output(self.DATA_Pin, GPIO.HIGH)
            else:
                GPIO.output(self.DATA_Pin, GPIO.LOW)
        
            if self.s_clk_flag == True:
                GPIO.output(self.CLK_Pin, GPIO.LOW)
                self.s_clk_flag = 0
            else:
                GPIO.output(self.CLK_Pin, GPIO.HIGH)
                self.s_clk_flag = 1
            time.sleep(0.001)
            data = data << 1
  
    def latchData(self):
        latch_flag = 0
        GPIO.output(self.DATA_Pin, GPIO.LOW)
    
        time.sleep(0.05)
        for i in range(0, 8):
            if latch_flag == True:
                GPIO.output(self.DATA_Pin, GPIO.LOW)
                latch_flag = 0
            else:
                GPIO.output(self.DATA_Pin, GPIO.HIGH)
                latch_flag = 1
        time.sleep(0.05)
  
    def sendLED(self, LEDstate):
        for i in range(0, 12):
            if (LEDstate & 0x0001) == True:
                self.send16bitData(self.ON)
            else:
                self.send16bitData(self.SHUT)
            LEDstate = LEDstate >> 1
  
    def setup(self):
        print ("Adeept LED bar test code!")
        print ("Using DATA = PIN16(GPIO23), CLK = PIN18(GPIO24)")   

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.DATA_Pin, GPIO.OUT)
        GPIO.setup(self.CLK_Pin,  GPIO.OUT)

        GPIO.output(self.DATA_Pin, GPIO.LOW)
        GPIO.output(self.CLK_Pin,  GPIO.LOW)

    def destroy(self):
        GPIO.cleanup()

    def set_percentage(self, percentage = 0):
        if not(percentage > 100) or not(percentage < 0):
            self.send16bitData(self.CmdMode)
            self.sendLED(self.percentage_values[self.round_nearest(percentage)])
            self.latchData()
        
        
    # rounds number to 10, either up or under
    def round_nearest(self, x):
        rem = x % 10
        if rem < 5:
            x = int(x / 10) * 10
        else:
            x = int((x + 10) / 10) * 10
        return x