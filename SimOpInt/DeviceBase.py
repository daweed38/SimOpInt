##################################################
# FarmerSoft Sim Open Interface Device Class
##################################################
# Base Device Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging

# SimOpInt Import
from SimOpInt.SimOpIntI2C import I2CBus


class DeviceBase(I2CBus):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface I2C Device Base Class'

    ###################################
    # Properties
    ###################################

    maskpins = {
        0b00000001: 1, 0b00000010: 2, 0b00000100: 3, 0b00001000: 4,
        0b00010000: 5, 0b00100000: 6, 0b01000000: 7, 0b10000000: 8
    }

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

    ###################################
    # Constructor
    ###################################

    def __init__(self, devicename: str, deviceaddr: str, deviceintgpio: dict | None, debug: int = 30) -> None:
        super().__init__()

        self.devicename = devicename
        self.deviceaddr = int(deviceaddr, 16)
        self.deviceintgpio = deviceintgpio
        self.devicetype = 'Base'
        self.state = 0

        if self.i2c is None:
            self.dummy = True
        else:
            self.dummy = False

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

    # getName()
    # Return device name (str)
    def getName(self) -> str:
        return self.devicename

    # setName(devicename)
    # devicename is str
    # Set device name to devicename
    def setName(self, devicename: str) -> None:
        self.devicename = devicename

    # getAddr()
    # Return device address (int)
    def getAddr(self) -> int:
        return self.deviceaddr

    # setAddr(deviceaddr)
    # deviceaddr is int
    # Set device address to deviceaddr
    def setAddr(self, deviceaddr: int) -> None:
        self.deviceaddr = deviceaddr

    # getHexAddr()
    # Return Device Addr in hex format (str)
    def getHexAddr(self) -> str:
        return hex(self.deviceaddr)

    # getStatus()
    # Return device status (int)
    def getStatus(self) -> int:
        return self.state

    # setStatus(state)
    # state is int
    # Set device status to state
    def setStatus(self, state) -> None:
        self.state = state

    # getIntGpio()
    # Return device Interrupt GPIO (dict)
    def getIntGpio(self) -> dict | None:
        return self.deviceintgpio

    # setIntGpio(deviceintgpio)
    # deviceintgpio is dict
    # Set device Interrupt GPIO
    def setIntGpio(self, deviceintgpio: dict | None) -> None:
        self.state = deviceintgpio

    # isDummy()
    # Return if is a dummy device (bool)
    def isDummy(self) -> bool:
        return self.dummy

    # getDeviceType()
    # Return device Interrupt GPIO (dict)
    def getDeviceType(self) -> str:
        return self.devicetype

    # setDeviceType(devicetype)
    # deviceintgpio is dict
    # Set device Interrupt GPIO
    def setDeviceType(self, devicetype: str) -> None:
        self.devicetype = devicetype

    # configMCP(state)
    # state is int
    # Enable or Disable the device
    def configMCP(self, state: int) -> None:
        if state == 1 and self.state == 0:
            self.logger.debug(f'Device {self.devicename} Started')
            self.state = 1
        elif state == 0 and self.state == 1:
            self.logger.debug(f'Device {self.devicename} Stopped')
            self.state = 0

    # start()
    # Start the device and return state
    def start(self) -> int:
        if self.state != 1:
            self.configMCP(1)
        return self.state

    # stop()
    # Stop the device and return state
    def stop(self) -> int:
        if self.state != 0:
            self.configMCP(0)
        return self.state

    # getPinFromMask(mask)
    # mask is int value
    def getPinFromMask(self, mask):
        return self.maskpins[mask]

    ###################################
    # GPIO Interrupt Methods
    ###################################

    ###################################
    # Interrupt CallBack Methods
    ###################################

    ###################################
    # Standard Register Methods
    ###################################

    # Method listRegister():
    # Return Register List (dict)
    def listRegisters(self) -> dict:
        return self.registers

    # Method getRegisterAddr(registername)
    # registername is str
    # Return register address (int) or False if not found (bool)
    def getRegisterAddr(self, registername: str) -> int | bool:
        if registername in self.registers:
            registeraddr = self.registers[registername]['addr']
            self.logger.debug(f'Register {registername} Address on Device {self.devicename} is {hex(registeraddr)}')
        else:
            registeraddr = False
            self.logger.debug(f'Register {registername} not found in registers dict for device {self.devicename}')

        return registeraddr

    # Method getRegisterInit(registername)
    # registername is str
    # Return register init value (int) or False if not found
    def getRegisterInit(self, registername: str) -> int | bool:
        if registername in self.registers:
            registerinit = self.registers[registername]['init']
            self.logger.debug(f'Register {registername} Init Value on Device {self.devicename} is {hex(registerinit)}')
        else:
            registerinit = False
            self.logger.debug(f'Register {registername} not found in registers dict for device {self.devicename}')

        return registerinit

    # clearAllRegisters()
    # Reset all register declared in
    # registers dict to their initial state
    def resetDeviceRegisters(self) -> None:
        self.logger.debug(f'Resetting all buffers to their initial state ...')
        if not self.dummy:
            for registername in self.registers:
                if self.debug:
                    self.logger.debug(f'Resetting register {registername}')
                    self.writeRegister(self.getRegisterAddr(registername), self.getRegisterInit(registername))
        else:
            self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')

    ###################################
    # I2C Device Base Management Methods
    ###################################

    # Method readDevice()
    # Return one bytes from device
    def readDevice(self) -> int | None:
        if not self.dummy:
            self.logger.debug(f'Reading Device {self.devicename}')
            return self.i2c.read_byte(self.deviceaddr)
        else:
            self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
            return None

    # Method writeDevice(data)
    # Write data to device
    def writeDevice(self, data: int) -> None:
        if not self.dummy:
            self.logger.debug(f'Writing Data {data} to Device {self.devicename}')
            self.i2c.write_byte(self.deviceaddr, data)
        else:
            self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')

    # readRegister(registeraddr)
    # registeraddr is int
    # Return value from device register at registeraddr
    def readRegister(self, registeraddr) -> int | None:
        if not self.dummy:
            data = self.i2c.read_byte_data(self.deviceaddr, registeraddr)
            self.logger.debug(f'Reading Value from Register at Address {hex(registeraddr)} : {bin(data)}')
            return data
        else:
            self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
            return None

    # writeRegister(registeraddr, registervalue)
    # registeraddr is int
    # registervalue is int
    # Write registervalue on device register at registeraddr Address
    def writeRegister(self, registeraddr, data) -> None:
        if not self.dummy:
            self.logger.debug(f'Writing Value {hex(data)} to Register at Address {hex(registeraddr)}')
            self.i2c.write_byte_data(self.deviceaddr, registeraddr, data)
        else:
            self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')

    # Method readBit(registeraddr, bit)
    # registeraddr is int
    # bit is int
    # Return bit value from register at registeraddr
    def readBit(self, registeraddr, bit) -> int | None:
        if not self.dummy:
            mask = self.maskup[bit]
            bitvalue = self.readRegister(registeraddr) & mask
            self.logger.debug(f'Reading Bit {bit} Value from Register at Address {hex(registeraddr)} : {bitvalue}')
            if int(bitvalue) > 0:
                return 1
            else:
                return 0
        else:
            self.logger.debug(f'Dummy Device! Cannot read on I2C Bus')
            return None

    # Method writeBit(registeraddr, bit, state)
    # registeraddr is int
    # bit is int
    # state is int
    # Write 1 or 0 to bit on register at registeraddr
    def writeBit(self, registeraddr, bit, state) -> None:
        if not self.dummy:
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
            self.logger.debug(f'Writing Value {state} to Bit {bit} from Register at Address {hex(registeraddr)}')
            self.writeRegister(registeraddr, newregisterdata)
        else:
            self.logger.debug(f'Dummy Device! Cannot write on I2C Bus')
