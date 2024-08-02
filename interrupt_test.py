##################################################
# FarmerSoft Open Interface Test
##################################################
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging
import platform
import RPi.GPIO as GPIO

import time

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


def interrupt_callback(channel):
   intflag = IOPACK01.getPortInterruptFlag('A')
   intcapture = IOPACK01.getPortInterruptCapture('A')
   print(f'Interrupt Occured {bin(intcapture)} Flag {intflag}')

INTA0_GPIO = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(INTA0_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Test MCP23017 Initialisation
IOPACK01 = MCP23017('IOPACK01', '0x20', logging.DEBUG)
IOPACK01.resetDeviceRegisters()
IOPACK01.setBankMode(1)
IOPACK01.getPortDirection('A')
IOPACK01.getPortInterruptConfig('A')
IOPACK01.getPortCompareMode('A')
IOPACK01.getIntActiveConfig('A')
IOPACK01.setIntActiveConfig('A', 1)
IOPACK01.setPortInterruptConfig('A', 0xff)

GPIO.add_event_detect(INTA0_GPIO, GPIO.RISING, callback=interrupt_callback, bouncetime=100)

try:
    while True:
        #print(f'GPIO INPUT : {GPIO.input(INTA0_GPIO)}')
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()

