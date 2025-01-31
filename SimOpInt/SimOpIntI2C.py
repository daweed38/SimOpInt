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
import sys
from typing import Type

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
    def i2cBusScan(self, startaddr: int = 0, endaddr: int = 128) -> list:

        headerline = f'   '
        addrline = f''
        devicelist = list()

        self.logger.debug(f'Scanning I2C Bus N° {self.bus} .... ')
        self.logger.debug(f'   ')

        for address in range(16):
            headerline = f'{headerline} {address:2x}'

        self.logger.debug(headerline)

        for address in range(startaddr, endaddr):
            if not address % 16:
                addrline = f'{address:02x}'

            if 2 < address < 120:  # Skip reserved addresses
                try:
                    if self.i2c is not None:
                        self.i2c.read_byte(address)
                        addrline = f'{addrline} {address:02x}'  # Device address
                    else:
                        addrline = f'{addrline} --'  # Dummy Bus, nothing can be detect
                    devicelist.append(address)

                except:
                    addrline = f'{addrline} --'  # No device detected
            else:
                addrline = f'{addrline}   '

            if not (address + 1) % 16:
                self.logger.debug(addrline)

        return devicelist
