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

    def __init__(self, i2cdriver, i2cbus, devicename: str, deviceaddr: str, debug: bool = False) -> None:

        self.debug = debug
        self.i2cdriver = i2cdriver
        self.i2c = i2cbus
        self.devicetype = 'Base'
        self.devicename = devicename
        self.deviceaddr = int(deviceaddr, 16)
        self.state = 0

        if self.i2cdriver == 'ftdi':
            self.i2cdevice = self.i2c.get_port(self.deviceaddr)
        else:
            self.i2cdevice = None

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
                print(f"######################################################################")
                print(f"# Device {self.devicename} Started at {datetime.now()}")
                print(f"######################################################################")
                print("\r")

            self.state = 1

        elif state == 0 and self.state == 1:
            if self.debug:
                print(f"######################################################################")
                print(f"# Device {self.devicename} Stopped at {datetime.now()}")
                print(f"######################################################################")
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
    # Register Methods
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
                print(f"######################################################################")
                print(f"# Register {register} Address on Device {self.devicename} is {hex(registeraddr)}")
                print(f"######################################################################")
                print("\r")
        else:
            registeraddr = False
            if self.debug:
                print(f"######################################################################")
                print(f"# Register {register} not found in registers dict for device {self.devicename}")
                print(f"######################################################################")
                print("\r")

        return registeraddr

    # Method getRegisterInit(register)
    # Return Register Init Value
    # register is str
    def getRegisterInit(self, register: str) -> int | bool:
        if register in self.registers:
            registerinit = self.registers[register]['init']
            if self.debug:
                print(f"######################################################################")
                print(f"# Register {register} Init Value on Device {self.devicename} is {hex(registerinit)}")
                print(f"######################################################################")
                print("\r")
        else:
            registerinit = False
            if self.debug:
                print(f"######################################################################")
                print(f"# Register {register} not found in registers dict for device {self.devicename}")
                print(f"######################################################################")
                print("\r")

        return registerinit

    # clearAllRegisters()
    # Reset all register declared in
    # registeraddr dict to their initial state
    def resetDeviceRegisters(self) -> None:
        if self.debug:
            print("######################################################################")
            print("# Resetting All Buffers")
            print("######################################################################")
            print("\r")

        for register in self.registers:
            initvalue = self.getRegisterInit(register)
            registeraddr = self.getRegisterAddr(register)

            if self.debug:
                print(f"# Resetting Register {register} at Address {hex(registeraddr)} to {initvalue}")

            self.writeRegister(registeraddr, initvalue)

    ########################################
    # Device Methods
    ########################################

    # Method readDevice()
    # Return one bytes from device
    def readDevice(self) -> int | None:
        if self.i2cdriver == 'rpi':
            data = self.i2c.read_byte(self.deviceaddr)
        elif self.i2cdriver == 'ftdi':
            data = int.from_bytes(self.i2cdevice.read(1), 'big')
        else:
            data = None

        if self.debug == 3:
            print(f"######################################################################")
            print(f"# Reading Device {self.devicename} : {hex(data)}")
            print(f"######################################################################")
            print("\r")

        return data

    # Method writeDevice(data)
    # Write data to device
    def writeDevice(self, data) -> None:
        if int(self.debug) == 3:
            print(f"######################################################################")
            print(f"# Writing Data {data} to Device {self.devicename}")
            print(f"######################################################################")
            print("\r")

        if self.i2cdriver == 'rpi':
            self.i2c.write_byte(self.deviceaddr, data)
        elif self.i2cdriver == 'ftdi':
            self.i2cdevice.write([data])
        else:
            pass

    # readRegister(registeraddr)
    # Return value from Device Register at registeraddr Address
    def readRegister(self, registeraddr) -> int | None:
        if self.i2cdriver == 'rpi':
            data = self.i2c.read_byte_data(self.deviceaddr, registeraddr)
        elif self.i2cdriver == 'ftdi':
            data = int.from_bytes(self.i2cdevice.read_from(registeraddr, 1), 'big')
        else:
            data = None

        if int(self.debug) == 3:
            print(f"######################################################################")
            print(f"# Reading Value from Register at Address {hex(registeraddr)} : {hex(data)}")
            print(f"######################################################################")
            print("\r")

        return data

    # writeRegister(registeraddr, registervalue)
    # Write Value on Device Register at registeraddr Address
    def writeRegister(self, registeraddr, data) -> None:
        if int(self.debug) == 3:
            print(f"######################################################################")
            print(f"# Writing Value {hex(data)} to Register at Address {hex(registeraddr)}")
            print(f"######################################################################")
            print("\r")

        if self.i2cdriver == 'rpi':
            self.i2c.write_byte_data(self.deviceaddr, registeraddr, data)
        elif self.i2cdriver == 'ftdi':
            self.i2cdevice.write_to(registeraddr, [data])
        else:
            pass

    # Method readBit(registeraddr, bit)
    # Return Bit value from Register at registeraddr
    def readBit(self, registeraddr, bit) -> int:
        mask = self.maskup[bit]
        bitvalue = self.readRegister(registeraddr) & mask
        if int(self.debug) == 3:
            print(f"######################################################################")
            print(f"# Reading Bit {bit} Value from Register at Address {hex(registeraddr)} : {bitvalue}")
            print(f"######################################################################")
            print("\r")

        if int(bitvalue) > 0:
            return 1
        else:
            return 0

    # Method writeBit(registeraddr, bit, state)
    # Write 1|0 to Bit on Register at registeraddr
    def writeBit(self, registeraddr, bit, state) -> None:
        registerdata = self.readRegister(registeraddr)
        if state == 1:
            maskname = 'maskup'
            operation = 'OR'
            mask = self.maskup[bit]
            newregisterdata = registerdata | mask
        else:
            maskname = 'maskdown'
            operation = 'AND'
            mask = self.maskdown[bit]
            newregisterdata = registerdata & mask

        if int(self.debug) == 3:
            print(f"######################################################################")
            print(f"# Writing Value {state} to Bit {bit} from Register at Address {hex(registeraddr)}")
            print(f"######################################################################")
            print("\r")

        self.writeRegister(registeraddr, newregisterdata)
