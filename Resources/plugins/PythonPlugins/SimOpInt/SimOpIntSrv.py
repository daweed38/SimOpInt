# System Modules Import
import socket
import selectors
import types
import pickle
import hashlib
import time
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

    def __init__(self, name: str = 'SimOpIntSrv', srvaddr: str = 'localhost', srvport: int = 7000, debug: int = 0) -> None:
        self.debug = debug
        self.srvname = name
        self.srvaddr = srvaddr
        self.srvport = int(srvport)
        self.srvsock = None
        self.headersize = 10
        self.buffersize = 32
        self.signals = {'shutdown': False, 'loop': False, 'connect': False, 'kill': False}
        self.state = 0

        self.selector = selectors.DefaultSelector()
        self.looptimeout = 0.2
        self.seltimeout = 0.025

        self.inData = {}
        self.outData = {}
        
        self.clients = {}

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

    def start(self) -> None:
        if not self.getSignal('loop'):
            self.setSignal('loop', True)

        if self.state != 1:
            self.state = 1

        if self.debug == 11:
            print(f"SimOpInt Server Started at {datetime.now()}")

    def stop(self) -> None:
        if self.getSignal('loop'):
            self.setSignal('loop', False)

        if self.state != 0:
            self.state = 0

        if self.debug == 11:
            print(f"SimOpInt Server Stopped at {datetime.now()}")

    def shutdown(self) -> None:
        self.stop()

        if not self.getSignal('shutdown'):
            self.setSignal('shutdown', True)

    #############################################
    # DATA Method
    #############################################

    # In Data

    def getInData(self) -> dict:
        return self.inData

    def setInData(self, data: dict) -> None:
        self.inData = data

    def createInterInData(self, intname: str) -> None:
        self.inData[intname] = {}

    def getInterInData(self, intname: str) -> dict | bool:
        if intname in self.inData:
            return self.inData[intname]
        else:
            return False

    def setInterInData(self, intname: str, indata: dict) -> None | bool:
        if intname in self.inData:
            self.inData[intname] = indata
        else:
            return False

    def removeObjInType(self, intname, objtype):
        if objtype in self.inData[intname]:
            del self.inData[intname][objtype]

    def removeObjIn(self, intname, objtype, objname):
        if objtype in self.inData[intname]:
            if objname in self.inData[intname][objtype]:
                del self.inData[intname][objtype][objname]

    # Out Data

    def getOutData(self) -> dict:
        return self.outData

    def setOutData(self, data: dict) -> None:
        self.outData = data

    def createInterOutData(self, intname: str) -> None:
        self.outData[intname] = {}

    def getInterOutData(self, intname: str) -> dict | bool:
        if intname in self.outData:
            return self.outData[intname]
        else:
            return False

    def setInterOuData(self, intname: str, data: dict) -> None | bool:
        if intname in self.outData:
            self.outData[intname] = data
        else:
            return False

    def removeObjOutType(self, intname, objtype):
        if objtype in self.outData[intname]:
            del self.outData[intname][objtype]

    def removeObjOut(self, intname, objtype, objname):
        if objtype in self.outData[intname]:
            if objname in self.outData[intname][objtype]:
                del self.outData[intname][objtype][objname]

    #############################################
    # CLIENT Method
    #############################################

    def getClient(self, intname: str) -> dict:
        return self.clients[intname]

    def getClientProp(self, intname, prop):
        client = self.getClient(intname)
        return client[prop]

    def setClientProp(self, intname, prop, propval):
        self.clients[intname][prop] = propval

    #############################################
    # Server Method
    #############################################

    def serverOpenSocket(self) -> None:
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srvsock.bind((self.srvaddr, self.srvport))
        self.srvsock.listen()
        self.srvsock.setblocking(False)
        self.selector.register(self.srvsock, selectors.EVENT_READ, data=None)

        if self.debug == 12:
            print(f"Server Socket Opened at {datetime.now()} : {self.srvsock}")

    def serverCloseSocket(self) -> None:
        self.selector.unregister(self.srvsock)
        self.srvsock.close()

    def serverAcceptConn(self) -> None:

        sock, addr = self.srvsock.accept()

        if self.debug == 11:
            print(f"Connexion from {addr} at {datetime.now()}")

        sock.setblocking(True)

        intname_r = sock.recv(1024)
        intname = pickle.loads(intname_r[self.headersize:])

        if self.debug == 11:
            print(f"Header : {intname_r[:self.headersize]}")
            print(f"Length Received : {len(intname_r)} Length intname {len(intname)}")
            print(f"Interface Name Message : {intname}")

        srvname = pickle.dumps(self.srvname)
        srvname_s = bytes(f'{len(srvname):<{10}}', "utf-8") + srvname
        sock.sendall(srvname_s)

        sock.setblocking(False)

        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # data = types.SimpleNamespace(addr=addr, intname=intname, buffersize=self.buffersize, inData=b'', outData=b'', outData_md5='', msg_new_r=True, msg_full_r=b'', msglen_r=0, remain_size_r=0)
        data = types.SimpleNamespace(addr=addr, intname=intname)
        self.selector.register(sock, events, data=data)

        self.clients[intname] = {}
        self.setClientProp(intname, 'msg_new_r', True)
        self.setClientProp(intname, 'msg_full_r', b'')
        self.setClientProp(intname, 'msglen_r', 0)
        self.setClientProp(intname, 'remain_size_r', 0)
        self.setClientProp(intname, 'buffersize', 16)
        self.setClientProp(intname, 'inData_md5', '')
        self.setClientProp(intname, 'outData_md5', '')
        self.setClientProp(intname, 'startmsg', None)
        self.setClientProp(intname, 'endmsg', None)

    def serverDataProcess(self, key, mask) -> None:

        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:

            if self.debug == 12:
                print(f"Reading Socket from {sock} on Addr {data.addr}")

            try:
                msg_r = sock.recv(self.clients[data.intname]['buffersize'])

                if self.getClientProp(data.intname, 'msg_new_r') and msg_r != b'':

                    if self.debug == 98:
                        self.setClientProp(data.intname, 'startmsg', str(datetime.now()))

                    self.setClientProp(data.intname, 'msg_new_r', False)
                    self.setClientProp(data.intname, 'msglen_r', int(msg_r[:self.headersize]))
                    self.setClientProp(data.intname, 'msg_full_r', msg_r[self.headersize:])

                    remain_size_r = self.clients[data.intname]['msglen_r'] - len(msg_r[self.headersize:])
                    self.setClientProp(data.intname, 'remain_size_r', remain_size_r)

                    if self.debug == 15:
                        print(f"New Message. Message Length : {self.getClientProp(data.intname, 'msglen_r')} Remaining Length : {self.getClientProp(data.intname, 'remain_size_r')}")

                elif msg_r != b'' and len(msg_r) > 0:
                    full_msg_r = self.getClientProp(data.intname, 'msg_full_r') + msg_r
                    self.setClientProp(data.intname, 'msg_full_r', full_msg_r)

                    remain_size_r = self.getClientProp(data.intname, 'remain_size_r') - len(msg_r)
                    self.setClientProp(data.intname, 'remain_size_r', remain_size_r)

                    if self.getClientProp(data.intname, 'remain_size_r') < 0:
                        self.setClientProp(data.intname, 'remain_size_r', 0)

                    if self.debug == 15:
                        print(f"Continue Message. Message Length : {self.getClientProp(data.intname, 'msglen_r')} Remaining Length : {self.getClientProp(data.intname, 'remain_size_r')}")

                if self.getClientProp(data.intname, 'remain_size_r') < self.getClientProp(data.intname, 'buffersize'):
                    self.setClientProp(data.intname, 'buffersize', self.getClientProp(data.intname, 'remain_size_r'))

                if self.getClientProp(data.intname, 'remain_size_r') == 0 and self.getClientProp(data.intname, 'msg_full_r') != b'':
                    indata = pickle.loads(self.getClientProp(data.intname, 'msg_full_r'))

                    if self.debug == 98:
                        self.setClientProp(data.intname, 'endmsg', str(datetime.now()))
                        duration = datetime.strptime(self.getClientProp(data.intname, 'endmsg'), "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(self.getClientProp(data.intname, 'startmsg'), "%Y-%m-%d %H:%M:%S.%f")
                        print(f"Start Read : {self.getClientProp(data.intname, 'startmsg')} End Read {self.getClientProp(data.intname, 'endmsg')} Duration : {duration} Message : {indata}")

                    if self.debug == 16:
                        print(f"Full Message Received from {data.intname} : {indata}")

                    if indata == 'shutdown':
                        self.selector.unregister(sock)
                        sock.close()

                    else:
                        self.setInterInData(data.intname, indata)
                        self.setClientProp(data.intname, 'msg_new_r', True)
                        self.setClientProp(data.intname, 'msg_full_r', b'')
                        self.setClientProp(data.intname, 'msglen_r', 0)
                        self.setClientProp(data.intname, 'buffersize', 16)

            except OSError as e:
                print(f"Error Reading From Socket {e}")

        if mask & selectors.EVENT_WRITE:

            if self.debug == 99:
                print(f"Start Write .... at {datetime.now()}")

            msg_s = pickle.dumps(self.getInterOutData(data.intname))
            msg_full_s = bytes(f'{len(msg_s):<{10}}', "utf-8") + msg_s
            outData_md5 = hashlib.md5(msg_full_s).hexdigest()

            if self.getClientProp(data.intname, 'outData_md5') != outData_md5:
                try:
                    sock.sendall(msg_full_s)
                    if self.debug == 17:
                        print(f"Sending Data to {data.intname} ... {self.getInterOutData(data.intname)}")

                    self.setClientProp(data.intname, 'outData_md5', outData_md5)

                except OSError as e:
                    if self.debug == 17:
                        print(f"OSError {e}")

            if self.debug == 99:
                print(f"End Write .... at {datetime.now()}")

    #############################################
    # Server Loop Method
    #############################################

    def loopSimOpIntServer(self) -> None:
        self.serverOpenSocket()

        while not self.getSignal('shutdown'):

            if self.debug == 13:
                print("Server Loop Stopped, Waiting to Start  ....")

            while self.getSignal('loop'):

                if self.debug == 13:
                    print(f"Server Loop in Progress ... {datetime.now()}")

                events = self.selector.select(timeout=self.seltimeout)

                for key, mask in events:

                    if key.data is None:
                        if self.debug == 97:
                            print(f"Start Accept Con at {datetime.now()}")

                        self.serverAcceptConn()

                        if self.debug == 97:
                            print(f"End Accept Con at {datetime.now()}")

                    else:
                        if self.debug == 97:
                            print(f"Start Server Data Process at {datetime.now()}")

                        self.serverDataProcess(key, mask)

                        if self.debug == 97:
                            print(f"End Server Data Process at {datetime.now()}")

            time.sleep(self.looptimeout)

        if self.debug == 12:
            print(f"Server Socket {self.srvsock} Closed at {datetime.now()}")

        if self.debug == 11:
            print(f"SimOpInt Server Shutdown at {datetime.now()}")

        self.serverCloseSocket()
