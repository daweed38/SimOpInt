##################################################
# FarmerSoft Open Interface Message Class
##################################################
# SimOpIntMessage Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# System Modules Import
# import sys
# import pickle
# import socket
# import selectors
import sys
# import time
# import types
import logging
# import signal
# import threading

# Standard Modules Import

# Sim Open Interface Import
# from SimOpInt.SimOpIntConfig import SimOpIntConfig
# from SimOpInt.SimOpIntUtils import SimOpIntUtils
# from SimOpInt.SimOpIntClient import SimOpIntClient
# from SimOpInt.SimOpInt import SimOpInt


class SimOpIntMessage:

    ###################################
    # Class Description
    ###################################

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, debug: int = 30) -> None:
        self.debug = debug

        # Get Logger
        self.logger = logging.getLogger('SimOpInt.SimOpIntMessage')

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        self.logger.info(f'Sim Open Interface Message Class Unloaded')

    ###################################
    # System Methods
    ###################################

    ###################################
    # Config Message Methods
    ###################################

    def processcfg(self, message, config):
        self.logger.debug(f'Processing configuration Message')
        match message['cmd']:
            case 'read':
                self.logger.debug(f'Reading SimOpInt configuration file ...{config}')
            case 'write':
                self.logger.debug(f'Writing SimOpInt configuration file ...')

            case 'new':
                self.logger.debug(f'Creating new SimOpInt configuration file ...')

            case _:
                self.logger.debug(f'Cannot process configuration. Command {message['cmd']} unknown...')

    ###################################
    # Command Message Methods
    ###################################

    def processcmd(self, message):
        self.logger.debug(f'Processing command Message')

    ###################################
    # Interface Message Methods
    ###################################

    def processint(self, message):
        self.logger.debug(f'Processing interface Message')

    ###################################
    # Data Message Methods
    ###################################

    def processdref(self, message):
        self.logger.debug(f'Processing data Message')