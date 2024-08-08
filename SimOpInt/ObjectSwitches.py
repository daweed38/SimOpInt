# Standard Modules Import
import logging

# SimOpInt Import
from SimOpInt.ObjectBase import ObjectBase


##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Switch Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################


class Switch(ObjectBase):

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)

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


class DoubleSwitch(ObjectBase):

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)

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


class RotarySwitch(ObjectBase):

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)

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


class PushButtonSwitch(ObjectBase):

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

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)

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
