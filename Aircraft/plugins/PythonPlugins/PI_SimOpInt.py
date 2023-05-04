# System Module Import
import os
from datetime import datetime
import threading

# XPPython3 Module Import
import xp

# Sim Open Interface Module Import
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
        self.Name = "SimOpInt"
        self.Sig = "xppython3.simopint"
        self.Desc = "Sim Open Interface"

        self.debug = 0
        self.srvdebug = 0

        self.tools = SimOpIntTools(0)

        self.aircraftdir = xp.extractFileAndPath(xp.getNthAircraftModel(0)[1])[1].removeprefix(xp.getSystemPath())
        self.configdir = self.aircraftdir + '/plugins/PythonPlugins/SimOpint/Config'
        self.configdir_ok = False
        self.configfile = 'simopint.json'
        self.configfile_ok = False

        self.initialized = False
        self.datarefinit = False

        self.flightloopID = None
        self.pluginMenuID = None
        self.interfacesMenuID = None
        self.configMenuID = None

        self.simopintsrv = {}
        self.threadsrv = {}
        self.simopintcli = {}
        self.threadcli = {}

        self.simopintcfg = {}
        self.simopints = {}

        self.shared_data = {}
        self.outData = {}
        self.inData = {}

        self.flightloopcbktime = 0.02

    ##################################################
    # Plugin System Method (Required)
    ##################################################

    def XPluginStart(self) -> tuple:
        # Required by XPPython3
        # Called once by X-Plane on startup (or when plugins are re-starting as part of reload)
        # You need to return three strings

        # Sim Open Interface Plugin Menu Creation
        self.pluginMenuID = xp.createMenu(name='SimOpInt', parentMenuID=None, parentItem=0, handler=self.pluginMenuCB, refCon='simopint')

        xp.appendMenuItem(menuID=self.pluginMenuID, name='Interfaces', refCon=None)
        self.interfacesMenuID = xp.createMenu(name='Interfaces', parentMenuID=self.pluginMenuID, parentItem=0, handler=self.interfacesMenuCB, refCon=None)

        xp.appendMenuItem(menuID=self.pluginMenuID, name='Config', refCon=None)
        self.configMenuID = xp.createMenu(name='Config', parentMenuID=self.pluginMenuID, parentItem=1, handler=self.configMenuCB, refCon='config')

        xp.appendMenuItem(menuID=self.configMenuID, name='Open', refCon='open')
        xp.appendMenuItem(menuID=self.configMenuID, name='Reload', refCon='reload')

        xp.appendMenuSeparator(menuID=self.pluginMenuID)

        xp.appendMenuItem(menuID=self.pluginMenuID, name='Start', refCon='loopstart')
        xp.appendMenuItem(menuID=self.pluginMenuID, name='Stop', refCon='loopstop')

        xp.appendMenuSeparator(menuID=self.pluginMenuID)

        xp.appendMenuItem(menuID=self.pluginMenuID, name='About', refCon='about')

        self.loadPluginConfig()

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self) -> None:
        # Called once by X-Plane on quit (or when plugins are exiting as part of reload)
        # Return is ignored
        if self.debug == 10:
            xp.log(f"Stopping Plugin at {datetime.now()}")

        xp.destroyMenu(self.pluginMenuID)

    def XPluginEnable(self) -> int:
        # Required by XPPython3
        # Called once by X-Plane, after all plugins have "Started" (including during reload sequence).
        # You need to return an integer 1, if you have successfully enabled, 0 otherwise.
        if self.debug == 10:
            xp.log(f"Enable Plugin at {datetime.now()}")

        # Create Flight Loop
        self.flightloopID = xp.createFlightLoop(self.flightLoopCB, refCon=None)

        if self.debug == 10:
            xp.log(f"Flight Loop ID : {self.flightloopID}")

        # Schedule Flight Loop
        xp.scheduleFlightLoop(self.flightloopID, 0)

        return 1

    def XPluginDisable(self) -> None:
        # Called once by X-Plane, when plugin is requested to be disabled. All plugins
        # are disabled prior to Stop.
        # Return is ignored
        if self.debug == 10:
            xp.log(f"Disable Plugin at {datetime.now()}")

        # If there is a Flight Loop ID , it is destroyed
        if self.flightloopID:
            xp.destroyFlightLoop(self.flightloopID)

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam) -> None:
        # Called by X-Plane whenever a plugin message is being sent to your
        # plugin. Messages include MSG_PLANE_LOADED, MSG_ENTERED_VR, etc., as
        # described in XPLMPlugin module.
        # Messages may be custom inter-plugin messages, as defined by other plugins.
        # Return is ignored
        if self.debug == 10:
            xp.log(f"Message Receive From {inFromWho} : {inMessage} Param : {inParam}")
            xp.log()

        # Message Receive From 0: 114 Param: -1383074416
        if inFromWho == 0 and inMessage == 114 and self.datarefinit is False:
            for intname in self.listInterfaces():
                self.createNodeRefId(intname)
            self.datarefinit = True
        pass

    ##################################################
    # Plugin System Method
    ##################################################

    def getDebugLevel(self) -> int:
        return self.debug

    def setDebugLevel(self, debuglevel: int) -> None:
        self.debug = debuglevel

    def getConfig(self) -> dict:
        return self.simopintcfg

    def getConfigSection(self, section) -> dict:
        return self.simopintcfg[section]

    def getConfigParam(self, section, param) -> str | int | bool:
        return self.simopintcfg[section][param]

    ##################################################
    # Plugin Configuration Method
    ##################################################

    def loadPluginConfig(self) -> None:
        self.configdir_ok = os.path.exists(self.configdir)
        self.configfile_ok = os.path.isfile(self.configdir+'/'+self.configfile)
        self.simopintcfg = self.tools.readJsonFile(self.configdir, self.configfile)

        if self.configdir_ok is True and self.configfile_ok is True and self.simopintcfg is not False:
            if self.debug == 20:
                xp.log(f"Sim Open Interface Plugin Configuration : {self.simopintcfg}")
                xp.log()

            # Interfaces Creation
            self.createInterfaces()

            self.initialized = True
        else:
            if self.debug == 20:
                xp.log(f"Configuration File {self.configfile} not found in {self.configdir}")
                xp.log()

    ##################################################
    # Plugin Menu Callback Method
    ##################################################

    def pluginMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 30:
            xp.log(f"SimOpInt Menu : {menuRefCon} / {itemRefCon}")
            xp.log()

        if itemRefCon == 'loopstart':
            xp.scheduleFlightLoop(self.flightloopID, self.flightloopcbktime)

        elif itemRefCon == 'loopstop':
            xp.scheduleFlightLoop(self.flightloopID, 0)

    def interfacesMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 30:
            xp.log(f"Interfaces Menu : {menuRefCon} / {itemRefCon}")

        if itemRefCon == 'srvstart':
            if self.debug == 32:
                xp.log(f"Starting Interface {menuRefCon} Server at {datetime.now()}")
                xp.log(f"Interface {menuRefCon} Server Started at {datetime.now()}")
                xp.log()

            intsrv = self.getInterfaceSrv(menuRefCon)
            if intsrv.getSignal('shutdown'):
                intsrv.setSignal('shutdown', False)
            self.threadsrv[menuRefCon] = threading.Thread(target=intsrv.mainLoop)
            self.threadsrv[menuRefCon].start()
            # intsrv.start()
            intsrv.run()
            xp.enableMenuItem(menuID=self.simopints[menuRefCon]['menuID'], index=3, enabled=0)
            xp.enableMenuItem(menuID=self.simopints[menuRefCon]['menuID'], index=4, enabled=1)

        elif itemRefCon == 'srvstop':
            if self.debug == 32:
                xp.log(f"Stopping Interface {menuRefCon} Server at {datetime.now()}")
                xp.log(f"Interface {menuRefCon} Server Stopped at {datetime.now()}")
                xp.log()

            intsrv = self.getInterfaceSrv(menuRefCon)
            intsrv.shutdown()
            # self.threadsrv[menuRefCon].join()

            xp.enableMenuItem(menuID=self.simopints[menuRefCon]['menuID'], index=3, enabled=1)
            xp.enableMenuItem(menuID=self.simopints[menuRefCon]['menuID'], index=4, enabled=0)

        elif itemRefCon == 'reloadconf':
            if self.debug == 32:
                xp.log(f"Reloading Interface {menuRefCon} Configuration at {datetime.now()}")
                xp.log(f"Interface {menuRefCon} Configuration Reloaded at {datetime.now()}")
                xp.log()

    def configMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 30:
            xp.log(f"Plugin Configuration Menu: {menuRefCon} / {itemRefCon}")

        if itemRefCon == 'reload':
            if self.debug == 33:
                xp.log(f"Reloading Plugin Configuration at {datetime.now()}")
                xp.log()
            self.loadPluginConfig()

        if self.debug == 30:
            xp.log()

    ##################################################
    # Plugin Flight Loop Callback Method
    ##################################################

    def flightLoopCB(self, _since, _elapsed, _counter, refCon) -> float:
        if self.debug == 40:
            xp.log(f"Flight Loop Started at {datetime.now()}")

        # Get Data From X-Plane for Objects To be Exported
        for intname in self.listInterfaces():
            self.refreshExportedData(intname)

            if self.debug == 41:
                xp.log(f"Interface {intname} {self.outData}")
                xp.log()

            intsrv = self.getInterfaceSrv(intname)
            intsrv.setOutData(self.outData[intname])

        if self.debug == 40:
            xp.log(f"Flight Loop Ended at {datetime.now()}")

        return self.flightloopcbktime

    ##################################################
    # Plugin Interfaces Method
    ##################################################

    def listInterfaces(self) -> dict:
        return self.simopints

    def getInterface(self, intname) -> SimOpInt | bool:
        if intname in self.simopints:
            return self.simopints[intname]['SimOpInt']
        else:
            return False

    def createInterface(self, intname: str) -> None:
        configdir = self.configdir+'/'+intname
        configfile = self.simopintcfg['INTERFACES'][intname]['configfile']
        interface = SimOpInt(configdir, configfile, 0)
        if interface is not False:
            self.simopints[intname] = {}
            self.simopints[intname]['SimOpInt'] = interface
            xp.appendMenuItem(menuID=self.interfacesMenuID, name=intname, refCon=None)
            self.simopints[intname]['menuID'] = xp.createMenu(name=intname, parentMenuID=self.interfacesMenuID, parentItem=0, handler=self.interfacesMenuCB, refCon=intname)
            xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Open Config', refCon='openconf')
            xp.enableMenuItem(menuID=self.simopints[intname]['menuID'], index=0, enabled=0)  # Open Action is actually not active
            xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Reload Config', refCon='reloadconf')
            intsrv = SimOpIntSrv(interface.getSrvName(), interface.getSrvAddr(), interface.getSrvPort())
            if intsrv is not False:
                self.simopints[intname]['SimOpIntSrv'] = intsrv
                xp.appendMenuSeparator(self.simopints[intname]['menuID']) # Caution This
                xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Start Srv', refCon='srvstart')
                xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Stop Srv', refCon='srvstop')
                xp.enableMenuItem(menuID=self.simopints[intname]['menuID'], index=4, enabled=0)

    def createInterfaces(self) -> None:
        for intname in self.simopintcfg['INTERFACES']:
            self.createInterface(intname)

    ##################################################
    # Interfaces Servers Method
    ##################################################

    def getInterfaceSrv(self, intname: str) -> SimOpIntSrv | bool:
        if intname in self.simopints:
            return self.simopints[intname]['SimOpIntSrv']
        else:
            return False

    def startInterfaceSrv(self, intname: str) -> None:
        # Thread Creation
        """
        srvname.setSignal('shutdown', False)
        self.thrsrv[srvname.getName()] = threading.Thread(target=srvname.mainLoop)
        self.thrsrv[srvname.getName()].start()
        """
        pass

    def stopInterfaceSrv(self, intname: str) -> None:
        """
        srvname.shutdown()
        self.thrsrv[srvname.getName()].join()
        """
        pass

    ##################################################
    # DataRef & Command Method
    ##################################################

    def createNodeRefId(self, intname):
        for objtype, objs in self.getInterface(intname).listExportedObjects().items():
            for objtitle, obj in objs.items():
                if self.debug == 50:
                    xp.log(f"Obj Name {obj.getName()} NodeRef {obj.getNodeRef()}")

                obj.setNodeRef(xp.findDataRef(obj.getNode()))

                if obj.getNodeConds():
                    for cond in obj.getNodeConds():
                        if self.debug == 50:
                            xp.log(f"Obj {obj.getName()} Condition {cond} Node {obj.getNodeCond(cond)} NodeRef {xp.findDataRef(obj.getNodeCond(cond))}")
                        obj.setNodeCondRef(cond, xp.findDataRef(obj.getNodeCond(cond)))
        xp.log()

    ##################################################
    # Plugin Data Method
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

    @staticmethod
    def setDataRefValue(dataref, value, dataformat='string'):
        if bool(xp.getDatai(dataref) & xp.Type_Int):
            xp.setDatai(dataref, value)

        elif bool(xp.getDataRefTypes(dataref) & xp.Type_Float):
            xp.setDataf(dataref, value)

        elif bool(xp.getDatad(dataref) & xp.Type_Double):
            xp.setDatad(dataref, value)

        elif bool(xp.getDataRefTypes(dataref) & xp.Type_FloatArray):
            xp.setDatavf(dataref, value, 0, -1)

        elif bool(xp.getDataRefTypes(dataref) & xp.Type_IntArray):
            xp.setDatavi(dataref, value, 0, -1)

        elif bool(xp.getDataRefTypes(dataref) & xp.Type_Data):
            if dataformat == 'string':
                return xp.setDatas(dataref, value)
            else:
                xp.setDatab(dataref, value, 0, -1)

        else:
            # Case Data Type is Unknow
            return "Unknow Type"

    def refreshExportedData(self, intname):
        self.outData[intname] = {}
        for objtype, objs in self.getInterface(intname).listExportedObjects().items():
            self.outData[intname][objtype] = {}
            for objtitle, obj in objs.items():
                if self.debug == 60:
                    xp.log(f"Obj Name {obj.getName()} NodeRef {obj.getNodeRef()} Value {self.getDataRefValue(obj.getNodeRef())}")
                self.outData[intname][objtype][obj.getName()] = {}
                self.outData[intname][objtype][obj.getName()]['nodeval'] = self.getDataRefValue(obj.getNodeRef())
                if obj.getNodeConds():
                    self.outData[intname][objtype][obj.getName()]['nodeconds'] = {}
                    for cond in obj.getNodeConds():
                        if self.debug == 60:
                            xp.log(f"Obj {obj.getName()} Condition {cond} Node {obj.getNodeCond(cond)} NodeRef {obj.getNodeCondRef(cond)} Value {self.getDataRefValue(obj.getNodeCondRef(cond))}")
                        self.outData[intname][objtype][obj.getName()]['nodeconds'][cond] = self.getDataRefValue(obj.getNodeCondRef(cond))
        if self.debug == 60:
            xp.log()

    ##################################################
    # TEMP / JUNK
    ##################################################
