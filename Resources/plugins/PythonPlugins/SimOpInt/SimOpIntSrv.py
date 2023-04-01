# System Modules Import
import socket
import selectors
import types
import pickle
import time
import hashlib
from datetime import datetime

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
    Level 1 : SimOpIntSrv Class Debug Level
    """

    #############################################
    # Properties
    #############################################

    #############################################
    # Constructor
    #############################################

    def __init__(self, name='SimOpIntSrv', addr='localhost', port=7000, debug=0):
        self.debug = debug
        self.srvname = name
        self.srvaddr = addr
        self.srvport = int(port)
        self.srvsock = None
        self.srvtimeout = 1
        self.clitimeout = 0.025
        self.headersize = 10
        self.BUFFERSIZE = 16
        self.signals = {'shutdown': False, 'loop': False, 'connect': False, 'kill': False}
        self.state = 0

        self.selector = selectors.DefaultSelector()

        self.inData = {}
        self.inData_md5 = ''
        self.outData = {}
        self.outData_md5 = ''

        self.client = 0

        if self.debug == 1:
            print("######################################################################")
            print("# Sim Open Interface Server {} initialization".format(self.srvname))
            print("# on {} port {}".format(self.srvaddr, self.srvport))
            print("######################################################################")
            print("\r")

    #############################################
    # Destructor
    #############################################

    def __del__(self):
        if self.debug == 1:
            print("######################################################################")
            print("# Sim Open Interface Server {} Ended".format(self.srvname))
            print("######################################################################")
            print("\r")

    #############################################
    # System Method
    #############################################

    def getName(self):
        return self.srvname

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
            signalvalue = self.signals[signal]
        else:
            signalvalue = False
        return signalvalue

    def setSignal(self, signal, value):
        if signal in self.signals.keys():
            self.signals[signal] = value
            return self.signals[signal]
        else:
            return False

    def getDebugLevel(self):
        return self.debug

    def setDebugLevel(self, debuglevel):
        self.debug = debuglevel

    def start(self):
        if not self.getSignal('loop'):
            self.setSignal('loop', True)
        if self.state != 1:
            self.state = 1
        if self.debug == 11:
            print("SimOpInt Server Started at {}".format(datetime.now()))

    def stop(self):
        if self.getSignal('loop'):
            self.setSignal('loop', False)
        if self.state != 0:
            self.state = 0
        if self.debug == 11:
            print("SimOpInt Server Stopped at {}".format(datetime.now()))

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

    def getInterInData(self, intname):
        return self.inData[intname]

    def setInData(self, data):
        self.inData = data

    def setInterInData(self, intname, indata):
        self.inData[intname] = indata


    #############################################
    # Server Method
    #############################################

    def serverAcceptConn(self):

        sock, addr = self.srvsock.accept()
        if self.debug == 11:
            print("Connexion from {} at {}".format(addr, datetime.now()))

        sock.setblocking(True)

        intname_r = sock.recv(1024)
        intname = pickle.loads(intname_r[self.headersize:])

        if self.debug == 11:
            print("Header : {}".format(intname_r[:self.headersize]))
            print("Length Received : {} Length intname".format(len(intname_r), len(intname)))
            print("Interface Name Message : {}".format(intname))

        srvname = pickle.dumps(self.srvname)
        srvname_s = bytes(f'{len(srvname):<{10}}', "utf-8") + srvname
        sock.sendall(srvname_s)

        sock.setblocking(False)

        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(addr=addr, intname=intname, msg_new_r=True, msg_full_r=b'', msglen_r=0, remain_size_r=0, oldmask='', olddata='')
        self.selector.register(sock, events, data=data)

        self.client += 1

        self.inData[intname] = {}

    def serverDataProcess(self, key, mask):

        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:

            msg_r = sock.recv(self.BUFFERSIZE)

            if data.msg_new_r and msg_r != b'':
                if self.debug == 15:
                    print("New Message. Message Length : {} Remaining Length : {}".format(data.msglen_r, data.remain_size_r))

                data.msg_new_r = False
                data.msglen_r = int(msg_r[:self.headersize])
                data.msg_full_r = msg_r[self.headersize:]
                data.remain_size_r = data.msglen_r - len(msg_r[self.headersize:])

            elif msg_r != b'' and len(msg_r) > 0:
                if self.debug == 15:
                    print("Continue Message. Message Length : {} Remaining Length : {}".format(data.msglen_r, data.remain_size_r))
                data.msg_full_r += msg_r
                data.remain_size_r -= len(msg_r)

            if data.remain_size_r < self.BUFFERSIZE:
                self.BUFFERSIZE = data.remain_size_r

            if data.remain_size_r == 0 and data.msg_full_r != b'':
                inData = pickle.loads(data.msg_full_r)

                if inData == 'shutdown':
                    print("Client {} Shutdown".format(data.intname))
                    try:
                        del self.inData[data.intname]
                    except KeyError:
                        print("Error when removing {} key in self.inData")
                    self.selector.unregister(sock)
                    sock.close()

                else:
                    if self.debug == 16:
                        print("Full Message Received from {} : {}".format(data.intname, inData))
                    self.inData[data.intname] = inData
                    data.msg_new_r = True
                    data.msg_full_r = b''
                    data.msglen_r = 0
                    self.BUFFERSIZE = 16

        if mask & selectors.EVENT_WRITE:

            msg_s = pickle.dumps(self.getOutData())
            msg_full_s = bytes(f'{len(msg_s):<{10}}', "utf-8") + msg_s
            outData_md5 = hashlib.md5(msg_full_s).hexdigest()

            if self.outData_md5 != outData_md5:
                try:
                    sock.sendall(msg_full_s)
                    if self.debug == 17:
                        print("Sending Data ...")
                    self.outData_md5 = outData_md5

                except OSError as e:
                    print("OSError")
                    if self.debug == 17:
                        print("Error Sending : {}".format(e))

    #############################################
    # Server Loop Method
    #############################################

    def loopSimOpIntServer(self):
        """
        Level 11 : SimOpIntSrv Level (Stop / Start Operation)
        Level 12 : SimOpIntSrv Socket Debug Level (Socket Open / Close)
        Level 13 : SimOpIntSrv Loop Debug Level (Stop / Start Loop)
        Level 14 : SimOpIntSrv Selector Debug Level
        Level 15 : SimOpIntSrv Socket Data Debug Level (Data Send / Received on Socket)
        Level 16 : SimOpIntSrv Received Message Debug Level
        Level 17 : SimOpIntSrv Sending Message Debug Level
        """
        oldmask = 0

        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.bind((self.srvaddr, self.srvport))
        self.srvsock.listen()
        self.srvsock.setblocking(False)

        if self.debug == 12:
            print("Server Socket Opened at {} : {}".format(datetime.now(), self.srvsock))

        self.selector.register(self.srvsock, selectors.EVENT_READ, data=None)

        while not self.getSignal('shutdown'):

            if self.debug == 13:
                print("Server Loop Stopped, Waiting to Start  ....")

            while self.getSignal('loop'):

                if self.debug == 13:
                    print("Server Loop in Progress ... ")

                events = self.selector.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.serverAcceptConn()
                    else:
                        self.serverDataProcess(key, mask)

                time.sleep(0.02)

            time.sleep(0.5)

        if self.debug == 12:
            print("Server Socket {} Closed at {}".format(self.srvsock, datetime.now()))

        if self.debug == 11:
            print("SimOpInt Server Shutdown at {}".format(datetime.now()))

        self.srvsock.close()