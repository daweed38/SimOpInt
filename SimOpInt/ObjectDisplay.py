##################################################
# FarmerSoft Sim Open Interface Object Class
##################################################
# SegDisplay Class (7 Segments Displays) REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging

# SimOpInt Import
from SimOpInt.ObjectBase import ObjectBase
from SimOpInt.DeviceHT16K33 import HT16K33


class SegDisplay(ObjectBase):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface Object 7 Segments Display Class'

    ###################################
    # Properties
    ###################################

    digitvalues = {
        '0': 0x3F, '1': 0x06, '2': 0x5B, '3': 0x4F,
        '4': 0x66, '5': 0x6D, '6': 0x7D, '7': 0x07,
        '8': 0x7F, '9': 0x6F,
        'A': 0x77, 'B': 0x7C, 'C': 0x39, 'D': 0x5E, 'E': 0x79, 'F': 0x71,
        'a': 0x77, 'b': 0x7C, 'c': 0x39, 'd': 0x5E, 'e': 0x79, 'f': 0x71,
        'S': 0x6D, 's': 0x6D, 'T': 0x78, 't': 0x78,
        '-': 0x40, ' ': 0x00,
    }

    ###################################
    # Constructor
    ###################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: HT16K33, port: str, row1: int, nbdigit: int, decdigit: int, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)

        self.objtype = '7 Segments Display'
        self.name = name
        self.device = device
        self.port = port
        self.row1 = row1
        self.nbdigit = nbdigit
        self.decdigit = decdigit
        self.status = 'OFF'
        self.debug = debug

        self.value = ' '

        self.logger = logging.getLogger(__name__)
        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    # Method getDebugLevel()
    # Return object debug level
    def getDebugLevel(self) -> int:
        return self.debug

    # Method settDevice(debuglevel)
    # debuglevel is int
    # Set object debug level
    def setDebugLevel(self, debuglevel: int) -> None:
        self.debug = debuglevel
        self.logger.setLevel(self.debug)

    # Method getDevice()
    # Return Display device object
    def getDevice(self) -> HT16K33:
        return self.device

    # Method settDevice(device)
    # device is HT16K33 instance
    # Set Display device object
    def setDevice(self, device: HT16K33) -> None:
        self.device = device

    # Method getDevicePort()
    # Return Display device port
    def getDevicePort(self) -> str:
        return self.port

    # Method setDevicePort(port)
    # port is str
    # Set Display device port
    def setDevicePort(self, port: str) -> None:
        self.port = port

    # Method getDisplayFirstRow()
    # Return Display device first common
    def getDisplayFirstRow(self) -> int:
        return self.row1

    # Method setDisplayFirstRow(row)
    # row is int
    # Set Display device first common
    def setDisplayFirstRow(self, row: int) -> None:
        self.row1 = row

    # Method getDisplayNbDigit()
    # Return Display digit(s) number
    def getDisplayNbDigit(self) -> int:
        return self.nbdigit

    # Method setDisplayNbDigit(nbdigit)
    # nbdigit is int
    # Set Display digit(s) number
    def setDisplayNbDigit(self, nbdigit: int) -> None:
        self.nbdigit = nbdigit

    # Method getDisplayDeciDigit()
    # Return Display decimal digit number
    def getDisplayDeciDigit(self) -> int:
        return self.decdigit

    # Method setDisplayDeciDigit(decdigit)
    # decdigit is int
    # Set Display decimal digit number
    def setDisplayDeciDigit(self, decdigit: int) -> None:
        self.decdigit = decdigit

    # Method getValue()
    # Return Display Value
    def getValue(self) -> str:
        return self.value

    # Method setValue(value)
    # value is str
    # Set Display Value to value
    def setValue(self, value: str) -> None:
        self.value = value

    # Method getStatus()
    # Return Display Status
    def getStatus(self) -> str:
        return self.status

    # Method setStatus(status)
    # status is str
    # Set Display Status
    def setStatus(self, status: str) -> None:
        if status == 'OFF':
            value = ''
            for i in range(1, int(self.nbdigit) + 1):
                value = value + ' '

            self.logger.debug(f'Writing value "{value}" on Display {self.getName()}')
            # self.writeDisplay(value, False)
            self.status = 'OFF'

        elif status == 'ON':
            self.logger.debug(f'Writing value "{self.value}" on Display {self.getName()}')
            # self.writeDisplay(self.value, False)
            self.status = 'ON'

        else:
            self.logger.error(f'Status {status} not recognized')

    ########################################
    # 7 Segments Display Object Methods
    ########################################

    # Method getDigitRegister(digit)
    # Return Digit Register Address
    # digit is int. self.row1 is digit number 0
    def getDigitRegister(self, digit: int) -> int | bool:
        row = self.row1 + digit
        registeraddr = self.device.getRowRegisterAddr(self.port, row)
        return registeraddr

    # Method listDigitsRegisters()
    # Return Digit(s) Register List
    def listDigitsRegisters(self) -> dict:
        digitregisterlist = {}
        for i in range(0, self.nbdigit):
            digitregisterlist[i] = hex(self.getDigitRegister(i))
        return digitregisterlist

    # Method writeDigit(digit, digitval, decimal)
    # Write digitval on digit
    # If decimal is True and digit is the decdigit
    # then decimal point is display on digit
    # digit is int, value is str, decimal is bool
    def writeDigit(self, digit: int, value: str, decimal: bool) -> None:
        digitval = value
        row = int(self.row1) + (digit - 1)
        if digitval in self.digitvalues:

            if decimal and digit == self.decdigit:
                value = self.digitvalues[digitval] | 0b10000000
            else:
                value = self.digitvalues[digitval]

            self.logger.debug(f'Writing value {digitval} on Digit {digit} defined as Row {row} on Port {self.port}. Register Address {hex(self.getDigitRegister(row))} Register value {hex(value)}')

            self.device.setRow(self.port, row, value)

        else:
            self.logger.error(f'Value {digitval} not found in digitvalue dict')

    # Method writeDisplay(value)
    # Display value on display
    # If decimal is True, then decimal point
    # will be display on the decdigit
    # value is int, float or str, decimal is bool
    def writeDisplay(self, value: int | float | str, decimal: bool) -> None:
        if decimal:
            dispmode = 'Float'
            # formatstr = '{:0>'+str(self.nbdigit+1)+'}'
            # datadigit = formatstr.format(round(value, self.nbdigit - self.decdigit)).replace('.', '')[:self.nbdigit]
            formatstr = '{:0' + str(self.nbdigit) + '.' + str(self.nbdigit - self.decdigit) + 'f}'
            datadigit = formatstr.format(round(value, self.nbdigit - self.decdigit)).replace('.', '')[:self.nbdigit]
        else:
            if isinstance(value, str):
                dispmode = 'String'
                datadigit = value.zfill(self.nbdigit)[:self.nbdigit]
            else:
                dispmode = 'Integer'
                datadigit = str(int(round(value))).zfill(self.nbdigit)

        self.logger.debug(f'Nb Digit : {self.nbdigit} DecDigit {self.decdigit}')
        self.logger.debug(f'Value Before Processing : {value} Value Rounded : {datadigit}')
        self.logger.debug(f'Mode {dispmode} Writing value {datadigit} on Display {self.name} Mode Decimal {decimal}')

        digitnum = 1

        for digitval in datadigit:
            self.writeDigit(digitnum, digitval, decimal)
            digitnum += 1
