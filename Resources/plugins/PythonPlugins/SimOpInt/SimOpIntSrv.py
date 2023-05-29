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
# FarmerSoft Open Interface Server Class
##################################################
# SimOpIntSrv Class
# FarmerSoft © 2022
# By Daweed
##################################################


class SimOpIntSrv:
    """
    This Class is the main Interface TCP Server class
    Manage communication between X-Plane Plugin and Hardware
    Level 1  : SimOpIntSrv Class Debug Level
    Level 11 : SimOpIntSrv Server Loop Debug Level
    Level 12 : SimOpIntSrv Server Socket Debug Level
    Level 13 : SimOpIntSrv Server Selector Debug Level
    Level 14 : SimOpIntSrv Server Socket Read Debug Level
    Level 15 : SimOpIntSrv Server Read Message Debug Level
    Level 16 : SimOpIntSrv Server Socket Write Debug Level
    """

    #############################################
    # Properties
    #############################################

    #############################################
    # Constructor
    #############################################

    def __init__(self, name: str = 'SimOpIntSrv', srvaddr: str = 'localhost', srvport: int = 7000, debug: int = 0) -> None:
        self.debug = debug
        self.srvname = name
        self.srvaddr = srvaddr
        self.srvport = int(srvport)
        self.srvsock = None
        self.selsock = None
        self.headersize = 10
        self.buffersize = 32
        self.signals = {'connected': False, 'loop': False, 'shutdown': False}
        self.state = 0

        self.waitsleep = 0.5
        self.loopsleep = 0.01

        self.inData = {}
        self.inDatamd5 = {}
        self.outData = {}
        self.outDatamd5 = {}

        self.newmsg = True
        self.msglen = 0
        self.fullmsg = b''
        self.remainsize = 0

        self.interfaces = {}

        if self.debug == 1:
            print(f"######################################################################")
            print(f"# Sim Open Interface Server {self.srvname} initialization on {self.srvaddr} port {self.srvport}")
            print(f"######################################################################")
            print("\r")

    #############################################
    # Destructor
    #############################################

    def __del__(self) -> None:
        if self.debug == 1:
            print(f"######################################################################")
            print(f"# Sim Open Interface Server {self.srvname} Ended")
            print(f"######################################################################")
            print("\r")

    #############################################
    # System Method
    #############################################

    def getName(self) -> str:
        return self.srvname

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

    # Return Out Data Dictionary
    def getOutData(self) -> dict:
        return self.outData

    # Set Out Data Dictionary
    def setOutData(self, outdata: dict) -> None:
        self.outData = outdata

    # Return Out Data Dictionary for Interface intname
    def getIntOutData(self, intname: str) -> dict | bool:
        if intname in self.outData:
            return self.outData[intname]
        else:
            return False

    # Set Out Data Dictionary for Interface intname
    def setIntOutData(self, intname: str, outdata: dict) -> dict | bool:
        if intname in self.outData:
            self.outData[intname] = outdata
            return outdata
        else:
            return False

    def getIntMd5OutData(self, intname: str) -> str | bool:
        if intname in self.outDatamd5:
            return self.outDatamd5[intname]
        else:
            return False

    def setIntMd5OutData(self, intname: str, md5hash: str) -> str | bool:
        if intname in self.outDatamd5:
            self.outDatamd5[intname] = md5hash
            return md5hash
        else:
            return False

    #############################################
    # Server Method
    #############################################

    def run(self) -> None:
        self.setSignal('loop', True)

    def pause(self) -> None:
        self.setSignal('loop', False)

    def shutdown(self) -> None:
        self.waitsleep = 0.02
        self.pause()
        self.setSignal('shutdown', True)

    def openSocket(self) -> None:
        if self.debug == 12:
            print(f"Opening Server Socket at {datetime.now()} : {self.srvsock}")

        self.selsock = selectors.DefaultSelector()
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.srvsock.bind((self.srvaddr, self.srvport))
        self.srvsock.listen()
        self.srvsock.setblocking(False)
        self.selsock.register(self.srvsock, selectors.EVENT_READ, data=None)

        if self.debug == 12:
            print(f"Server Socket Opened at {datetime.now()} : {self.srvsock}")

    def closeSocket(self) -> None:
        if self.debug == 12:
            print(f"Closing Server Socket at {datetime.now()} : {self.srvsock}")

        self.selsock.unregister(self.srvsock)
        self.srvsock.close()
        self.selsock.close()

        if self.debug == 12:
            print(f"Server Socket Closed at {datetime.now()} : {self.srvsock}")

    def connexionHandle(self) -> None:
        try:
            # Accept Connexion from Sim Open Interface
            intsock, intaddr = self.srvsock.accept()

            # Receive Interface Name
            intname_r = intsock.recv(1024)
            intname = pickle.loads(intname_r[self.headersize:])

            # Sending Server Name
            srvname = pickle.dumps(self.getName())
            srvname_msg = bytes(f'{len(srvname):<{10}}', "utf-8") + srvname
            intsock.sendall(srvname_msg)

            if self.debug == 12:
                print(f"Connexion from Interface {intname} Address {intaddr}")

            # Set Client Socket in Non Blocking Mode
            intsock.setblocking(False)

            # Set Client Socket Events & Register Client Socket
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(intname=intname, intaddr=intaddr)
            self.selsock.register(intsock, events, data=data)
            self.outData[intname] = {}
            self.outDatamd5[intname] = ''

        except TimeoutError:
            pass

        except OSError as e:
            if self.debug == 12:
                print(f"OSError : {e}")
            else:
                pass

    def dataHandle(self, key, mask) -> None:
        sock = key.fileobj
        data = key.data
        intname = data.intname

        if mask & selectors.EVENT_READ:
            if self.debug == 13:
                print(f"Selector Read Step")

            try:
                indata = sock.recv(self.buffersize)

                if self.newmsg is True and len(indata) > 0:
                    self.newmsg = False
                    self.msglen = int(indata[:self.headersize])
                    self.remainsize = self.msglen + self.headersize
                    if self.debug == 14:
                        print(f"New Message at {datetime.now()} from {intname}. Message Length {self.msglen}")

                self.fullmsg += indata
                self.remainsize -= len(indata)

                if self.remainsize < self.buffersize:
                    if self.remainsize < 0:
                        self.buffersize = 16
                    else:
                        self.buffersize = self.remainsize

                if self.debug == 14:
                    print(f"Message Length Waited {self.msglen} Full Message Length {len(self.fullmsg)}")

                if self.remainsize == 0 and self.newmsg is False:
                    self.inData = pickle.loads(self.fullmsg[self.headersize:])
                    if self.debug == 15:
                        print(f"Full Message Received {self.inData} From {intname}")
                    self.newmsg = True
                    self.msglen = 0
                    self.fullmsg = b''
                    self.remainsize = 0
                    self.buffersize = 16

            except TimeoutError:
                pass

            except OSError as e:
                if self.debug == 12:
                    print(f"OSError {e}")

        if mask & selectors.EVENT_WRITE:
            if self.debug == 13:
                print(f"Selector Write Step for {intname}")

            if len(self.outData) > 0:
                outDatamd5 = hashlib.md5(json.dumps(self.outData[intname], sort_keys=True).encode()).hexdigest()
                if outDatamd5 != self.outDatamd5[intname]:
                    try:
                        if self.debug == 16:
                            print(f"Sending Data {self.outData[intname]}")
                        oudata = pickle.dumps(self.outData[intname])
                        oudata_msg = bytes(f'{len(oudata):<{10}}', "utf-8") + oudata
                        sock.sendall(oudata_msg)
                        self.outDatamd5[intname] = outDatamd5

                    except OSError as e:
                        if self.debug == 12:
                            print(f"OSError {e}")
                        self.selsock.unregister(sock)
                        if intname in self.outData:
                            del self.outData[intname]
                        if intname in self.outDatamd5:
                            del self.outDatamd5[intname]
                        sock.close()

    def closeClient(self, key):
        if self.debug == 12:
            print(f"Closing Interface Socket at {datetime.now()}")
        sock = key.fileobj
        self.selsock.unregister(sock)
        sock.close()

    #############################################
    # Server Loop Method
    #############################################

    def mainLoop(self):
        self.openSocket()

        while self.getSignal('shutdown') is not True:

            while self.getSignal('loop') is True:

                if self.debug == 11:
                    print(f"Server Loop in Progress at {datetime.now()}")

                events = self.selsock.select(timeout=self.waitsleep)
                for key, mask in events:
                    if key.data is None:
                        self.connexionHandle()
                    else:
                        self.dataHandle(key, mask)

                time.sleep(self.loopsleep)

            if self.debug == 11:
                print(f"Waiting for Server Loop to Start at {datetime.now()}")
            time.sleep(self.waitsleep)

        self.closeSocket()

        if self.debug == 11:
            print(f"Server Shutdown at {datetime.now()}")
