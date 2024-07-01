# System Modules Import
import pickle
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
# SimOpIntClient Class
# FarmerSoft © 2024
# By Daweed
##################################################


class SimOpIntClient:
    """
    This is the main Interface Client Class
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

    def __init__(self, cliname: str, srvname: str, srvaddr: str, srvport: str, debug: int = 30) -> None:
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
        self.receiveMessage()

    #############################################
    # DATA Method
    #############################################

    def receiveMessage(self):
        if self.newmsg:
            incom_data = self.clisock.recv(self.headersize)
            if incom_data:
                self.newmsg = False
                self.msgfullsize = int(incom_data.decode('utf-8'))
                self.remainsize = self.msgfullsize
                self.logger.info(f'New Message ! Full Message Length {self.msgfullsize} [{type(self.msgfullsize)}]. Remaining Size : {self.remainsize} [{type(self.remainsize)}]')

                incom_data = self.clisock.recv(self.buffersize)
                incom_data_len = len(incom_data)
                self.fullmsg = incom_data
                self.remainsize = self.remainsize - incom_data_len

            else:
                self.selsock.unregister(self.clisock)
                self.clisock.close()

        else:
            if self.remainsize > self.buffersize:
                incom_data = self.clisock.recv(self.buffersize)
            else:
                incom_data = self.clisock.recv(self.remainsize)
            incom_data_len = len(incom_data)
            self.fullmsg += incom_data
            self.remainsize = self.remainsize - incom_data_len
            self.logger.info(f'New Message ! Full Message Length {self.msgfullsize}. Remaining Size : {self.remainsize}')
            if self.remainsize == 0:
                self.logger.info(f'New Message Fully Received ! {self.fullmsg.decode('utf-8')}')
                self.newmsg = True
                self.remainsize = 0
                self.msgfullsize = 0
                self.fullmsg = b''
                    
    def sendMessage(self, data):
        enc_data = self.encodeMessage(data)
        self.clisock.send(enc_data)

    def encodeMessage(self, data) -> bytes:
        dataheader = f'{len(pickle.dumps(data)):<{self.headersize}}'.encode('utf-8')
        return dataheader + pickle.dumps(data)

    def decodeMessage(self, data):
        message = data[self.headersize:]
        return pickle.loads(message)

    #############################################
    # Loop Method
    #############################################
