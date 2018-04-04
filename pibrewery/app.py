# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Justin Weber
# Licensed under the terms of the MIT License
# see LICENSE
#
# The main app.

import threading
import logging

import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.properties import ListProperty, NumericProperty, StringProperty

from pibrewery.read_sensors import ReadSensors, count_bubbles
from pibrewery.tools import c_to_f, get_kv
from pibrewery.constants import *

# log data
DATA_LOGGER = logging.getLogger('data')
DATA_LOGGER.setLevel(logging.INFO)
fh = logging.FileHandler('./data.log')
fr = logging.Formatter('%(asctime)s %(message)s')
fh.setFormatter(fr)
DATA_LOGGER.addHandler(fh)


class MainScreen(Screen):
    pass


class MashScreen(Screen):
    pass


class BrewScreen(Screen):
    pass


class FermentScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


class BubbleCountThread(threading.Thread):
    def __init__(self, sensors):
        threading.Thread.__init__(self)

        self.read_sensors = sensors
        self.bubbles_per_min = 0
        self.stop = False

    def run(self):
        count_bubbles(self)


class PiBrewery(App):
    temperature_values = ListProperty([])
    temperature_max = NumericProperty(100)
    temperature_min = NumericProperty(50)
    current_temperature = StringProperty('##')
    current_bubbles_minute = StringProperty('##')
    

    def __init__(self):
        App.__init__(self)

        # setup the sensors
        sr = self.sensors = ReadSensors()
        bc = self.bubble_count = BubbleCountThread(sr)
        bc.start()

    def build(self):
        self.title = 'Pibrewery'
        self.root = Builder.load_file(get_kv("app.kv"))
        return

    def close(self):
        # stop the bubble count thread
        self.bubble_count.stop = True

        # stop the app
        self.get_running_app().stop()

    def update_fermentation_plot(self, dt):

        # read the temperatures
        temp = self.sensors.read_temperature()
        temp = c_to_f(temp)
        temp_str = '{0:.1f}'.format(temp)

        # get the bpm
        bpm = self.bubble_count.bubbles_per_min
        bpm_str = str(bpm)

        # log to file
        DATA_LOGGER.info(','.join([temp_str, bpm_str]))

        # update labels
        self.current_temperature = temp_str
        self.current_bubbles_minute = bpm_str

        # update plot
        self.temperature_values.append(temp)
        self.temperature_values = self.temperature_values[-MAXIMUMPLOTLENGTH:]
        self.temperature_max = max(self.temperature_values) + 1
        self.temperature_min = min(self.temperature_values) - 1


def main():
    PiBrewery().run()


if __name__ == '__main__':
    main()    
