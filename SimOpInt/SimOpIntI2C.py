#!/usr/bin/env python3
# -*-coding:Utf-8 -*

import smbus2

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

    def __init__(self):
        self.i2c = smbus2.SMBus(1)

    ###############
    # Destructor
    ###############

    def __del__(self):
        self.i2c = None

    ###############
    # Destructor
    ###############

    def getBus(self) -> smbus2:
        return self.i2c

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


class I2CDevice(I2CBus):
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
    def __init__(self, devicename, deviceaddr, debug=0):
        super().__init__()
        self.debug = debug
        self.bus = 1
        self.devicename = devicename
        self.deviceaddr = deviceaddr
        # self.i2c = smbus2.SMBus(self.bus)

        if int(self.debug) == 3:
            print("######################################################################")
            print("# Device I2C {} initialization at {}".format(self.devicename, hex(self.deviceaddr)))
            print("######################################################################")
            print("\r")

    ###############
    # Destructor
    ###############
    def __del__(self):
        if int(self.debug) == 3:
            print("######################################################################")
            print("# Device I2C {} removed".format(self.devicename))
            print("######################################################################")
            print("\r")

    ###############
    # Methods
    ###############

    # Method readDevice()
    # Return one bytes from device
    def readDevice(self) -> int:
        if int(self.debug) == 3:
            print("######################################################################")
            print("# Reading Device {}".format(self.devicename))
            print("######################################################################")
            print("\r")
        return self.i2c.read_byte(self.deviceaddr)

    # Method writeDevice(data)
    # Write data to device
    def writeDevice(self, data) -> None:
        if int(self.debug) == 3:
            print("######################################################################")
            print("# Writing Data {} to Device {}".format(data, self.devicename))
            print("######################################################################")
            print("\r")
        self.i2c.write_byte(self.deviceaddr, data)

    # readRegister(registeraddr)
    # Return value from Device Register at registeraddr Address
    def readRegister(self, registeraddr) -> int:
        data = self.i2c.read_byte_data(self.deviceaddr, registeraddr)
        if int(self.debug) == 3:
            print("######################################################################")
            print("# Reading Value from Register at Address {} : {}".format(hex(registeraddr),bin(data)))
            print("######################################################################")
            print("\r")
        return data

    # writeRegister(registeraddr, registervalue)
    # Write Value on Device Register at registeraddr Address
    def writeRegister(self, registeraddr, data) -> None:
        if int(self.debug) == 3:
            print("######################################################################")
            print("# Writing Value {} to Register at Address {}".format(hex(data), hex(registeraddr)))
            print("######################################################################")
            print("\r")
        self.i2c.write_byte_data(self.deviceaddr, registeraddr, data)

    # Method readBit(registeraddr, bit)
    # Return Bit value from Register at registeraddr
    def readBit(self, registeraddr, bit) -> int:
        mask = self.maskup[bit]
        bitvalue = self.readRegister(registeraddr) & mask
        if int(self.debug) == 3:
            print("######################################################################")
            print("# Reading Bit {} Value from Register at Address {} : {}".format(bit, hex(registeraddr), bitvalue))
            print("######################################################################")
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
            print("######################################################################")
            print("# Writing Value {} to Bit {} from Register at Address {}".format(state, bit, hex(registeraddr)))
            print("######################################################################")        
            print("\r")

        self.writeRegister(registeraddr, newregisterdata)
