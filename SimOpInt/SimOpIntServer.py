##################################################
# FarmerSoft Open Interface Daemon Class
##################################################
# SimOpIntServer Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# System Modules Import
import pickle
import sys
import socket
import selectors
import time
import types
import logging
import signal

# Standard Modules Import

# Sim Open Interface Import


class SimOpIntServer:

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return 'This is the main Interface Daemon Server Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

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

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        signal.signal(signal.SIGTERM, self.signalHandler)
        signal.signal(signal.SIGINT, self.signalHandler)

        self.logger.debug(f'Sim Open Interface Server Class Intialisation')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Method
    ###################################

    ###################################
    # Server Method
    ###################################

    # getSrvName()
    # Return server name
    def getSrvName(self) -> str:
        return self.srvname

    # setSrvName(srvname)
    # srvname is str
    # Set Server Name
    def setSrvName(self, srvname) -> None:
        self.srvname = srvname

    # getSrvAddr()
    # Return server address (int)
    def getSrvAddr(self) -> str:
        return self.srvaddr

    # setSrvAddr(srvaddr)
    # srvaddr is int
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

    # getSrvStatus()
    # Return server status
    def getSrvStatus(self) -> int:
        return self.srvstate

    # setSrvStatus(state)
    # Set server status to state
    def setSrvStatus(self, state) -> None:
        self.srvstate = state

    # openSrvSocket()
    # Open Server Socket
    def openSrvSocket(self) -> None:
        self.logger.info(f'Opening Server Socket ...')
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.srvsock.bind((self.srvaddr, self.srvport))
        self.srvsock.listen()
        self.srvsock.setblocking(False)
        events = selectors.EVENT_READ
        data = types.SimpleNamespace(srvaddr=self.srvaddr, handler=self.connexionHandler)
        self.selsock.register(self.srvsock, events, data=data)
        self.logger.info(f'Server Socket Opened...')
        self.srvstate = True

    # closeSrvSocket()
    # Close Server Socket
    def closeSrvSocket(self) -> None:
        self.logger.info(f'Closing Server Socket ...')
        self.selsock.close()
        if self.srvsock:
            self.srvsock.close()
        self.logger.info(f'Server Socket Closed ...')

    # startSrvLoop()
    # Start Server Loop
    def startSrvLoop(self) -> None:
        self.running = True

    # stopSrvLoop()
    # Stop Server Loop
    def stopSrvLoop(self) -> None:
        self.running = False

    # closeServer()
    # Close Server
    def closeServer(self) -> None:
        self.setSrvStatus(False)

    # signalHandler()
    # SIGTERM Handler
    def signalHandler(self, sig, frame) -> None:
        self.stopSrvLoop()
        self.closeServer()

    ###################################
    # DATA Method
    ###################################

    # Connexion Handler
    def connexionHandler(self, sock, mask) -> None:
        clisock, cliaddr = sock.accept()
        self.logger.debug(f'Connexion {clisock} from {cliaddr}')

        msgsrvname = self.encodeMessage(self.srvname)
        clisock.send(msgsrvname)

        clisock.setblocking(False)
        data = types.SimpleNamespace(cliaddr=cliaddr, handler=self.dataHandler, newmsg=True)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selsock.register(clisock, events, data=data)

    # Data Handler
    def dataHandler(self, clisock, mask) -> None:
        data = self.selsock.get_map()[clisock].data

        if mask & selectors.EVENT_READ:
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
                self.logger.debug(f'Receiving message. Remaining data to be received : {self.remainsize}')
                if self.remainsize == 0:
                    self.logger.info(f'Fully message received : {pickle.loads(self.fullmsg)}')
                    data.newmsg = True
                    self.remainsize = 0
                    self.msgfullsize = 0
                    self.fullmsg = b''

        if mask & selectors.EVENT_WRITE:
            """
            enc_data = self.encodeMessage(data)
            self.clisock.send(enc_data)
            """

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

    # Server Main Loop
    def mainLoop(self):

        self.logger.info(f'Starting Server ....')

        self.openSrvSocket()

        self.logger.info(f'Server Started ....')

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

        self.logger.info(f'Stopping Server ....')

        self.closeSrvSocket()

        self.logger.info(f'Server Stopped ....')
