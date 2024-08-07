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

    ###################################
    # Constructor
    ###################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: HT16K33, port: str, row1: str, nbdigit: str, decdigit: str, output: bool = False, command: bool = False, debug: int = 30) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)

        self.objtype = '7 Segments Display'
        self.device = device
        self.port = port
        self.row1 = row1
        self.nbdigit = nbdigit
        self.decdigit = decdigit
        self.status = 'OFF'
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
