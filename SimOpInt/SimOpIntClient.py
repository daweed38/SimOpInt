##################################################
# FarmerSoft Open Interface TCP Client Class
##################################################
# SimOpIntClient Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# System Modules Import
import sys
import pickle
import socket
import selectors
import sys
import time
import types
import logging
import signal

# Standard Modules Import

# Sim Open Interface Import
# from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntUtils import SimOpIntUtils
# from SimOpInt.SimOpInt import SimOpInt


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

    # def __init__(self, cliname: str, srvname: str, srvaddr: str, srvport: str, debug: int = 30) -> None:
    # def __init__(self, debug: int = 30) -> None:
    # def __init__(self, configfile: str = 'config.json', debug: int = 30) -> None:
    def __init__(self, cliname: str = 'SimOpIntCli', srvname: str = 'SimOpIntSrv', srvaddr: str = 'localhost', srvport: int = 49500, debug: int = 30) -> None:
        self.debug = debug
        # self.configdir = 'Config/Client'
        # self.configfile = 'config.json'
        # self.configfile = configfile
        # self.baseconfigintdir = 'Config/Interfaces'
        self.cliname = cliname
        self.srvname = srvname
        self.srvaddr = srvaddr
        self.srvport = srvport
        self.clisock = None
        self.selsock = selectors.DefaultSelector()
        self.headersize = 10
        self.buffersize = 32
        self.running = False
        self.clistate = 0
        self.newmsg = True
        self.msgfullsize = 0
        self.fullmsg = b''
        self.remainsize = 0
        self.dataout = None

        # Get Logger
        self.logger = logging.getLogger('SimOpInt.SimOpIntClient')

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        # Loading Sim Open Interface Client Configuration
        # self.cliconfig = SimOpIntConfig(self.configdir, self.configfile)
        # self.cliname = self.cliconfig.getConfigParameter('CLIENT', 'cliname')
        # self.srvname = self.cliconfig.getConfigParameter('SERVER', 'srvname')
        # self.srvaddr = self.cliconfig.getConfigParameter('SERVER', 'srvaddr')
        # self.srvport = int(self.cliconfig.getConfigParameter('SERVER', 'srvport'))

        # Loading Sim Open Interfaces Utilities
        self.utils = SimOpIntUtils()

        signal.signal(signal.SIGTERM, self.signalHandler)
        signal.signal(signal.SIGINT, self.signalHandler)

        self.logger.info(f'Sim Open Interface Client Initialized')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        self.logger.info(f'Sim Open Interface Client Unloaded')

    ###################################
    # System Method
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
    def setSrvName(self, srvname: str) -> None:
        self.srvname = srvname

    # getSrvAddr()
    # Return server address (str)
    def getSrvAddr(self) -> str:
        return self.srvaddr

    # setSrvAddr(srvaddr)
    # srvaddr is str
    # Set server address to srvaddr
    def setSrvAddr(self, srvaddr: str) -> None:
        self.srvaddr = srvaddr

    # getSrvPort()
    # Return server port (int)
    def getSrvPort(self) -> int:
        return self.srvport

    # setSrvPort(srvport)
    # srvport is int
    # Set server port to srvport
    def setSrvPort(self, srvport: int) -> None:
        self.srvport = srvport

    # getCliStatus()
    # Return server status
    def getCliStatus(self) -> int:
        return self.clistate

    # setCliStatus(state)
    # Set server status to state
    def setCliStatus(self, state: int) -> None:
        self.clistate = state

    # getCliConfig() # Remove as no client config is loaded 2025/05/15
    # Return Client configuration (SimOpIntConfig Object)
    # def getCliConfig(self) -> SimOpIntConfig:
    #    return self.cliconfig

    ###################################
    # Client Method
    ###################################

    # openCliSocket()
    # Open client socket
    def openCliSocket(self) -> None:
        self.logger.debug(f'Opening Client Socket ...')
        self.clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clisock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.logger.debug(f'Client Socket Opened ...')
        # self.connectClient()
        # srvname = self.receiveMessage()
        # self.clisock.setblocking(False)
        # data = types.SimpleNamespace(srvaddr=self.srvaddr, srvname=srvname, handler=self.dataHandler, newmsg=True)
        # events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # self.selsock.register(self.clisock, events, data=data)
        self.setCliStatus(1)

    # closeCliSocket()
    # Close client socket
    def closeCliSocket(self) -> None:
        self.logger.debug(f'Closing Client Socket ...')
        if self.clisock:
            self.clisock.close()
        self.setCliStatus(0)
        self.clisock = None
        self.logger.debug(f'Client Socket Closed ...')

    # connectClient()
    # Connect client socket to server socket
    # def connectClient(self) -> None:
    def connectClient(self):
        if self.getCliStatus() < 1:
            self.logger.error(f'Client socket not opened')
        elif self.getCliStatus() > 2:
            self.logger.warning(f'Client already connected')
        else:
            self.clisock.connect((self.srvaddr, self.srvport))
            self.sendMessage(self.getCliName())
            srvname = self.receiveMessage()
            self.clisock.setblocking(False)
            data = types.SimpleNamespace(srvname=srvname, srvaddr=self.srvaddr, srvport=self.srvport, handler=self.dataHandler, newmsg=True)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            self.selsock.register(self.clisock, events, data=data)
            self.setCliStatus(2)

    # disconnectClient()
    # Disconnect Client
    def stopClient(self) -> None:
        if self.getCliStatus() > 2:
            self.stopCliLoop()
        self.setCliStatus(0)

    # startCliLoop()
    # Start Client Loop
    def startCliLoop(self) -> None:
        if self.getCliStatus() < 2:
            self.logger.error(f'startCliLoop : Client not connected')
        else:
            self.running = True
            self.setCliStatus(3)
            self.logger.debug(f'Main loop Started .... ')

    # stopCliLoop()
    # Stop Client Loop
    def stopCliLoop(self) -> None:
        if self.getCliStatus() < 2:
            self.logger.error(f'stopCliLoop : Client not connected')
        elif self.getCliStatus() < 3:
            self.logger.error(f'Client not running')
        else:
            self.running = False
            self.setCliStatus(2)
            self.logger.debug(f'Main loop Stopped .... ')

    # signalHandler()
    # SIGTERM Handler
    def signalHandler(self, sig, frame) -> None:
        self.stopCliLoop()
        self.stopClient()

    ###################################
    # DATA Method
    ###################################

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
                    self.logger.debug(f'New message arrived. Message length : {self.msgfullsize}. Remaining data to be received : {self.remainsize}')

                # else:
                #    self.selsock.unregister(clisock)
                #    clisock.close()

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
                    self.logger.info(f'Fully message received : {pickle.loads(self.fullmsg)} {type(self.fullmsg)} {type(pickle.loads(self.fullmsg))}')
                    self.processMessage(data.srvname, pickle.loads(self.fullmsg))
                    data.newmsg = True
                    self.remainsize = 0
                    self.msgfullsize = 0
                    self.fullmsg = b''

        if mask & selectors.EVENT_WRITE:
            if self.dataout is not None:
                self.logger.info(f'Sending dataout : {self.dataout}')
                enc_data = self.encodeMessage(self.dataout)
                clisock.send(enc_data)
                self.dataout = None

    # receiveMessage()
    # Receive Message Process
    def receiveMessage(self):
        data = None
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
                    data = self.fullmsg
                    self.newmsg = True
                    self.remainsize = 0
                    self.msgfullsize = 0
                    self.fullmsg = b''
                    break
        return pickle.loads(data)

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
    # Process Method
    ###################################

    # processMessage(srvname, message)
    # Process Message received from Client
    # Message should be formated as a dictionary
    def processMessage(self, srvname: str, message) -> None:
        # Setting debug level Temporary
        self.logger.setLevel(logging.DEBUG)

        # Begin Body Method
        self.logger.debug(f'Message Format Type : {type(message)}')
        if isinstance(message, dict):
            self.logger.debug(f'Processing message from Server {srvname} : {message}')
            self.logger.debug(f'Message from Server processed {srvname} : {message}')
        else:
            self.logger.error(f'Message from client cannot be processed. Wrong format. ({message})')
        # End Body Method

        # Reset debug level (Temporary)
        self.logger.setLevel(self.debug)

    ###################################
    # Loop Method
    ###################################

    # Server Main Loop
    def mainLoop(self):

        self.logger.info(f'Starting Client ....')

        self.openCliSocket()

        self.logger.info(f'Client Started ....')

        while self.clistate != 0:

            while self.running:
                events = self.selsock.select(timeout=.5)
                for key, mask in events:
                    callback = key.data.handler
                    callback(key.fileobj, mask)

                # time.sleep(1)

            time.sleep(5)

        self.logger.info(f'Stopping Client ....')

        self.closeCliSocket()

        self.logger.info(f'Client Stopped ....')

        # sys.exit()
