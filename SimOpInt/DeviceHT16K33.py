##################################################
# FarmerSoft Sim Open Interface MCP23017 Device Class
##################################################
# MCP23017 Device Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging
from datetime import datetime

# SimOpInt Import
from SimOpInt.DeviceBase import DeviceBase


class HT16K33(DeviceBase):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface I2C Device Base Class'

    ###################################
    # Properties
    ###################################

    system_cmd_base = 0x20
    display_cmd_base = 0x80
    brightness_cmd_base = 0xe0

    blinkrate = {
        'blinkoff': 0x00, 'blink2hz': 0x02, 'blink1hz': 0x04, 'blinkhlf': 0x06
    }

    registers = {
        'rowa1': {'addr': 0x00, 'init': 0x00},
        'rowa2': {'addr': 0x02, 'init': 0x00},
        'rowa3': {'addr': 0x04, 'init': 0x00},
        'rowa4': {'addr': 0x06, 'init': 0x00},
        'rowa5': {'addr': 0x08, 'init': 0x00},
        'rowa6': {'addr': 0x0a, 'init': 0x00},
        'rowa7': {'addr': 0x0c, 'init': 0x00},
        'rowa8': {'addr': 0x0e, 'init': 0x00},
        'rowb1': {'addr': 0x01, 'init': 0x00},
        'rowb2': {'addr': 0x03, 'init': 0x00},
        'rowb3': {'addr': 0x05, 'init': 0x00},
        'rowb4': {'addr': 0x07, 'init': 0x00},
        'rowb5': {'addr': 0x09, 'init': 0x00},
        'rowb6': {'addr': 0x0b, 'init': 0x00},
        'rowb7': {'addr': 0x0d, 'init': 0x00},
        'rowb8': {'addr': 0x0f, 'init': 0x00},
        'inter': {'addr': 0x60, 'init': 0x00}
    }

    ###################################
    # Constructor
    ###################################

    def __init__(self, devicename: str, deviceaddr: str, debug: int = 30) -> None:
        super().__init__(devicename, deviceaddr)

        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.devicetype = 'HT16K33'

        self.logger.debug(f'Device {self.devicename}  [Device Addr : {hex(self.deviceaddr)} / Device Type : {self.devicetype}] initialized. (Dummy Device : {self.dummy})')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    # configMCP(state) (Override from DeviceBase)
    # Enable or Disable the device
    # state is int
    def configMCP(self, state: int) -> None:
        if state == 1 and self.state == 0:
            self.logger.debug(f'Device {self.devicename} Started at {datetime.now()}')

            # Turning On System Oscillator
            if not self.dummy:
                self.writeDevice(self.system_cmd_base | 1)
            self.state = 1

        elif state == 0 and self.state == 1:
            self.logger.debug(f'Device {self.devicename} Stopped at {datetime.now()}')

            # Turning Off System Oscillator
            if not self.dummy:
                self.writeDevice(self.system_cmd_base)
            self.state = 0

        self.resetDeviceRegisters()

    # start() (Override from DeviceBase)
    # Start the device's intervening oscillator
    def start(self) -> int:
        if self.state != 1:
            self.configMCP(1)
            if not self.dummy:
                # Setting Display Status to On
                self.writeDevice(self.display_cmd_base | 1)
        return self.state

    # stop() (Override from DeviceBase)
    # Stop the device's internal oscillator
    def stop(self) -> int:
        if self.state != 0:
            self.configMCP(0)
            if not self.dummy:
                # Setting Display Status to Off
                self.writeDevice(self.display_cmd_base)
        return self.state

    ###################################
    # Standard Register Methods
    ###################################

    ###################################
    # HT16K33 Device Management Methods
    ###################################
