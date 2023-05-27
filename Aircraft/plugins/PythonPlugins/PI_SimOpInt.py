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
        # self.srvdebug = 0

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
                self.createObjectsRefId(intname)
                # self.createCmdRefId(intname)
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
        # Check Configuration Directory
        self.configdir_ok = os.path.exists(self.configdir)
        # Check Configuration File
        self.configfile_ok = os.path.isfile(self.configdir+'/'+self.configfile)
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
            xp.scheduleFlightLoop(self.flightloopID, self.flightloopcbktime)

        elif itemRefCon == 'loopstop':
            xp.scheduleFlightLoop(self.flightloopID, 0)

    def interfacesMenuCB(self, menuRefCon, itemRefCon) -> None:
        if self.debug == 30:
            xp.log(f"Interfaces Menu : {menuRefCon} / {itemRefCon}")
            xp.log()

        if itemRefCon == 'start':
            if self.debug == 32:
                xp.log(f"Starting Interface {menuRefCon} at {datetime.now()}")
                xp.log(f"Interface {menuRefCon} Started at {datetime.now()}")
                xp.log()
            xp.enableMenuItem(menuID=self.simopints[menuRefCon]['menuID'], index=3, enabled=0)
            xp.enableMenuItem(menuID=self.simopints[menuRefCon]['menuID'], index=4, enabled=1)
            self.startInterfaceSrv(menuRefCon)
            self.startInterfaceCli(menuRefCon)

        elif itemRefCon == 'stop':
            if self.debug == 32:
                xp.log(f"Stopping Interface {menuRefCon} at {datetime.now()}")
                xp.log(f"Interface {menuRefCon} Stopped at {datetime.now()}")
                xp.log()
            xp.enableMenuItem(menuID=self.simopints[menuRefCon]['menuID'], index=3, enabled=1)
            xp.enableMenuItem(menuID=self.simopints[menuRefCon]['menuID'], index=4, enabled=0)
            self.stopInterfaceSrv(menuRefCon)
            self.stopInterfaceCli(menuRefCon)

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
        # for each declared Interface
        for intname in self.listInterfaces():
            self.refreshExportedData(intname)

            if self.debug == 41:
                xp.log(f"Interface {intname} {self.outData}")
                xp.log()

            # Interface intname Server Out Data Update
            self.getInterfaceSrv(intname).setOutData(self.outData[intname])

            # Refresh Cockpit
            self.refreshImportedData(intname)

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
        self.inData[intname] = {}

        if interface is not False:
            self.simopints[intname] = {}
            self.simopints[intname]['SimOpInt'] = interface
            xp.appendMenuItem(menuID=self.interfacesMenuID, name=intname, refCon=None)
            self.simopints[intname]['menuID'] = xp.createMenu(name=intname, parentMenuID=self.interfacesMenuID, parentItem=0, handler=self.interfacesMenuCB, refCon=intname)
            xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Open Config', refCon='openconf')
            xp.enableMenuItem(menuID=self.simopints[intname]['menuID'], index=0, enabled=0)  # Open Action is actually not active
            xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Reload Config', refCon='reloadconf')

            intsrv = SimOpIntSrv(interface.getSrvName(), interface.getXplAddr(), interface.getXplPort())
            intcli = SimOpIntCli(interface.getCliName(), interface.getIntAddr(), interface.getIntPort())

            if intsrv is not False and intcli is not False:
                self.simopints[intname]['SimOpIntSrv'] = intsrv
                self.simopints[intname]['SimOpIntCli'] = intcli
                xp.appendMenuSeparator(self.simopints[intname]['menuID'])  # Caution This
                xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Start Srv', refCon='start')
                xp.appendMenuItem(menuID=self.simopints[intname]['menuID'], name='Stop Srv', refCon='stop')
                xp.enableMenuItem(menuID=self.simopints[intname]['menuID'], index=4, enabled=0)

    def createInterfaces(self) -> None:
        for intname in self.simopintcfg['INTERFACES']:
            self.createInterface(intname)

    ##################################################
    # Interfaces Client & Servers Method
    ##################################################

    def getInterfaceCli(self, intname: str) -> SimOpIntCli | bool:
        if intname in self.simopints:
            return self.simopints[intname]['SimOpIntCli']
        else:
            return False

    def startInterfaceCli(self, intname: str) -> None:
        # Thread Creation
        intcli = self.getInterfaceCli(intname)
        self.simopints[intname]['CliThread'] = threading.Thread(target=intcli.mainLoop)
        self.simopints[intname]['CliThread'].start()
        intcli.run()

    def stopInterfaceCli(self, intname: str) -> None:
        intcli = self.getInterfaceCli(intname)
        intcli.shutdown()
        self.simopints[intname]['CliThread'].join()

    def getInterfaceSrv(self, intname: str) -> SimOpIntSrv | bool:
        if intname in self.simopints:
            return self.simopints[intname]['SimOpIntSrv']
        else:
            return False

    def startInterfaceSrv(self, intname: str) -> None:
        # Thread Creation
        intsrv = self.getInterfaceSrv(intname)
        self.simopints[intname]['SrvThread'] = threading.Thread(target=intsrv.mainLoop)
        self.simopints[intname]['SrvThread'].start()
        intsrv.run()

    def stopInterfaceSrv(self, intname: str) -> None:
        intsrv = self.getInterfaceSrv(intname)
        intsrv.shutdown()
        self.simopints[intname]['SrvThread'].join()

    ##################################################
    # DataRef & Command Method
    ##################################################

    def createObjectsRefId(self, intname: str) -> None:
        interface = self.getInterface(intname)
        if self.debug == 50:
            xp.log(f"Exported Objects Processing")
            xp.log()

        for objtype, objs in interface.getExportedObjects().items():
            for obj in objs.values():
                self.createObjectRefId(objtype, obj)

        if self.debug == 50:
            xp.log(f"Imported Objects Processing")
            xp.log()

        for objtype, objs in interface.getImportedObjects().items():
            for obj in objs.values():
                self.createObjectRefId(objtype, obj)

    def createObjectRefId(self, objtype: str, obj) -> None:
        node = None
        noderef = None

        # Object RefId Management
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

        elif obj.getNodeFormat() == 'encoder':
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
            xp.log(
                f"Object Type {objtype} Object {obj.getName()} Node Type {obj.getNodeType()} Node Format {obj.getNodeFormat()} Node {node} Node Ref {noderef}")
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

    def refreshExportedData(self, intname) -> None:
        interface = self.getInterface(intname)
        self.outData[intname] = {}

        # Phase 1 Getting Exported Objects
        for objtype, objs in interface.getExportedObjects().items():
            self.outData[intname][objtype] = {}

            # Phase 2 Main Node Value Processing
            for obj in objs.values():
                self.outData[intname][objtype][obj.getName()] = {}

                if obj.getNodeFormat() == 'base':
                    self.outData[intname][objtype][obj.getName()]['nodeval'] = self.getDataRefValue(obj.getNodeRef())

                else:
                    self.outData[intname][objtype][obj.getName()]['nodeval'] = 'Unknow'

                # Phase 3 Conditions Node Value Processing
                if obj.getNodeConds():
                    self.outData[intname][objtype][obj.getName()]['nodeconds'] = {}
                    for cond in obj.getNodeConds():
                        self.outData[intname][objtype][obj.getName()]['nodeconds'][cond] = self.getDataRefValue(obj.getNodeCondRef(cond))
                else:
                    self.outData[intname][objtype][obj.getName()]['nodeconds'] = None

                if self.debug == 60:
                    xp.log(f"Obj {obj.getName()} Node Val {self.outData[intname][objtype][obj.getName()]['nodeval']} Node Cond {self.outData[intname][objtype][obj.getName()]['nodeconds']}")
                    xp.log()

    def refreshImportedData(self, intname):
        interface = self.getInterface(intname)
        interfacecli = self.getInterfaceCli(intname)
        self.inData[intname] = interfacecli.getInData()
        if interfacecli.getSignal('newmsg'):
            if self.debug == 70:
                xp.log(f"Received Data {self.inData[intname]}")
                xp.log()
            for objtype, objs in self.inData[intname].items():
                if len(interfacecli.getInData()[objtype]) > 0:
                    for rcvobj in objs.values():
                        # obj = interface.getObject(objtype, rcvobj)
                        xp.log(f"{interfacecli.getInData()[objtype]} {rcvobj}")
                        xp.log()

            interfacecli.setSignal('newmsg', False)

    ##################################################
    # TEMP / JUNK
    ##################################################

    """
    # V2
                            if obj.getNodeFormat() == 'base':
                            if obj.getNodeType() == 'dref':
                                pass
                            elif obj.getNodeType() == 'cmd':
                                pass

                        elif obj.getNodeFormat() == 'encoder':
                            if obj.getNodeType() == 'dref':
                                pass
                            elif obj.getNodeType() == 'cmd':
                                pass

                        else:
                            pass
                            
                            
                            
    # V1
    def refreshImportedData(self, intname):
    self.inData[intname] = {}
    interface = self.getInterface(intname)
    for objtype, objs in interface.getImportedObjects().items():
        for obj in objs.values():
            if obj.getNodeFormat() == 'base':
                pass
            elif obj.getNodeFormat() == 'encoder':
                pass
            else:
                pass

            if self.debug == 70:
                xp.log(f"Type : {objtype} Object {obj.getName()} Object Type {obj.getObjType()} Node Format {obj.getNodeFormat()} Node Type {obj.getNodeType()}")
                xp.log()
                    
    
    # V0    
    # To be Review to take Encoder data form
    def refreshImportedData(self, intname, data):
        for objtype, objs in self.getInterface(intname).listImportedObjects().items():

            if objtype in data and len(data[objtype]) > 0:

                if objtype not in self.inData[intname]:
                    self.inData[intname][objtype] = {}

                for objtitle, obj in objs.items():
                    
                    if obj.getName() in data[objtype] and obj.getNode is not None:

                        if obj.getName() not in self.inData[intname][objtype] or self.inData[intname][objtype][obj.getName()] != data[objtype][obj.getName()]:
                            self.inData[intname][objtype][obj.getName()] = data[objtype][obj.getName()]
                            if self.debug == 70:
                                xp.log(f"Object {obj.getName()} Recv Value {self.inData[intname][objtype][obj.getName()]} Node {obj.getNode()} Node Type {obj.getNodeType()} Node Ref {obj.getNodeRef()}")
                                xp.log()

                            if obj.getNodeType() == 'cmd' and data[objtype][obj.getName()] == 1:
                                xp.commandOnce(obj.getNodeRef())
                            elif obj.getNodeType() == 'dref':
                                if self.getDataRefValue(obj.getNodeRef()) != data[objtype][obj.getName()]:
                                    # self.setDataRefValue(obj.getNodeRef(), data[objtype][obj.getName()])
                                    xp.log(f"{self.getDataRefValue(obj.getNodeRef())} / {data[objtype][obj.getName()]}")
                                    xp.log()
    """
