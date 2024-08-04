##################################################
# FarmerSoft Open Interface Test
##################################################
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging
import time

# SimOpInt Module Import
from SimOpInt.SimOpIntLogger import SimOpIntLogger
# from SimOpInt.DeviceBase import DeviceBase
from SimOpInt.DeviceMCP23017 import MCP23017
from SimOpInt.DeviceHT16K33 import HT16K33
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

"""
# Test MCP23017 Initialisation
IOPACK01 = MCP23017('IOPACK01', '0x20', logging.DEBUG)
"""

# Test HT16K33 Initialisation
LEDPACK01 = HT16K33('LEDPACK01', '0x70', logging.DEBUG)
LEDPACK01.configMCP(1)
LEDPACK01.start()
LEDPACK01.setRow(1, 'A', 0xff)
time.sleep(2)
LEDPACK01.setRow(1, 'A', 0x00)
LEDPACK01.setOut(1, 'A', 1, 1)
time.sleep(2)
LEDPACK01.setOut(1, 'A', 1, 0)
LEDPACK01.stop()
LEDPACK01.configMCP(0)

"""
# Test Interface Initialisation
INT1 = SimOpInt('Config/Interfaces', 'SimOpIntTest.json', 'JSON', logging.DEBUG)
"""