#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ========================================================================================
# title           : magicbluelib.py
# description     : Python library to control Magic Blue bulbs over Bluetooth
# author          : Benjamin Piouffle
# date            : 23/11/2015
# python_version  : 3.4
# ========================================================================================

import random
from gattlib import GATTRequester

# Handles
HANDLE_CHANGE_COLOR = 0x0c

# Magics
MAGIC_CHANGE_COLOR = 0x56


class MagicBlue:
    def __init__(self, mac_address):
        self.mac_address = mac_address
        self._connection = None

    def connect(self):
        """
        Connect to device
        :return: True if connection succeed, False otherwise
        """
        self._connection = GATTRequester(self.mac_address, False)
        try:
            self._connection.connect(True, "random")
        except RuntimeError as e:
            print('Connection failed : {}'.format(e))
            return False
        return True

    def disconnect(self):
        """
        Disconnect from device
        """
        self._connection.disconnect()

    def is_connected(self):
        """
        :return: True if connection succeed, False otherwise
        """
        return self._connection.is_connected()

    def set_color(self, rgb_color):
        """
        Change bulb's color
        :param rgb_color: color as a list of 3 values between 0 and 255
        """
        self._connection.write_by_handle(HANDLE_CHANGE_COLOR, bytes(bytearray([MAGIC_CHANGE_COLOR] + list(rgb_color))))

    def set_random_color(self):
        """
        Change bulb's color with a random color
        """
        self.set_color([random.randint(1, 255) for i in range(3)])

    def turn_off(self):
        """
        Turn off the light by setting color to black (rgb(0,0,0))
        """
        self.set_color([0, 0, 0])

    def turn_on(self, brightness=1.0):
        """
        Set white color on the light
        :param brightness: a float value between 0.0 and 1.0 defining the brightness
        """
        self.set_color([int(255 * brightness) for i in range(3)])
