#!/usr/bin/env python
# -*-coding:Utf-8 -*

# System Modules Import
import os
import hashlib
import json
from datetime import datetime

# Standard Modules Import
import threading

# XPPython3
import xp

# SimOpInt
from PythonPlugins.SimOpInt.SimOpIntTools import SimOpIntTools
from PythonPlugins.SimOpInt.SimOpInt import SimOpInt
from PythonPlugins.SimOpInt.SimOpIntSrv import SimOpIntSrv
from PythonPlugins.SimOpInt.SimOpIntCli import SimOpIntCli

########################################
# FarmerSoft Sim Open Interface Plugin
########################################
# PythonInterface Class
# FarmerSoft © 2022
# By Daweed
########################################


class PythonInterface:
    def __init__(self) -> None:
        self.debug = 41
        self.srvdebug = 0

        self.Name = "SimOpInt"
        self.Sig = "xppython3.simopint"
        self.Desc = "Sim Open Interface"

        self.initialized = False
        self.datarefinit = False

        self.tools = SimOpIntTools(self.debug)

        self.aircraftdir = xp.extractFileAndPath(xp.getNthAircraftModel(0)[1])[1].removeprefix(xp.getSystemPath())
        self.configdir = self.aircraftdir + '/plugins/PythonPlugins/SimOpint/Config/'
        self.configdir_ok = False
        self.configfile = 'simopint.json'
        self.configfile_ok = False

        self.flightloopID = None
        self.pluginMenuID = None
        self.actionMenuID = None
        self.configMenuID = None

        self.simopintsrv = None
        self.threadsrv = None
        self.simopintcli = None
        self.threadcli = None

        self.simopintcfg = {}
        self.simopints = {}
        self.shared_data = {}

        self.flightloopcbktime = 0.02

        if self.debug == 1:
            xp.log(f"Plugin Init at {datetime.now()}")

    ##################################################
    # Plugin System Method (Required)
    ##################################################

    def XPluginStart(self) -> tuple:
        # Required by XPPython3
        # Called once by X-Plane on startup (or when plugins are re-starting as part of reload)
        # You need to return three strings

        if self.debug == 1:
            xp.log(f"Starting Plugin at {datetime.now()}")

        # Sim Open Interface Plugin Menu Creation
        self.pluginMenuID = xp.createMenu(name='SimOpInt', parentMenuID=None, parentItem=0, handler=self.pluginMenuCB,  refCon='simopint')

        xp.appendMenuItem(menuID=self.pluginMenuID, name='Actions', refCon=None)
        self.actionMenuID = xp.createMenu(name='Actions', parentMenuID=self.pluginMenuID, parentItem=0, handler=self.serverMenuCB, refCon='simopintcli')
        xp.appendMenuItem(menuID=self.actionMenuID, name='Start', refCon='start')
        xp.appendMenuItem(menuID=self.actionMenuID, name='Stop', refCon='stop')

        xp.appendMenuItem(menuID=self.pluginMenuID, name='Config', refCon=None)
        self.configMenuID = xp.createMenu(name='Config', parentMenuID=self.pluginMenuID, parentItem=1, handler=self.configMenuCB, refCon='config')
        xp.appendMenuItem(menuID=self.configMenuID, name='Open', refCon='open')
        xp.appendMenuItem(menuID=self.configMenuID, name='Read', refCon='read')

        xp.appendMenuSeparator(self.pluginMenuID)

        xp.appendMenuItem(menuID=self.pluginMenuID, name='About', refCon='about')

        if os.path.exists(self.configdir):
            if self.debug == 2:
                xp.log(f"Configuration Directory {self.configdir} Exist")
            self.configdir_ok = True

        if os.path.isfile(self.configdir+self.configfile):
            if self.debug == 2:
                xp.log(f"Configuration {self.configfile} found in {self.configdir}")
            self.configfile_ok = True

        if self.configdir_ok and self.configfile_ok:
            self.simopintcfg = self.tools.readJsonFile(self.configdir, self.configfile)
            if self.debug == 2:
                xp.log(f"Sim Open Interface Plugin Configuration : {self.simopintcfg}")
        else:
            xp.log(f"Configuration File {self.configdir} not found in {self.configfile}")

        if self.simopintcfg is not False:

            # Sim Open Interface Server Creation
            srvname = self.getConfigParam('NETWORK', 'srvname')
            srvaddr = self.getConfigParam('NETWORK', 'srvaddr')
            srvport = self.getConfigParam('NETWORK', 'srvport')

            if self.debug == 2:
                xp.log(f"Sim Open Interface Server {srvname} Creation with param Addr {srvaddr} / Port {srvport}")

            self.simopintsrv = SimOpIntSrv(name=srvname, srvaddr=srvaddr, srvport=srvport, debug=self.srvdebug)

            if self.debug == 2:
                xp.log(f"Sim Open Interface Client {srvname} Creation with param Addr {srvaddr} / Port {srvport}")

            # Sim Open Interface Creation
            if self.debug == 2:
                xp.log(f"Creating Sim Open Interfaces ...")
            self.createInterfaces()

            if self.debug == 2:
                xp.log(f"SimOpInt Interfaces List : {self.getSimOpInterfacesList()}")

            if self.debug == 1:
                xp.log(f"Plugin Initialization OK at {datetime.now()}")

            self.initialized = True

        else:
            xp.log(f"Sim Open Interface Plugin Not Initialized, Configuration Error")

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self) -> None:
        # Called once by X-Plane on quit (or when plugins are exiting as part of reload)
        # Return is ignored
        if self.debug == 1:
            xp.log(f"Stopping Plugin at {datetime.now()}")

        xp.destroyMenu(self.pluginMenuID)

        pass

    def XPluginEnable(self) -> int:
        # Required by XPPython3
        # Called once by X-Plane, after all plugins have "Started" (including during reload sequence).
        # You need to return an integer 1, if you have successfully enabled, 0 otherwise.
        if self.debug == 1:
            xp.log(f"Enable Plugin at {datetime.now()}")

        # Create Flight Loop
        self.flightloopID = xp.createFlightLoop(self.flightLoopCB, refCon=None)

        if self.debug == 30:
            xp.log(f"Flight Loop ID : {self.flightloopID}")

        # Schedule Flight Loop
        xp.scheduleFlightLoop(self.flightloopID, 0)

        return 1

    def XPluginDisable(self) -> None:
        # Called once by X-Plane, when plugin is requested to be disabled. All plugins
        # are disabled prior to Stop.
        # Return is ignored
        if self.debug == 1:
            xp.log(f"Disable Plugin at {datetime.now()}")

        # If there is a Flight Loop ID , it is destroyed
        if self.flightloopID:
            xp.destroyFlightLoop(self.flightloopID)

        self.simopintsrv.shutdown()

        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam) -> None:
        # Called by X-Plane whenever a plugin message is being sent to your
        # plugin. Messages include MSG_PLANE_LOADED, MSG_ENTERED_VR, etc., as
        # described in XPLMPlugin module.
        # Messages may be custom inter-plugin messages, as defined by other plugins.
        # Return is ignored
        if self.debug == 1:
            xp.log(f"Message Receive From {inFromWho} : {inMessage} Param : {inParam}")
            xp.log()

        if inFromWho == 0 and inMessage == 114:
            if self.debug == 1:
                xp.log(f"Message DataRef have been added to A330")
                xp.log()

            if self.initialized:
                self.createDataRefId()
                self.createCmdRefId()

        pass

    ##################################################
    # Plugin System Method
    ##################################################

    def getDebugLevel(self) -> int:
        return self.debug

    def setDebugLevel(self, debuglevel: int) -> None:
        self.debug = debuglevel

    def getConfig(self):
        return self.simopintcfg

    def getConfigSection(self, section):
        return self.simopintcfg[section]

    def getConfigParam(self, section, param):
        return self.simopintcfg[section][param]

    def getSimOpIntServer(self):
        return self.simopintsrv

    ##################################################
    # Plugin Menu Callback Method
    ##################################################

    def pluginMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 21:
            xp.log(f"SimOpInt Menu : {menuRefCon} / {itemRefCon}")
    
    def serverMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 22:
            xp.log(f"Actions Menu : {menuRefCon} / {itemRefCon}")

        if itemRefCon == 'start':
            if self.initialized:
                if self.debug == 22:
                    xp.log(f"Starting ... at {datetime.now()}")
                    xp.log()

                # Starting Flight Loop is plugin initialized
                if self.debug == 22:
                    xp.log(f"Starting Flight Loop ... at {datetime.now()}")
                    xp.log()

                xp.scheduleFlightLoop(self.flightloopID, self.flightloopcbktime)

                # Thread Server Creation
                self.threadsrv = threading.Thread(target=self.simopintsrv.loopSimOpIntServer)
                self.threadsrv.start()
                self.simopintsrv.start()

                if self.debug == 22:
                    xp.log(f"Started ... at {datetime.now()}")
                    xp.log()
            else:
                xp.log(f"Plugin Not Initialized")
                xp.log()

        elif itemRefCon == 'stop':
            if self.initialized:
                if self.debug == 22:
                    xp.log(f"Stopping ... at {datetime.now()}")
                    xp.log()

                # Stopping Flight Loop
                if self.debug == 22:
                    xp.log(f"Stopping Flight Loop ... at {datetime.now()}")
                    xp.log()

                xp.scheduleFlightLoop(self.flightloopID, 0)

                # Stopping Server Thread
                self.simopintsrv.shutdown()
                self.threadsrv.join()

                if self.debug == 22:
                    xp.log(f"Stopped ... at {datetime.now()}")
                    xp.log()
            else:
                xp.log(f"Plugin Not Initialized")
                xp.log()

    def configMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 23:
            xp.log(f"Configuration Menu: {menuRefCon} / {itemRefCon}")

        if itemRefCon == 'open':
            if self.debug == 23:
                xp.log(f"Opening Configuration ...")

        if itemRefCon == 'reload':
            if self.debug == 23:
                xp.log(f"Reloading Configuration ...")
    
    ##################################################
    # Plugin Flight Loop Callback Method
    ##################################################

    def flightLoopCB(self, _since, _elapsed, _counter, refCon) -> float:

        if self.debug == 30:
            fploopstart = datetime.now()

        for interface in self.getSimOpInterfaces():
            self.updateCockpit(interface)

        fploopend = datetime.now()
        if self.debug == 30:
            xp.log(f"Flight Loop Started at {fploopstart} Ended at {fploopend}")
            xp.log()

        return self.flightloopcbktime

    ##################################################
    # Plugin Interface Method
    ##################################################

    def getSimOpInterfacesList(self) -> list:
        intlist = []
        for interface in self.simopints:
            intlist.append(interface)
        return intlist

    def getSimOpInterfaces(self) -> dict:
        return self.simopints

    def getSimOpInterface(self, interface: str) -> SimOpInt:
        return self.simopints[interface]['object']

    def createInterface(self, intname: str) -> None:
        if intname in self.simopintcfg['INTERFACES']:
            self.simopints[intname] = {}
            intconfigdir = self.configdir + intname
            self.simopints[intname]['object'] = SimOpInt(intconfigdir, self.simopintcfg['INTERFACES'][intname]['configfile'], 0)
            self.simopintsrv.createInterInData(intname)
            self.simopintsrv.createInterOutData(intname)
        else:
            self.simopints[intname]['object'] = False
        pass

    def createInterfaces(self) -> None:
        for interface in self.simopintcfg['INTERFACES']:
            self.createInterface(interface)
        pass

    ##################################################
    # DataRefId Method
    ##################################################

    @staticmethod
    def getDataRefValue(dataref, dataformat='string'):
        if bool(xp.getDataRefTypes(dataref) & xp.Type_Int):
            return xp.getDatai(dataref)

        elif bool(xp.getDataRefTypes(dataref) & xp.Type_Float):
            return xp.getDataf(dataref)

        elif bool(xp.getDataRefTypes(dataref) & xp.Type_Double):
            return xp.getDatad(dataref)

        elif bool(xp.getDataRefTypes(dataref) & xp.Type_FloatArray):
            value = []
            xp.getDatavf(dataref, value, 0, -1)
            return value

        elif bool(xp.getDataRefTypes(dataref) & xp.Type_IntArray):
            value = []
            xp.getDatavi(dataref, value, 0, -1)
            return value

        elif bool(xp.getDataRefTypes(dataref) & xp.Type_Data):
            if dataformat == 'string':
                return xp.getDatas(dataref)
            else:
                value = []
                xp.getDatab(dataref, value, 0, -1)
                return value

        else:
            # Case Data Type is Unknow
            return "Unknow Type"

    def createDataRefId(self) -> None:
        for interface in self.simopints:
            simopint = self.getSimOpInterface(interface)

            for objtype in simopint.listExportedObjects():

                for objname, obj in simopint.getObjectOfType(objtype).items():
                    if obj.getNode() is not None:
                        dataRefId = xp.findDataRef(obj.getNode())
                        obj.setNodeRef(dataRefId)

                        if obj.getNodeConds() is not None:
                            for nodecond in obj.getNodeConds():
                                noderefid = xp.findDataRef(obj.getNodeCond(nodecond))
                                obj.setNodeCondRef(nodecond, noderefid)

    def createCmdRefId(self) -> None:
        for interface in self.simopints:
            simopint = self.getSimOpInterface(interface)

            for objtype in simopint.listImportedObjects():

                for objname, obj in simopint.getObjectOfType(objtype).items():
                    if obj.getNode() is not None:
                        if obj.getNodeType() == 'cmd':
                            cmdRefId = xp.findCommand(obj.getNode())
                            obj.setNodeRef(cmdRefId)

    ##################################################
    # Plugin Data Method
    ##################################################

    def updateInterfaceData(self, intname: str) -> None:
        pass

    def updateCockpit(self, interface: str):
        updatestart = datetime.now()

        obj2remove = []

        intobj = self.getSimOpInterface(interface)
        objdict = self.simopintsrv.getInterInData(interface)
        for objtype, objs in objdict.items():
            if len(objs) > 0:
                for objname, objvalue in objs.items():
                    obj = intobj.getObject(objtype, objname)
                    if obj.getNode() is not None:
                        if self.debug == 41:
                            xp.log(f"Obj Name : {objname} Obj Value {objvalue} Node {obj.getNode()} ({type(obj.getNode())}) Node Ref {obj.getNodeRef()}")
                            xp.log()
                        if objvalue == 1:
                            if obj.getNodeType() == 'cmd':
                                xp.commandOnce(obj.getNodeRef())

                    obj2remove.append((objtype, objname))

        for objinfos in obj2remove:
            objtype = objinfos[0]
            objname = objinfos[1]
            del objdict[objtype][objname]

        updatesend = datetime.now()

        if self.debug == 40:
            xp.log(f"Update Cockpit Start at {updatestart} End at {updatesend}")
