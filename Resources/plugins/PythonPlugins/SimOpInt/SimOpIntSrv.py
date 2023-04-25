# System Modules Import
from datetime import datetime
import time
import pickle
import socket

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
        self.headersize = 10
        self.buffersize = 16
        self.signals = {'connected': False, 'loop': False, 'shutdown': False}
        self.state = 0
        self.inData = {}
        self.outData = {}
        self.msg_new_r = True
        self.msglen_r = 0
        self.remain_size_r = 0
        self.msg_full_r = b''

        self.waitsleep = 0.5
        self.loopsleep = 0.25

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
    # Server Method
    #############################################

    def start(self) -> None:
        self.setSignal('loop', True)

    def stop(self) -> None:
        self.setSignal('loop', False)

    def shutdown(self) -> None:
        self.stop()
        self.setSignal('shutdown', True)

    def serverOpenSocket(self) -> None:
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srvsock.bind((self.srvaddr, self.srvport))
        self.srvsock.settimeout(0.25)
        self.srvsock.listen()

    def serverCloseSocket(self) -> None:
        self.srvsock.close()
        self.setSignal('connected', False)

    def serveWaitConn(self) -> None:

        if self.debug == 11:
            print(f"Waiting for Connexion at {datetime.now()}")

        try:
            sock, addr = self.srvsock.accept()

            if self.debug == 11:
                print(f"Connexion from {addr} at {datetime.now()}")

            intname_r = sock.recv(1024)
            intname = pickle.loads(intname_r[self.headersize:])

            if self.debug == 11:
                print(f"Header : {intname_r[:self.headersize]}")
                print(f"Length Received : {len(intname_r)} Length intname {len(intname)}")
                print(f"Interface Name Message : {intname}")

            srvname = pickle.dumps(self.srvname)
            srvname_s = bytes(f'{len(srvname):<{10}}', "utf-8") + srvname
            sock.sendall(srvname_s)

            self.setSignal('connected', True)

        except TimeoutError:
            pass

    def serverDataProcess(self) -> None:
        if self.debug == 12:
            print(f"Processing Data at {datetime.now()}")

    #############################################
    # Server Loop Method
    #############################################

    def serverLoop(self):
        self.serverOpenSocket()
        while self.getSignal('shutdown') is not True:

            while self.getSignal('loop') is True:

                if self.getSignal('connected') is False:
                    if self.debug == 13:
                        print(f"Waiting for Connexion at {datetime.now()}")
                    self.serveWaitConn()

                else:
                    if self.debug == 13:
                        print(f"Server Loop in Progress at {datetime.now()}")
                    self.serverDataProcess()

                time.sleep(self.loopsleep)

            if self.debug == 13:
                print(f"Waiting for Server Loop to Start at {datetime.now()}")
            time.sleep(self.waitsleep)

        self.serverCloseSocket()

        if self.debug == 13:
            print(f"Server Shutdown at {datetime.now()}")
