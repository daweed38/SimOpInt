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

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntUtils import SimOpIntUtils
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

    def __init__(self, debug: int = 30) -> None:
        self.debug = debug
        self.configdir = 'Config/Daemon'
        self.configfile = 'config.json'
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

        # Get Logger
        self.logger = logging.getLogger('SimOpInt.SimOpIntServer')

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        # Loading Sim Open Interface Server Configuration
        self.srvconfig = SimOpIntConfig(self.configdir, self.configfile)
        self.srvname = self.srvconfig.getConfigParameter('SERVER', 'srvname')
        self.srvaddr = self.srvconfig.getConfigParameter('SERVER', 'srvaddr')
        self.srvport = int(self.srvconfig.getConfigParameter('SERVER', 'srvport'))

        # Loading Sim Open Interfaces Utilities
        self.utils = SimOpIntUtils()

        # Loading Sim Open Interface Configuration
        self.intshortname = self.srvconfig.getConfigParameter('INTERFACE', 'intshortname')
        self.interface = SimOpInt('Config/Interfaces/' + self.intshortname, self.intshortname + '.json', logging.DEBUG)

        signal.signal(signal.SIGTERM, self.signalHandler)
        signal.signal(signal.SIGINT, self.signalHandler)

        self.logger.info(f'Sim Open Interface Daemon Initialized')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

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
        self.logger.debug(f'Main loop Stopped .... ')
        self.running = False
        self.setSrvStatus(1)

    # closeServer()
    # Close Server
    def closeServer(self) -> None:
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
                    self.logger.info(f'Fully message received : {pickle.loads(self.fullmsg)} {type(self.fullmsg)} {type(pickle.loads(self.fullmsg))}')
                    # self.processMessage(pickle.loads(self.fullmsg))
                    data.newmsg = True
                    self.remainsize = 0
                    self.msgfullsize = 0
                    self.fullmsg = b''

        if mask & selectors.EVENT_WRITE:
            if data.cliname in self.clisocks and self.clisocks[data.cliname]['output'] is not None:
                self.logger.info(f'Sending dataout : {self.clisocks[data.cliname]['output']}')
                enc_data = self.encodeMessage(self.clisocks[data.cliname]['output'])
                clisock.send(enc_data)
                self.clisocks[data.cliname]['output'] = None

    # receiveMessage()
    # Receive Message Process
    def receiveMessage(self, clisock):
        data = None
        while True:
            if self.newmsg:
                incom_data = clisock.recv(self.headersize)
                if incom_data:
                    self.newmsg = False
                    self.msgfullsize = int(incom_data.decode('utf-8'))
                    self.remainsize = self.msgfullsize
                    self.logger.info(f'New message arrived. Message length : {self.msgfullsize}. Remaining data to be received : {self.remainsize}')
            else:
                if self.remainsize > self.buffersize:
                    incom_data = clisock.recv(self.buffersize)
                else:
                    incom_data = clisock.recv(self.remainsize)
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

    # processMessage(message)
    # Process Message received from Client
    # Message should be formated as a dictionary
    def processMessage(self, message) -> None:
        self.logger.debug(f'Message Format Type : {type(message)}')
        if isinstance(message, dict) and 'type' in message:
            self.logger.debug(f'Processing message : {message}')
            if message['type'] == 'cmd':
                self.processCmd(message['name'], message['args'])
            else:
                msgtype = message['type']
                self.logger.error(f'Message type {msgtype} are not yet supported.')
        else:
            self.logger.warning(f'Message cannot be processed. Wrong format. ({message})')

    # processCmd(cmdname, cmdargs)
    # Process Command received from Message
    # cmdname is a string, cmdargs is a dictionary
    def processCmd(self, cmdname: str, cmdargs: dict) -> None:
        self.logger.debug(f'Executing Command {cmdname} with arguments {cmdargs}')
        """
        # list command
        if cmdname.lower() == 'list':
            try:
                objlist = self.utils.listObject(cmdargs['object'], cmdargs['filter'])
                self.logger.debug(f'{objlist}')
            except Exception as e:
                self.logger.error(f'Error in {cmdname} execution : {e}')
        # read command
        elif cmdname.lower() == 'read':
            try:
                data = self.utils.readData(cmdargs['object'], cmdargs['filter'])
            except Exception as e:
                self.logger.error(f'Error in {cmdname} execution : {e}')

        else:
            self.logger.error(f'Command {cmdname.lower()} not recognized or not yet implemented.')
        """

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
