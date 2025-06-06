##################################################
# FarmerSoft Open Interface Daemon Class
##################################################
# SimOpIntServer Class REV 5.0
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
import threading

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntUtils import SimOpIntUtils
from SimOpInt.SimOpIntClient import SimOpIntClient
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
        self.configdir = 'Config/Daemon'
        self.configfile = configfile
        self.baseconfigintdir = 'Config/Interfaces'
        self.srvsock = None
        self.selsock = selectors.DefaultSelector()
        self.headersize = 10
        self.buffersize = 32
        self.running = False
        self.srvstate = 0
        self.newmsg = True
        self.msgfullsize = 0
        self.fullmsg = b''
        self.remainsize = 0
        self.clisocks = {}
        self.interface = None
        self.simopintcli = None
        self.simopintcli_thread = None

        # Get Logger
        self.logger = logging.getLogger('SimOpInt.SimOpIntServer')

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        # Loading Sim Open Interface Server Configuration
        self.srvconfig = SimOpIntConfig(self.configdir, self.configfile)
        self.srvname = self.srvconfig.getConfigParameter('SERVER', 'srvname')
        self.srvaddr = self.srvconfig.getConfigParameter('SERVER', 'srvaddr')
        self.srvport = int(self.srvconfig.getConfigParameter('SERVER', 'srvport'))
        self.srvintautoload = self.srvconfig.getConfigParameter('SERVER', 'srvintautoload')

        # Loading Sim Open Interfaces Utilities
        self.utils = SimOpIntUtils()

        # Loading Sim Open Interface Configuration
        if self.srvintautoload:
            # SimOpInt Interface Creation
            self.intshortname = self.srvconfig.getConfigParameter('INTERFACE', 'intshortname')
            self.interface = SimOpInt('Config/Interfaces/' + self.intshortname, self.intshortname + '.json')

            # SimOpInt Client Creation
            self.simopintcli = SimOpIntClient(debug=logging.INFO)
            self.startClient()

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

    # getSrvName()
    # Return server name
    def getSrvName(self) -> str:
        return self.srvname

    # setSrvName(srvname)
    # srvname is str
    # Set Server Name
    def setSrvName(self, srvname: str) -> None:
        self.srvname = srvname

    # getSrvAddr()
    # Return server address (int)
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

    # getSrvStatus()
    # Return server status
    def getSrvStatus(self) -> int:
        return self.srvstate

    # setSrvStatus(state)
    # Set server status to state
    def setSrvStatus(self, state: int) -> None:
        self.srvstate = state

    # getSrvConfig()
    # Return server configuration (SimOpIntConfig Object)
    def getSrvConfig(self) -> SimOpIntConfig:
        return self.srvconfig

    ###################################
    # Server Methods
    ###################################

    # openSrvSocket()
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
        self.setSrvStatus(1)
        self.logger.debug(f'Server Socket Opened...')

    # closeSrvSocket()
    # Close Server Socket
    def closeSrvSocket(self) -> None:
        self.logger.debug(f'Closing Server Socket ...')
        self.selsock.close()
        if self.srvsock:
            self.srvsock.close()
        self.setSrvStatus(0)
        self.logger.debug(f'Server Socket Closed ...')

    # startSrvLoop()
    # Start Server Loop
    def startSrvLoop(self) -> None:
        self.running = True
        self.setSrvStatus(2)
        self.logger.debug(f'Main loop Started .... ')

    # stopSrvLoop()
    # Stop Server Loop
    def stopSrvLoop(self) -> None:
        self.running = False
        self.setSrvStatus(1)
        self.logger.debug(f'Main loop Stopped .... ')

    # closeServer()
    # Close Server
    def closeServer(self) -> None:
        if self.getInterface() is not None:
            if self.getInterface().getIntThreadState():
                self.stopInterface()
            while self.getInterface().getIntThreadState():
                time.sleep(1)

        if self.getSrvStatus() > 1:
            self.stopSrvLoop()
        self.setSrvStatus(0)

    # signalHandler()
    # SIGTERM Handler
    def signalHandler(self, sig, frame) -> None:
        self.stopSrvLoop()
        self.closeServer()

    ###################################
    # INTERFACE Methods
    ###################################

    # getInterface()
    # Return SimOpInt object initialized by the Server
    def getInterface(self) -> SimOpInt:
        return self.interface

    # startInterface()
    # Open & Start Main Loop Interface
    def startInterface(self) -> None:
        simopint = self.getInterface()
        if simopint is not None:
            simopint.openInterface()
            while simopint.getIntStatus() != 1:
                time.sleep(0.5)
            simopint.startIntLoop()
        else:
            self.logger.error(f'Interface not defined. Cannot Start.')

    # stopInterface()
    # Stop Main Loop & Close Interface
    def stopInterface(self) -> None:
        simopint = self.getInterface()
        if simopint is not None:
            simopint.stopIntLoop()
            while simopint.getIntStatus() != 1:
                time.sleep(0.5)
            simopint.closeInterface()
        else:
            self.logger.error(f'Interface not defined. Cannot Stop.')

    ###################################
    # Client Methods
    ###################################

    def startClient(self):
        self.logger.info(f'Starting Interface Client {self.simopintcli.getCliName()}')
        # SimOpInt Client loop thread creation
        self.simopintcli_thread = threading.Thread(target=self.simopintcli.mainLoop)
        self.simopintcli_thread.start()

        while self.simopintcli.getCliStatus() < 1:
            time.sleep(1)

        self.logger.debug(f'startClient : simopintcli_thread : {self.simopintcli_thread.is_alive()} simopintcli status : {self.simopintcli.getCliStatus()}')
        self.simopintcli.connectClient()

        while self.simopintcli.getCliStatus() < 2:
            time.sleep(1)

        self.simopintcli.startCliLoop()
        self.logger.debug(f'startClient : simopintcli_thread : {self.simopintcli_thread.is_alive()} simopintcli status : {self.simopintcli.getCliStatus()}')
        self.logger.info(f'Interface Client {self.simopintcli.getCliName()} Started')

    ###################################
    # DATA Methods
    ###################################

    # Connexion Handler
    def connexionHandler(self, sock, mask) -> None:
        clisock, cliaddr = sock.accept()
        self.logger.debug(f'Connexion {clisock} from {cliaddr}')
        msgsrvname = self.encodeMessage(self.srvname)
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
                    self.logger.debug(f'New message arrived. Message length : {self.msgfullsize}. Remaining data to be received : {self.remainsize}')

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
                    self.logger.debug(f'Fully message received : {pickle.loads(self.fullmsg)} {type(self.fullmsg)} {type(pickle.loads(self.fullmsg))}')
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
                    self.logger.debug(f'New message arrived. Message length : {self.msgfullsize}. Remaining data to be received : {self.remainsize}')
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

    # processMessage(cliname, message)
    # Process Message received from Client
    # Message should be formated as a dictionary
    def processMessage(self, cliname, message) -> None:
        # Setting debug level Temporary
        self.logger.setLevel(logging.DEBUG)

        self.logger.debug(f'Processing message from client {cliname}: {message}')

        # Begin Body Method

        if isinstance(message, dict) and 'msgtype' in message:

            if message['msgtype'] == 'cmd':
                self.processcmd(message)

            elif message['msgtype'] == 'dref':
                self.processdref(message)

            else:
                self.logger.debug(f'Wrong message type. Cannot be processed')

        else:
            self.logger.error(f'Message from client {cliname} cannot be processed. Wrong format. ({message})')

        # End Body Method

        self.logger.debug(f'Message from client {cliname} processed : {message}')

        # Reset debug level (Temporary)
        self.logger.setLevel(self.debug)

    def processcmd(self, message):
        self.logger.debug(f'Processing command Message')

    def processdref(self, message):
        self.logger.debug(f'Processing data Message')
        
    ###################################
    # Loop Method
    ###################################

    # Server Main Loop
    def mainLoop(self):

        self.logger.info(f'Starting Server ....')

        self.openSrvSocket()

        self.logger.info(f'Server Started ....')

        while self.srvstate != 0:

            while self.running:

                events = self.selsock.select(timeout=.5)
                for key, mask in events:
                    callback = key.data.handler
                    callback(key.fileobj, mask)

                # time.sleep(1)

            time.sleep(5)

        self.logger.info(f'Stopping Server ....')

        self.closeSrvSocket()

        self.logger.info(f'Server Stopped ....')

        sys.exit()
