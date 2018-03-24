# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Justin Weber
# Licensed under the terms of the MIT License
# see LICENSE

import logging
DATA_LOGGER = logging.getLogger('data')
DATA_LOGGER.setLevel(logging.INFO)
fh = logging.FileHandler('./data.log')
fr = logging.Formatter('%(asctime)s %(message)s')
fh.setFormatter(fr)
DATA_LOGGER.addHandler(fh)

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.properties import ListProperty, NumericProperty, StringProperty

from read_sensors import ReadSensors
from tools import c_to_f
from constants import *

class MainScreen(Screen):
    pass

class BrewingScreen(Screen):
    pass

class FermentationScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class PiBrewery(App):
    temperature_values = ListProperty([])
    temperature_max = NumericProperty(100)
    temperature_min = NumericProperty(50)
    current_temperature = StringProperty('##')
    sensors = ReadSensors()

    def build(self):
        self.title = 'Pibrewery'
        self.root = Builder.load_file("pibrewery.kv")
        return

    def update_fermentation_plot(self, dt):
        temp = self.sensors.read_temperature()
        temp = c_to_f(temp)
        temp_str = '{0:.1f}'.format(temp)
        DATA_LOGGER.info(temp_str)
        self.current_temperature = temp_str
        self.temperature_values.append(temp)
        self.temperature_values = self.temperature_values[-MAXIMUMPLOTLENGTH:]
        self.temperature_max = max(self.temperature_values) + 1
        self.temperature_min = min(self.temperature_values) - 1

def main():
    PiBrewery().run()

if __name__ == '__main__':
    main()    
