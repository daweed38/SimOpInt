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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, values: dict, valuestype: str, export: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, export, command, debug)

        self.values = values
        self.valuestype = valuestype

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: int, values: dict, valuestype: str, export: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, values, valuestype, export, command, debug)

        self.objtype = 'Switch'
        self.device = device
        self.port = port
        self.pin = pin

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: int, values: dict, valuestype: str, export: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, values, valuestype, export, command, debug)

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: int, values: dict, valuestype: str, export: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, values, valuestype, export, command, debug)

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: int, values: dict, valuestype: str, export: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, values, valuestype, export, command, debug)

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
