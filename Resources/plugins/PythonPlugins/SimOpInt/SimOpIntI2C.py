#!/usr/bin/env python3
# -*-coding:Utf-8 -*

# import smbus2

##################################################
# FarmerSoft Open Interface I2C Class
##################################################
# I2C Class (I2C Bus Devices)
# FarmerSoft © 2022
# By Daweed
##################################################


class I2CBus:
    """
    Class to create an I2C Bus
    """

    ###############
    # Properties
    ###############

    ###############
    # Constructor
    ###############

    def __init__(self, i2cdriver, i2cbusaddr):
        if i2cdriver == 'rpi':
            import smbus2
            self.i2c = smbus2.SMBus(i2cbusaddr)
        elif i2cdriver == 'ftdi':
            from pyftdi.i2c import I2cController
            self.i2c = I2cController()
            self.i2c.configure(i2cbusaddr, frequency=400000.0)
        else:
            self.i2c = 'dummy'

    ###############
    # Destructor
    ###############

    def __del__(self):
        self.i2c = None

    ###############
    # Destructor
    ###############

    def getBus(self):
        return self.i2c

    """
    def scan(self):
        # Try to read a byte from each address, if you get an OSError
        # it means the device isnt there
        found = []
        for addr in range(0, 0x80):
            try:
                self.i2c.read_byte(addr)
            except OSError:
                continue
            found.append(addr)
        return found
    """


class I2CDevice:
    """
    This Class Defined I2C Device
    FarmerSoft 2023
    """

    ###############
    # Properties
    ###############
    
    maskup = {
        1: 0b00000001, 2: 0b00000010, 3: 0b00000100, 4: 0b00001000,
        5: 0b00010000, 6: 0b00100000, 7: 0b01000000, 8: 0b10000000
        }

    maskdown = {
        1: 0b11111110, 2: 0b11111101, 3: 0b11111011, 4: 0b11110111,
        5: 0b11101111, 6: 0b11011111, 7: 0b10111111, 8: 0b01111111
        }

    ###############
    # Constructor
    ###############
    def __init__(self, i2cdriver, i2cbus, devicename, deviceaddr, debug=0):
        self.debug = debug
        self.i2cdriver = i2cdriver
        self.i2c = i2cbus
        self.devicename = devicename
        self.deviceaddr = deviceaddr

        if self.i2cdriver == 'ftdi':
            self.i2cdevice = self.i2c.get_port(self.deviceaddr)
        else:
            self.i2cdevice = None

        if int(self.debug) == 3:
            print(f"######################################################################")
            print(f"# Device I2C {self.devicename} initialization at {hex(self.deviceaddr)}")
            print(f"######################################################################")
            print("\r")

    ###############
    # Destructor
    ###############
    def __del__(self):
        if int(self.debug) == 3:
            print(f"######################################################################")
            print(f"# Device I2C {self.devicename} removed")
            print(f"######################################################################")
            print("\r")

    ###############
    # Device Methods
    ###############

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
