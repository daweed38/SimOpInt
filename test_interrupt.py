##################################################
# FarmerSoft Open Interface Test
##################################################
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging
import time
import platform

if platform.system() == 'Linux':
    print(f'Importing RPi.GPIO Module')
    import RPi.GPIO as GPIO

# SimOpInt Module Import
from SimOpInt.SimOpIntLogger import SimOpIntLogger
from SimOpInt.SimOpInt import SimOpInt

simopintlogger = SimOpIntLogger('SimOpInt', 'Logs', 'simopint.log')
logger = simopintlogger.getLogger()
logger.setLevel(logging.DEBUG)

# Test Interface Initialisation
INT1 = SimOpInt('Config/Interfaces/SimOpIntTest', 'SimOpIntTest.json', logging.DEBUG)
INT1.setGpioMode('BCM')

INT1.logger.setLevel(logging.DEBUG)

IOPACK03 = INT1.getDevice('IOPACK03')
IOPACK03.setBankMode(1)
logger.info(f'Setup Interrupt for Device IOPACK03 Port A on Channel {IOPACK03.getIntPortGPIO("A")}')
IOPACK03.setIntActiveConfig('A', 1)
print(IOPACK03.getIntActiveConfig('A'))
IOPACK03.setPortInterruptConfig('A', 0xff)
INT1.setupInterruptGpio(IOPACK03.getIntPortGPIO('A'), GPIO.PUD_DOWN)
INT1.addInterruptEvent(IOPACK03.getIntPortGPIO('A'), GPIO.RISING, IOPACK03.getName(), 180)
# IOPACK03.logger.setLevel(logging.DEBUG)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    if platform.system() == 'Linux':
        print(f'GPIO Cleanup')
        GPIO.cleanup()
    IOPACK03.resetDeviceRegisters()
