#!/usr/bin/python
#
## @file
#
# This file contains hardware classes that interface with AOTFs.
#
# Hazen 04/14
#

from PyQt4 import QtCore

import illumination.hardwareModule as hardwareModule


## CrystalTechAOTF
#
# Crystal Technologies AOTF.
#
class CrystalTechAOTF(hardwareModule.BufferedAmplitudeModulation):

    ## __init__
    #
    # @param parameters A XML object containing initial parameters.
    # @param parent The PyQt parent of this object.
    #
    def __init__(self, parameters, parent):
        hardwareModule.BufferedAmplitudeModulation.__init__(self, parameters, parent)

        if not (self.aotf.getStatus()):
            self.working = False

        if self.working:
            self.use_fsk = parameters.use_fsk
            if self.use_fsk:
                self.analogModulationOn()
            else:
                self.analogModulationOff()

    ## cleanup
    #
    # Called when the program closes to clean up.
    #
    def cleanup(self):
        hardwareModule.BufferedAmplitudeModulation.cleanup(self)
        self.aotf.shutDown()

    ## deviceSetAmplitude
    #
    # @param channel_id The channel.
    # @param amplitude The channel amplitude.
    #
    def deviceSetAmplitude(self, channel_id, amplitude):
        aotf_channel = self.channel_parameters[channel_id].channel
        self.device_mutex.lock()
        self.aotf.setAmplitude(aotf_chanel, amplitude)
        self.device_mutex.unlock()

    ## initialize
    #
    # This is called by each of the channels that wants to use this module.
    #
    # @param interface Interface type (from the perspective of the channel).
    # @param channel_id The channel id.
    # @param parameters A parameters object for this channel.
    #
    def initialize(self, interface, channel_id, parameters):
        hardwareModule.BufferedAmplitudeModulation.initialize(interface, channel_id, parameters)

        aotf_channel = self.channel_parameters[channel_id].channel
        off_frequency = self.channel_paraemters[channel_id].off_frequency
        on_frequency = self.channel_parameters[channel_id].on_frequency
        if self.use_fsk:
            frequencies = [off_frequency, on_frequency, off_frequency, off_frequency]
        else:
            frequencies = [on_frequency, off_frequency, off_frequency, off_frequency]
        self.device_mutex.lock()
        self.aotf.setFrequencies(aotf_channel, frequencies)
        self.device_mutex.unlock()


## CrystalTechAOTF32bit
#
# Crystal Technologies (32 bit) AOTF.
#
class CrystalTechAOTF32Bit(CrystalTechAOTF):

    ## __init__
    #
    # @param parameters A XML object containing initial parameters.
    # @param parent The PyQt parent of this object.
    #
    def __init__(self, parameters, parent):

        import crystalTechnologies.AOTF as AOTF
        self.aotf = AOTF.AOTF()

        CrystalTechAOTF.__init__(self, parameters, parent)


## CrystalTechAOTF64bit
#
# Crystal Technologies (64 bit) AOTF.
#
class CrystalTechAOTF64Bit(CrystalTechAOTF):

    ## __init__
    #
    # @param parameters A XML object containing initial parameters.
    # @param parent The PyQt parent of this object.
    #
    def __init__(self, parameters, parent):

        import crystalTechnologies.AOTF as AOTF
        self.aotf = AOTF.AOTF64Bit()

        CrystalTechAOTF.__init__(self, parameters, parent)


## NoneAOTF
#
# AOTF emulator.
#
class NoneAOTF(hardwareModule.AmplitudeModulation):

    ## __init__
    #
    # @param parameters A XML object containing initial parameters.
    # @param parent The PyQt parent of this object.
    #
    def __init__(self, parameters, parent):
        hardwareModule.AmplitudeModulation.__init__(self, parameters, parent)


#
# The MIT License
#
# Copyright (c) 2014 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
