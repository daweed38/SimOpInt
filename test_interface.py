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
INT1 = SimOpInt('Config/Interfaces', 'SimOpIntTest.json', 'JSON', logging.DEBUG)

logger.info(f'{INT1.listLoadedModules()}')
logger.info(f'{INT1.listLoadedDevices()}')
logger.info(f'{INT1.listLoadedObjects()}')

RMP0ACTIVFREQ = INT1.getObject('DISPLAYS', 'RMP0ACTIVFREQ')

logger.info(f'{RMP0ACTIVFREQ.getName()}')
