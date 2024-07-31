##################################################
# FarmerSoft Sim Open Interface MCP23017 Device Class
##################################################
# MCP23017 Device Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging

# SimOpInt Import
from SimOpInt.DeviceBase import DeviceBase

class MCP23017(DeviceBase):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface I2C Device Base Class'

    ###################################
    # Properties
    ###################################

    registers_bank0 = {
        'iodira': {'addr': 0x00, 'init': 0xff},
        'iopola': {'addr': 0x02, 'init': 0x00},
        'gpintena': {'addr': 0x04, 'init': 0x00},
        'defavala': {'addr': 0x06, 'init': 0x00},
        'intcona': {'addr': 0x08, 'init': 0x00},
        'iocona': {'addr': 0x0a, 'init': 0x00},
        'gppua': {'addr': 0x0c, 'init': 0x00},
        'intfa': {'addr': 0x0e, 'init': 0x00},
        'intcapa': {'addr': 0x10, 'init': 0x00},
        'gpioa': {'addr': 0x12, 'init': 0x00},
        'olata': {'addr': 0x14, 'init': 0x00},
        'iodirb': {'addr': 0x01, 'init': 0xff},
        'iopolb': {'addr': 0x03, 'init': 0x00},
        'gpintenb': {'addr': 0x05, 'init': 0x00},
        'defavalb': {'addr': 0x07, 'init': 0x00},
        'intconb': {'addr': 0x09, 'init': 0x00},
        'ioconb': {'addr': 0x0b, 'init': 0x00},
        'gppub': {'addr': 0x0d, 'init': 0x00},
        'intfb': {'addr': 0x0f, 'init': 0x00},
        'intcapb': {'addr': 0x11, 'init': 0x00},
        'gpiob': {'addr': 0x13, 'init': 0x00},
        'olatb': {'addr': 0x15, 'init': 0x00}
    }

    registers_bank1 = {
        'iodira': {'addr': 0x00, 'init': 0xff},
        'iopola': {'addr': 0x01, 'init': 0x00},
        'gpintena': {'addr': 0x02, 'init': 0x00},
        'defavala': {'addr': 0x03, 'init': 0x00},
        'intcona': {'addr': 0x04, 'init': 0x00},
        'iocona': {'addr': 0x05, 'init': 0x00},
        'gppua': {'addr': 0x06, 'init': 0x00},
        'intfa': {'addr': 0x07, 'init': 0x00},
        'intcapa': {'addr': 0x08, 'init': 0x00},
        'gpioa': {'addr': 0x09, 'init': 0x00},
        'olata': {'addr': 0x0a, 'init': 0x00},
        'iodirb': {'addr': 0x10, 'init': 0xff},
        'iopolb': {'addr': 0x11, 'init': 0x00},
        'gpintenb': {'addr': 0x12, 'init': 0x00},
        'defavalb': {'addr': 0x13, 'init': 0x00},
        'intconb': {'addr': 0x14, 'init': 0x00},
        'ioconb': {'addr': 0x15, 'init': 0x00},
        'gppub': {'addr': 0x16, 'init': 0x00},
        'intfb': {'addr': 0x17, 'init': 0x00},
        'intcapb': {'addr': 0x18, 'init': 0x00},
        'gpiob': {'addr': 0x19, 'init': 0x00},
        'olatb': {'addr': 0x1a, 'init': 0x00}
    }

    ###################################
    # Constructor
    ###################################

    def __init__(self, devicename: str, deviceaddr: str, debug: int = 30) -> None:
        super().__init__(devicename, deviceaddr)

        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.devicetype = 'MCP23017'
        self.bankmode = 0
        self.registers = self.registers_bank0
        self.pullup = 0

        self.logger.debug(f'Device {self.devicename}  [Device Addr : {hex(self.deviceaddr)} / Device Type : {self.devicetype}] initialized. (Dummy Device : {self.dummy})')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    ###################################
    # MCP23017 Device Management Methods
    ###################################

    # ----- System -----

    # Method getBankMode()
    # Return Actual MCP23017 Bank Mode (int)
    def getBankMode(self) -> int:
        return self.bankmode

    # Method setBankMode(bankmode)
    # bankmode is int
    # Setup the MCP23017 in bankmode
    def setBankMode(self, bankmode: int) -> None:
        registeraddr = self.getRegisterAddr('iocona')
        if registeraddr is not False:
            self.logger.debug(f'Setting Device {self.getName()} in Bank Mode {bankmode}')
            if not self.dummy:
                if bankmode == 1:
                    self.i2c.writeBit(registeraddr, 8, 1)
                    self.registers = self.registers_bank1
                else:
                    self.i2c.writeBit(registeraddr, 8, 0)
                    self.registers = self.registers_bank0
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
            self.bankmode = bankmode

    # ----- GPIO Direction -----

    # ----- GPIO Polarity -----

    # ----- GPIO Interrupt -----

    # ----- GPIO Pullup Resistor -----

    # ----- GPIO -----