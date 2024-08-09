# Standard Modules Import
import logging

# SimOpInt Import
from SimOpInt.ObjectBase import ObjectBase
from SimOpInt.DeviceHT16K33 import HT16K33


##################################################
# FarmerSoft Sim Open Interface Object Class
##################################################
# SegDisplay Classes REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################


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
        self.offvalue = self.genOffValue()
        self.value = {'value': self.getOffValue(), 'decimal': False}
        self.debug = debug

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
        return self.value['value']

    # Method setValue(value)
    # value is str
    # Set Display Value to value
    def setValue(self, value: str) -> None:
        self.value['value'] = value

    # Method getValue()
    # Return Display Value
    def isDecimal(self) -> bool:
        return self.value['decimal']

    # Method setValue(value)
    # value is str
    # Set Display Value to value
    def setDecimal(self, decimal: bool) -> None:
        self.value['decimal'] = decimal

    # Method getOffValue()
    # Return Display Value
    def getOffValue(self) -> str:
        return self.offvalue

    # Method setOffValue(value)
    # value is str
    # Set Display Value to value
    def setOffValue(self, offvalue: str) -> None:
        self.offvalue = offvalue

    # Method genOffValue()
    # Generate the OFF Display value
    def genOffValue(self) -> str:
        value = ''
        for i in range(1, int(self.nbdigit) + 1):
            value = value + ' '
        return value

    # Method getStatus()
    # Return Display Status
    def getStatus(self) -> str:
        return self.status

    # Method setStatus(status)
    # status is str
    # Set Display Status
    def setStatus(self, status: str) -> None:
        if status == 'OFF':
            oldvalue = self.getValue()
            olddecimal = self.isDecimal()
            self.writeDisplay(self.getOffValue(), False)
            self.setValue(oldvalue)
            self.setDecimal(olddecimal)
            self.status = 'OFF'

        elif status == 'ON':
            self.status = 'ON'
            self.writeDisplay(self.getValue(), self.isDecimal())

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
        if self.getStatus() == 'ON':
            if isinstance(value, str):
                if decimal:
                    dispmode = 'Float String'
                    formatstr = '{:0' + str(self.nbdigit) + '.' + str(self.nbdigit - self.decdigit) + 'f}'
                    datadigit = formatstr.format(round(float(value), self.nbdigit - self.decdigit)).replace('.', '')[:self.nbdigit].zfill(self.nbdigit)
                else:
                    dispmode = 'Integer String'
                    datadigit = value.zfill(self.nbdigit)[:self.nbdigit]
            else:
                if decimal:
                    dispmode = 'Float'
                    formatstr = '{:0' + str(self.nbdigit) + '.' + str(self.nbdigit - self.decdigit) + 'f}'
                    datadigit = formatstr.format(round(value, self.nbdigit - self.decdigit)).replace('.', '')[:self.nbdigit].zfill(self.nbdigit)
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

                self.value = {'value': value, 'decimal': decimal}

        else:
            self.logger.warning(f'Display is OFF.')


##################################################
# FarmerSoft Sim Open Interface Object Class
##################################################
# Annunciator Class (Annunciator Displays) REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################


class Annunciator(ObjectBase):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface Object Annunciator Display Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: HT16K33, port: str, row: int, out1: int, nblight: int, activemode: int, initstate: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)

        # ----- Object properties -----
        self.objtype = 'Annunciator'
        self.name = name
        self.device = device
        self.port = port
        self.row = row
        self.out1 = out1
        self.nblight = nblight
        self.activemode = activemode
        self.status = True
        self.value = initstate
        self.debug = debug

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

    # Method getStatus()
    # Return Object Status
    def getStatus(self) -> bool:
        return self.status

    # Method setStatus(status)
    # status is bool
    # Set Object Status to status
    def setStatus(self, status: bool) -> None:
        self.status = status

    # Method getValue()
    # Return Object Current Value
    def getValue(self) -> str:
        return self.value

    # Method setValue(value)
    # value is str
    # Set Object Value to value
    def setValue(self, value: str) -> None:
        self.value = value

    ###################################
    # Annunciator Display Object Methods
    ###################################

    # Method getLightState()
    # Return the Switch Light State
    def getLightState(self) -> str:
        return self.value

    # Method setLightState(state)
    # Set the Switch Light in the state 'state'
    # state  = 'ON' or 'OFF'
    def setLightState(self, state: str) -> None:
        if self.status:
            self.logger.debug(f'Updating Annunciator Group {self.name} to {state}')

            for out in range(self.nblight):
                if self.activemode == 1:
                    if state == 'ON':
                        self.device.setOut(self.port, self.row, self.out1 + out, 1)
                    elif state == 'OFF':
                        self.device.setOut(self.port, self.row, self.out1 + out, 0)
                else:
                    if state == 'ON':
                        self.device.setOut(self.port, self.row, self.out1 + out, 0)
                    elif state == 'OFF':
                        self.device.setOut(self.port, self.row, self.out1 + out, 1)

            self.value = state
