import math
import time
import threading

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# constants
SERIES_RESISTOR = 9970.0

# Steinhart Coefficients to convert from resistance to temperature
THERMISTOR_NOMINAL = 9741.4  # 10000.0
TEMPERATURE_NOMINAL = 25.0
BCOEFFICIENT = 3404.6  # 3950.0

# ADS1015/ADS1115 gains
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
ADS_GAIN = {
    2/3: 6.144,
    1:   4.096,
    2:   2.048,
    4:   1.024,
    8:   0.512,
    16:  0.256
    }


class ReadSensors(object):
    """class for reading sensors"""
    def __init__(self):

       # Create an ADS1115 ADC (16-bit) instance.
        self.adc = Adafruit_ADS1x15.ADS1115()

    def read_voltage(self, channel=0, gain=1):
        """read and return the  voltage of the specified channel"""
        value = self.adc.read_adc(channel, gain=gain)
        # convert to voltage
        voltage = value/32767.0*ADS_GAIN.get(gain)
        return voltage

    def get_ref_voltage(self):

        # sample multiple times to take an average reading
        nsamples = 10
        voltages = 0
        for i in range(nsamples):
            voltage = self.read_voltage(1, 2/3)
            voltages += voltage

        voltage = voltages/nsamples
        return voltage

    def read_temperature(self, verbose=False):

        # sample multiple times to take an average reading
        nsamples = 10
        voltages = 0
        for i in range(nsamples):
            voltage = self.read_voltage(0, 1)
            voltages += voltage
        voltage = voltages/nsamples

        # get the reference voltage
        vref = self.get_ref_voltage()
        
        # resistance
        res = SERIES_RESISTOR*voltage/(vref-voltage)
        
        # temperature
        temp_c = 1/(1/(TEMPERATURE_NOMINAL + 273.15)+1/BCOEFFICIENT*math.log(res/THERMISTOR_NOMINAL)) - 273.15

        if verbose:
            return vref, voltage, res, temp_c
        return temp_c

    def read_photo_interrupter(self):
        voltage = self.read_voltage(2, 1)

        return voltage


def count_bubbles(src):
    sr = src.read_sensors
    st = 0.1 # seconds
    s = 0
    s_list = [0]*int(60/st)
    ns = len(s_list)
    lv = -1
    src.bubbles_per_min = 0
    while not src.stop:
        v = sr.read_photo_interrupter()

        s_list[s] = v < 1 and lv - v > 3
        src.bubbles_per_min = sum(s_list)
        lv = v
        s += 1
        if s == ns:
            s = 0
        time.sleep(st)


def test_thermister():
    sr = ReadSensors()
    print('Vref, V, R, Temp [C]')
    while True:
        print('{0:.2f}, {1:.2f}, {2:.2f}, {3:.2f}'.format(*sr.read_temperature(True)))
        time.sleep(1)


def test_photo_interrupter():
    sr = ReadSensors()
    print('V')
    while True:
        print('{0:.2f}'.format(sr.read_photo_interrupter()))
        time.sleep(.01)

def test_count_bubbles():

    read_senors = ReadSensors()
    
    class Test(threading.Thread):
        def __init__(self, read_sensors):
            threading.Thread.__init__(self)
            self.read_sensors = read_sensors
            self.stop = False
            self.bubbles_per_min = 0
        def run(self):
            count_bubbles(self)

    tc = Test(read_senors)
    tc.start()

if __name__ == "__main__":
    # test_photo_interrupter()
    test_count_bubbles()
