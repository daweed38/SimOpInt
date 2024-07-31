##################################################
# FarmerSoft Open Interface Test
##################################################
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging

# SimOpInt Module Import
from SimOpInt.SimOpIntLogger import SimOpIntLogger
from SimOpInt.DeviceBase import DeviceBase

simopintlogger = SimOpIntLogger('SimOpInt', 'Logs', 'simopint.log')
logger = simopintlogger.getLogger()
logger.setLevel(logging.DEBUG)

"""
IOPACK01 = DeviceBase('IOPACK01', '0x20', logging.DEBUG)
IOPACK01.readDevice()
IOPACK01.writeDevice(0xff)
IOPACK01.readRegister(0x00)
IOPACK01.writeRegister(0x00, 0xff)
IOPACK01.readBit(0x00, 1)
IOPACK01.writeBit(0x00, 1, 1)
"""