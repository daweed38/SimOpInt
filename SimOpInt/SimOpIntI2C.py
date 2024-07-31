##################################################
# FarmerSoft Sim Open Interface I2C Class
##################################################
# I2C Class (I2C Bus Devices) REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging
import platform

if platform.system() != 'Windows':
    import smbus2

# SimOpInt Module Import


class I2CBus:

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface I2C Bus Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, debug: int = 30) -> None:

        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.bus = 1
        self.i2c = None
        self.devices = {}

        if platform.system() != 'Windows':
            self.i2c = smbus2.SMBus(self.bus)

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    # getI2CBus()
    # Return I2C bus
    def getI2CBus(self):
        return self.i2c

    # i2cBusScan()
    # Scan I2C bus and return result as a dict
    def i2cBusScan(self) -> dict:
        if self.i2c is not None:
            # ... Process I2C Bus Scan
            self.logger.debug(f'Scanning I2C Bus N° {self.bus} .... ')
        return self.devices
