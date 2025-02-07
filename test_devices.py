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
from SimOpInt.DeviceMCP23017 import MCP23017
from SimOpInt.DeviceHT16K33 import HT16K33

simopintlogger = SimOpIntLogger('SimOpInt', 'Logs', 'simopint.log')
logger = simopintlogger.getLogger()
logger.setLevel(logging.DEBUG)

# Test MCP23017 Initialisation
IOPACK01 = MCP23017('IOPACK01', '0x20', None, logging.DEBUG)

# Test HT16K33 Initialisation
LEDPACK01 = HT16K33('LEDPACK01', '0x70', None, logging.DEBUG)
LEDPACK01.configMCP(1)
LEDPACK01.start()
LEDPACK01.setRow('A', 1, 0xff)
LEDPACK01.setBrightness(10)
time.sleep(2)
LEDPACK01.setBrightness(5)
time.sleep(2)
LEDPACK01.setBrightness(15)
time.sleep(2)
LEDPACK01.setRow('A', 1, 0x00)
LEDPACK01.setOut('A', 1, 1, 1)
LEDPACK01.setBlinkRate('blink1hz')
time.sleep(5)
LEDPACK01.setBlinkRate('blink2hz')
time.sleep(5)
LEDPACK01.setBlinkRate('blinkoff')
time.sleep(2)
LEDPACK01.setOut('A', 1, 1, 0)
LEDPACK01.stop()
LEDPACK01.configMCP(0)
