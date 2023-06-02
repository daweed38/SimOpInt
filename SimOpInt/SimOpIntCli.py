# System Modules Import
from datetime import datetime
import time
import pickle
import socket
import selectors
import types
import hashlib
import json

##################################################
# FarmerSoft Open Interface Client Class
##################################################
# SimOpIntCli Class
# FarmerSoft © 2022
# By Daweed
##################################################


class SimOpIntCli:
    """
    This Class is the main Interface TCP Client class
    Manage communication between X-Plane Plugin and Hardware
    Level 2  : SimOpIntCli Class Debug Level
    Level 21 : SimOpIntCli Server Loop Debug Level
    Level 22 : SimOpIntCli Server Socket Debug Level
    Level 23 : SimOpIntCli Server Selector Debug Level
    Level 24 : SimOpIntSrv Server Socket Read Debug Level
    Level 25 : SimOpIntSrv Server Read Message Debug Level
    Level 26 : SimOpIntSrv Server Socket Write Debug Level
    """

    #############################################
    # Properties
    #############################################

    #############################################
    # Constructor
    #############################################

    def __init__(self, name='SimOpIntCli', srvaddr='localhost', srvport=7000, debug=0) -> None:
        self.debug = debug
        self.intname = name
        self.intaddr = None
        self.intsock = None
        self.srvname = None
        self.srvaddr = srvaddr
        self.srvport = int(srvport)
        self.selsock = selectors.DefaultSelector()
        self.headersize = 10
        self.buffersize = 16
        self.signals = {'connected': False, 'loop': False, 'shutdown': False, 'newmsg': False}
        self.state = 0

        self.waitsleep = 0.5
        self.loopsleep = 0.005

        self.inData = {}
        self.inDatamd5 = ''
        self.outData = {}
        self.outDatamd5 = ''

        self.newmsg = True
        self.msglen = 0
        self.fullmsg = b''
        self.remainsize = 0

        if self.debug == 2:
            print(f"######################################################################")
            print(f"# Sim Open Interface Client {self.intname} initialization")
            print(f"######################################################################")
            print("\r")

    #############################################
    # Destructor
    #############################################

    def __del__(self) -> None:
        if self.debug == 2:
            print(f"######################################################################")
            print(f"# Sim Open Interface Client {self.intname} Ended")
            print(f"######################################################################")
            print("\r")

    #############################################
    # System Method
    #############################################

    def getName(self) -> str:
        return self.intname

    def getStatus(self) -> int:
        return self.state

    def getSrvAddr(self) -> str:
        return self.srvaddr

    def getSrvPort(self) -> int:
        return self.srvport

    def listSignals(self) -> dict:
        return self.signals

    def getSignal(self, signal) -> bool:
        if signal in self.signals.keys():
            signalvalue = self.signals[signal]
        else:
            signalvalue = False
        return signalvalue

    def setSignal(self, signal, value) -> None | bool:
        if signal in self.signals.keys():
            self.signals[signal] = value
        else:
            return False

    def getDebugLevel(self) -> int:
        return self.debug

    def setDebugLevel(self, debuglevel) -> None:
        self.debug = debuglevel

    #############################################
    # DATA Method
    #############################################

    # Return In Data Dictionary
    def getInData(self) -> dict:
        return self.inData

    # Set In Data Dictionary
    def setInData(self, indata: dict) -> None:
        self.inData = indata

    #############################################
    # Client Method
    #############################################

    def run(self) -> None:
        self.setSignal('loop', True)

    def pause(self) -> None:
        self.setSignal('loop', False)

    def shutdown(self) -> None:
        self.pause()
        self.setSignal('shutdown', True)

    def openSocket(self) -> None:
        if self.debug == 22:
            print(f"Opening Interface Socket at {datetime.now()} : {self.intsock}")

        self.intsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.intsock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)

        if self.debug == 22:
            print(f"Interface Socket Opened at {datetime.now()} : {self.intsock}")

    def closeSocket(self) -> None:
        if self.debug == 22:
            print(f"Closing Interface Socket at {datetime.now()} : {self.intsock}")

        self.setSignal('connected', False)

        self.selsock.unregister(self.intsock)
        self.intsock.close()

        if self.debug == 22:
            print(f"Interface Socket Closed at {datetime.now()} : {self.intsock}")

    def connexionHandle(self) -> None:
        try:
            # Connect to Sim Open Interface Server
            self.intsock.connect_ex((self.srvaddr, self.srvport))

            # Send Interface Name
            intname = pickle.dumps(self.getName())
            intname_msg = bytes(f'{len(intname):<{self.headersize}}', "utf-8") + intname
            self.intsock.sendall(intname_msg)

            # Receive Server Name
            srvname_r = self.intsock.recv(1024)
            srvname = pickle.loads(srvname_r[self.headersize:])

            if self.debug == 22:
                print(f"Connected to Server {srvname} Address {self.srvaddr} on Port {self.srvport}")

            # Set Signal "connected" to True
            self.setSignal('connected', True)

            # Set Interface Socket in Non Blocking Mode
            self.intsock.setblocking(False)

            # Set Client Socket Events & Register Client Socket
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(srvname=srvname, srvaddr=self.srvaddr, srvport=self.srvport)
            self.selsock.register(self.intsock, events, data=data)

        except TimeoutError:
            pass

        except OSError as e:
            print(f"OSError : {e}")

    def dataHandle(self, key, mask) -> None:
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            if self.debug == 23:
                print(f"Selector Read Step")

            try:
                indata = sock.recv(self.buffersize)

                if self.newmsg is True and len(indata) > 0:
                    self.newmsg = False
                    self.msglen = int(indata[:self.headersize])
                    self.remainsize = self.msglen + self.headersize
                    if self.debug == 24:
                        print(f"New Message at {datetime.now()}. Message Length {self.msglen}")

                self.fullmsg += indata
                self.remainsize -= len(indata)

                if self.remainsize < self.buffersize:
                    if self.remainsize < 0:
                        self.buffersize = 16
                    else:
                        self.buffersize = self.remainsize

                if self.debug == 24:
                    print(f"Message Length Waited {self.msglen} Full Message Length {len(self.fullmsg)}")

                if self.remainsize == 0 and self.newmsg is False:
                    self.inData = pickle.loads(self.fullmsg[self.headersize:])
                    self.setSignal('newmsg', True)
                    if self.debug == 25:
                        print(f"Full Message Received {self.inData}")
                    self.newmsg = True
                    self.msglen = 0
                    self.fullmsg = b''
                    self.remainsize = 0
                    self.buffersize = 16

            except TimeoutError:
                pass

            except OSError as e:
                print(f"OSError : {e}")

        if mask & selectors.EVENT_WRITE:
            if self.debug == 23:
                print(f"Selector Write Step")

            if len(self.outData) > 0:
                outDatamd5 = hashlib.md5(json.dumps(self.outData, sort_keys=True).encode()).hexdigest()
                if outDatamd5 != self.outDatamd5:
                    try:
                        if self.debug == 26:
                            print(f"Sending Data {self.outData}")
                        oudata = pickle.dumps(self.outData)
                        oudata_msg = bytes(f'{len(oudata):<{self.headersize}}', "utf-8") + oudata
                        sock.sendall(oudata_msg)

                    except OSError as e:
                        if self.debug == 22:
                            print(f"OSError {e}")
                        self.selsock.unregister(sock)
                        sock.close()

    #############################################
    # Client Loop Method
    #############################################

    def mainLoop(self):
        self.openSocket()

        while self.getSignal('shutdown') is not True:

            while self.getSignal('loop') is True:

                if self.debug == 21:
                    print(f"Client Loop in Progress at {datetime.now()}")

                if self.getSignal('connected') is False:
                    self.connexionHandle()

                else:
                    events = self.selsock.select(timeout=None)
                    for key, mask in events:
                        self.dataHandle(key, mask)

                # time.sleep(self.loopsleep)

            if self.debug == 21:
                print(f"Waiting for Client Loop to Start at {datetime.now()}")
            time.sleep(self.waitsleep)

        self.closeSocket()

        if self.debug == 21:
            print(f"Client Shutdown at {datetime.now()}")