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

# SimOpInt Module Import
from SimOpInt.SimOpIntLogger import SimOpIntLogger
from SimOpInt.SimOpInt import SimOpInt

INTA3_GPIO = 24

if platform.system() == 'Linux':
    print(f'Importing RPi.GPIO Module')
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INTA3_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def interrupt_callback(channel):
    intflag = IOPACK03.getPortInterruptFlag('A')
    intcapture = IOPACK03.getPortInterruptCapture('A')
    print(f'Interrupt Occurred {bin(intcapture)} Flag {bin(intflag)}')


simopintlogger = SimOpIntLogger('SimOpInt', 'Logs', 'simopint.log')
logger = simopintlogger.getLogger()
logger.setLevel(logging.INFO)

# Test Interface Initialisation
INT1 = SimOpInt('Config/Interfaces', 'SimOpIntTest.json', 'JSON')
RMP0MSTSW = INT1.getObject('SWITCHES', 'RMP0MSTSW')
IOPACK03 = INT1.getDevice('IOPACK03')
IOPACK03.setBankMode(1)
IOPACK03.setIntActiveConfig('A', 1)
IOPACK03.setPortInterruptConfig('A', 0xff)

logger.info(f'{INT1.listLoadedModules()}')
logger.info(f'{INT1.listLoadedDevices()}')
logger.info(f'{INT1.listLoadedObjects()}')

logger.info(f'{RMP0MSTSW.getName()}')

if platform.system() == 'Linux':
    print(f'Setup GPIO.add_event_detect')
    GPIO.add_event_detect(INTA3_GPIO, GPIO.RISING, callback=interrupt_callback, bouncetime=180)

try:
    while True:
        time.sleep(0.1)
        
except KeyboardInterrupt:
    if platform.system() == 'Linux':
        print(f'GPIO Cleanup')
        GPIO.cleanup()
    IOPACK03.resetDeviceRegisters()
