# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Justin Weber
# Licensed under the terms of the MIT License
# see LICENSE

from math import sin
from random import gauss

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.properties import ListProperty

class MainScreen(Screen):
    pass

class BrewingScreen(Screen):
    pass

class FermentationScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class PiBrewery(App):
    running_values = ListProperty([])

    def build(self):
        self.title = 'Pibrewery'
        self.root = Builder.load_file("pibrewery.kv")

#        self.root.ids.sm

#        print self.root.ids.sm
#        for wid in self.root.walk():
#            print(wid, wid.id)
#            if hasattr(wid, 'name'):
#                print('name', wid.name)
#            if wid.id == 'ferm_graph':
#                self.ferm_graph = wid

        return

    def update_fermentation_plot(self, dt):
        self.running_values.append(gauss(.5, .1))
        self.running_values = self.running_values[-100:]

if __name__ == '__main__':
    PiBrewery().run()
