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
# from SimOpInt.DeviceBase import DeviceBase
from SimOpInt.DeviceMCP23017 import MCP23017
# from SimOpInt.SimOpInt import SimOpInt

simopintlogger = SimOpIntLogger('SimOpInt', 'Logs', 'simopint.log')
logger = simopintlogger.getLogger()
logger.setLevel(logging.DEBUG)

# Test Base Device Initialisation
"""
IOPACK01 = DeviceBase('IOPACK01', '0x20', logging.DEBUG)
IOPACK01.readDevice()
IOPACK01.writeDevice(0xff)
IOPACK01.readRegister(0x00)
IOPACK01.writeRegister(0x00, 0xff)
IOPACK01.readBit(0x00, 1)
IOPACK01.writeBit(0x00, 1, 1)
"""

# Test Interface Initialisation
"""
INT1 = SimOpInt('Config/Interfaces', 'SimOpIntTest.json', 'JSON', logging.DEBUG)
"""

# Test MCP23017 Initialisation
IOPACK01 = MCP23017('IOPACK01', '0x20', logging.DEBUG)
IOPACK01.getPortDirection('A')
IOPACK01.getPortDirection('B')
IOPACK01.setBankMode(1)
IOPACK01.getPortDirection('A')
IOPACK01.getPortDirection('B')
IOPACK01.setPortDirection('b', 'output')
IOPACK01.getPortDirection('B')
