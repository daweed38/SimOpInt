# System Modules Import
import sys
import socket
import selectors
import time
import types
import logging

# Standard Modules Import

# Sim Open Interface Import

##################################################
# FarmerSoft Open Interface TCP Client Class
##################################################
# SimOpIntd Class
# FarmerSoft © 2024
# By Daweed
##################################################


class SimOpIntClient:
    """
    This is the main Interface Daemon Class
    """

    #############################################
    # Class Description
    #############################################

    def __str__(self) -> str:
        return 'This is the main Interface TCP Client Class'

    #############################################
    # Properties
    #############################################

    #############################################
    # Constructor
    #############################################

    def __init__(self, cliname:str, srvname: str, srvaddr: str, srvport: str, debug: int = 30) -> None:
        self.debug = debug
        self.cliname = cliname
        self.srvname = srvname
        self.srvaddr = srvaddr
        self.srvport = int(srvport)
        self.clisock = None
        self.selsock = selectors.DefaultSelector()
        self.headersize = 10
        self.buffersize = 32
        self.running = False
        self.srvstate = False
        self.newmsg = True
        self.msgfullsize = 0
        self.fullmsg = b''
        self.remainsize = 0

        # Get Logger
        self.logger = logging.getLogger(__name__)

        if self.getLoggingLevel() != self.debug:
            self.logger.setLevel(self.debug)
            self.logger.info(f'Updating {__name__} logger level to {logging.getLevelName(self.debug)}')

        self.logger.info(f'Sim Open Interface TCP Client Class Intialisation')

    #############################################
    # Destructor
    #############################################

    def __del__(self) -> None:
        pass

    #############################################
    # System Method
    #############################################

    # Get Current Logging Level for this Module
    def getLoggingLevel(self) -> int:
        return self.logger.getEffectiveLevel()

    # Set Current Logging Level for this Module
    def setLoggingLevel(self, level) -> None:
        self.logger.setLevel(level)
        self.debug = level
        self.logger.info(f'Updating {__name__} logger level to {logging.getLevelName(level)}')

    #############################################
    # Client Method
    #############################################

    # Get Client Name
    def getCliName(self) -> str:
        return self.cliname

    # Set Client Name
    def setCliname(self, name: str) -> None:
        self.cliname = name

    # Get Server Name
    def getSrvName(self) -> str:
        return self.srvname

    # Set Server Name
    def setSrvName(self, name) -> None:
        self.srvname = name

    # Get Server Address
    def getSrvAddr(self) -> str:
        return self.srvaddr

    # Set Server Address
    def setSrvAddr(self, addr) -> None:
        self.srvaddr = addr

    # Get Server Port
    def getSrvPort(self) -> int:
        return self.srvport

    # Set Server Port
    def setSrvPort(self, port) -> None:
        self.srvport = port

    # Open Client Socket
    def openCliSocket(self) -> None:
        self.logger.debug(f'Opening Server Socket ...')
        self.clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clisock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.logger.debug(f'Client Socket Opened ...')

    # Close Client Socket
    def closeCliSocket(self) -> None:
        self.logger.debug(f'Closing Client Socket ...')
        if self.clisock:
            self.clisock.close()
        self.logger.debug(f'Client Socket Closed ...')

    # Connect Client Socket
    def connectClient(self) -> None:
        self.clisock.connect((self.srvaddr, self.srvport))

    #############################################
    # DATA Method
    #############################################

    def receiveMessage(self):
        pass

    def sendMessage(self):
        pass

    def decodeMessage(self):
        pass

    def encodeMessage(self):
        pass

    #############################################
    # Loop Method
    #############################################
