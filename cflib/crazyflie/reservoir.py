#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2020 Zane Kaminski
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Used for downloading reservoir networks to the CrazyFlie
and attaching those reservoirs to setpoint types.
"""
import struct

from cflib.crtp.crtpstack import CRTPPacket
from cflib.crtp.crtpstack import CRTPPort

__author__ = 'Zane Kaminski'
__all__ = ['ReservoirLoader']

TYPE_ALLOC_RES = 0
TYPE_SET_INPUT = 1
TYPE_APPEND_INTERNAL = 2
TYPE_SET_OUTPUT = 3
TYPE_COMPUTE_CHECKSUM = 4


class ReservoirLoader():
    """
    Used for downloading reservoir networks to the CrazyFlie
    and attaching those reservoirs to setpoint types.
    """

    def __init__(self, crazyflie=None):
        """
        Initialize the ReservoirLoader object.
        """
        self._cf = crazyflie

    def alloc_reservoir(self, i_res, size, connectivity):
        pk = CRTPPacket()
        pk.port = CRTPPort.RESERVOIR
        pk.data = struct.pack('<BBBH', TYPE_ALLOC_RES,
                              i_res, size, connectivity)
        self._cf.send_packet(pk)

    def set_input_weight(self, i_res, i_input, i_neuron, weight):
        pk = CRTPPacket()
        pk.port = CRTPPort.RESERVOIR
        pk.data = struct.pack('<BBBBf', TYPE_SET_INPUT,
                              i_res, i_input, i_neuron, weight)
        self._cf.send_packet(pk)

    def append_internal_weight(self, i_res, i_neuron_neuron,
                               i_neuron_out, i_neuron_in, weight):
        pk = CRTPPacket()
        pk.port = CRTPPort.RESERVOIR
        pk.data = struct.pack('<BBHBBf', TYPE_APPEND_INTERNAL,
                              i_res, i_neuron_neuron,
                              i_neuron_out, i_neuron_in, weight)
        self._cf.send_packet(pk)

    def set_output_weight(self, i_res, i_output, i_neuron, weight):
        pk = CRTPPacket()
        pk.port = CRTPPort.RESERVOIR
        pk.data = struct.pack('<BBBBf', TYPE_SET_OUTPUT,
                              i_res, i_output, i_neuron, weight)
        self._cf.send_packet(pk)

    def compute_checksum(self):
        pk = CRTPPacket()
        pk.port = CRTPPort.RESERVOIR
        pk.data = struct.pack('<B', TYPE_COMPUTE_CHECKSUM)
        self._cf.send_packet(pk)
