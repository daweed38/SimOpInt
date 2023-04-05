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

    def __init__(self, name='SimOpIntCli', srvaddr='localhost', srvport=7000, debug=0):
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

        self.inData = {}
        self.inData_md5 = ''
        self.outData = {}
        self.outData_md5 = ''

        self.connected = False

        if self.debug == 2:
            print("######################################################################")
            print("# Sim Open Interface Client {} initialization".format(self.name))
            print("######################################################################")
            print("\r")

    #############################################
    # Destructor
    #############################################

    def __del__(self):
        if self.debug == 2:
            print("######################################################################")
            print("# Sim Open Interface Client {} Ended".format(self.name))
            print("######################################################################")
            print("\r")

    #############################################
    # System Method
    #############################################

    def getName(self):
        return self.name

    def getStatus(self):
        return self.state

    def getSrvAddr(self):
        return self.srvaddr

    def getSrvPort(self):
        return self.srvport

    def listSignals(self):
        return self.signals

    def getSignal(self, signal):
        if signal in self.signals.keys():
            return self.signals[signal]
        else:
            return False

    def setSignal(self, signal, value):
        self.signals[signal] = value

    def getDebugLevel(self):
        return self.debug

    def setDebugLevel(self, debuglevel):
        self.debug = debuglevel

    def start(self):
        if not self.getSignal('loop'):
            self.setSignal('loop', True)

        if self.state != 1:
            self.state = 1

        if self.debug == 21:
            print("Client Started at {}".format(datetime.now()))

    def stop(self):
        if self.getSignal('loop'):
            self.setSignal('loop', False)

        if self.state != 0:
            self.state = 0

        if self.debug == 21:
            print("Client Stopped at {}".format(datetime.now()))

    def shutdown(self):
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
            print("Header : {}".format(srvname_r[:self.headersize]))
            print("Length Received : {} Length intname".format(len(srvname_r), len(srvname)))
            print("Interface Name Message : {}".format(srvname))

        sock.setblocking(False)

        data = types.SimpleNamespace(srvname=srvname, addr=self.srvaddr, buffersize=self.buffersize, inData=b'', outData=b'', outData_md5='', msg_new_r=True, msg_full_r=b'', msglen_r=0, remain_size_r=0)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        self.selector.register(sock, events, data=data)

    def clientDataProcess(self, key, mask):

        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:

            msg_r = sock.recv(data.buffersize)

            try:
                if data.msg_new_r and msg_r != b'':
                    data.msg_new_r = False
                    data.msglen_r = int(msg_r[:self.headersize])
                    data.msg_full_r = msg_r[self.headersize:]
                    data.remain_size_r = data.msglen_r - len(msg_r[self.headersize:])

                    if self.debug == 25:
                        print("New Message. Message Length : {} Remaining Length : {}".format(data.msglen_r, data.remain_size_r))

                elif msg_r != b'' and len(msg_r) > 0:
                    data.msg_full_r += msg_r
                    data.remain_size_r -= len(msg_r)

                    if self.debug == 25:
                        print("Continue Message. Message Length : {} Remaining Length : {}".format(data.msglen_r,data.remain_size_r))

                if data.remain_size_r < data.buffersize:
                    data.buffersize = data.remain_size_r

                if data.remain_size_r == 0 and data.msg_full_r != b'':
                    data.inData = pickle.loads(data.msg_full_r)

                    if self.debug == 26:
                        print("Full Message Received from {} : {}".format(data.srvname, data.inData))

                    self.inData = data.inData

                    data.msg_new_r = True
                    data.msg_full_r = b''
                    data.msglen_r = 0
                    data.buffersize = 16

            except OSError as e:
                print(f"Error Reading From Socket {e}")

        if mask & selectors.EVENT_WRITE:

            msg_s = pickle.dumps(self.getOutData())
            msg_full_s = bytes(f'{len(msg_s):<{10}}', "utf-8") + msg_s
            outData_md5 = hashlib.md5(msg_full_s).hexdigest()

            if data.outData_md5 != outData_md5:
                try:
                    if self.debug == 27:
                        print("Sending Data ...")

                    sock.sendall(msg_full_s)

                    data.outData_md5 = outData_md5

                except OSError as e:
                    if self.debug == 27:
                        print("Error Sending : {}".format(e))

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
                print("Error Sending : {}".format(e))

        self.selector.unregister(sock)
        sock.close()

    #############################################
    # Client Loop Method
    #############################################

    def loopSimOpIntClient(self):
        """
        Level 21 : SimOpIntCli Debug Level (Stop / Start Operation)
        Level 22 : SimOpIntCli Socket Debug Level (Socket Open / Close)
        Level 23 : SimOpIntCli Loop Debug Level (Stop / Start Loop)
        Level 24 : SimOpIntCli Selector Debug Level
        Level 25 : SimOpIntCli Socket Data Debug Level (Data Send / Received on Socket)
        Level 26 : SimOpIntCli Received Message Debug Level
        Level 27 : SimOpIntCli Sending Message Debug Level
        """

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
