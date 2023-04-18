# System Modules Import
import socket
import selectors
import types
import pickle
import time
import hashlib
from datetime import datetime

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
    Level 2 : SimOpIntCli Class Debug Level
    """

    #############################################
    # Properties
    #############################################

    #############################################
    # Constructor
    #############################################

    def __init__(self, name='SimOpIntCli', srvaddr='localhost', srvport=7000, debug=0) -> None:
        self.debug = debug
        self.name = name
        self.srvaddr = srvaddr
        self.srvport = int(srvport)
        self.clisock = None
        self.headersize = 10
        self.buffersize = 16
        self.signals = {'shutdown': False, 'loop': False, 'connect': False, 'kill': False}
        self.state = 0

        self.selector = selectors.DefaultSelector()
        self.looptimeout = 0.2
        self.seltimeout = 0.025

        self.msg_new_r = False
        self.msglen_r = 0
        self.remain_size_r = 0
        self.msg_full_r = b''
        
        self.inData = {}
        self.inData_md5 = ''
        self.outData = {}
        self.outData_md5 = ''

        self.connected = False

        if self.debug == 2:
            print(f"######################################################################")
            print(f"# Sim Open Interface Client {self.name} initialization")
            print(f"######################################################################")
            print("\r")

    #############################################
    # Destructor
    #############################################

    def __del__(self) -> None:
        if self.debug == 2:
            print(f"######################################################################")
            print(f"# Sim Open Interface Client {self.name} Ended")
            print(f"######################################################################")
            print("\r")

    #############################################
    # System Method
    #############################################

    def getName(self) -> str:
        return self.name

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

    def start(self) -> None:
        if not self.getSignal('loop'):
            self.setSignal('loop', True)

        if self.state != 1:
            self.state = 1

        if self.debug == 21:
            print(f"Client Started at {datetime.now()}")

    def stop(self) -> None:
        if self.getSignal('loop'):
            self.setSignal('loop', False)

        if self.state != 0:
            self.state = 0

        if self.debug == 21:
            print(f"Client Stopped at {datetime.now()}")

    def shutdown(self) -> None:
        self.stop()

        if not self.getSignal('shutdown'):
            self.setSignal('shutdown', True)

    #############################################
    # DATA Method
    #############################################

    def getOutData(self):
        return self.outData

    def setOutData(self, data):
        self.outData = data

    def getInData(self):
        return self.inData

    def setInData(self, data):
        self.inData = data

    #############################################
    # Client Methods
    #############################################

    def clientConnect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(True)
        sock.connect_ex((self.srvaddr, self.srvport))
        if self.debug == 21:
            print("Connecting to {} on port {}".format(self.srvaddr, self.srvport))

        self.connected = True

        intname = pickle.dumps(self.name)
        intname_msg = bytes(f'{len(intname):<{10}}', "utf-8") + intname
        sock.sendall(intname_msg)

        srvname_r = sock.recv(1024)
        srvname = pickle.loads(srvname_r[self.headersize:])

        if self.debug == 21:
            print(f"Header : {srvname_r[:self.headersize]}")
            print(f"Length Received : {len(srvname_r)} Length intname {len(srvname)}")
            print(f"Interface Name Message : {srvname}")

        sock.setblocking(False)

        data = types.SimpleNamespace(srvname=srvname, addr=self.srvaddr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        self.selector.register(sock, events, data=data)

    def clientDataProcess(self, key, mask):

        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:

            msg_r = sock.recv(self.buffersize)

            try:
                if self.msg_new_r and msg_r != b'':
                    self.msg_new_r = False
                    self.msglen_r = int(msg_r[:self.headersize])
                    self.msg_full_r = msg_r[self.headersize:]
                    self.remain_size_r = self.msglen_r - len(msg_r[self.headersize:])

                    if self.debug == 25:
                        print(f"New Message. Message Length : {self.msglen_r} Remaining Length : {self.remain_size_r}")

                elif msg_r != b'' and len(msg_r) > 0:
                    self.msg_full_r += msg_r
                    self.remain_size_r -= len(msg_r)

                    if self.debug == 25:
                        print(f"Continue Message. Message Length : {self.msglen_r} Remaining Length : {self.remain_size_r}")

                if self.remain_size_r < self.buffersize:
                    self.buffersize = self.remain_size_r

                if self.remain_size_r == 0 and self.msg_full_r != b'':
                    inData = pickle.loads(self.msg_full_r)

                    if self.debug == 26:
                        print(f"Full Message Received from {data.srvname} : {inData}")

                    self.inData = inData

                    self.msg_new_r = True
                    self.msg_full_r = b''
                    self.msglen_r = 0
                    self.buffersize = 16

            except OSError as e:
                print(f"Error Reading From Socket {e}")

        if mask & selectors.EVENT_WRITE:

            msg_s = pickle.dumps(self.getOutData())
            msg_full_s = bytes(f'{len(msg_s):<{10}}', "utf-8") + msg_s
            outData_md5 = hashlib.md5(msg_full_s).hexdigest()

            if self.outData_md5 != outData_md5:
                try:
                    if self.debug == 27:
                        print(f"Sending Data {self.getOutData()}")

                    sock.sendall(msg_full_s)

                    self.outData_md5 = outData_md5

                except OSError as e:
                    if self.debug == 27:
                        print(f"Error Sending : {e}")

    def clientShutdown(self, key, mask):
        sock = key.fileobj
        msg_shut = pickle.dumps('shutdown')
        msg_shut_s = bytes(f'{len(msg_shut):<{10}}', "utf-8") + msg_shut

        try:
            sock.sendall(msg_shut_s)
            if self.debug == 27:
                print("Sending Data ...")

        except OSError as e:
            if self.debug == 27:
                print(f"Error Sending : {e}")

        self.selector.unregister(sock)
        sock.close()

    #############################################
    # Client Loop Method
    #############################################

    def loopSimOpIntClient(self):

        while not self.getSignal('shutdown'):

            if self.debug == 23:
                print("Client Loop Stopped, Waiting to Start  ....")

            while self.getSignal('loop'):

                if not self.connected:
                    self.clientConnect()

                if self.debug == 23:
                    print("Client Loop in Progress")

                events = self.selector.select(timeout=self.seltimeout)

                for key, mask in events:
                    self.clientDataProcess(key, mask)

                # time.sleep(self.looptimeout)

            if self.connected:
                for key, mask in self.selector.select(timeout=0.5):
                    self.clientShutdown(key, mask)
                    self.connected = False

            time.sleep(self.looptimeout)

        if self.debug == 22:
            print("Client Socket Closed at {}".format(datetime.now()))

        if self.debug == 21:
            print("SimOpInt Server Shutdown at {}".format(datetime.now()))
