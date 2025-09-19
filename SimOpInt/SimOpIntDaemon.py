##################################################
# FarmerSoft Open Interface Daemon Class
##################################################
# SimOpIntServer Class REV 5.0
# FarmerSoft © 2025
# By Daweed
##################################################

# Standard Modules Import
import pickle
import socket
import selectors
import sys
import time
import types
import logging
import signal

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

        # Get Logger
        self.logger = logging.getLogger('SimOpInt.SimOpIntServer')

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.config = SimOpIntConfig(self.configdir, self.configfile)
        self.name = self.config.getConfigParameter('DAEMON', 'name')
        self.addr = self.config.getConfigParameter('DAEMON', 'addr')
        self.port = int(self.config.getConfigParameter('DAEMON', 'port'))
        self.intautoload = self.config.getConfigParameter('DAEMON', 'intautoload')

        # IF autoload is True Then loading Sim Open Interface Configuration
        if self.intautoload:
            # SimOpInt Interface Creation
            self.intshortname = self.config.getConfigParameter('INTERFACE', 'intshortname')
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

    ###################################
    # TCP Socket Methods
    ###################################

    # openSrvSocket()
    # Open Server Socket
    def openSrvSocket(self) -> None:
        self.logger.debug(f'Opening Server Socket ...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.sock.bind((self.addr, self.addr))
        self.sock.listen()
        self.sock.setblocking(False)
        events = selectors.EVENT_READ
        data = types.SimpleNamespace(srvaddr=self.addr, handler=self.connexionHandler)
        self.selsock.register(self.sock, events, data=data)
        self.setStatus(1)
        self.logger.debug(f'Server Socket Opened...')

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
    # TCP Server Methods
    ###################################

    # signalHandler()
    # SIGTERM Handler
    def signalHandler(self, sig, frame) -> None:
        self.stopSrvLoop()
        self.stopServer()

    # startServer()
    # Star Server
    def startServer(self) -> None:
        pass

    # stopServer()
    # stop Server
    def stopServer(self) -> None:
        if self.getInterface() is not None:
            if self.getInterface().getIntThreadState():
                self.interface.stopInterface()
            while self.getInterface().getIntThreadState():
                time.sleep(1)
        if self.getStatus() > 1:
            self.stopSrvLoop()
        self.setStatus(0)

    # startSrvLoop()
    # Start Server Loop
    def startSrvLoop(self) -> None:
        self.running = True
        self.setStatus(2)
        self.logger.debug(f'Main loop Started .... ')

    # stopSrvLoop()
    # Stop Server Loop
    def stopSrvLoop(self) -> None:
        self.running = False
        self.setStatus(1)
        self.logger.debug(f'Main loop Stopped .... ')