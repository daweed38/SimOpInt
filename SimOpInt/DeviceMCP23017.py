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
        return f'This is the Sim Open Interface I2C Device MCP23017 Class'

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

    def __init__(self, devicename: str, deviceaddr: str, deviceintgpio: dict | None, debug: int = 30) -> None:
        super().__init__(devicename, deviceaddr, deviceintgpio)

        self.devicetype = 'MCP23017'
        self.bankmode = 0
        self.registers = self.registers_bank0
        self.pullup = 0
        self.deviceintgpio = deviceintgpio
        self.intgpioa = None
        self.intgpiob = None

        if self.deviceintgpio is not None:
            self.genIntPortGpio()

        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.logger.debug(f'Device {self.devicename}  [Device Addr : {hex(self.deviceaddr)} / Device Type : {self.devicetype}] initialized. (Dummy Device : {self.dummy})')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    def getDeviceIntGPIO(self):
        return self.deviceintgpio

    def getIntPortGPIO(self, port: str) -> int | None:
        if port == 'A':
            return self.intgpioa
        elif port == 'B':
            return self.intgpiob
        else:
            self.logger.error(f'Port {port} not recognized')
            return None

    def setIntPortGPIO(self, port: str, intportgpio: int) -> None:
        if port == 'A':
            self.intgpioa = intportgpio
        elif port == 'B':
            self.intgpiob = intportgpio
        else:
            self.logger.error(f'Port {port} not recognized')

    def getIntChannelPort(self, channel) -> str | bool:
        if channel == self.intgpioa:
            return 'A'
        elif channel == self.intgpiob:
            return 'B'
        else:
            return False

    def genIntPortGpio(self):
        for port in ['A', 'B']:
            if port in self.getIntGpio():
                self.setIntPortGPIO(port, self.getIntGpio()[port])

    ###################################
    # Interrupt CallBack Methods
    ###################################

    def callBackMCP23017(self, channel) -> dict | bool:
        port = self.getIntChannelPort(channel)
        if port in ['A', 'B']:
            intflag = self.getPortInterruptFlag(port)
            intcapture = self.getPortInterruptCapture(port)
            self.logger.debug(f'Interrupt Occurred on channel {channel}: Device {self.devicename} Port {port} {bin(intcapture)} Flag {bin(intflag)}')
            return {'intcapture': intcapture, 'intflag': intflag}
        else:
            return False

    ###################################
    # Standard Register Methods
    ###################################

    # clearAllRegisters() (override DeviceBase)
    # Reset all register declared in
    # registers dict to their initial state
    def resetDeviceRegisters(self) -> None:
        if not self.dummy:
            self.logger.debug(f'Resetting all buffers to their initial state ...')
            for registername in self.registers:
                if self.debug:
                    self.logger.debug(f'Resetting register {registername}')
                    self.writeRegister(self.getRegisterAddr(registername), self.getRegisterInit(registername))
            self.setBankMode(0)
        else:
            self.logger.debug(f'Dummy Device! Cannot write on I2C Bus. No Buffers reset')

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
            if not self.dummy:
                self.logger.debug(f'Setting Device {self.getName()} in Bank Mode {bankmode}')
                if bankmode == 1:
                    self.writeBit(registeraddr, 8, 1)
                    self.registers = self.registers_bank1
                else:
                    self.writeBit(registeraddr, 8, 0)
                    self.registers = self.registers_bank0
                self.bankmode = bankmode
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus. BankMode not changed !')
        else:
            self.logger.error(f'Register iocona not found in self.registers')

    # Method getIntActiveConfig(port)
    # port is str
    # Return Actual Interrupt Active Configuration
    def getIntActiveConfig(self, port: str) -> int:
        register = f'iocon{port.lower()}'
        registeraddr = self.getRegisterAddr(register)
        if registeraddr:
            if not self.dummy:
                intactiveconfig = self.readBit(registeraddr, 2)
                self.logger.debug(f'Interruption Active Configuration on port {port.upper()} is {intactiveconfig}')
                return intactiveconfig
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register {register} not found in self.registers')
            return False

    def setIntActiveConfig(self, port: str, intactiveconfig: int):
        register = f'iocon{port.lower()}'
        registeraddr = self.getRegisterAddr(register)
        if registeraddr:
            if not self.dummy:
                self.logger.debug(f'Setting Interruption Active Configuration on port {port.upper()} to {intactiveconfig}')
                self.writeBit(registeraddr, 2, intactiveconfig)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus. Interruption Active Configuration not changed !')
        else:
            self.logger.error(f'Register {register} not found in self.registers')

    # ----- GPIO Direction -----

    # Method getPortDirection(port)
    # port is str
    # Return data from direction configuration for GPIO Port
    def getPortDirection(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr(f'iodir{port.lower()}')
        if registeraddr is not False:
            if not self.dummy:
                portiodirconfig = self.readRegister(registeraddr)
                self.logger.debug(f'Reading Port {port.upper()} GPIO Direction configuration: {bin(portiodirconfig)}')
                return portiodirconfig
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register iodir{port.lower()} not found in self.registers')
            return False

    # Method setPortDirection(port, direction)
    # port is str (A|B) and direction is str (input|output)
    # Setup direction for GPIO Port
    def setPortDirection(self, port: str, portiodirconfig: str) -> None:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if portiodirconfig == 'input':
                registervalue = 0x00
            else:
                registervalue = 0xff

            if not self.dummy:
                self.logger.debug(f'Setting GPIO Direction configuration Port {port.upper()} as {portiodirconfig}')
                self.writeRegister(registeraddr, registervalue)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register iodir{port.lower()} not found in self.registers')

    # Method getPinDirection(port, pin)
    # port is str (A|B) and pin is int
    # Return direction for pin on GPIO port
    def getPinDirection(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                pindirection = self.readBit(registeraddr, pin)
                self.logger.debug(f'Reading Pin {pin} Direction on Port {port.upper()} : {pindirection}')
                return pindirection
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register iodir{port.lower()} not found in self.registers')
            return False

    # Method setPinDirection(port, pin, piniodirconfig)
    # port is str (A|B) and pin is int and direction is str (input|output)
    # Setup direction for pin on GPIO port
    def setPinDirection(self, port: str, pin: int, piniodirconfig: str) -> None:
        registeraddr = self.getRegisterAddr('iodir' + port.lower())
        if registeraddr is not False:
            if piniodirconfig == 'input':
                piniodir = 1
            else:
                piniodir = 0

            if not self.dummy:
                self.logger.debug(f'Setting Pin {pin} Direction on Port {port.upper()} to {piniodirconfig}')
                self.writeBit(registeraddr, pin, piniodir)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register iodir{port.lower()} not found in self.registers')

    # ----- GPIO Polarity -----

    # Method getPortoPolarity(port)
    # port is str
    # Return GPIO Polarity for port
    def getPortoPolarity(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('iopol' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                portpolarity = self.readRegister(registeraddr)
                self.logger.debug(f'Reading Input Polarity for Port {port.upper()} : {bin(portpolarity)}')
                return portpolarity
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register iopol{port.lower()} not found in self.registers')
            return False

    # Method setPortPolarity(port, polarity)
    # port is str and polarity is int
    # Setup GPIO Polarity on Port port
    def setPortPolarity(self, port: str, polarity: int) -> None:
        registeraddr = self.getRegisterAddr('iopol' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Setting Input Polarity for Port {port.upper()} to {bin(polarity)}')
                self.writeRegister(registeraddr, polarity)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register iopol{port.lower()} not found in self.registers')

    # ----- GPIO Interrupt -----

    # Method getPortInterruptConfig(port)
    # port is str
    # Return GPIO Interrupt on Change configuration for port
    def getPortInterruptConfig(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('gpinten' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                interruptconfig = self.readRegister(registeraddr)
                self.logger.debug(f'Reading GPIO Interrupt Configuration for Port {port.upper()} : {bin(interruptconfig)}')
                return interruptconfig
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register gpinten{port.lower()} not found in self.registers')
            return False

    # Method setPortInterruptConfig(port, interruptconf)
    # port is str and interrupconfig is int
    # Setup GPIO Interrupt on Change configuration for port
    def setPortInterruptConfig(self, port: str, interruptconf: int) -> None:
        registeraddr = self.getRegisterAddr('gpinten' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Setting GPIO Interrupt Configuration for Port {port.upper()} to {bin(interruptconf)}')
                self.writeRegister(registeraddr, interruptconf)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register gpinten{port.lower()} not found in self.registers')

    # Method getPortCompareDefault(port)
    # port is str
    # Return GPIO Default Compare Value for port
    def getPortCompareDefault(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('defval' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                comparedefval = self.readRegister(registeraddr)
                self.logger.debug(f'Reading GPIO Default Compare Value for Port {port.upper()} : {bin(comparedefval)}')
                return comparedefval
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register defval{port.lower()} not found in self.registers')
            return False

    # Method setPortCompareDefault(port, comparedefval)
    # port is str and comparedefval is int
    # Setup GPIO Default Compare Value for port
    def setPortCompareDefault(self, port: str, comparedefval: int) -> None:
        registeraddr = self.getRegisterAddr('defval' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Setting GPIO Default Compare Value for Port {port.upper()} to {bin(comparedefval)}')
                self.writeRegister(registeraddr, comparedefval)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register defval{port.lower()} not found in self.registers')

    # Method getPortCompareMode(port)
    # port is str
    # Return GPIO Compare Mode for port
    def getPortCompareMode(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('intcon' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                comparemodeconfig = self.readRegister(registeraddr)
                self.logger.debug(f'Reading GPIO Compare Mode for Port {port.upper()} : {bin(comparemodeconfig)}')
                return comparemodeconfig
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register intcon{port.lower()} not found in self.registers')
            return False

    # Method setPortCompareMode(port, comparemodeconfig)
    # port is str and comparemodeconfig is int
    # Setup GPIO Compare Mode for port
    def setPortCompareMode(self, port: str, comparemodeconfig: int) -> None:
        registeraddr = self.getRegisterAddr('intcon' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Setting GPIO Default Mode for Port {port.upper()} to {bin(comparemodeconfig)}')
                self.writeRegister(registeraddr, comparemodeconfig)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register intcon{port.lower()} not found in self.registers')

    # Method getPortInterrupt(port)
    # port is str
    # Return GPIO Interrupt on Change Flag for port
    def getPortInterruptFlag(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('intf' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                interruptflagconfig = self.readRegister(registeraddr)
                self.logger.debug(f'Reading GPIO Interrupt Configuration for Port {port.upper()} : {bin(interruptflagconfig)}')
                return interruptflagconfig
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register intf{port.lower()} not found in self.registers')
            return False

    # Method getPortInterrupt(port)
    # port is str
    # Return GPIO State When Interrupt on Change Occur for port
    def getPortInterruptCapture(self, port):
        registeraddr = self.getRegisterAddr('intcap' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                interruptcapture = self.readRegister(registeraddr)
                self.logger.debug(f'Reading GPIO Interrupt Configuration for Port {port.upper()} : {bin(interruptcapture)}')
                return interruptcapture
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register intcap{port.lower()} not found in self.registers')
            return False

    # ----- GPIO Pullup Resistor -----

    # Method getPullUpPort(port)
    # port is str
    # Return Value from Port PullUp Register
    def getPullUpPort(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                pullupconfig = self.readRegister(registeraddr)
                self.logger.debug(f'Reading Pull Up Register for Port {port.upper()} : {pullupconfig}')
                return pullupconfig
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register gppu{port.lower()} not found in self.registers')
            return False

    # Method setPullUpPort(port, pullupconfig)
    # Setup Port PullUp Register with pullupconfig
    # port is str and pullupconfig is int
    def setPullUpPort(self, port: str, pullupconfig: int) -> None:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Setting Pull Up Register for Port {port.upper()} to {pullupconfig}')
                self.writeRegister(registeraddr, pullupconfig)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register gppu{port.lower()} not found in self.registers')

    # Method getPullUpPin(port, pin)
    # port is str and pin is int
    # Return Value for pin from Port PullUp Register
    def getPullUpPin(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                pinpullupconfig = self.readBit(registeraddr, pin)
                self.logger.debug(f'Reading Pull Up Status for Pin {pin} on Port {port.upper()} : {pinpullupconfig}')
                return pinpullupconfig
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register gppu{port.lower()} not found in self.registers')
            return False

    # Method setPullUpPin(port, pin, pinpullupconfig)
    # port is str, pin is int and pinpullupconfig is bool
    # Setup PullUp Resistor for pin Port PullUp Register
    def setPullUpPin(self, port: str, pin: int, pinpullupconfig: bool) -> None:
        registeraddr = self.getRegisterAddr('gppu' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Setting Pull Up Status for Pin {pin} on Port {port.upper()} to {pinpullupconfig}')
                self.writeBit(registeraddr, pin, pinpullupconfig)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register gppu{port.lower()} not found in self.registers')

    # ----- GPIO -----

    # Method readGpio(port)
    # port is str
    # Return GPIO port
    def readGpio(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                gpiodata = self.readRegister(registeraddr)
                self.logger.debug(f'Reading GPIO {port.upper()} : {gpiodata}')
                return gpiodata
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register gpio{port.lower()} not found in self.registers')
            return False

    # Method writeGpio(port, data)
    # port is str, data is int
    # Write data on GPIO port (Update Output Latch)
    def writeGpio(self, port: str, data: int) -> None:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Writing Data {data} on GPIO {port.upper()}')
                self.writeRegister(registeraddr, data)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register gpio{port.lower()} not found in self.registers')

    # Method readGpioPin(port, pin)
    # port is str
    # Return GPIO Pin Value
    def readGpioPin(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                gpiopindata = self.readBit(registeraddr, pin)
                self.logger.debug(f'Reading Pin {pin} on GPIO {port.upper()} : {gpiopindata}')
                return gpiopindata
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register gpio{port.lower()} not found in self.registers')
            return False

    # Method writeGpioPin(port, pin, data)
    # port is str, pin is int, data is int
    # Write data for Pin on GPIO port (Update Output Latch)
    def writeGpioPin(self, port: str, pin: int, data: int) -> None:
        registeraddr = self.getRegisterAddr('gpio' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Writing Data {data} to Pin {pin} on GPIO {port.upper()}')
                self.writeBit(registeraddr, pin, data)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register gpio{port.lower()} not found in self.registers')

    # Method readOutLatch(port)
    # port is str
    # Return GPIO Output Latch (not actual GPIO State)
    def readOutputLatch(self, port: str) -> int | bool:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                latchdata = self.readRegister(registeraddr)
                self.logger.debug(f'Reading GPIO Output Latch {port.upper()} : {latchdata}')
                return latchdata
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register olat{port.lower()} not found in self.registers')
            return False

    # Method writeOutputLatch(port, data)
    # port is str, data is int
    # Write data on GPIO Output Latch
    # Update Pin configured as output
    def writeOutputLatch(self, port: str, data: int) -> None:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Writing Data {data} on GPIO Output Latch {port.upper()}')
                self.writeRegister(registeraddr, data)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register olat{port.lower()} not found in self.registers')

    # Method readOutputLatchPin(port, pin)
    # port is str, pin is int
    # Return GPIO Output Latch Pin state
    def readOutputLatchPin(self, port: str, pin: int) -> int | bool:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                pinlatchdata = self.readBit(registeraddr, pin)
                self.logger.debug(f'Reading Pin {pin} on GPIO Output Latch {port.upper()} : {pinlatchdata}')
                return pinlatchdata
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register olat{port.lower()} not found in self.registers')
            return False

    # Method writeOutputLatchPin(port, pin, data)
    # port is str, pin is int, data is int
    # Write data on GPIO Output Latch Pin
    def writeOutputLatchPin(self, port: str, pin: int, data: int) -> None:
        registeraddr = self.getRegisterAddr('olat' + port.lower())
        if registeraddr is not False:
            if not self.dummy:
                self.logger.debug(f'Writing Data {data} to Pin {pin} on GPIO Output Latch {port.upper()}')
                self.writeBit(registeraddr, pin, data)
            else:
                self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
        else:
            self.logger.error(f'Register olat{port.lower()} not found in self.registers')
