# System Modules Import
from datetime import datetime
# Device Base Import
from DeviceBase import DeviceBase

##################################################
# FarmerSoft Sim Open Interface Device Class
##################################################
# MCP23017 Class (Pack I/O) REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class MCP23017(DeviceBase):
    """
    This Class allow the MCP23017 object creation
    to manage an MCP23017 I2C hardware device
    MCP23017 : 16 I/O I2C expander.
    Copyright FarmerSoft © 2022 By Daweed
    """

    ########################################
    # Properties
    ########################################

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

    ########################################
    # Constructor
    ########################################

    def __init__(self, devicename: str, deviceaddr: str, dummy=False, debug=False) -> None:
        super().__init__(devicename, deviceaddr, dummy, debug)

        self.devicetype = 'MCP23017'
        self.bankmode = 0
        self.registers = self.registers_bank0
        self.pullup = 0

        if self.debug:
            print("######################################################################")
            print("# Device {} Addr {} initialization at {}".format(self.devicename, hex(self.deviceaddr), datetime.now()))
            print("######################################################################")
            print("\r")

    ########################################
    # Destructor
    ########################################

    def __del__(self) -> None:

        if self.debug:
            print("######################################################################")
            print("# Device {} removed at {}".format(self.devicename, datetime.now()))
            print("######################################################################")
            print("\r")

        self.configMCP(0)

    ########################################
    # System Methods
    ########################################

    ########################################
    # Configuration
    ########################################

    ########################################
    # Standard Register Methods
    ########################################

    ########################################
    # MCP23017 Device Management Methods
    ########################################

    # ----- System -----

    # Method getBankMode()
    # Return Actual MCP23017 Bank Mode
    def getBankMode(self) -> int:
        return self.bankmode

    # Method setBankMode(bankmode)
    # Set the MCP23017 in bankmode
    # This affect Registers Addresses
    # bankmode is int
    def setBankMode(self, bankmode: int) -> None:
        registeraddr = self.getRegisterAddr('iocona')
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Setting Device {} in Bank Mode {}".format(self.getName(), bankmode))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                if bankmode == 1:
                    self.i2cdevice.writeBit(registeraddr, 8, 1)
                    self.registers = self.registers_bank1
                else:
                    self.i2cdevice.writeBit(registeraddr, 8, 0)
                    self.registers = self.registers_bank0

            self.bankmode = bankmode

    # ----- GPIO Direction -----

    # Method getPortDirection(port)
    # Return direction for GPIO port
    # port is str
    def getPortDirection(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Direction for Port {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method setPortDirection(port, direction)
    # Setup direction for GPIO port
    # port is str and direction is str
    def setPortDirection(self, port: str, direction: str) -> None:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if direction == 'input':
                registervalue = 0x00
            else:
                registervalue = 0xff

            if self.debug:
                print("######################################################################")
                print("# Setting Direction for Port {} to {}".format(port.upper(), direction))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeRegister(registeraddr, registervalue)

    # Method getPinDirection(port, pin)
    # Return direction for pin on GPIO port
    # port is str and pin is int
    def getPinDirection(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Pin {} Direction on Port {}".format(pin, port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readBit(registeraddr, pin)
            else:
                return False
        else:
            return False

    # Method setPinDirection(port, pin, direction)
    # Setup direction for pin on GPIO port
    # port is str and pin is int
    def setPinDirection(self, port: str, pin: int, direction: str) -> None:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Setting Pin {} Direction on Port {} to {}".format(pin, port.upper(), direction))
                print("######################################################################")
                print("\r")

            if direction == 'input':
                pindir = 1
            else:
                pindir = 0

            if self.dummy is not True:
                self.i2cdevice.writeBit(registeraddr, pin, pindir)

    # ----- GPIO Polarity -----

    # Method getPortoPolarity(port)
    # Return GPIO Polarity for port
    # port is str
    def getPortoPolarity(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('iopol' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Input Polarity for Port {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method setPortPolarity(port, polarity)
    # Setup GPIO Polarity on Port port
    # port is str and polarity is int
    def setPortPolarity(self, port: str, polarity: int) -> None:
        registeraddr = self.getRegisterAddr('iopol' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Setting Input Polarity for Port {} to {}".format(port.upper(), polarity))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeRegister(registeraddr, polarity)

    # ----- GPIO Interrupt -----

    # Method getPortInterruptConfig(port)
    # Return GPIO Interrupt on Change configuration for port
    # port is str
    def getPortInterruptConfig(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('gpinten' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading GPIO Interrupt Configuration for Port {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method setPortInterruptConfig(port, interruptconf)
    # Setup GPIO Interrupt on Change configuration for port
    # port is str and interrupconfig is int
    def setPortInterruptConfig(self, port: str, interruptconf: int) -> None:
        registeraddr = self.getRegisterAddr('gpinten' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Setting GPIO Interrupt Configuration for Port {} to {}".format(port.upper(), interruptconf))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeRegister(registeraddr, interruptconf)

    # Method getPortCompareDefault(port)
    # Return GPIO Default Compare Value for port
    # port is str
    def getPortCompareDefault(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('defval' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading GPIO Default Compare Value for Port {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method setPortCompareDefault(port, default)
    # Setup GPIO Default Compare Value for port
    # port is str and default is int
    def setPortCompareDefault(self, port: str, default: int) -> None:
        registeraddr = self.getRegisterAddr('defval' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Setting GPIO Default Compare Value for Port {} to {}".format(port.upper(), hex(default)))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeRegister(registeraddr, default)

    # Method getPortCompareMode(port)
    # Return GPIO Compare Mode for port
    # port is str
    def getPortCompareMode(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('intcon' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading GPIO Compare Mode for Port {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method setPortCompareMode(port, default)
    # Setup GPIO Compare Mode for port
    # port is str and default is int
    def setPortCompareMode(self, port: str, compareconfig: int) -> None:
        registeraddr = self.getRegisterAddr('intcon' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Setting GPIO Default Mode for Port {} to {}".format(port.upper(), hex(compareconfig)))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeRegister(registeraddr, compareconfig)

    # Method getPortInterrupt(port)
    # Return GPIO Interrupt on Change Flag for port
    # port is str
    def getPortInterruptFlag(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('intf' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading GPIO Interrupt Configuration for Port {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method getPortInterrupt(port)
    # Return GPIO State When Interrupt on Change Occur for port
    # port is str
    def getPortInterruptCapture(self, port):
        registeraddr = self.getRegisterAddr('intcap' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading GPIO Interrupt Configuration for Port {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # ----- GPIO Pullup Resistor -----

    # Method getPullUpPort(port)
    # Return Value from Port PullUp Register
    # port is str
    def getPullUpPort(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Pull Up Register for Port {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method setPullUpPort(port, pullupdata)
    # Setup Port PullUp Register with pullupdata
    # port is str and pullupdata is int
    def setPullUpPort(self, port: str, pullupdata: int) -> None:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Setting Pull Up Register for Port {} to {}".format(port.upper(), hex(pullupdata)))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeRegister(registeraddr, pullupdata)

    # Method getPullUpPin(port, pin)
    # Return Value for pin from Port PullUp Register
    # port is str and pin is int
    def getPullUpPin(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Pull Up Status for Pin {} on Port {}".format(pin, port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readBit(registeraddr, pin)
            else:
                return False
        else:
            return False

    # Method setPullUpPin(port, pin, pullupstatus)
    # Setup PullUp Resistor for pin Port PullUp Register
    # port is str, pin is int and pullupstatus is bool
    def setPullUpPin(self, port: str, pin: int, pullupstatus: bool) -> None:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Setting Pull Up Status for Pin {} on Port {} to {}".format(pin, port.upper(), pullupstatus))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeBit(registeraddr, pin, pullupstatus)

    # ----- GPIO -----

    # Method readGpio(port)
    # Return GPIO port
    # port is str
    def readGpio(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading GPIO {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method writeGpio(port, data)
    # Write data on GPIO port (Update Output Latch)
    # port is str, data is int
    def writeGpio(self, port: str, data: int) -> None:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Writing Data {} on GPIO {}".format(hex(data), port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeRegister(registeraddr, data)

    # Method readGpioPin(port, pin)
    # Return GPIO Pin Value
    # port is str
    def readGpioPin(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Pin {} on GPIO {}".format(pin, port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readBit(registeraddr, pin)
            else:
                return False
        else:
            return False

    # Method writeGpioPin(port, pin, data)
    # Write data for Pin on GPIO port (Update Output Latch)
    # port is str, pin is int, data is int
    def writeGpioPin(self, port: str, pin: int, data: int) -> None:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Writing Data {} to Pin {} on GPIO {}".format(data, pin, port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeBit(registeraddr, pin, data)

    # Method readOutLatch(port)
    # Return GPIO Output Latch (not actual GPIO State)
    # port is str
    def readOutputLatch(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading GPIO Output Latch {}".format(port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method writeOutputLatch(port, data)
    # Write data on GPIO Output Latch
    # Update Pin configured as output
    # port is str, data is int
    def writeOutputLatch(self, port: str, data: int) -> None:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Writing Data {} on GPIO Output Latch {}".format(hex(data), port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeRegister(registeraddr, data)

    # Method readOutputLatchPin(port, pin)
    # Return GPIO Output Latch Pin state
    # port is str, pin is int
    def readOutputLatchPin(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Pin {} on GPIO Output Latch {}".format(pin, port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readBit(registeraddr, pin)
            else:
                return False
        else:
            return False

    # Method writeOutputLatchPin(port, pin, data)
    # Write data on GPIO Output Latch Pin
    # port is str, pin is int, data is int
    def writeOutputLatchPin(self, port: str, pin: int, data: int) -> None:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Writing Data {} to Pin {} on GPIO Output Latch {}".format(data, pin, port.upper()))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeBit(registeraddr, pin, data)
