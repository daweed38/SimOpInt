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
from SimOpInt.SimOpInt import SimOpInt

simopintlogger = SimOpIntLogger('SimOpInt', 'Logs', 'simopint.log')
logger = simopintlogger.getLogger()
logger.setLevel(logging.INFO)

# Test Interface Initialisation
INT1 = SimOpInt('Config/Interfaces', 'SimOpIntTest.json', 'JSON')

LEDPACK01 = INT1.getDevice('LEDPACK01')
LEDPACK01.start()

logger.info(f'{INT1.listLoadedModules()}')
logger.info(f'{INT1.listLoadedDevices()}')
logger.info(f'{INT1.listLoadedObjects()}')

RMP0ACTIVFREQ = INT1.getObject('DISPLAYS', 'RMP0ACTIVFREQ')

logger.info(f'{RMP0ACTIVFREQ.getName()}')

"""
RMP0ACTIVFREQ.getDebugLevel()
RMP0ACTIVFREQ.setDebugLevel(logging.DEBUG)
RMP0ACTIVFREQ.getStatus()
RMP0ACTIVFREQ.setStatus('ON')
RMP0ACTIVFREQ.getStatus()
RMP0ACTIVFREQ.setStatus('OFF')
RMP0ACTIVFREQ.getStatus()

logger.info(f'Display Device : {type(RMP0ACTIVFREQ.getDevice())}')
logger.info(f'Number of digit of Display {RMP0ACTIVFREQ.getName()} : {RMP0ACTIVFREQ.getDisplayNbDigit()}')
logger.info(f'First Row {RMP0ACTIVFREQ.getDisplayFirstRow()} / First Row Type [{type(RMP0ACTIVFREQ.getDisplayFirstRow())}]')
logger.info(f'First Digit Register of Display {RMP0ACTIVFREQ.getName()} : {hex(RMP0ACTIVFREQ.getDigitRegister(RMP0ACTIVFREQ.getDisplayFirstRow()))}')
logger.info(f'Digit(s) Register of Display {RMP0ACTIVFREQ.getName()} : {RMP0ACTIVFREQ.listDigitsRegisters()}')
logger.info(f'Decimal Digit : {RMP0ACTIVFREQ.getDisplayDeciDigit()}')
"""

RMP0ACTIVFREQ.getDebugLevel()
RMP0ACTIVFREQ.setDebugLevel(logging.DEBUG)
RMP0ACTIVFREQ.setStatus('ON')
RMP0ACTIVFREQ.writeDisplay('120.45', True)
time.sleep(2)
RMP0ACTIVFREQ.setStatus('OFF')
time.sleep(2)
RMP0ACTIVFREQ.setStatus('ON')
LEDPACK01.stop()
