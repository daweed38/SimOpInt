##################################################
# FarmerSoft Open Interface Utilities Class
##################################################
# SimOpIntUtils Class REV 5.0
# FarmerSoft © 2025
# By Daweed
##################################################

# System Modules Import
import logging

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntI2C import I2CBus


class SimOpIntUtils:

    ###################################
    # Class Description
    ###################################

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, debug: int = 30) -> None:
        self.debug = debug
        self.i2c = I2CBus(self.debug)

        # Get Logger
        self.logger = logging.getLogger(__name__)

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Method
    ###################################

    def listObject(self, objtype: str, objfilter: str | int) -> list | None:
        if objtype.lower() == 'device':
            if objfilter.lower() == 'all':
                return self.i2c.i2cBusScan()
            elif objfilter.lower() == 'mcp23017':
                return self.i2c.i2cBusScan(32, 39)
            elif objfilter.lower() == 'ht16k33':
                return self.i2c.i2cBusScan(112, 119)
            else:
                self.logger.error(f'Listing object(s) {objfilter.lower()} not supported by list command')
                return None
        else:
            self.logger.error(f'Object type {objtype} not supported by list command')
            return None

    def readData(self, objtype: str, objfilter: str | int) -> dict | None:
        if objtype.lower() == 'config':
            if objfilter.lower() == 'simopintd':
                self.logger.info(f'Reading configuration of {objfilter.lower()} not yet supported by read command')
                return None
            elif objfilter.lower() == 'simopint':
                self.logger.info(f'Reading configuration of {objfilter.lower()} not yet supported by read command')
                return None
            else:
                self.logger.error(f'Reading configuration of {objfilter.lower()} not supported by read command')
                return None
        else:
            self.logger.error(f'Object type {objtype} not supported by read command')
            return None
