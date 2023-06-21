# System Modules Import
# from datetime import datetime
# Device Base Import
from ObjBase import ObjBase
# HT16K33 Import
from DeviceHT16K33 import HT16K33

##################################################
# FarmerSoft Sim Open Interface
##################################################
# SegDisplay Class (7 Segments Displays) REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class SegDisplay(ObjBase):
    """
    This class allow Segment Display management
    based on hardware driver HT16K33
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    digitvalues = {
        '0': 0x3F, '1': 0x06, '2': 0x5B, '3': 0x4F,
        '4': 0x66, '5': 0x6D, '6': 0x7D, '7': 0x07,
        '8': 0x7F, '9': 0x6F,
        'A': 0x77, 'B': 0x7C, 'C': 0x39, 'D': 0x5E, 'E': 0x79, 'F': 0x71,
        'a': 0x77, 'b': 0x7C, 'c': 0x39, 'd': 0x5E, 'e': 0x79, 'f': 0x71,
        'S': 0x6D, 's': 0x6D, 'T': 0x78,  't': 0x78,
        '-': 0x40,' ': 0x00,
    }

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: HT16K33, port: str, row1: str, nbdigit: str, decdigit: str, output: bool = False, command: bool = False, debug: bool = False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)
        # ----- standard properties -----
        self.objtype = '7 Segments Display'
        self.device = device
        self.port = str(port)
        self.row1 = int(row1)
        self.nbdigit = int(nbdigit)
        self.decdigit = int(decdigit)
        self.status = 'OFF'
        self.value = str(0).zfill(self.nbdigit)

        if self.debug:
            print("######################################################################")
            print("# {} Object {} creation with {} digit(s)".format(self.objtype, self.name, self.nbdigit))
            print("# First digit register : {}".format(hex(self.device.getRowRegisterAddr(self.port, self.row1))))
            print("# Create on device {}".format(self.device.devicename))
            print("######################################################################")
            print("\r")

    ########################################
    # Destructor
    ########################################

    def __del__(self) -> None:
        if self.debug:
            print("######################################################################")
            print("# {} Object {} removed".format(self.objtype, self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # System Methods
    ########################################

    ########################################
    # Object Status & Value
    ########################################

    # Method getStatus()
    # Return Display Status
    def getStatus(self) -> str:
        return self.status

    # Method setStatus(status)
    # Set Display Status
    def setStatus(self, status: str) -> None:
        if self.debug:
            print("######################################################################")
            print("# Display status set to {}".format(status))
            print("######################################################################")
            print("\r")
        if self.getStatus() != status:
            if status == 'OFF':
                value = ''
                for i in range(1, int(self.nbdigit) + 1):
                    value = value + ' '
                self.writeDisplay(value, False)
                self.status = status
            elif status == 'ON':
                self.status = 'ON'

    # Method getValue()
    # Return Display Value
    def getValue(self) -> str:
        return self.value

    # Method setValue(value)
    # Set Display Value to value
    # value is str
    def setValue(self, value: str) -> None:
        self.value = str(value)

    ########################################
    # Object Methods
    ########################################

    # Method getDigitNumber()
    # Return Number of Digit on Display
    def getDigitNumber(self) -> int:
        return self.nbdigit

    # Method getDigitRegister(digit)
    # Return Digit Register Address
    # digit is int
    def getDigitRegister(self, digit: int) -> int | bool:
        row = self.row1 + (digit - 1)
        registeraddr = self.device.getRowRegisterAddr(self.port, row)
        if self.debug:
            print("######################################################################")
            print("# Digit {} in Row {} on Port {}".format(digit, row, self.port))
            print("# Register Address {}".format(hex(registeraddr)))
            print("######################################################################")
            print("\r")

        return registeraddr

    # Method listDigitsRegisters()
    # Return Digits Register List
    def listDigitsRegister(self) -> dict:
        digitregisterlist = {}
        for i in range(1, int(self.nbdigit) + 1):
            digitregisterlist[i] = self.getDigitRegister(i)

        return digitregisterlist

    # Method writeDigit(digit, digitval, decimal)
    # Write digitval on digit
    # If decimal is True and digit is the decdigit
    # then decimal point is display on digit
    # digit is int, value is str, decimal is bool
    def writeDigit(self, digit: int, value: str, decimal: bool) -> None:
        digitval = str(value)
        row = int(self.row1) + (digit - 1)
        if digitval in self.digitvalues:
            if self.debug:
                print("######################################################################")
                print("# Writing value {} on Digit {} defined as Row {} on Port {} ".format(digitval, digit, row, self.port))
                print("# Register value : {}".format(hex(self.digitvalues[str(digitval)])))
                print("######################################################################")

            if decimal and digit == self.decdigit:
                value = int(self.digitvalues[str(digitval)]) | 0b10000000
            else:
                value = int(self.digitvalues[str(digitval)])

            self.device.setRow(row, self.port, value)
        else:
            if self.debug:
                print("######################################################################")
                print("# Value {} not found in digitvalue dict".format(digitval))
                print("######################################################################")

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

        if self.debug:
            print("######################################################################")
            print("# Nb Digit : {} DecDigit {}".format(self.nbdigit, self.decdigit))
            print("# Value Before Processing : {}".format(value))
            print("# Value Rounded : {}".format(datadigit))
            print("# Mode {} Writing value {} on Display {} Mode Decimal {}".format(dispmode, datadigit, self.name, decimal))
            print("######################################################################")
            print("\r")

        digitnum = 1

        for digitval in datadigit:
            self.writeDigit(digitnum, digitval, decimal)
            digitnum += 1

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Annunciator Class (Annunciator Displays) REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class Annunciator(ObjBase):

    """
    This class allow Annunciator Display management
    based on hardware driver HT16K33
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: HT16K33, port: str, row: str, out1: str, nblight: str, activemode: str, initstate: str, output: bool = False, command: bool = False, debug: bool = False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)
        # ----- Object properties -----
        self.objtype = 'Annunciator'
        self.device = device
        self.port = str(port)
        self.row = int(row)
        self.out1 = int(out1)
        self.nblight = int(nblight)
        self.activemode = int(activemode)
        self.status = True
        self.value = initstate

        if self.debug:
            print("######################################################################")
            print("# {} Object {} Group Creation".format(self.objtype, self.name))
            print("# {} Object {} Group is composed of {} Out :".format(self.objtype, self.name, self.nblight))
            print("# Created on Device {}".format(self.device.getName()))
            for out in range(self.nblight):
                print("# -> Out {} : {} in Row {} on port {}".format(out, self.out1 + out, self.row, self.port))
            print("######################################################################")
            print("\r")

    ########################################
    # Destructor
    ########################################

    def __del__(self) -> None:
        if self.debug:
            print("######################################################################")
            print("# Annunciator {} Group Removed".format(self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # System Methods
    ########################################

    ########################################
    # Object Status & Value
    ########################################

    # Method getStatus()
    # Return Object Status
    def getStatus(self) -> bool:
        return self.status

    # Method setStatus(status)
    # Set Object Status to status
    # status is str
    def setStatus(self, status: bool) -> None:
        self.status = status

    # Method getValue()
    # Return Object Current Value
    def getValue(self) -> str:
        return self.value

    # Method setValue(value)
    # Set Object Value to value
    # value is int
    def setValue(self, value: str) -> None:
        self.value = value

    ########################################
    # Object Methods
    ########################################

    # Method getLightState()
    # Return the Switch Light State
    def getLightState(self) -> str:
        return self.value

    # Method setLightState(state)
    # Set the Switch Light in the state 'state' 
    # state  = 'ON' or 'OFF'
    def setLightState(self, state: str) -> None:
        if self.status:
            if self.debug:
                print("######################################################################")
                print("# DEBUG .... Updating Annunciator Group {} to {}".format(self.name, state))
                print("######################################################################")
            for out in range(self.nblight):
                if self.activemode == 1:
                    if state == 'ON':
                        self.device.setOut(self.row, self.port, self.out1 + out, 1)
                    elif state == 'OFF':
                        self.device.setOut(self.row, self.port, self.out1 + out, 0)
                else:
                    if state == 'ON':
                        self.device.setOut(self.row, self.port, self.out1 + out, 0)
                    elif state == 'OFF':
                        self.device.setOut(self.row, self.port, self.out1 + out, 1)

            self.value = state
