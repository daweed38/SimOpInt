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
logger.setLevel(logging.DEBUG)

# Test Interface Initialisation
INT1 = SimOpInt('Config/Interfaces', 'SimOpIntTest.json', 'JSON', logging.DEBUG)
print(INT1.listLoadedModules())
module = INT1.getModule('MCP23017')
print(module)