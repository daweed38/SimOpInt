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

RMP0VHF1SWL = INT1.getObject('SWLIGHTS', 'RMP0VHF1SWL')
RMP0NAVSWL = INT1.getObject('SWLIGHTS', 'RMP0NAVSWL')

logger.info(f'RMP0VHF1SWL Status : {RMP0VHF1SWL.getLightState()}')
RMP0VHF1SWL.setLightState('ON')
time.sleep(2)
logger.info(f'RMP0VHF1SWL Status : {RMP0VHF1SWL.getLightState()}')
RMP0VHF1SWL.setLightState('OFF')
logger.info(f'RMP0VHF1SWL Status : {RMP0VHF1SWL.getLightState()}')
logger.info(f'RMP0NAVSWL Status : {RMP0NAVSWL.getLightState()}')
RMP0NAVSWL.setLightState('ON')
time.sleep(2)
logger.info(f'RMP0VHF1SWL Status : {RMP0VHF1SWL.getLightState()}')
RMP0NAVSWL.setLightState('OFF')

LEDPACK01.stop()
