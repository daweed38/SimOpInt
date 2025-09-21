##################################################
# FarmerSoft Open Interface Daemon Class
##################################################
# SimOpIntServer Class REV 5.0
# FarmerSoft © 2025
# By Daweed
##################################################

# Standard Modules Import
import sys
import logging
import time
import socket
import signal
import selectors
import types
import pickle
import threading

# Sim Open Interface Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpInt import SimOpInt


class SimOpIntDaemon:

    ###################################
    # Class Description
    ###################################

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, configfile: str = 'config.json', debug: int = 30) -> None:
        self.debug = debug
        self.side = None
        self.configdir = 'Config/Daemon'
        self.configfile = configfile
        self.baseconfigintdir = 'Config/Interfaces'
        self.sock = None
        self.selsock = selectors.DefaultSelector()
        self.headersize = 10
        self.buffersize = 32
        self.status = 0
        self.running = False
        self.newmsg = True
        self.msgfullsize = 0
        self.fullmsg = b''
        self.remainsize = 0
        self.clisocks = {}
        self.interface = None
        self.daemon_thread = None

        # Get Logger
        self.logger = logging.getLogger('SimOpInt.SimOpIntDaemon')

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.config = SimOpIntConfig(self.configdir, self.configfile)
        self.name = self.config.getConfigParameter('DAEMON', 'name')
        self.addr = self.config.getConfigParameter('DAEMON', 'addr')
        self.port = int(self.config.getConfigParameter('DAEMON', 'port'))
        self.side = self.config.getConfigParameter('DAEMON', 'side')
        self.intautoload = self.config.getConfigParameter('DAEMON', 'intautoload')

        # IF autoload is True Then loading Sim Open Interface Configuration
        if self.intautoload:
            # SimOpInt Interface Creation
            self.intshortname = self.config.getConfigParameter('INTERFACE', 'shortname')
            self.interface = SimOpInt('Config/Interfaces/' + self.intshortname, self.intshortname + '.json')

        signal.signal(signal.SIGTERM, self.signalHandler)
        signal.signal(signal.SIGINT, self.signalHandler)

        self.logger.info(f'Sim Open Interface Daemon Initialized')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        self.logger.info(f'Sim Open Interface Daemon Unloaded')
        
    ###################################
    # System Methods
    ###################################
    
    # getName()
    # Return Daemon name
    def getName(self) -> str:
        return self.name
    
    # setName(name)
    # name is str
    # Set Server Name
    def setName(self, name: str) -> None:
        self.name = name
    
    # getAddr()
    # Return server address (str)
    def getAddr(self) -> str:
        return self.addr
    
    # setAddr(addr)
    # addr is str
    # Set daemon address to addr
    def setAddr(self, addr: str) -> None:
        self.addr = addr
    
    # getPort()
    # Return daemon port (int)
    def getPort(self) -> int:
        return self.port
    
    # setDaemonPort(port)
    # port is int
    # Set daemon port to port
    def setPort(self, port: int) -> None:
        self.port = port
    
    # getDaemonStatus()
    # Return server status
    def getStatus(self) -> int:
        return self.status
    
    # setDaemonStatus(status)
    # Set server status to state
    def setStatus(self, status: int) -> None:
        self.status = status
    
    # getConfig()
    # Return server configuration (SimOpIntConfig Object)
    def getConfig(self) -> SimOpIntConfig:
        return self.config

    # getInterface()
    # Return SimOpInt interface object
    def getInterface(self):
        return self.interface

    # getDaemonThreadState()
    # Get Interface Thread Status
    def getDaemonThreadState(self) -> bool | None:
        if self.daemon_thread is not None:
            return self.daemon_thread.is_alive()
        else:
            return None

    ###################################
    # TCP Socket Methods
    ###################################

    # openSrvSocket()
    # Open Server Socket
    def openSrvSocket(self) -> None:
        self.logger.debug(f'Opening Server Socket ...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.sock.bind((self.addr, self.port))
        self.sock.listen()
        self.sock.setblocking(False)
        events = selectors.EVENT_READ
        data = types.SimpleNamespace(srvaddr=self.addr, handler=self.connexionHandler)
        self.selsock.register(self.sock, events, data=data)
        self.logger.debug(f'Server Socket Opened...')
        self.setStatus(1)

    # closeSrvSocket()
    # Close Server Socket
    def closeSrvSocket(self) -> None:
        self.logger.debug(f'Closing Server Socket ...')
        self.selsock.close()
        if self.sock:
            self.sock.close()
        self.setStatus(0)
        self.logger.debug(f'Server Socket Closed ...')

    # openCliSocket()
    # Open client socket
    def openCliSocket(self) -> None:
        self.logger.debug(f'Opening Client Socket ...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.logger.debug(f'Client Socket Opened ...')
        self.setStatus(1)

    # closeCliSocket()
    # Close client socket
    def closeCliSocket(self) -> None:
        self.logger.debug(f'Closing Client Socket ...')
        if self.sock:
            self.sock.close()
        self.setStatus(0)
        self.sock = None
        self.logger.debug(f'Client Socket Closed ...')

    ###################################
    # TCP DATA Methods
    ###################################

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

    # sendMessage()
    # Send Message Process
    def sendMessage(self, data):
        self.logger.info(f'Sending message {data} to {self.name}')
        enc_data = self.encodeMessage(data)
        self.sock.send(enc_data)

    # receiveMessage()
    # Receive Message Process
    def receiveMessage(self, clisock):
        while True:
            if self.newmsg:
                incom_data = clisock.recv(self.headersize)
                if incom_data:
                    self.newmsg = False
                    self.msgfullsize = int(incom_data.decode('utf-8'))
                    self.remainsize = self.msgfullsize
                    self.logger.debug(
                        f'New message arrived. Message length : {self.msgfullsize}. Remaining data to be received : {self.remainsize}')
            else:
                if self.remainsize > self.buffersize:
                    incom_data = clisock.recv(self.buffersize)
                else:
                    incom_data = clisock.recv(self.remainsize)
                received_data_len = len(incom_data)
                self.fullmsg += incom_data
                self.remainsize -= received_data_len
                self.logger.debug(f'Receiving Message. Remaining data to be received : {self.remainsize}')
                if self.remainsize == 0:
                    self.logger.debug(f'Fully message received : {pickle.loads(self.fullmsg)}')
                    data = self.fullmsg
                    self.newmsg = True
                    self.remainsize = 0
                    self.msgfullsize = 0
                    self.fullmsg = b''
                    break
        return pickle.loads(data)

    # Connexion Handler
    def connexionHandler(self, sock, mask) -> None:
        clisock, cliaddr = sock.accept()
        self.logger.debug(f'Connexion {clisock} from {cliaddr}')
        msgsrvname = self.encodeMessage(self.name)
        clisock.send(msgsrvname)
        cliname = self.receiveMessage(clisock)
        self.logger.debug(cliname)
        clisock.setblocking(False)
        data = types.SimpleNamespace(cliaddr=cliaddr, cliname=cliname, handler=self.dataHandler, newmsg=True)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.clisocks[cliname] = {}
        self.clisocks[cliname]['output'] = None
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
                    self.logger.debug(
                        f'New message arrived. Message length : {self.msgfullsize}. Remaining data to be received : {self.remainsize}')

                else:
                    self.selsock.unregister(clisock)
                    if data.cliname in self.clisocks:
                        del self.clisocks[data.cliname]
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
                    self.logger.debug(
                        f'Fully message received : {pickle.loads(self.fullmsg)} {type(self.fullmsg)} {type(pickle.loads(self.fullmsg))}')
                    self.processMessage(data.cliname, pickle.loads(self.fullmsg))
                    data.newmsg = True
                    self.remainsize = 0
                    self.msgfullsize = 0
                    self.fullmsg = b''

        if mask & selectors.EVENT_WRITE:
            if data.cliname in self.clisocks and self.clisocks[data.cliname]['output'] is not None:
                outputdata = self.clisocks[data.cliname]['output']
                self.logger.debug(f'Sending dataout : {outputdata}')
                enc_data = self.encodeMessage(self.clisocks[data.cliname]['output'])
                clisock.send(enc_data)
                self.clisocks[data.cliname]['output'] = None

    ###################################
    # Server Methods
    ###################################

    # startSrvLoop()
    # Start Server Loop
    def startSrvLoop(self) -> None:
        self.setStatus(2)
        self.logger.debug(f'Main loop Started .... ')

    # stopSrvLoop()
    # Stop Server Loop
    def stopSrvLoop(self) -> None:
        self.setStatus(1)
        self.logger.debug(f'Main loop Stopped .... ')

    # startServer()
    # Star Server
    def startServer(self) -> None:
        if self.daemon_thread is None:
            self.logger.info(f'Starting SimOpInt Daemon Server')

            self.daemon_thread = threading.Thread(target=self.mainLoop)
            self.daemon_thread.start()

            while not self.getDaemonThreadState():
                time.sleep(1)

            while self.getStatus() != 1:
                time.sleep(1)

            self.startSrvLoop()

            self.logger.info(f'SimOpInt Daemon started')
        else:
            self.logger.critical(f'Daemon thread can\'t be created, already existing. Starting SimOpInt Daemon not started')
            self.stopServer()

    # stopServer()
    # stop Server
    def stopServer(self) -> None:
        if self.daemon_thread is not None:
            self.logger.info(f'Stopping SimOpInt Daemon Server')

            self.stopSrvLoop()

            while self.getStatus() != 1:
                time.sleep(1)

            self.setStatus(0)

            while self.getDaemonThreadState():
                time.sleep(1)

            self.logger.info(f'SimOpInt Daemon Server stopped')

        else:
            self.logger.critical(f'Daemon thread not found. Error in stopping server')

        sys.exit()

    # signalHandler()
    # SIGTERM Handler
    def signalHandler(self, sig, frame) -> None:
        self.stopSrvLoop()
        self.stopServer()

    ###################################
    # Client Methods
    ###################################

    # startCliLoop()
    # Start Client Loop
    def startCliLoop(self) -> None:
        if self.getStatus() < 2:
            self.logger.error(f'startCliLoop : Client not connected')
        else:
            self.running = True
            self.setStatus(3)
            self.logger.debug(f'Main loop Started .... ')

    # stopCliLoop()
    # Stop Client Loop
    def stopCliLoop(self) -> None:
        if self.getStatus() < 2:
            self.logger.error(f'stopCliLoop : Client not connected')
        elif self.getStatus() < 3:
            self.logger.error(f'Client not running')
        else:
            self.running = False
            self.setStatus(2)
            self.logger.debug(f'Main loop Stopped .... ')

    """
    # connectClient()
    # Connect client socket to server socket
    # def connectClient(self) -> None:
    def connectClient(self):
        if self.getStatus() < 1:
            self.logger.error(f'Client socket not opened')
        elif self.getStatus() > 2:
            self.logger.warning(f'Client already connected')
        else:
            self.sock.connect((self.addr, self.port))
            self.sendMessage(self.getName())
            srvname = self.receiveMessage()
            self.sock.setblocking(False)
            data = types.SimpleNamespace(srvname=srvname, srvaddr=self.addr, srvport=self.port, handler=self.dataHandler, newmsg=True)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            self.selsock.register(self.sock, events, data=data)
            self.setStatus(2)

    # disconnectClient()
    # Disconnect Client
    def stopClient(self) -> None:
        if self.getStatus() > 2:
            self.stopCliLoop()
        while self.getStatus() > 2:
            time.sleep(1)
        self.setStatus(0)
    """

    ###################################
    # Messages Process Method
    ###################################

    # processMessage(cliname, message)
    # Process Message received from Client
    # Message should be formated as a dictionary
    def processMessage(self, cliname, message) -> None:
        # Setting debug level Temporary
        # self.logger.setLevel(logging.DEBUG)

        self.logger.debug(f'Processing message from client {cliname}: {message}')

        # Begin Body Method

        if isinstance(message, dict) and 'msgtype' in message:
            match message['msgtype']:
                case 'cmd':
                    self.logger.debug(f'Processing Command Message ...')

                case 'dref':
                    self.logger.debug(f'Processing Data Message ...')

                case 'int':
                    self.logger.debug(f'Processing Interface Message ...')

                case 'config':
                    self.logger.debug(f'Processing Configuration Message ...')

                case _:
                    self.logger.debug(f'Wrong message type. Cannot be processed')

        else:
            self.logger.error(f'Message from client {cliname} cannot be processed. Wrong format. ({message})')

        # End Body Method

        self.logger.debug(f'Message from client {cliname} processed : {message}')

        # Reset debug level (Temporary)
        # self.logger.setLevel(self.debug)

    ###################################
    # Main Loop
    ###################################

    # Server Main Loop
    # side is str [ server | client ]
    def mainLoop(self):
        if self.side is not None:
            self.openSrvSocket()

            # while self.status != 0:
            while self.getStatus() != 0:

                # while self.running:
                while self.getStatus() > 1:

                    events = self.selsock.select(timeout=.5)
                    for key, mask in events:
                        callback = key.data.handler
                        callback(key.fileobj, mask)

                time.sleep(5)

            self.closeSrvSocket()

        else:
            self.logger.error(f'Daemon side (Server or Client) not defined ! Please add side parameter un daemon configuration')
