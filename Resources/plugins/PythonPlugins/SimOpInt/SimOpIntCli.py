# System Modules Import
from datetime import datetime
import time
import pickle
import socket

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
    """

    #############################################
    # Properties
    #############################################

    #############################################
    # Constructor
    #############################################

    def __init__(self, name='SimOpIntCli', srvaddr='localhost', srvport=7000, debug=0) -> None:
        self.debug = debug
        self.cliname = name
        self.srvaddr = srvaddr
        self.srvport = int(srvport)
        self.clisock = None
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

        if self.debug == 2:
            print(f"######################################################################")
            print(f"# Sim Open Interface Client {self.cliname} initialization")
            print(f"######################################################################")
            print("\r")

    #############################################
    # Destructor
    #############################################

    def __del__(self) -> None:
        if self.debug == 2:
            print(f"######################################################################")
            print(f"# Sim Open Interface Client {self.cliname} Ended")
            print(f"######################################################################")
            print("\r")

    #############################################
    # System Method
    #############################################

    def getName(self) -> str:
        return self.cliname

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
    # Client Method
    #############################################

    def start(self) -> None:
        self.setSignal('loop', True)

    def stop(self) -> None:
        self.setSignal('loop', False)

    def shutdown(self) -> None:
        self.stop()
        self.setSignal('shutdown', True)

    def clientOpenSocket(self) -> None:
        self.clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clisock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clisock.settimeout(0.25)

    def clientCloseSocket(self) -> None:
        self.clisock.close()
        self.setSignal('connected', False)

    def clientConnect(self) -> None:
        if self.debug == 21:
            print(f"Connection to Server {self.srvaddr} on Port {self.srvport} at {datetime.now()}")

        try:
            self.clisock.connect((self.srvaddr, self.srvport))

            cliname = pickle.dumps(self.cliname)
            srvname_s = bytes(f'{len(cliname):<{10}}', "utf-8") + cliname
            self.clisock.sendall(srvname_s)

            srvname_r = self.clisock.recv(1024)
            srvname = pickle.loads(srvname_r[self.headersize:])

            if self.debug == 21:
                print(f"Header : {srvname_r[:self.headersize]}")
                print(f"Length Received : {len(srvname_r)} Length intname {len(srvname)}")
                print(f"Server Name Message : {srvname}")

            self.setSignal('connected', True)

        except TimeoutError:
            pass

    def clientDataProcess(self) -> None:
        if self.debug == 22:
            print(f"Processing Data at {datetime.now()}")

    #############################################
    # Client Loop Method
    #############################################

    def clientLoop(self):
        self.clientOpenSocket()
        while self.getSignal('shutdown') is not True:

            while self.getSignal('loop') is True:

                if self.getSignal('connected') is False:
                    if self.debug == 23:
                        print(f"Waiting for Connexion at {datetime.now()}")
                    self.clientConnect()

                else:
                    if self.debug == 23:
                        print(f"Client Loop in Progress at {datetime.now()}")
                    self.clientDataProcess()

                time.sleep(self.loopsleep)

            if self.debug == 23:
                print(f"Waiting for Client Loop to Start at {datetime.now()}")
            time.sleep(self.waitsleep)

        self.clientCloseSocket()

        if self.debug == 23:
            print(f"Client Shutdown at {datetime.now()}")
