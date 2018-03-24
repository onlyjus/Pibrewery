# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Justin Weber
# Licensed under the terms of the MIT License
# see LICENSE
#
# This file contains tools.

from pibrewery import __dir__
import os

def c_to_f(c):
    """given a temperature in C, convert to F"""
    return 9/5.0*c+32

def get_kv(fname):
    return os.path.join(__dir__, fname)
