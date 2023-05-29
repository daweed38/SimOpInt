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

    def __init__(self, i2cdriver, i2cbus, devicename: str, deviceaddr: str, debug=False) -> None:
        super().__init__(i2cdriver, i2cbus, devicename, deviceaddr, debug)

        self.devicetype = 'MCP23017'
        self.bankmode = 0
        self.registers = self.registers_bank0
        self.pullup = 0

        if self.debug:
            print(f"######################################################################")
            print(f"# Device {self.devicename} Addr {hex(self.deviceaddr)} initialization at {datetime.now()}")
            print(f"######################################################################")
            print("\r")

    ########################################
    # Destructor
    ########################################

    def __del__(self) -> None:

        if self.debug:
            print(f"######################################################################")
            print(f"# Device {self.devicename} removed at {datetime.now()}")
            print(f"######################################################################")
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
                print(f"######################################################################")
                print(f"# Setting Device {self.getName()} in Bank Mode {bankmode}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                if bankmode == 1:
                    self.writeBit(registeraddr, 8, 1)
                    self.registers = self.registers_bank1
                else:
                    self.writeBit(registeraddr, 8, 0)
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
                print(f"######################################################################")
                print(f"# Reading Direction for Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
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
                print(f"######################################################################")
                print(f"# Setting Direction for Port {port.upper()} to {direction}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeRegister(registeraddr, registervalue)

    # Method getPinDirection(port, pin)
    # Return direction for pin on GPIO port
    # port is str and pin is int
    def getPinDirection(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading Pin {pin} Direction on Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readBit(registeraddr, pin)
            else:
                return False
        else:
            return False

    # Method setPinDirection(port, pin, direction)
    # Setup direction for pin on GPIO port
    # port is str and pin is int
    # dir is 'input' or 'output'
    def setPinDirection(self, port: str, pin: int, direction: str) -> None:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Setting Pin {pin} Direction on Port {port.upper()} to {direction}")
                print(f"######################################################################")
                print("\r")

            if direction == 'input':
                pindir = 1
            else:
                pindir = 0

            if self.i2cdriver != 'dummy':
                self.writeBit(registeraddr, pin, pindir)

    # ----- GPIO Polarity -----

    # Method getPortoPolarity(port)
    # Return GPIO Polarity for port
    # port is str
    def getPortoPolarity(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('iopol' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading Input Polarity for Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
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
                print(f"######################################################################")
                print(f"# Setting Input Polarity for Port {port.upper()} to {polarity}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeRegister(registeraddr, polarity)

    # ----- GPIO Interrupt -----

    # Method getPortInterruptConfig(port)
    # Return GPIO Interrupt on Change configuration for port
    # port is str
    def getPortInterruptConfig(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('gpinten' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading GPIO Interrupt Configuration for Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # Method setPortInterruptConfig(port, interruptconf)
    # Setup GPIO Interrupt on Change configuration for port
    # port is str and interruptconf is int
    def setPortInterruptConfig(self, port: str, interruptconf: int) -> None:
        registeraddr = self.getRegisterAddr('gpinten' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Setting GPIO Interrupt Configuration for Port {port.upper()} to {interruptconf}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeRegister(registeraddr, interruptconf)

    # Method getPortCompareDefault(port)
    # Return GPIO Default Compare Value for port
    # port is str
    def getPortCompareDefault(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('defval' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading GPIO Default Compare Value for Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
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
                print(f"######################################################################")
                print(f"# Setting GPIO Default Compare Value for Port {port.upper()} to {hex(default)}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeRegister(registeraddr, default)

    # Method getPortCompareMode(port)
    # Return GPIO Compare Mode for port
    # port is str
    def getPortCompareMode(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('intcon' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading GPIO Compare Mode for Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
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
                print(f"######################################################################")
                print(f"# Setting GPIO Default Mode for Port {port.upper()} to {hex(compareconfig)}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeRegister(registeraddr, compareconfig)

    # Method getPortInterrupt(port)
    # Return GPIO Interrupt on Change Flag for port
    # port is str
    def getPortInterruptFlag(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('intf' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading GPIO Interrupt Configuration for Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
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
                print(f"######################################################################")
                print(f"# Reading GPIO Interrupt Configuration for Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
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
                print(f"######################################################################")
                print(f"# Reading Pull Up Register for Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
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
                print(f"######################################################################")
                print(f"# Setting Pull Up Register for Port {port.upper()} to {hex(pullupdata)}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeRegister(registeraddr, pullupdata)

    # Method getPullUpPin(port, pin)
    # Return Value for pin from Port PullUp Register
    # port is str and pin is int
    def getPullUpPin(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading Pull Up Status for Pin {pin} on Port {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readBit(registeraddr, pin)
            else:
                return False
        else:
            return False

    # Method setPullUpPin(port, pin, pullupstatus)
    # Setup PullUp Resistor for pin Port PullUp Register
    # port is str, pin is int and pullupstatus is bool
    def setPullUpPin(self, port: str, pin: int, pullupstatus: int) -> None:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Setting Pull Up Status for Pin {pin} on Port {port.upper()} to {pullupstatus}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeBit(registeraddr, pin, pullupstatus)

    # ----- GPIO -----

    # Method readGpio(port)
    # Return GPIO port
    # port is str
    def readGpio(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading GPIO {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
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
                print(f"######################################################################")
                print(f"# Writing Data {hex(data)} on GPIO {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeRegister(registeraddr, data)

    # Method readGpioPin(port, pin)
    # Return GPIO Pin Value
    # port is str
    def readGpioPin(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading Pin {pin} on GPIO {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readBit(registeraddr, pin)
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
                print(f"######################################################################")
                print(f"# Writing Data {data} to Pin {pin} on GPIO {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeBit(registeraddr, pin, data)

    # Method readOutLatch(port)
    # Return GPIO Output Latch (not actual GPIO State)
    # port is str
    def readOutputLatch(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading GPIO Output Latch {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readRegister(registeraddr)
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
                print(f"######################################################################")
                print(f"# Writing Data {hex(data)} on GPIO Output Latch {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeRegister(registeraddr, data)

    # Method readOutputLatchPin(port, pin)
    # Return GPIO Output Latch Pin state
    # port is str, pin is int
    def readOutputLatchPin(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if self.debug:
                print(f"######################################################################")
                print(f"# Reading Pin {pin} on GPIO Output Latch {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                return self.readBit(registeraddr, pin)
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
                print(f"######################################################################")
                print(f"# Writing Data {data} to Pin {pin} on GPIO Output Latch {port.upper()}")
                print(f"######################################################################")
                print("\r")

            if self.i2cdriver != 'dummy':
                self.writeBit(registeraddr, pin, data)
