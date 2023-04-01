# System Modules Import
from datetime import datetime
# Device Base Import
from ObjBase import ObjBase
# MCP23017 Import
from DeviceMCP23017 import MCP23017

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Switch Class REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class Switch(ObjBase):
    """
    This class allow Simple Switch management (Off / On)
    based on hardware driver MCP23017
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: str, values: str, valuestype: str, debug=False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, debug)
        # ----- Object properties -----
        self.objtype = 'Switch'
        self.device = device
        self.port = str(port)
        self.pin = int(pin)
        self.values = values
        self.valuestype = valuestype

        if self.debug:
            print("######################################################################")
            print("{} Object {} creation".format(self.objtype, self.name))
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

    def getTypedData(self, data) -> int | str | bool:
        if self.valuestype == 'string':
            return str(data)
        elif self.valuestype == 'int':
            return int(data)
        elif self.valuestype == 'bool':
            return bool(data)
        else:
            return data

    def getValueType(self) -> str:
        return self.valuestype

    ########################################
    # Object Status & Value
    ########################################

    # Method getInputState()
    # Return Switch GPIO Pin Status
    def getSwitchState(self) -> int | str | bool:
        if self.device.readGpioPin(self.port, self.pin) == 1:
            return self.values[1]
        else:
            return self.values[0]

    ########################################
    # Object Methods
    ########################################

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Switch Class REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class DoubleSwitch(ObjBase):
    """
    This class allow Double Switch management (On / Off / On)
    based on hardware driver MCP23017
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin1: str, pin2: str, values: str, valuestype: str, debug=False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, debug)
        # ----- Object properties -----
        self.objtype = 'Double Switch'
        self.device = device
        self.port = str(port)
        self.pin1 = int(pin1)
        self.pin2 = int(pin2)
        self.values = values
        self.valuestype = valuestype

        if self.debug:
            print("######################################################################")
            print("{} Object {} creation".format(self.objtype, self.name))
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

    def getTypedData(self, data) -> int | str | bool:
        if self.valuestype == 'string':
            return str(data)
        elif self.valuestype == 'int':
            return int(data)
        elif self.valuestype == 'bool':
            return bool(data)
        else:
            return data

    def getValueType(self) -> str:
        return self.valuestype

    ########################################
    # Object Status & Value
    ########################################

    def getSwitchState(self) -> int | str | bool:
        if self.device.readGpioPin(self.port, self.pin1) == 1:
            return self.values[0]
        elif self.device.readGpioPin(self.port, self.pin2) == 1:
            return  self.values[2]
        else:
            return  self.values[1]

    ########################################
    # Object Methods
    ########################################

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Switch Class REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class RotarySwitch(ObjBase):
    """
    This class allow Rotary Switch management (N position)
    based on hardware driver MCP23017
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pins: str, values: str, valuestype: str, bincode: str, debug=False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, debug)
        # ----- Object properties -----
        self.objtype = 'Rotary Switch'
        self.device = device
        self.port = str(port)
        self.pins = {}
        self.values = values
        self.valuestype = valuestype
        self.bincode = bincode

        self.createPins(pins)

        if self.debug:
            print("######################################################################")
            print("{} Object {} creation".format(self.objtype, self.name))
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

    def getTypedData(self, data) -> int | str | bool:
        if self.valuestype == 'string':
            return str(data)
        elif self.valuestype == 'int':
            return int(data)
        elif self.valuestype == 'bool':
            return bool(data)
        else:
            return data

    def getValueType(self) -> str:
        return self.valuestype

    ########################################
    # Object Status & Value
    ########################################

    def getSwitchState(self) -> int | str | bool:
        pass

    ########################################
    # Object Methods
    ########################################

    def createPins(self, pins) -> None:
        pintab = pins.split(',')
        for pin in range(len(pintab)):
            pininfo = pintab[pin].split(':')
            pinkey = 'pin'+str(pin+1)
            self.pins[pinkey] = {}
            self.pins[pinkey]['port'] = pininfo[0]
            self.pins[pinkey]['input'] = int(pininfo[1])

    def getPins(self) -> dict:
        return self.pins

    def getPin(self, pin) -> dict:
        return self.pins[pin]

    def getPinPort(self, pin) -> str:
        return self.pins[pin]['port']

    def getPinInput(self, pin) -> int:
        return self.pins[pin]['input']

##################################################
# FarmerSoft Sim Open Interface
##################################################
# PushButtonSwitch Class (Push Button) REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class PushButtonSwitch(ObjBase):
    """
    This class allow Simple Push Button management
    based on hardware driver MCP23017
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: str, values: str, valuestype: str, debug=False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, debug)
        self.objtype = 'Rotary Switch'
        self.device = device
        self.port = str(port)
        self.pin = int(pin)
        self.values = values.split(',')
        self.valuestype = valuestype
        self.timestamp = datetime.now()

        """
        self.swstate = initstate
        self.swstate = self.getTypedData(initstate)
        """

        if self.debug:
            print("######################################################################")
            print("# Create Push Button Switch {} On Port {} On Device {}".format(self.name, self.port, self.device.getName()))
            print("######################################################################")
            print("\r")

    ########################################
    # Destructor
    ########################################

    def __del__(self) -> None:
        if self.debug:
            print("######################################################################")
            print("# ush Button Switch {} Removed".format(self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # System Methods
    ########################################

    def getTypedData(self, data) -> int | str | bool:
        if self.valuestype == 'string':
            return str(data)
        elif self.valuestype == 'int':
            return int(data)
        elif self.valuestype == 'bool':
            return bool(data)
        else:
            return data

    def getValueType(self) -> str:
        return self.valuestype

    ########################################
    # Object Status & Value
    ########################################

    # Method getSwitchState()
    # Return Switch GPIO Pin Status
    def getSwitchState(self) -> int | bool:
        return self.device.readGpioPin(self.port, self.pin)

    ########################################
    # Object Methods
    ########################################

    def getMillis(self) -> float:
        dt = datetime.now() - self.timestamp
        ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
        return ms
