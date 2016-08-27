# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Justin Weber
# Licensed under the terms of the MIT License
# see LICENSE

from math import sin

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.graph import Graph, MeshLinePlot

class MainScreen(Screen):
    pass

class BrewingScreen(Screen):
    pass

class FermentationScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("pibrewery.kv")

class PiBrewery(App):
    def __init__(self, *args, **kwargs):
        App.__init__(self, *args, **kwargs)

        self.ferm_plot = None
        self.ferm_graph = None

        Clock.schedule_interval(self.update_fermentation_plot, 5)


    def build(self):
        self.title = 'PiBrewery'
        Clock.schedule_once(self.post_build)
        return presentation

    def post_build(self, dt):
        for wid in self.root.walk(restrict=True):
            print(wid.id)
            if hasattr(wid, 'name'):
                print(wid.name)
            if wid.id == 'ferm_graph':
                self.ferm_graph = wid

#        self.ferm_plot = MeshLinePlot(color=[1, 0, 0, 1])
#        self.ferm_plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
#        self.ferm_graph.add_plot(self.ferm_plot)


    def update_fermentation_plot(self, dt):
        print('update')

if __name__ == '__main__':
    PiBrewery().run()
