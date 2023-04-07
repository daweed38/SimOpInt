# System Modules Import
import socket
import selectors
import types
import pickle
import time
import hashlib
import logging
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

    def __init__(self, name='SimOpIntSrv', srvaddr='localhost', srvport=7000, debug=0):
        self.debug = debug
        self.srvname = name
        self.srvaddr = srvaddr
        self.srvport = int(srvport)
        self.srvsock = None
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

        self.client = 0

        # logging.basicConfig(filename='simopintsrv.log', level=logging.INFO)

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

    def getIntOutData(self, interface):
        return self.outData[interface]

    def setIntOuData(self, interface, data):
        self.outData[interface] = data

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
        data = types.SimpleNamespace(addr=addr, intname=intname, buffersize=self.buffersize, inData=b'', outData=b'', outData_md5='', msg_new_r=True, msg_full_r=b'', msglen_r=0, remain_size_r=0)

        self.selector.register(sock, events, data=data)

        self.client += 1

        self.inData[intname] = {}

    def serverDataProcess(self, key, mask):

        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            if self.debug == 12:
                print(f"Reading Socket from {sock} on Addr {data.addr}")

            try:
                msg_r = sock.recv(data.buffersize)

                if data.msg_new_r and msg_r != b'':

                    data.msg_new_r = False
                    data.msglen_r = int(msg_r[:self.headersize])
                    data.msg_full_r = msg_r[self.headersize:]
                    data.remain_size_r = data.msglen_r - len(msg_r[self.headersize:])

                    if self.debug == 15:
                        print("New Message. Message Length : {} Remaining Length : {}".format(data.msglen_r, data.remain_size_r))

                elif msg_r != b'' and len(msg_r) > 0:
                    data.msg_full_r += msg_r
                    data.remain_size_r -= len(msg_r)

                    if self.debug == 15:
                        print("Continue Message. Message Length : {} Remaining Length : {}".format(data.msglen_r, data.remain_size_r))

                if data.remain_size_r < data.buffersize:
                    data.buffersize = data.remain_size_r

                if data.remain_size_r == 0 and data.msg_full_r != b'':
                    data.inData = pickle.loads(data.msg_full_r)

                    if self.debug == 16:
                        print("Full Message Received from {} : {}".format(data.intname, data.inData))

                    if data.inData == 'shutdown':
                        self.selector.unregister(sock)
                        sock.close()

                    else:
                        self.inData[data.intname] = data.inData
                        data.msg_new_r = True
                        data.msg_full_r = b''
                        data.msglen_r = 0
                        data.buffersize = 16

            except OSError:
                print(f"Error Reading From Socket")

        if mask & selectors.EVENT_WRITE:

            msg_s = pickle.dumps(self.getIntOutData(data.intname))
            msg_full_s = bytes(f'{len(msg_s):<{10}}', "utf-8") + msg_s
            outData_md5 = hashlib.md5(msg_full_s).hexdigest()

            if data.outData_md5 != outData_md5:
                try:
                    sock.sendall(msg_full_s)
                    if self.debug == 17:
                        print(f"Sending Data to {data.intname} ... {self.getIntOutData(data.intname)}")

                    data.outData_md5 = outData_md5

                except OSError as e:
                    if self.debug == 17:
                        print(f"OSError {e}")

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

        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

                events = self.selector.select(timeout=self.seltimeout)

                for key, mask in events:
                    if key.data is None:
                        self.serverAcceptConn()
                    else:
                        self.serverDataProcess(key, mask)

                # time.sleep(self.looptimeout)

            time.sleep(self.looptimeout)

        if self.debug == 12:
            print("Server Socket {} Closed at {}".format(self.srvsock, datetime.now()))

        if self.debug == 11:
            print("SimOpInt Server Shutdown at {}".format(datetime.now()))

        self.srvsock.close()
