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
# FarmerSoft Open Interface Daemon Class
##################################################
# SimOpIntd Class
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

        self.logger.info(f'Sim Open Interface Server Class Intialisation')

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

    # Get Server Address
    def getSrvAddr(self) -> str:
        return self.srvaddr

    # Get Server Port
    def getSrvPort(self) -> int:
        return self.srvport

    # Get Server Status
    def getSrvStatus(self) -> int:
        pass

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

    # Start Server
    def startSrvLoop(self) -> None:
        self.running = True

    # Stop Server
    def stopSrvLoop(self) -> None:
        self.running = False

    def closeServer(self) -> None:
        self.srvstate = False

    #############################################
    # DATA Method
    #############################################

    def connexionHandler(self, sock, mask) -> None:
        clisock, cliaddr = sock.accept()
        self.logger.debug(f'Connexion {clisock} from {cliaddr}')

        srvname_blen = len(self.srvname.encode('utf-8'))
        header = f'{srvname_blen:<{self.headersize}}'.encode('utf-8')
        srvname_msg = header+self.srvname.encode('utf-8')
        self.logger.info(f'Srv Name : {self.srvname} [bl : {srvname_blen}] | header : {header} | Srv Name Message : {srvname_msg}')

        clisock.send(srvname_msg)

        clisock.setblocking(False)
        data = types.SimpleNamespace(cliaddr=cliaddr, handler=self.dataHandler)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selsock.register(clisock, events, data=data)

    def dataHandler(self, clisock, mask) -> None:
        data = self.selsock.get_map()[clisock].data
        self.logger.debug(f'Processing Socket {clisock} from {data.cliaddr} [{type(self.fullmsg)}]')

        if mask & selectors.EVENT_READ:
            self.logger.debug(f'Reading Socket {clisock} from {data.cliaddr}')

            if self.newmsg:
                incom_data = clisock.recv(self.headersize)
                if incom_data:
                    self.newmsg = False
                    self.msgfullsize = int(incom_data.decode('utf-8'))
                    self.remainsize = int(incom_data.decode('utf-8'))
                    self.logger.info(f'New Message ! Full Message Length {self.msgfullsize} [{type(self.msgfullsize)}]. Remaining Size : {self.remainsize} [{type(self.remainsize)}]')

                    incom_data = clisock.recv(self.buffersize)
                    incom_data_len = len(incom_data)
                    self.fullmsg = incom_data
                    self.remainsize = self.remainsize - incom_data_len

                else:
                    self.selsock.unregister(clisock)
                    clisock.close()

            else:
                if self.remainsize > self.buffersize:
                    incom_data = clisock.recv(self.buffersize)
                else:
                    incom_data = clisock.recv(self.remainsize)
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

        if mask & selectors.EVENT_WRITE:
            self.logger.debug(f'Writing Socket {clisock} to {data.cliaddr}')

            """
            if self.newmsg:
                sent = clisock.send(f'Message Received'.encode('utf-8'))
                self.newmsg = False
            """

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
