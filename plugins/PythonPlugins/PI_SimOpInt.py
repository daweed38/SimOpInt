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


########################################
# FarmerSoft Sim Open Interface Plugin
########################################
# PythonInterface Class
# FarmerSoft © 2022
# By Daweed
########################################


class PythonInterface:
    def __init__(self):
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

        self.simopintsrv = None
        self.threadsrv = None

        self.simopintcfg = {}
        self.simopints = {}

        self.shared_data = {}
        self.outData = {}

        self.flightloopcbktime = 0.02

    ##################################################
    # Plugin System Method (Required)
    ##################################################

    def XPluginStart(self) -> tuple:
        # Required by XPPython3
        # Called once by X-Plane on startup (or when plugins are re-starting as part of reload)
        # You need to return three strings

        # Sim Open Interface Plugin Menu Creation
        # Menu Base
        self.pluginMenuID = xp.createMenu(name='SimOpInt', parentMenuID=None, parentItem=0, handler=self.pluginMenuCB, refCon='simopint')

        # Plugin Configuration Sub Menu
        xp.appendMenuItem(menuID=self.pluginMenuID, name='Config', refCon=None)
        self.configMenuID = xp.createMenu(name='Config', parentMenuID=self.pluginMenuID, parentItem=0, handler=self.configMenuCB, refCon='config')
        xp.appendMenuItem(menuID=self.configMenuID, name='Open', refCon='open')
        xp.enableMenuItem(menuID=self.configMenuID, index=0, enabled=0)  # Open Command not active for the moment
        xp.appendMenuItem(menuID=self.configMenuID, name='Reload', refCon='reload')

        # Adding Separator
        xp.appendMenuSeparator(menuID=self.pluginMenuID)

        # Global Start & Start Interface action
        xp.appendMenuItem(menuID=self.pluginMenuID, name='Start', refCon='loopstart')
        xp.enableMenuItem(menuID=self.pluginMenuID, index=2, enabled=1)
        xp.appendMenuItem(menuID=self.pluginMenuID, name='Stop', refCon='loopstop')
        xp.enableMenuItem(menuID=self.pluginMenuID, index=3, enabled=0)

        # Adding Separator
        # xp.appendMenuSeparator(menuID=self.pluginMenuID)

        # Interface Sub Menu (Future Configuration System. Not Active for nom)
        # xp.appendMenuItem(menuID=self.pluginMenuID, name='Interfaces', refCon=None)
        # self.interfacesMenuID = xp.createMenu(name='Interfaces', parentMenuID=self.pluginMenuID, parentItem=0, handler=self.interfacesMenuCB, refCon=None)

        # Adding Separator
        xp.appendMenuSeparator(menuID=self.pluginMenuID)

        # About
        xp.appendMenuItem(menuID=self.pluginMenuID, name='About', refCon='about')

        # Loading Plugin Configuration
        self.loadPluginConfig()

        # Sim Open Interface Server Creation
        if self.simopintcfg:
            srvname = self.getConfigParam('NETWORK', 'srvname')
            xpladdr = self.getConfigParam('NETWORK', 'xpladdr')
            xplport = self.getConfigParam('NETWORK', 'xplport')

            self.simopintsrv = SimOpIntSrv(srvname, xpladdr, xplport, self.srvdebug)
        else:
            self.simopintsrv = False

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self) -> None:
        # Called once by X-Plane on quit (or when plugins are exiting as part of reload)
        # Return is ignored
        if self.debug == 10:
            xp.log(f"Stopping Plugin at {datetime.now()}")
            xp.log()

        xp.destroyMenu(self.pluginMenuID)

    def XPluginEnable(self) -> int:
        # Required by XPPython3
        # Called once by X-Plane, after all plugins have "Started" (including during reload sequence).
        # You need to return an integer 1, if you have successfully enabled, 0 otherwise.
        if self.debug == 10:
            xp.log(f"Enable Plugin at {datetime.now()}")
            xp.log()

        # Create Flight Loop
        self.flightloopID = xp.createFlightLoop(self.flightLoopCB, refCon=None)

        if self.debug == 10:
            xp.log(f"Flight Loop ID : {self.flightloopID}")
            xp.log()

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
                self.createObjectsRefId(intname)

            self.datarefinit = True

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

    def getSimOpIntSrv(self):
        return self.simopintsrv

    ##################################################
    # Plugin Configuration Method
    ##################################################

    def loadPluginConfig(self) -> None:
        # Check Configuration Directory
        self.configdir_ok = os.path.exists(self.configdir)
        # Check Configuration File
        self.configfile_ok = os.path.isfile(self.configdir + '/' + self.configfile)
        # Loading Plugin Configuration in self.simopintcfg dict
        self.simopintcfg = self.tools.readJsonFile(self.configdir, self.configfile)

        if self.configdir_ok is True and self.configfile_ok is True and self.simopintcfg is not False:
            if self.debug == 20:
                xp.log(f"Sim Open Interface Plugin Configuration : {self.simopintcfg}")
                xp.log()

            # Interfaces Creation
            self.createInterfaces()

            # Plugin Init Flag
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
            self.threadsrv = threading.Thread(target=self.simopintsrv.mainLoop)
            self.threadsrv.start()
            if self.simopintsrv.getSignal('shutdown'):
                self.simopintsrv.setSignal('shutdown', False)
            self.simopintsrv.run()
            xp.scheduleFlightLoop(self.flightloopID, self.flightloopcbktime)
            xp.enableMenuItem(menuID=self.pluginMenuID, index=2, enabled=0)
            xp.enableMenuItem(menuID=self.pluginMenuID, index=3, enabled=1)

        elif itemRefCon == 'loopstop':
            xp.scheduleFlightLoop(self.flightloopID, 0)
            self.simopintsrv.shutdown()
            self.threadsrv.join()
            xp.enableMenuItem(menuID=self.pluginMenuID, index=2, enabled=1)
            xp.enableMenuItem(menuID=self.pluginMenuID, index=3, enabled=0)

        else:
            pass

    def interfacesMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 30:
            xp.log(f"Interfaces Menu : {menuRefCon} / {itemRefCon}")
            xp.log()

        if itemRefCon == 'openconf':
            if self.debug == 32:
                xp.log(f"Opening Interface {menuRefCon} Configuration at {datetime.now()}")
                xp.log(f"Interface {menuRefCon} Configuration Opened at {datetime.now()}")
                xp.log()
        elif itemRefCon == 'reloadconf':
            if self.debug == 32:
                xp.log(f"Reloading Interface {menuRefCon} Configuration at {datetime.now()}")
                xp.log(f"Interface {menuRefCon} Configuration Reloaded at {datetime.now()}")
                xp.log()
        else:
            pass

    def configMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 30:
            xp.log(f"Plugin Configuration Menu: {menuRefCon} / {itemRefCon}")
            xp.log()

        if itemRefCon == 'open':
            if self.debug == 33:
                xp.log(f"Opening Plugin Configuration at {datetime.now()}")
                xp.log()

        elif itemRefCon == 'reload':
            if self.debug == 33:
                xp.log(f"Reloading Plugin Configuration at {datetime.now()}")
                xp.log()
            self.loadPluginConfig()

    ##################################################
    # Plugin Flight Loop Callback Method
    ##################################################

    def flightLoopCB(self, _since, _elapsed, _counter, refCon) -> float:
        if self.debug == 40:
            xp.log(f"Flight Loop Started at {datetime.now()}")

        for intname in self.listInterfaces():
            outData = self.refreshInterfaceData(intname)

            if self.debug == 41:
                xp.log(f"Interface {intname} {outData}")
                xp.log()

            if intname in self.simopintsrv.getOutData():
                self.simopintsrv.setIntOutData(intname, outData)

        if self.debug == 40:
            xp.log(f"Flight Loop Ended at {datetime.now()}")

        return self.flightloopcbktime

    ##################################################
    # Plugin Interface Method
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
            # Interface Sub Menu (Future Configuration System. Not Active for nom)
            # xp.appendMenuItem(menuID=self.interfacesMenuID, name=intname, refCon=None)
            # self.simopints[intname]['menuID'] = xp.createMenu(name=intname, parentMenuID=self.interfacesMenuID, parentItem=0, handler=self.interfacesMenuCB, refCon=intname)
            # xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Open Config', refCon='openconf')
            # xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Reload Config', refCon='reloadconf')

    def createInterfaces(self) -> None:
        for intname in self.simopintcfg['INTERFACES']:
            self.createInterface(intname)

    ##################################################
    # DataRef & Command Method
    ##################################################

    def createObjectRefId(self, objtype: str, obj) -> None:
        node = None
        noderef = None

        # Standard Object RefId Management
        if obj.getNodeFormat() == 'base':
            if obj.getNodeType() == 'dref':
                obj.setNodeRef(xp.findDataRef(obj.getNode()))
            elif obj.getNodeType() == 'cmd':
                obj.setNodeRef(xp.findCommand(obj.getNode()))
            else:
                obj.setNodeRef(None)

            if self.debug == 50:
                node = obj.getNode()
                noderef = obj.getNodeRef()

        # Encoder Object RefId Management
        elif obj.getNodeFormat() == ['encoder', 'rotaryswitch']:
            for nodekey in obj.getAllNodes():
                if obj.getNodeType() == 'dref':
                    obj.setNodeRef(nodekey, xp.findDataRef(obj.getNode(nodekey)))
                elif obj.getNodeType() == 'cmd':
                    obj.setNodeRef(nodekey, xp.findCommand(obj.getNode(nodekey)))
                else:
                    obj.setNodeRef(nodekey, None)

            if self.debug == 50:
                node = obj.getAllNodes()
                noderef = obj.getAllNodesRef()

        else:
            obj.setNodeRef(None)

        # Object Condition RefId Management
        if obj.getNodeConds():
            for nodecond in obj.getNodeConds():
                obj.setNodeCondRef(nodecond, xp.findDataRef(obj.getNodeCond(nodecond)))

        if self.debug == 50:
            xp.log(f"Object Type {objtype} Object {obj.getName()} Node Type {obj.getNodeType()} Node Format {obj.getNodeFormat()} Node {node} Node Ref {noderef}")
            xp.log()

    def createObjectsRefId(self, intname: str) -> None:
        interface = self.getInterface(intname)
        if self.debug == 50:
            xp.log(f"Exported Objects Processing")
            xp.log()

        for objtype, objs in interface.getOutputObjects().items():
            for obj in objs.values():
                if self.debug == 50:
                    xp.log(f"{obj} {obj.getName()} {obj.getNode()}")
                    xp.log()
                if obj.getNode() is not None:
                    self.createObjectRefId(objtype, obj)

        # Command Object RefId generation removed as they are now processed via UDP Connexion
        """
        if self.debug == 50:
            xp.log(f"Imported Objects Processing")
            xp.log()

        for objtype, objs in interface.getCommandObjects().items():
            for obj in objs.values():
                self.createObjectRefId(objtype, obj)
        """

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

    def refreshInterfaceData(self, intname):
        interface = self.getInterface(intname)
        outData = {}

        # Phase 1 Getting Exported Objects
        for objtype, objs in interface.getOutputObjects().items():
            outData[objtype] = {}
            if self.debug == 60:
                xp.log(f"Interface {intname}. Processing Object Type {objtype}")
                xp.log()

            # Phase 2 Main Node Value Processing
            for obj in objs.values():
                outData[objtype][obj.getName()] = {}

                if obj.getNodeFormat() == 'base':
                    outData[objtype][obj.getName()]['nodeval'] = self.getDataRefValue(obj.getNodeRef())
                else:
                    outData[objtype][obj.getName()]['nodeval'] = 'Unknow'

                # Phase 3 Conditions Node Value Processing
                if obj.getNodeConds():
                    outData[objtype][obj.getName()]['nodeconds'] = {}
                    for cond in obj.getNodeConds():
                        outData[objtype][obj.getName()]['nodeconds'][cond] = self.getDataRefValue(obj.getNodeCondRef(cond))
                else:
                    outData[objtype][obj.getName()]['nodeconds'] = None

                if self.debug == 60:
                    xp.log(f"Obj {obj.getName()} Node Val {outData[objtype][obj.getName()]['nodeval']} Node Cond {outData[objtype][obj.getName()]['nodeconds']}")
                    xp.log()

        return outData
