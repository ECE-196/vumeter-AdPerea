import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from time import sleep, time

class main:
    def __init__(self):
        self.setup()
        self.calibrate()
    # set up
    def setup(self):
        self.max_volume = 0
        # setup pins
        self.microphone = AnalogIn(board.IO1)
        self.status = DigitalInOut(board.IO17)
        self.status.direction = Direction.OUTPUT
        led_pins = [
            board.IO21,
            board.IO26,  # type: ignore
            board.IO47,
            board.IO33,  # type: ignore
            board.IO34,  # type: ignore
            board.IO48,
            board.IO35,
            board.IO36,
            board.IO37,
            board.IO38,
            board.IO39,
        ]
        self.num_leds = len(led_pins)
        self.leds = [DigitalInOut(pin) for pin in led_pins]
        self.leds_revs = self.leds[::-1]
        for led in self.leds:
            led.direction = Direction.OUTPUT
    # calibration
    def calibrate(self):
        curr_time = time()
        elapsed_time = 0
        print("Calibration In Progress\n")
        # blink to indicate start of calibration sequence
        for i in range(11):
            self.leds[-1].value = not self.leds[-1].value
            sleep(0.25)
        while elapsed_time < 5:
            if self.microphone.value > self.max_volume:
                self.max_volume = self.microphone.value
            elapsed_time = time()-curr_time
        print("Calibration Complete\n")
        # switch light off to indicate end of calibration sequence
        self.leds[-1].value = not self.leds[-1].value

    # scale input --> map analog input to discrete index values between 0 and 10
    def scale(self,val):
        return int(self.num_leds*(val/self.max_volume))

    # main method
    def main_loop(self):
        while True:
            volume = self.scale(self.microphone.value)
            #print(volume)
            for i in range(self.num_leds - volume):
                led_idx = self.num_leds-1 - i
                #print(led_idx)
                self.leds[led_idx].value = False
            for led_idx in range(volume):
                #print(led_idx)
                self.leds[led_idx].value = True
            sleep(0.25)

m = main()
m.main_loop()
