# System Modules Import
from datetime import datetime
# Device Base Import
from DeviceBase import DeviceBase

##################################################
# FarmerSoft Sim Open Interface Device Class
##################################################
# HT16K33 Class (Pack LED) REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class HT16K33(DeviceBase):
    """
    This class allow the HT16K33 object creation
    to manage an HT16K33 I2C hardware device
    HT16K33 : Backpack LED I2C.
    Copyright FarmerSoft © 2023 By Daweed
    """

    ########################################
    # Properties
    ########################################

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

    ########################################
    # Constructor
    ########################################

    def __init__(self, devicename: str, deviceaddr: str, dummy: bool = False, debug: bool = False) -> None:
        super().__init__(devicename, deviceaddr, dummy, debug)

        self.devicetype = 'HT16K33'

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

    # configMCP(state) (Override from DeviceBase)
    # Enable or Disable the device
    # state is int
    def configMCP(self, state: int) -> None:
        if state == 1 and self.state == 0:
            if self.debug:
                print("######################################################################")
                print("# Device {} Started at {}".format(self.devicename, datetime.now()))
                print("######################################################################")
                print("\r")

            # Turning On System Oscillator
            if self.dummy is not True:
                self.i2cdevice.writeDevice(self.system_cmd_base | 1)
            self.state = 1

        elif state == 0 and self.state == 1:
            if self.debug:
                print("######################################################################")
                print("# Device {} Stopped at {}".format(self.devicename, datetime.now()))
                print("######################################################################")
                print("\r")

            # Turning Off System Oscillator
            if self.dummy is not True:
                self.i2cdevice.writeDevice(self.system_cmd_base)
            self.state = 0

        self.resetDeviceRegisters()

    # start() (Override from DeviceBase)
    # Start the device's intervening oscillator
    def start(self) -> int:
        if self.state != 1:
            self.configMCP(1)
            if self.dummy is not True:
                # Setting Display Status to On
                self.i2cdevice.writeDevice(self.display_cmd_base | 1)
        return self.state

    # Method stop() (Override from DeviceBase)
    # Stop the device's internal oscillator
    def stop(self) -> int:
        if self.state != 0:
            self.configMCP(0)
            if self.dummy is not True:
                # Setting Display Status to Off
                self.i2cdevice.writeDevice(self.display_cmd_base)
        return self.state

    ########################################
    # Standard Register Methods
    ########################################

    ########################################
    # HT16K33 Device Management Methods
    ########################################

    # getRowRegister(port, row)
    # Return register address regarding common & port
    # port is str and row is int
    def getRowRegisterAddr(self, port: str, row: int) -> int | bool:
        if port in ['a', 'A', 'b', 'B']:
            register = 'row'+port.lower()+str(row)
            registeraddr = self.getRegisterAddr(register)
            return registeraddr
        else:
            return False

    # readInterruptRegister()
    # return Interruption Register value
    def readInterruptRegister(self) -> int | bool:
        registeraddr = self.getRegisterAddr('inter')
        if self.debug:
            print("######################################################################")
            print("# Reading Interrupt Register at Address {}".format(hex(registeraddr)))
            print("######################################################################")
            print("\r")
        if self.dummy is not True:
            return self.i2cdevice.readRegister(registeraddr)
        else:
            return False

    # setBrightness(brightness)
    # Adjust the Outputs brightness in range 1 -> 15
    # brightness is int
    def setBrightness(self, brightness: int) -> None:
        birghtness_cmd = self.brightness_cmd_base | brightness
        if self.debug:
            print("######################################################################")
            print("# Updating Displays Brightness to {}".format(brightness))
            print("######################################################################")
            print("\r")

        if self.dummy is not True:
            self.i2cdevice.writeDevice(birghtness_cmd)

    # setBlinkRate(blinkrate)
    # Set output blinking frequency
    # blinkrate is str
    def setBlinkRate(self, blinkrate: str) -> None:
        if self.debug:
            print("######################################################################")
            print("# Updating Blink Rate Frequency : {}".format(blinkrate))
            print("######################################################################")
            print("\r")

        if blinkrate in self.blinkrate:
            blinkrate_cmd = self.system_cmd_base | 1 | self.blinkrate[blinkrate]
            if self.dummy is not True:
                self.i2cdevice.writeDevice(blinkrate_cmd)

    # getScanRow(row, port)
    # Return Value from row register on port
    # row is int and port is str
    def getRow(self, row: int, port: str) -> int | bool:
        registeraddr = self.getRowRegisterAddr(port.lower(), row)
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Row {} On Port {}".format(row, port.lower()))
                print("# Row Register Address : {}".format(hex(registeraddr)))
                print("######################################################################")
                print("\r")
            if self.dummy is not True:
                return self.i2cdevice.readRegister(registeraddr)
            else:
                return False
        else:
            return False

    # setRow(row, port, data)
    # Update the Row register Value on Port port
    # row is int , port is str and data is int
    def setRow(self, row: int, port: str, data: int) -> None:
        registeraddr = self.getRowRegisterAddr(port.lower(), row)
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Updating Row {} on Port {} to value {}".format(row, port.lower(), hex(data)))
                print("# Row Register Address : {}".format(hex(registeraddr)))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeRegister(registeraddr, data)

    # getOut(row, port, out)
    # Read Output in Row on Port
    # row is int, port is str and out is int
    def getOut(self, row: int, port: str, out: int) -> int | bool:
        registeraddr = self.getRowRegisterAddr(port.lower(), row)
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Reading Output {} In Row {} On Port {}".format(out, row, port.lower()))
                print("# Row Register Address : {}".format(hex(registeraddr)))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                return self.i2cdevice.readBit(registeraddr, out)
            else:
                return False
        else:
            return False

    # setOut(row, port, out, state)
    # Update Output in Row on Port
    # row is int, port is str, out is int and state is int
    def setOut(self, row: int, port: str, out: int, state: int) -> None:
        registeraddr = self.getRowRegisterAddr(port.lower(), row)
        if registeraddr is not False:
            if self.debug:
                print("######################################################################")
                print("# Updating Output {} In Row {} On Port {} to State {}".format(out, row, port.lower(), state))
                print("# Row Register Address : {}".format(hex(registeraddr)))
                print("######################################################################")
                print("\r")

            if self.dummy is not True:
                self.i2cdevice.writeBit(registeraddr, out, state)
