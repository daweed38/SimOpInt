# Standard Modules Import
import logging

# SimOpInt Import
from SimOpInt.ObjectBase import ObjectBase
from SimOpInt.DeviceBase import DeviceBase
from SimOpInt.DeviceMCP23017 import MCP23017

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object DoubleSwitch Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################


class BaseSwitch(ObjectBase):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface Object Base Switch Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: DeviceBase, pins: dict, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)

        self.device = device
        self.pins = pins
        self.values = values
        self.valuestype = valuestype
        self.swstate = self.readSwitchState()

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    def getDevice(self) -> DeviceBase:
        return self.device

    def setDevice(self, device: DeviceBase) -> None:
        self.device = device

    def getPins(self) -> dict:
        return self.pins

    def setPins(self, pins: dict) -> None:
        self.pins = pins

    def getTypedData(self, data) -> int | str | bool:
        if self.getValueType() == 'string':
            return str(data)
        elif self.getValueType() == 'int':
            return int(data)
        elif self.getValueType() == 'bool':
            return bool(data)
        else:
            return data

    def getValueType(self) -> str:
        return self.valuestype

    ###################################
    # Switch Object Methods
    ###################################

    def getSwitchState(self):
        return self.swstate

    def readSwitchState(self):
        pass

    def getInterruptChannel(self):
        pass


##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Switch Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################


class Switch(BaseSwitch):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface Object Switch Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, pins: dict, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, device, pins, values, valuestype, output, command, debug)

        self.objtype = 'Switch'
        self.device = device
        self.pins = pins
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

    ###################################
    # Switch Object Methods
    ###################################

    def readSwitchState(self):
        pin = self.pins['pin1']['pin']
        port = self.pins['pin1']['port']
        return self.device.readGpioPin(port, pin)

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object DoubleSwitch Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################


class DoubleSwitch(BaseSwitch):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface Object Double Switch Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, pins: dict, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, device, pins, values, valuestype, output, command, debug)

        self.objtype = 'Double Switch'
        self.device = device
        self.pins = pins
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

    ###################################
    # Double Switch Object Methods
    ###################################


##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object RotarySwitch Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################


class RotarySwitch(BaseSwitch):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface Object Rotary Switch Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, pins: dict, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, device, pins, values, valuestype, output, command, debug)

        self.objtype = 'Rotary Switch'
        self.device = device
        self.pins = pins
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

    ###################################
    # Switch Object Methods
    ###################################


##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object PushButtonSwitch Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################


class PushButtonSwitch(BaseSwitch):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface Object Push Button Switch Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, pins: dict, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, device, pins, values, valuestype, output, command, debug)

        self.objtype = 'Push Button'
        self.device = device
        self.pins = pins
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

    ###################################
    # Switch Object Methods
    ###################################

    def readSwitchState(self):
        pin = self.pins['pin1']['pin']
        port = self.pins['pin1']['port']
        return self.device.readGpioPin(port, pin)