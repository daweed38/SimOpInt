# Standard Modules Import
import logging

# SimOpInt Import
from SimOpInt.ObjectBase import ObjectBase
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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)

        self.values = values
        self.valuestype = valuestype
        self.swstate = 0

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    def getSwitchState(self):
        return self.swstate

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: int, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, values, valuestype, output, command, debug)

        self.objtype = 'Switch'
        self.device = device
        self.port = port
        self.pin = pin
        self.swstate = self.readSwitchState()

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

    # Method getInputState()
    # Return Switch GPIO Pin Status
    def readSwitchState(self) -> int | str | bool:
        if self.device.readGpioPin(self.port, self.pin) == 1:
            return self.values[1]
        else:
            return self.values[0]


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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin1: int, pin2: int, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, values, valuestype, output, command, debug)

        self.objtype = 'Double Switch'
        self.device = device
        self.port = port
        self.pin1 = pin1
        self.pin2 = pin2
        self.swstate = self.readSwitchState()

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

    def readSwitchState(self) -> int | str | bool | None:
        if self.device.readGpioPin(self.port, self.pin1) == 1:
            swstate = self.values[0]
        elif self.device.readGpioPin(self.port, self.pin2) == 1:
            swstate = self.values[2]
        else:
            swstate = self.values[1]

        return swstate


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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: int, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, values, valuestype, output, command, debug)

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: int, values: list, valuestype: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, values, valuestype, output, command, debug)

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
