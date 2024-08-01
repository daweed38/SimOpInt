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
        self.logger.debug(f'Bank Mode : {self.bankmode}')
        return self.bankmode

    # Method setBankMode(bankmode)
    # bankmode is int
    # Setup the MCP23017 in bankmode
    def setBankMode(self, bankmode: int) -> None:
        registeraddr = self.getRegisterAddr('iocona')
        if registeraddr:
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
        else:
            self.logger.error(f'Register iocona not found in self.registers')

    # ----- GPIO Direction -----

    # Method getPortDirection(port)
    # port is str
    # Return data from direction configuration for GPIO Port
    def getPortDirection(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr(f'iodir{port.lower()}')
        if registeraddr:
            if not self.dummy:
                portdir = self.i2c.readRegister(registeraddr)
                self.logger.debug(f'Reading Direction for Port {port.upper()} : {portdir}')
                return portdir
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register iodir{port.lower()} not found in self.registers')
            return False

    # Method setPortDirection(port, direction)
    # port is str (A|B) and direction is str (input|output)
    # Setup direction for GPIO Port
    def setPortDirection(self, port: str, direction: str) -> None:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if direction == 'input':
                registervalue = 0x00
            else:
                registervalue = 0xff

            if not self.dummy:
                self.logger.debug(f'Setting Direction for Port {port.upper()} to {direction}')
                self.i2c.writeRegister(registeraddr, registervalue)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register iodir{port.lower()} not found in self.registers')

    # Method getPinDirection(port, pin)
    # port is str (A|B) and pin is int
    # Return direction for pin on GPIO port
    def getPinDirection(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr:
            if not self.dummy:
                pindirection = self.i2c.readBit(registeraddr, pin)
                self.logger.debug(f'Reading Pin {pin} Direction on Port {port.upper()} : {pindirection}')
                return pindirection
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register iodir{port.lower()} not found in self.registers')
            return False

    # Method setPinDirection(port, pin, direction)
    # port is str (A|B) and pin is int and direction is str (input|output)
    # Setup direction for pin on GPIO port
    def setPinDirection(self, port: str, pin: int, direction: str) -> None:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr:
            self.logger.debug(f'Setting Pin {pin} Direction on Port {port.upper()} to {direction}')

            if direction == 'input':
                pindir = 1
            else:
                pindir = 0

            if not self.dummy:
                self.logger.debug(f'Setting Direction for Pin {pin} on Port {port.upper()} to {direction}')
                self.i2c.writeBit(registeraddr, pin, pindir)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register iodir{port.lower()} not found in self.registers')

    # ----- GPIO Polarity -----

    # ----- GPIO Interrupt -----

    # ----- GPIO Pullup Resistor -----

    # ----- GPIO -----
