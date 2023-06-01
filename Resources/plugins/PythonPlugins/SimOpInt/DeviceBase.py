# System Modules Import
from datetime import datetime

##################################################
# FarmerSoft Sim Open Interface Device Class
##################################################
# Base Device Class REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class DeviceBase:
    """
    SimOpInt Device Base Class
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    maskup = {
        1: 0b00000001, 2: 0b00000010, 3: 0b00000100, 4: 0b00001000,
        5: 0b00010000, 6: 0b00100000, 7: 0b01000000, 8: 0b10000000
    }

    maskdown = {
        1: 0b11111110, 2: 0b11111101, 3: 0b11111011, 4: 0b11110111,
        5: 0b11101111, 6: 0b11011111, 7: 0b10111111, 8: 0b01111111
    }

    registers = {

    }

    ########################################
    # Constructor
    ########################################

    def __init__(self, devicename: str, deviceaddr: str, dummy: bool = False, debug: bool = False) -> None:

        self.debug = debug
        self.dummy = dummy
        self.devicetype = 'Base'
        self.devicename = devicename
        self.deviceaddr = int(deviceaddr, 16)
        self.i2cdevice = False
        self.state = 0

        if self.dummy is not True:
            from SimOpIntI2C import I2CDevice
            self.i2cdevice = I2CDevice(self.devicename, self.deviceaddr, self.debug)

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

    ########################################
    # System Methods
    ########################################

    # getDebugLevel()
    # return Device Debug Mode Status
    def getDebugLevel(self) -> bool:
        return self.debug

    # setDebugLevel(debuglevel)
    # Set Device Debug Mode
    # debuglevel is bool
    def setDebugLevel(self, debuglevel: bool) -> None:
        self.debug = debuglevel

    # getName()
    # return device name
    def getName(self) -> str:
        return self.devicename

    # getType()
    # return device type
    def getType(self) -> str:
        return self.devicetype

    # getAddress()
    # return device address
    def getAddress(self) -> int:
        return self.deviceaddr

    # getHexAddress()
    # return device address hex formated
    def getHexAddress(self) -> str:
        return hex(self.deviceaddr)

    # getStatus()
    # return device status
    def getStatus(self) -> int:
        return self.state

    # setStatus(state)
    # set Device status to state
    # state is int
    def setStatus(self, state: int) -> None:
        self.state = state

    ########################################
    # Configuration
    ########################################

    # configMCP(state)
    # Enable or Disable the device
    # state is int
    def configMCP(self, state: int) -> None:
        if state == 1 and self.state == 0:
            if self.debug:
                print("######################################################################")
                print("# Device {} Started at {}".format(self.devicename, datetime.now()))
                print("######################################################################")
                print("\r")

            self.state = 1

        elif state == 0 and self.state == 1:
            if self.debug:
                print("######################################################################")
                print("# Device {} Stopped at {}".format(self.devicename, datetime.now()))
                print("######################################################################")
                print("\r")

            self.state = 0

        self.resetDeviceRegisters()

    # start()
    # Start the device's intervening oscillator
    def start(self) -> int:
        if self.state != 1:
            self.configMCP(1)
        return self.state

    # stop()
    # Stop the device's internal oscillator
    def stop(self) -> int:
        if self.state != 0:
            self.configMCP(0)
        return self.state

    ########################################
    # Standard Register Methods
    ########################################

    # Method listRegister():
    # Return Register List
    def listRegisters(self) -> dict:
        return self.registers

    # Method getRegisterAddr(register)
    # Return Register Address
    # register is str
    def getRegisterAddr(self, register: str) -> int | bool:
        if register in self.registers:
            registeraddr = self.registers[register]['addr']
            if self.debug:
                print("######################################################################")
                print("# Register {} Address on Device {} is {}".format(register, self.devicename, hex(registeraddr)))
                print("######################################################################")
                print("\r")
        else:
            registeraddr = False
            if self.debug:
                print("######################################################################")
                print("# Register {} not found in registers dict for device {}".format(register, self.devicename))
                print("######################################################################")
                print("\r")

        return registeraddr

    # Method getRegisterInit(register)
    # Return Register Init Value
    # register is str
    def getRegisterInit(self, register: str) -> int | bool:
        if register in self.registers:
            registerinit = self.registers[register]['init']
            if self.debug:
                print("######################################################################")
                print("# Register {} Init Value on Device {} is {}".format(register, self.devicename, hex(registerinit)))
                print("######################################################################")
                print("\r")
        else:
            registerinit = False
            if self.debug:
                print("######################################################################")
                print("# Register {} not found in registers dict for device {}".format(register, self.devicename))
                print("######################################################################")
                print("\r")

        return registerinit

    # clearAllRegisters()
    # Reset all register declared in
    # registeradd dict to their initial state
    def resetDeviceRegisters(self) -> None:
        reset = True
        if self.debug:
            print("######################################################################")
            print("# Resetting All Buffers")
            print("######################################################################")
            print("\r")

        for register in self.registers:
            if self.debug:
                print("# Reseting Register {}".format(register))
            if self.dummy is not True:
                self.i2cdevice.writeRegister(self.getRegisterAddr(register), self.getRegisterInit(register))