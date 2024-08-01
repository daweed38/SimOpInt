##################################################
# FarmerSoft Sim Open Interface MCP23017 Device Class
##################################################
# HT16K33 Device Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging
from datetime import datetime

# SimOpInt Import
from SimOpInt.DeviceBase import DeviceBase


class HT16K33(DeviceBase):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface I2C Device Base Class'

    ###################################
    # Properties
    ###################################

    system_cmd_base = 0x20
    display_cmd_base = 0x80
    brightness_cmd_base = 0xe0

    blinkrate = {
        'blinkoff': 0x00, 'blink2hz': 0x02, 'blink1hz': 0x04, 'blinkhlf': 0x06
    }

    registers = {
        'rowa1': {'addr': 0x00, 'init': 0x00},
        'rowa2': {'addr': 0x02, 'init': 0x00},
        'rowa3': {'addr': 0x04, 'init': 0x00},
        'rowa4': {'addr': 0x06, 'init': 0x00},
        'rowa5': {'addr': 0x08, 'init': 0x00},
        'rowa6': {'addr': 0x0a, 'init': 0x00},
        'rowa7': {'addr': 0x0c, 'init': 0x00},
        'rowa8': {'addr': 0x0e, 'init': 0x00},
        'rowb1': {'addr': 0x01, 'init': 0x00},
        'rowb2': {'addr': 0x03, 'init': 0x00},
        'rowb3': {'addr': 0x05, 'init': 0x00},
        'rowb4': {'addr': 0x07, 'init': 0x00},
        'rowb5': {'addr': 0x09, 'init': 0x00},
        'rowb6': {'addr': 0x0b, 'init': 0x00},
        'rowb7': {'addr': 0x0d, 'init': 0x00},
        'rowb8': {'addr': 0x0f, 'init': 0x00},
        'inter': {'addr': 0x60, 'init': 0x00}
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

        self.devicetype = 'HT16K33'

        self.logger.debug(f'Device {self.devicename}  [Device Addr : {hex(self.deviceaddr)} / Device Type : {self.devicetype}] initialized. (Dummy Device : {self.dummy})')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    # configMCP(state) (Override from DeviceBase)
    # state is int
    # Enable or Disable the device
    def configMCP(self, state: int) -> None:
        if state == 1 and self.state == 0:
            self.logger.debug(f'Device {self.devicename} Started at {datetime.now()}')

            # Turning On System Oscillator
            if not self.dummy:
                self.writeDevice(self.system_cmd_base | 1)
            self.state = 1

        elif state == 0 and self.state == 1:
            self.logger.debug(f'Device {self.devicename} Stopped at {datetime.now()}')

            # Turning Off System Oscillator
            if not self.dummy:
                self.writeDevice(self.system_cmd_base)
            self.state = 0

        self.resetDeviceRegisters()

    # start() (Override from DeviceBase)
    # Start the device's intervening oscillator
    def start(self) -> int:
        if self.state != 1:
            self.configMCP(1)
            if not self.dummy:
                # Setting Display Status to On
                self.writeDevice(self.display_cmd_base | 1)
        return self.state

    # stop() (Override from DeviceBase)
    # Stop the device's internal oscillator
    def stop(self) -> int:
        if self.state != 0:
            self.configMCP(0)
            if not self.dummy:
                # Setting Display Status to Off
                self.writeDevice(self.display_cmd_base)
        return self.state

    ###################################
    # Standard Register Methods
    ###################################

    ###################################
    # HT16K33 Device Management Methods
    ###################################

    # getRowRegister(port, row)
    # port is str and row is int
    # Return register address regarding common & port
    def getRowRegisterAddr(self, port: str, row: int) -> int | bool:
        if port.lower() in ['a', 'b']:
            register = 'row' + port.lower() + str(row)
            registeraddr = self.getRegisterAddr(register)
            return registeraddr
        else:
            return False

    # readInterruptRegister()
    # return Interruption Register value
    def readInterruptRegister(self) -> int | bool:
        registeraddr = self.getRegisterAddr('inter')
        if registeraddr is not False:
            if not self.dummy:
                registervalue = self.readRegister(registeraddr)
                self.logger.debug(f'Reading Interrupt Register at Address {hex(registeraddr)} : {registervalue}')
                return registervalue
            else:
                self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
                return False
        else:
            self.logger.error(f'Register inter not found in self.registers')
            return False

    # setBrightness(brightness)
    # brightness is int
    # Adjust the Outputs brightness in range 1 -> 15
    def setBrightness(self, brightness: int) -> None:
        birghtness_cmd = self.brightness_cmd_base | brightness

        if not self.dummy:
            self.logger.debug(f'Updating Displays Brightness to {brightness}')
            self.writeDevice(birghtness_cmd)

    # setBlinkRate(blinkrate)
    # blinkrate is str
    # Set output blinking frequency
    def setBlinkRate(self, blinkrate: str) -> None:
        if self.debug:
            print("######################################################################")
            print("# Updating Blink Rate Frequency : {}".format(blinkrate))
            print("######################################################################")
            print("\r")

        if blinkrate in self.blinkrate:
            blinkrate_cmd = self.system_cmd_base | 1 | self.blinkrate[blinkrate]
            if not self.dummy:
                self.i2cdevice.writeDevice(blinkrate_cmd)

    # getScanRow(row, port)
    # row is int and port is str
    # Return Value from row register on port
    def getRow(self, row: int, port: str) -> int | bool:
        registeraddr = self.getRowRegisterAddr(port.lower(), row)
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Row {} On Port {}".format(row, port.lower()))
                print("# Row Register Address : {}".format(hex(registeraddr)))
                print("######################################################################")
                print("\r")
            if not self.dummy:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # setRow(row, port, data)
    # row is int , port is str and data is int
    # Update the Row register Value on Port port
    def setRow(self, row: int, port: str, data: int) -> None:
        registeraddr = self.getRowRegisterAddr(port.lower(), row)
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Updating Row {} on Port {} to value {}".format(row, port.lower(), hex(data)))
                print("# Row Register Address : {}".format(hex(registeraddr)))
                print("######################################################################")
                print("\r")

            if not self.dummy:
                self.i2cdevice.writeRegister(registeraddr, data)

    # getOut(row, port, out)
    # row is int, port is str and out is int
    # Read Output in Row on Port
    def getOut(self, row: int, port: str, out: int) -> int | bool:
        registeraddr = self.getRowRegisterAddr(port.lower(), row)
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Output {} In Row {} On Port {}".format(out, row, port.lower()))
                print("# Row Register Address : {}".format(hex(registeraddr)))
                print("######################################################################")
                print("\r")

            if not self.dummy:
                return self.i2cdevice.readBit(registeraddr, out)
            else:
                return False
        else:
            return False

    # setOut(row, port, out, state)
    # row is int, port is str, out is int and state is int
    # Update Output in Row on Port
    def setOut(self, row: int, port: str, out: int, state: int) -> None:
        registeraddr = self.getRowRegisterAddr(port.lower(), row)
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Updating Output {} In Row {} On Port {} to State {}".format(out, row, port.lower(), state))
                print("# Row Register Address : {}".format(hex(registeraddr)))
                print("######################################################################")
                print("\r")

            if not self.dummy:
                self.i2cdevice.writeBit(registeraddr, out, state)
