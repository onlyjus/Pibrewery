import math

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# constants
SERIES_RESISTOR = 9970.0
THERMISTOR_NOMINAL = 10000.0
BCOEFFICIENT = 3100.0
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.

class ReadSensors(object):
    """class for reading sensors"""
    def __init__(self):

       # Create an ADS1115 ADC (16-bit) instance.
        self.adc = Adafruit_ADS1x15.ADS1115()

    def read_voltage(self, channel=0, gain=1):
        """read and return the  voltage of the specified channel"""
        value = adc.read_adc(channel, gain=gain)
        # convert to voltage
        voltage = value/32767.0*4.096
        return voltage

    def read_temeprature(self):
        voltage = self.read_voltage(0, 1)
        # resistance
        res = SERIES_RESISTOR/(32767.0/voltage-1)
        # temperature
        temp_c = 1/(1/298.15+1/BCOEFFICIENT*math.log(res/THERMISTOR_NOMINAL)) - 273

        return temp_c
    
    def read_hall(self):
        """read and return the hall sensor value"""
        voltage = self.read_voltage(1, 1)
        return voltage

