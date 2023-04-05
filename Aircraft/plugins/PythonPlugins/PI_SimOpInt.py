#!/usr/bin/env python
# -*-coding:Utf-8 -*

# System Modules Import
import os
import time
from datetime import datetime

# Standard Modules Import
import threading

# XPPython3
import xp

# SimOpInt
from PythonPlugins.SimOpInt.SimOpIntTools import SimOpIntTools
from PythonPlugins.SimOpInt.SimOpInt import SimOpInt
from PythonPlugins.SimOpInt.SimOpIntSrv import SimOpIntSrv

########################################
# FarmerSoft Sim Open Interface Plugin
########################################
# PythonInterface Class
# FarmerSoft © 2022
# By Daweed
########################################


class PythonInterface:
    def __init__(self) -> None:
        self.debug = 0

        self.Name = "SimOpInt"
        self.Sig = "xppython3.simopint"
        self.Desc = "Sim Open Interface"

        self.initialized = False

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

        self.simopintcfg = {}
        self.simopints = {}
        self.shared_data = {}

        self.flightloopcbktime = 0.02

        if os.path.exists(self.configdir):
            if self.debug == 1:
                xp.log("Configuration Directory {} Exist".format(self.configdir))
            self.configdir_ok = True

        if os.path.isfile(self.configdir+self.configfile):
            if self.debug == 1:
                xp.log("Configuration {} found in {}".format(self.configfile, self.configdir))
            self.configfile_ok = True

        if self.configdir_ok and self.configfile_ok:
            self.simopintcfg = self.tools.readJsonFile(self.configdir, self.configfile)
            if self.debug == 1:
                xp.log("Sim Open Interface Plugin Configuration : {}".format(self.simopintcfg))

            # Sim Open Interface Server Creation
            if self.simopintcfg is not False:

                srvname = self.getConfigParam('NETWORK', 'srvname')
                srvaddr = self.getConfigParam('NETWORK', 'srvaddr')
                srvport = self.getConfigParam('NETWORK', 'srvport')
                if self.debug == 1:
                    xp.log("Sim Open Interface Server {} Creation with param Addr {} [{}] / Port {} [{}]".format(srvname, srvaddr, type(srvaddr), srvport, type(srvport)))

                self.simopintsrv = SimOpIntSrv(name='SimOpIntSrv', srvaddr=srvaddr, srvport=srvport, debug=17)
                self.simopintsrv.setOutData(self.shared_data)

                if self.debug == 1:
                    xp.log("Sim Open Interface Server Signals {}".format(self.simopintsrv.listSignals()))

                # Sim Open Interface Creation
                if self.debug == 1:
                    xp.log("Creating Sim Open Interfaces ...")
                self.createInterfaces()
                self.createDataRefId()

                if self.debug == 1:
                    xp.log("SimOpInt Interfaces List : {}".format(self.getSimOpInterfacesList()))

                if self.debug == 1:
                    xp.log("Plugin Initialization OK ...")

                self.initialized = True

            else:
                xp.log("Sim Open Interface Plugin Not Initialized, Configuration Error")
        else:
            xp.log("Configuration File {} not found in {}".format(self.configdir, self.configfile))

        if self.debug == 1:
            xp.log("Plugin Initialization OK ...")

    ##################################################
    # Plugin System Method (Required)
    ##################################################

    def XPluginStart(self) -> tuple:
        # Required by XPPython3
        # Called once by X-Plane on startup (or when plugins are re-starting as part of reload)
        # You need to return three strings

        if self.debug == 1:
            xp.log("Starting Plugin at {}".format(datetime.now()))

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

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self) -> None:
        # Called once by X-Plane on quit (or when plugins are exiting as part of reload)
        # Return is ignored
        if self.debug == 1:
            xp.log("Stopping Plugin at {}".format(datetime.now()))

        xp.destroyMenu(self.pluginMenuID)

        pass

    def XPluginEnable(self) -> int:
        # Required by XPPython3
        # Called once by X-Plane, after all plugins have "Started" (including during reload sequence).
        # You need to return an integer 1, if you have successfully enabled, 0 otherwise.
        if self.debug == 1:
            xp.log("Enable Plugin at {}".format(datetime.now()))

        # Create Flight Loop
        self.flightloopID = xp.createFlightLoop(self.flightLoopCB, refCon=self.shared_data)
        if self.debug == 30:
            xp.log("Flight Loop ID : {}".format(self.flightloopID))

        # Schedule Flight Loop
        xp.scheduleFlightLoop(self.flightloopID, 0)

        return 1

    def XPluginDisable(self) -> None:
        # Called once by X-Plane, when plugin is requested to be disabled. All plugins
        # are disabled prior to Stop.
        # Return is ignored
        if self.debug == 1:
            xp.log("Disable Plugin at {}".format(datetime.now()))

        # If there is a Flight Loop ID , it is destroyed
        if self.flightloopID:
            xp.destroyFlightLoop(self.flightloopID)

        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam) -> None:
        # Called by X-Plane whenever a plugin message is being sent to your
        # plugin. Messages include MSG_PLANE_LOADED, MSG_ENTERED_VR, etc., as
        # described in XPLMPlugin module.
        # Messages may be custom inter-plugin messages, as defined by other plugins.
        # Return is ignored
        if self.debug == 1:
            xp.log("Message Receive at {}".format(datetime.now()))
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
            xp.log("SimOpInt Menu : {} / {}".format(menuRefCon, itemRefCon))
    
    def serverMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 22:
            xp.log("Actions Menu : {} / {}".format(menuRefCon, itemRefCon))

        if itemRefCon == 'start':
            if self.initialized:
                if self.debug == 22:
                    xp.log("Starting ... at {}".format(datetime.now()))
                    xp.log()

                # Starting Flight Loop is plugin initialized
                if self.debug == 22:
                    xp.log("Starting Flight Loop ... at {}".format(datetime.now()))
                    xp.log()
                xp.scheduleFlightLoop(self.flightloopID, self.flightloopcbktime)

                # Thread Creation
                self.simopintsrv.setOutData(self.shared_data)
                self.threadsrv = threading.Thread(target=self.simopintsrv.loopSimOpIntServer)
                self.threadsrv.start()
                self.simopintsrv.start()

                if self.debug == 22:
                    xp.log("Started ... at {}".format(datetime.now()))
                    xp.log()
            else:
                xp.log("Plugin Not Initialized")
                xp.log()

        elif itemRefCon == 'stop':
            if self.initialized:
                if self.debug == 22:
                    xp.log("Stopping ... at {}".format(datetime.now()))
                    xp.log()

                # Stopping Flight Loop
                if self.debug == 22:
                    xp.log("Stopping Flight Loop ... at {}".format(datetime.now()))
                    xp.log()
                xp.scheduleFlightLoop(self.flightloopID, 0)

                # Stopping Server
                self.simopintsrv.shutdown()
                self.threadsrv.join()
                self.simopintsrv.setSignal('shutdown', False)

                if self.debug == 22:
                    xp.log("Stopped ... at {}".format(datetime.now()))
                    xp.log()
            else:
                xp.log("Plugin Not Initialized")
                xp.log()

    def configMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 23:
            xp.log("Configuration Menu: {} / {}".format(menuRefCon, itemRefCon))

        if itemRefCon == 'open':
            if self.debug == 23:
                xp.log("Opening Configuration ...")

        if itemRefCon == 'reload':
            if self.debug == 23:
                xp.log("Reloading Configuration ...")
    
    ##################################################
    # Plugin Flight Loop Callback Method
    ##################################################

    def flightLoopCB(self, _since, _elapsed, _counter, refCon) -> float:

        # Formatting OutData Stuff To be Sent
        for interface in self.simopints:
            simopint = self.getSimOpInterface(interface)

            self.shared_data[interface] = {}

            for objtype in simopint.listExportedObjects():

                self.shared_data[interface][objtype] = {}

                for objname, obj in simopint.getObjectOfType(objtype).items():
                    if obj.getNode() is not None:

                        self.shared_data[interface][objtype][objname] = {}
                        self.shared_data[interface][objtype][objname]['nodeval'] = self.getDataRefValue(obj.getNodeRef(), obj.getNodeFormat())
                        self.shared_data[interface][objtype][objname]['nodecond'] = {}

                        if obj.getNodeConds() is not None:
                            for nodecond in obj.getNodeConds():
                                self.shared_data[interface][objtype][objname]['nodecond'][nodecond] = self.getDataRefValue(obj.getNodeCondRef(nodecond))

        if self.debug == 30:
            xp.log('Flight Loop Executed at {} Shared Data : {}'.format(datetime.now(), self.shared_data))

        # Updating OutData in Sim Open Interface Client
        self.simopintsrv.setOutData(self.shared_data)

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

    def createInterface(self, interface: str) -> None:
        if interface in self.simopintcfg['INTERFACES']:
            self.simopints[interface] = {}
            interfacedir = self.configdir + interface
            self.simopints[interface]['object'] = SimOpInt(interfacedir, self.simopintcfg['INTERFACES'][interface]['configfile'], 0)
        else:
            self.simopints[interface]['object'] = False
        pass

    def createInterfaces(self) -> None:
        # {confsection: confdata for confsection, confdata in objects.items() if confsection not in ['CONF', 'PROPERTIES']}
        for interface in self.simopintcfg['INTERFACES']:
            self.createInterface(interface)
        pass

    ##################################################
    # Plugin Data Method
    ##################################################

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
                                nodeRefId = xp.findDataRef(obj.getNodeCond(nodecond))
                                obj.setNodeCondRef(nodecond, nodeRefId)

    @staticmethod
    def getDataRefValue(dataref, dataformat='string'):
        if xp.getDataRefTypes(dataref) == 1:
            return xp.getDatai(dataref)
        elif xp.getDataRefTypes(dataref) == 2:
            return xp.getDataf(dataref)
        elif xp.getDataRefTypes(dataref) == 4:
            return xp.getDatad(dataref)
        elif xp.getDataRefTypes(dataref) == 8:
            value = []
            xp.getDatavf(dataref, value, 0, -1)
            return value
        elif xp.getDataRefTypes(dataref) == 16:
            value = []
            xp.getDatavi(dataref, value, 0, -1)
            return value
        elif xp.getDataRefTypes(dataref) == 32:
            if dataformat == 'string':
                return xp.getDatas(dataref)
            else:
                value = []
                xp.getDatab(dataref, value, 0, -1)
                return value
        else:
            # Case Data Type is Unknow
            return "Unknow Type"
