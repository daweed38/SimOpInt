##################################################
# FarmerSoft Open Interface TCP Client Class
##################################################
# SimOpIntClient Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# System Modules Import
import pickle
# import sys
import socket
import selectors
# import time
# import types
import logging

# Standard Modules Import

# Sim Open Interface Import


class SimOpIntClient:

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return 'This is the main Interface TCP Client Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

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

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.logger.debug(f'Sim Open Interface TCP Client Class Intialisation')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Method
    ###################################

    ###################################
    # Client Method
    ###################################

    # getCliName()
    # Return client name (str)
    def getCliName(self) -> str:
        return self.cliname

    # setCliname(cliname)
    # cliname is str
    # Set client name to cliname
    def setCliname(self, cliname: str) -> None:
        self.cliname = cliname

    # getSrvName()
    # Return server name (str)
    def getSrvName(self) -> str:
        return self.srvname

    # setSrvName(srvname)
    # srvname is str
    # Set server name to srvname
    def setSrvName(self, srvname) -> None:
        self.srvname = srvname

    # getSrvAddr()
    # Return server address (str)
    def getSrvAddr(self) -> str:
        return self.srvaddr

    # setSrvAddr(srvaddr)
    # srvaddr is str
    # Set server address to srvaddr
    def setSrvAddr(self, srvaddr) -> None:
        self.srvaddr = srvaddr

    # getSrvPort()
    # Return server port (int)
    def getSrvPort(self) -> int:
        return self.srvport

    # setSrvPort(srvport)
    # srvport is int
    # Set server port to srvport
    def setSrvPort(self, srvport) -> None:
        self.srvport = srvport

    # openCliSocket()
    # Open client socket
    def openCliSocket(self) -> None:
        self.logger.debug(f'Opening Server Socket ...')
        self.clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clisock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.logger.debug(f'Client Socket Opened ...')

    # closeCliSocket()
    # Close client socket
    def closeCliSocket(self) -> None:
        self.logger.debug(f'Closing Client Socket ...')
        if self.clisock:
            self.clisock.close()
        self.logger.debug(f'Client Socket Closed ...')

    # connectClient()
    # Connect client socket to server socket
    def connectClient(self) -> None:
        self.clisock.connect((self.srvaddr, self.srvport))
        # self.receiveMessage()

    ###################################
    # DATA Method
    ###################################

    # receiveMessage()
    # Receive Message Process
    def receiveMessage(self):
        while True:
            if self.newmsg:
                incom_data = self.clisock.recv(self.headersize)
                if incom_data:
                    self.newmsg = False
                    self.msgfullsize = int(incom_data.decode('utf-8'))
                    self.remainsize = self.msgfullsize
                    self.logger.info(f'New message arrived. Message length : {self.msgfullsize}. Remaining data to be received : {self.remainsize}')
            else:
                if self.remainsize > self.buffersize:
                    incom_data = self.clisock.recv(self.buffersize)
                else:
                    incom_data = self.clisock.recv(self.remainsize)
                received_data_len = len(incom_data)
                self.fullmsg += incom_data
                self.remainsize -= received_data_len
                self.logger.info(f'Receiving Message. Remaining data to be received : {self.remainsize}')
                if self.remainsize == 0:
                    self.logger.info(f'Fully message received : {pickle.loads(self.fullmsg)}')
                    self.newmsg = True
                    self.remainsize = 0
                    self.msgfullsize = 0
                    self.fullmsg = b''
                    break

    # sendMessage()
    # Send Message Process
    def sendMessage(self, data):
        self.logger.info(f'Sending message {data} to {self.srvname}')
        enc_data = self.encodeMessage(data)
        self.clisock.send(enc_data)

    # encodeMessage(data)
    # Encoding Message Process
    # Return encoded data in bytes format
    def encodeMessage(self, data) -> bytes:
        dataheader = f'{len(pickle.dumps(data)):<{self.headersize}}'.encode('utf-8')
        return dataheader + pickle.dumps(data)

    # decodeMessage(data)
    # Decoding Message Process
    # Return decoded data encoded in bytes format
    def decodeMessage(self, data):
        message = data[self.headersize:]
        return pickle.loads(message)

    ###################################
    # Loop Method
    ###################################
