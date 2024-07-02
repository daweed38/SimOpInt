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
# FarmerSoft Open Interface Daemon Class
##################################################
# SimOpIntServer Class
# FarmerSoft © 2024
# By Daweed
##################################################


class SimOpIntServer:
    """
    This is the main Interface Daemon Class
    """

    #############################################
    # Class Description
    #############################################

    def __str__(self) -> str:
        return 'This is the main Interface Daemon Server Class'

    #############################################
    # Properties
    #############################################

    #############################################
    # Constructor
    #############################################

    def __init__(self, srvname: str, srvaddr: str, srvport: str, debug: int = 30) -> None:
        self.debug = debug
        self.srvname = srvname
        self.srvaddr = srvaddr
        self.srvport = int(srvport)
        self.srvsock = None
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

        self.logger.debug(f'Sim Open Interface Server Class Intialisation')

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
    # Server Method
    #############################################

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

    # Get Server Status
    def getSrvStatus(self) -> int:
        return self.srvstate

    # Get Server Status
    def setSrvStatus(self, status) -> None:
        self.srvstate = status

    # Open Server Socket
    def openSrvSocket(self) -> None:
        self.logger.debug(f'Opening Server Socket ...')
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.srvsock.bind((self.srvaddr, self.srvport))
        self.srvsock.listen()
        self.srvsock.setblocking(False)
        events = selectors.EVENT_READ
        data = types.SimpleNamespace(srvaddr=self.srvaddr, handler=self.connexionHandler)
        self.selsock.register(self.srvsock, events, data=data)
        self.logger.debug(f'Server Socket Opened...')
        self.srvstate = True

    # Close Server Socket
    def closeSrvSocket(self) -> None:
        self.logger.debug(f'Closing Server Socket ...')
        self.selsock.close()
        if self.srvsock:
            self.srvsock.close()
        self.logger.debug(f'Server Socket Closed ...')

    # Start Server Loop
    def startSrvLoop(self) -> None:
        self.running = True

    # Stop Server Loop
    def stopSrvLoop(self) -> None:
        self.running = False

    # Close Server
    def closeServer(self) -> None:
        self.setSrvStatus(False)

    #############################################
    # DATA Method
    #############################################

    def connexionHandler(self, sock, mask) -> None:
        clisock, cliaddr = sock.accept()
        self.logger.debug(f'Connexion {clisock} from {cliaddr}')

        msgsrvname = self.encodeMessage(self.srvname)
        clisock.send(msgsrvname)

        clisock.setblocking(False)
        data = types.SimpleNamespace(cliaddr=cliaddr, handler=self.dataHandler, newmsg=True)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selsock.register(clisock, events, data=data)

    def dataHandler(self, clisock, mask) -> None:
        data = self.selsock.get_map()[clisock].data
        self.logger.debug(f'Processing Socket {clisock} from {data.cliaddr} [{type(self.fullmsg)}]')

        if mask & selectors.EVENT_READ:
            self.logger.debug(f'Reading Socket {clisock} from {data.cliaddr}')

            if data.newmsg:
                incom_data = clisock.recv(self.headersize)
                if incom_data:
                    data.newmsg = False
                    self.msgfullsize = int(incom_data.decode('utf-8'))
                    self.remainsize = self.msgfullsize
                    self.logger.info(f'New message arrived. Message length : {self.msgfullsize}. Remaining data to be received : {self.remainsize}')

                else:
                    self.selsock.unregister(clisock)
                    clisock.close()

            else:
                if self.remainsize > self.buffersize:
                    incom_data = clisock.recv(self.buffersize)
                else:
                    incom_data = clisock.recv(self.remainsize)
                received_data_len = len(incom_data)
                self.fullmsg += incom_data
                self.remainsize -= received_data_len
                self.logger.info(f'Receiving message. Remaining data to be received : {self.remainsize}')
                if self.remainsize == 0:
                    self.logger.info(f'Fully message received : {pickle.loads(self.fullmsg)}')
                    data.newmsg = True
                    self.remainsize = 0
                    self.msgfullsize = 0
                    self.fullmsg = b''

        if mask & selectors.EVENT_WRITE:
            self.logger.debug(f'Writing Socket {clisock} to {data.cliaddr}')
            """
            enc_data = self.encodeMessage(data)
            self.clisock.send(enc_data)
            """

    def encodeMessage(self, data) -> bytes:
        dataheader = f'{len(pickle.dumps(data)):<{self.headersize}}'.encode('utf-8')
        return dataheader + pickle.dumps(data)

    def decodeMessage(self, data):
        message = data[self.headersize:]
        return pickle.loads(message)

    #############################################
    # Loop Method
    #############################################

    def mainLoop(self):

        self.openSrvSocket()

        while self.srvstate:
            self.logger.debug(f'Main loop stopped .... ')

            while self.running:
                self.logger.debug(f'Main loop running .... ')

                events = self.selsock.select(timeout=.5)
                for key, mask in events:
                    callback = key.data.handler
                    callback(key.fileobj, mask)

                # time.sleep(1)

            time.sleep(5)

        self.closeSrvSocket()
