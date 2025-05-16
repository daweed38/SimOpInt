##################################################
# FarmerSoft Open Interface Class
##################################################
# SimOpInt Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
# import sys
import logging
import os.path
import platform
import importlib
import time
import threading

if platform.system() == 'Linux':
    print(f'Importing RPi.GPIO Module')
    import RPi.GPIO as GPIO

# SimOpInt Module Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntClient import SimOpIntClient


class SimOpInt:

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, configdir: str, configfilename: str, debug: int = 30) -> None:

        self.debug = debug
        self.logger = logging.getLogger(__name__)

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.configdir = configdir
        self.configfilename = configfilename
        self.dummy = False
        self.modules = {}
        self.devices = {}
        self.objects = {}
        self.interrupt = {}
        self.running = False
        self.intstate = 0
        self.simopint_thread = None
        self.simopintcli_thread = None

        self.config = SimOpIntConfig(self.configdir, self.configfilename)
        self.logger.debug(f'Interface Config : {self.config.getConfig()}')

        if self.config.isNewConfig():
            self.logger.debug(f'New Interface Config')
            self.intname = os.path.splitext(self.getConfigFileName())[0]
            intconfig = self.createNewConfig()
            self.config.setConfig(intconfig)
            self.config.writeJsonConfigFile()
            self.config.setNewConfig(False)
        else:
            self.logger.debug(f'Reading Interface Config')
            self.intname = self.config.getConfigParameter('INTERFACE', 'intname')
            self.intaddr = self.config.getConfigParameter('NETWORK', 'intaddr')
            self.intport = self.config.getConfigParameter('NETWORK', 'intport')
            self.xpsrvaddr = self.config.getConfigParameter('NETWORK', 'xpsrvaddr')
            self.xpsrvport = self.config.getConfigParameter('NETWORK', 'xpsrvport')

        # self.simopintcli = SimOpIntClient(cliname=self.intname, srvaddr=self.xpsrvaddr, srvport=self.xpsrvport)

        if 'MODULES' in self.config.getConfig():
            self.logger.debug(f'--- Modules Configuration Management ---')
            modulesconfig = self.config.getConfigSection('MODULES')
            if modulesconfig:
                self.logger.debug(f'Loading Modules from Configuration {modulesconfig}')
                for modulestype, modules in modulesconfig.items():
                    if len(modules) > 0:
                        self.logger.debug(f'Module Section : {modulestype} : {modules}')
                        for modulename, moduledata in modules.items():
                            self.logger.debug(f'Loading Module {modulename} : Library {moduledata["module"]} => Class {moduledata["class"]}')
                            module = f'SimOpInt.{moduledata["module"]}'
                            self.loadModule(modulename, module, moduledata['class'])

                self.logger.debug(f'Loaded Modules : {self.listLoadedModules()}')
            else:
                self.logger.warning(f'No modules configuration found to load ...')

        if 'DEVICES' in self.config.getConfig():
            self.logger.debug(f'--- Devices Configuration Management ---')
            self.createDevices()
            self.logger.debug(f'Loaded Devices : {self.listLoadedDevices()}')

        if 'OBJECTS' in self.config.getConfig():
            self.logger.debug(f'--- Objects Configuration Management ---')
            self.createObjects()
            self.logger.debug(f'Loaded Objects : {self.listLoadedObjects()}')
        
        self.logger.info(f'Sim Open Interface {self.getName()} Initialized')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        self.logger.info(f'Sim Open Interface {self.getName()} Unloaded')

    ###################################
    # System Method
    ###################################

    # getName()
    # Return interface name (str)
    def getName(self) -> str:
        return self.intname

    # setName(intname)
    # intname is str
    # Set interface name to intname
    def setName(self, intname: str) -> None:
        self.intname = intname
        self.config.setConfigParameter('INTERFACE', 'intname', intname)

    # getAddr()
    # Return interface address (int)
    def getAddr(self) -> str:
        return self.intaddr

    # setAddr(intaddr)
    # intaddr is int
    # Set interface address to intaddr
    def setAddr(self, intaddr: str) -> None:
        self.intaddr = intaddr
        self.config.setConfigParameter('NETWORK', 'intaddr', intaddr)

    # getPort()
    # Return interface port (int)
    def getPort(self) -> int:
        return self.intport

    # setPort(intport)
    # intport is int
    # Set interface port to intport
    def setPort(self, intport: int) -> None:
        self.intport = intport
        self.config.setConfigParameter('NETWORK', 'intport', intport)

    # getInterrupts()
    # Return Interface Interrupt Dictionary
    def getInterrupts(self):
        return self.interrupt

    # getIntStatus()
    # Return Interface status
    def getIntStatus(self) -> int:
        return self.intstate

    # setIntStatus(state)
    # Set Interface status to state
    def setIntStatus(self, state: int) -> None:
        self.intstate = state

    # getIntThreadState()
    # Get Interface Thread Status
    def getIntThreadState(self) -> threading:
        if self.simopint_thread is not None:
            return self.simopint_thread.is_alive()
        else:
            return None

    ###################################
    # Interface Method
    ###################################

    # openInterface()
    # Open Interface
    def openInterface(self) -> None:
        self.logger.info(f'Opening Interface {self.getName()}')
        self.setIntStatus(1)
        self.simopint_thread = threading.Thread(target=self.mainLoop)
        self.simopint_thread.start()
        self.logger.info(f'Interface {self.getName()} Opened')

    # closeInterface()
    # Stop Main Loop Interface
    def closeInterface(self) -> None:
        if self.getIntStatus() != 1:
            self.stopIntLoop()
        while self.getIntStatus() > 1:
            time.sleep(0.5)
        self.logger.info(f'Closing Interface {self.getName()}')
        self.setIntStatus(0)
        # self.simopint_thread = None
        self.logger.info(f'Interface {self.getName()} Closed')

    # startIntLoop()
    # Start Main Loop Interface
    def startIntLoop(self) -> None:
        if self.getIntThreadState() and self.getIntThreadState() == 1:
            self.logger.info(f'Starting Interface {self.getName()} Main Loop')
            self.running = True
            self.setIntStatus(2)
            self.logger.info(f'Interface {self.getName()} Main Loop Started')
        else:
            self.logger.error(f'Interface {self.getName()} Not Opened! Main Loop Can\'t Be Started')

    # stopIntLoop()
    # Stop Main Loop Interface
    def stopIntLoop(self) -> None:
        self.logger.info(f'Stopping Interface {self.getName()} Main Loop')
        self.running = False
        self.setIntStatus(1)
        self.logger.info(f'Interface {self.getName()} Main Loop Stopped')

    ###################################
    # Client Methods
    ###################################
    """
    # getInterfaceClient()
    # Return the SimOpInt Client
    def getClient(self) -> SimOpIntClient:
        return self.simopintcli

    # startClient()
    # Start Interface Client
    def startClient(self) -> None:
        self.logger.info(f'Starting Interface Client {self.simopintcli.getCliName()}')
        self.simopintcli_thread = threading.Thread(target=self.simopintcli.mainLoop)
        self.simopintcli_thread.start()
        while self.simopintcli.getCliStatus() < 1:
            time.sleep(1)
        self.logger.debug(f'startClient : simopintcli_thread : {self.simopintcli_thread.is_alive()} simopintcli status : {self.simopintcli.getCliStatus()}')
        self.simopintcli.connectClient()
        self.logger.debug(f'startClient : simopintcli_thread : {self.simopintcli_thread.is_alive()} simopintcli status : {self.simopintcli.getCliStatus()}')
        while self.simopintcli.getCliStatus() < 2:
            time.sleep(1)
        self.simopintcli.startCliLoop()
        self.logger.debug(f'startClient : simopintcli_thread : {self.simopintcli_thread.is_alive()} simopintcli status : {self.simopintcli.getCliStatus()}')
        self.logger.info(f'Interface Client {self.simopintcli.getCliName()} Started')

    # stopClient()
    # Stop Interface Client
    def stopClient(self) -> None:
        self.logger.info(f'Stopping Interface Client {self.simopintcli.getCliName()}')
        self.simopintcli.stopClient()
        self.simopintcli_thread = None
        self.logger.info(f'Interface Client {self.simopintcli.getCliName()} Stopped')
    """

    ###################################
    # Configuration Methods
    ###################################

    # createNewConfig()
    # Return interface configuration as dictionary
    def createNewConfig(self):
        interfaceconfig = dict()
        interfaceconfig['INTERFACE'] = dict()
        interfaceconfig['INTERFACE']['intname'] = self.intname
        interfaceconfig['INTERFACE']['gpiomode'] = "BCM"
        interfaceconfig['NETWORK'] = dict()
        interfaceconfig['NETWORK']['intaddr'] = 'localhost'
        interfaceconfig['NETWORK']['intport'] = 49500
        interfaceconfig['NETWORK']['xpsrvaddr'] = 'localhost'
        interfaceconfig['NETWORK']['xpsrvport'] = 49500
        interfaceconfig['MODULES'] = dict()
        devicesmodulesconfig = SimOpIntConfig('Config/Daemon', 'default_device_modules.json').getConfigSection('DEVICESMODULES')
        interfaceconfig['MODULES']['DEVICESMODULES'] = devicesmodulesconfig
        objectsmodulesconfig = SimOpIntConfig('Config/Daemon', 'default_object_modules.json').getConfigSection('OBJECTSMODULES')
        interfaceconfig['MODULES']['OBJECTSMODULES'] = objectsmodulesconfig
        interfaceconfig['BOARDS'] = dict()
        interfaceconfig['DEVICES'] = dict()
        interfaceconfig['DEVICES']['configfile'] = "devices.json"
        interfaceconfig['DEVICES']['interrupt'] = list()
        interfaceconfig['DEVICES']['MCP23017'] = dict()
        interfaceconfig['DEVICES']['MCP23017']['bankmode'] = 1
        interfaceconfig['DEVICES']['HT16K33'] = dict()
        interfaceconfig['DEVICES']['HT16K33']['brightness'] = 8
        interfaceconfig['OBJECTS'] = dict()
        return interfaceconfig

    # getConfigDir()
    # Return config directory (str)
    def getConfigDir(self) -> str:
        return self.configdir

    # getConfigFile()
    # Return config file name (str)
    def getConfigFileName(self) -> str:
        return self.configfilename

    # setConfigFile(configfilename, configfiletype)
    # configfilename is str
    # Set Config file name to configfilename & Config file type to configfiletype
    def setConfigFileName(self, configfilename) -> None:
        self.configfilename = configfilename

    # getConfig()
    # Return interface configuration (SimOpIntConfig Class)
    def getConfigObj(self) -> SimOpIntConfig:
        return self.config

    # getIntConfig()
    # Return interface configuration dictionary
    def getConfig(self) -> dict:
        return self.config.getConfig()

    ###################################
    # GPIO Interrupt Methods
    ###################################

    # setGpioMode(gpiomode)
    # gpiomode is str (BCM or BOARD)
    def getGpioMode(self) -> str | None:
        if platform.system() == 'Linux':
            return GPIO.getmode()
        else:
            self.logger.warning(f'System is not Linux, RPi GPIO module not available')
            return None

    # setGpioMode(gpiomode)
    # gpiomode is str (BCM or BOARD)
    def setGpioMode(self, gpiomode) -> None:
        if platform.system() == 'Linux':
            if gpiomode == 'BCM':
                GPIO.setmode(GPIO.BCM)
            elif gpiomode == 'BOARD':
                GPIO.setmode(GPIO.BOARD)
            else:
                self.logger.error(f'GPIO Mode {gpiomode} not recognized')
        else:
            self.logger.warning(f'System is not Linux, RPi GPIO module not available')

    # setupIntPortGpio(gpio, [pull_up_down=GPIO.PUD_DOWN])
    # gpio is int
    # pull_up_down is internal pull up / pull down resistor configuration (Pull down by default)
    def setupInterruptGpio(self, channel: int, pullupdown: int) -> None:
        self.logger.debug(f'Setting GPIO {channel} as Input for Interrupt with the following PullUp / PullDown parameter {pullupdown}')
        if platform.system() == 'Linux':
            GPIO.setup(channel, GPIO.IN, pull_up_down=pullupdown)
        else:
            self.logger.warning(f'System is not Linux, RPi GPIO module not available')

    # addInterruptEvent(channel, edge, devicename, [bouncetime = 180])
    # gpio is int
    # edge is int
    # callback is a callback method
    # bouncetime is int
    def addInterruptEvent(self, channel: int, edge: int, devicename: str, bounce_time: int = 180) -> None:
        self.logger.debug(f'Add Event detect for edge {edge} on Channel {channel} for device {devicename}')
        if platform.system() == 'Linux':
            GPIO.add_event_detect(channel, edge, callback=self.interruptCallback, bouncetime=bounce_time)
        else:
            self.logger.warning(f'System is not Linux, RPi GPIO module not available')

    # removeInterruptEvent(gpio)
    # gpio is int
    def removeInterruptEvent(self, channel: int) -> None:
        self.logger.debug(f'Remove Event detect on Channel {channel}.')
        if platform.system() == 'Linux':
            GPIO.remove_event_detect(channel)
        else:
            self.logger.warning(f'System is not Linux, RPi GPIO module not available')

    def interruptCallback(self, channel: int) -> None:
        devicetype = self.interrupt[channel]['devicetype']
        devicename = self.interrupt[channel]['devicename']
        deviceport = self.interrupt[channel]['deviceport']
        device = self.getDevice(devicename)

        if devicetype == 'MCP23017':
            interruptinfo = device.callBackMCP23017(channel)

            if interruptinfo:
                intcapture = interruptinfo['intcapture']
                intflag = interruptinfo['intflag']
                interruptpin = device.getPinFromMask(intflag)
                if interruptpin in self.interrupt[channel]['objects'].keys():
                    objectname = self.interrupt[channel]['objects'][interruptpin]
                    self.logger.debug(f'Processing Interrupt on Channel {channel} [{devicename}({devicetype})]. Capture Register : {bin(intcapture)}. Flag Register : {bin(intflag)}. Pin : {interruptpin} . Object : {objectname}')
                else:
                    self.logger.warning(f'Key {interruptpin} for Channel {channel} is not in Interface Interrupt Dictionary')
            else:
                self.logger.error(f'Bad configuration for interrupt on Device {devicename} Port {deviceport}')
        else:
            self.logger.warning(f'Interrupt not managed for Device Type {devicetype}')

    ###################################
    # Modules Methods
    ###################################

    # listLoadedModules()
    # Return a dictionary containing loaded modules
    def listLoadedModules(self) -> dict:
        return self.modules

    # getModule(modulename)
    # modulename is str
    # return loaded module modulename
    def getModule(self, modulename):
        return getattr(self.modules[modulename], modulename)

    # loadModule(module, cls)
    # module is str / cls is str
    # Import Class (cls) from Module (module) and store it into self.modules
    def loadModule(self, modulename, module, cls) -> None:
        self.modules[modulename] = importlib.import_module(module, cls)

    ###################################
    # Boards Methods
    ###################################

    # getBoards()
    def getBoards(self) -> dict:
        return self.getConfigObj().getConfigSection('BOARDS')

    # setBoards(boards)
    def setBoards(self, boards) -> None:
        pass

    # getBoard(boardname)
    def getBoard(self, boardname) -> dict:
        return self.getConfigObj().getConfigParameter('BOARDS', boardname)

    # setBoard(boardname, board)
    def setBoard(self, boardname, board) -> None:
        pass

    ###################################
    # Devices Methods
    ###################################

    @staticmethod
    # createDeviceConfig()
    # Create a new Devices config file in interface config directory
    def createDeviceConfig() -> dict:
        devicesconfig = dict()
        return devicesconfig

    # listLoadedDevices()
    # Return all loaded devices from self.devices
    def listLoadedDevices(self) -> dict:
        return self.devices

    # getDevice(devicename)
    # Return device object <devicename> from self.devices
    def getDevice(self, devicename):
        if devicename in self.devices:
            return self.devices[devicename]
        else:
            return False

    # createDevice(devicename, deviceaddr, devicemodule)
    # Create Device object and store it into self.devices
    def createDevice(self, devicename: str, deviceaddr: str, devicemodule: str, deviceintgpio: dict | None):
        devicemod = self.getModule(devicemodule)
        if deviceintgpio is not None:
            for port, channel in deviceintgpio.items():
                self.interrupt[channel] = {}
                self.interrupt[channel]['devicename'] = devicename
                self.interrupt[channel]['devicetype'] = devicemodule
                self.interrupt[channel]['deviceport'] = port
                self.interrupt[channel]['objects'] = {}

        self.devices[devicename] = devicemod(devicename, deviceaddr, deviceintgpio)
        self.logger.debug(f'Creating Device {devicename} with following parameter : Address : {deviceaddr} Module : {devicemodule} [{devicemod}] Interrupt GPIO : {deviceintgpio} Object: {self.devices[devicename]}')

    # createDevices()
    # Create Devices objects from configuration file and store them into self.devices
    def createDevices(self):
        self.logger.debug(f'Create All devices from configuration')
        deviceconfigdir = self.configdir
        devicesconfigfile = self.config.getConfigSection("DEVICES")["configfile"]
        devicesconfig = SimOpIntConfig(deviceconfigdir, devicesconfigfile)

        if devicesconfig.isNewConfig():
            config = self.createDeviceConfig()
            devicesconfig.setConfig(config)
            devicesconfig.writeJsonConfigFile()
            devicesconfig.setNewConfig(False)

        if devicesconfig:
            for devicename, deviceconfig in devicesconfig.getConfig().items():
                self.createDevice(devicename, deviceconfig['deviceaddr'], deviceconfig['devicemodule'], deviceconfig['deviceintgpio'])
        else:
            self.logger.error(f'No devices configuration found to load ...')

    ###################################
    # Objects Methods
    ###################################

    # listLoadedObjects()
    # Return all objects created from configuration
    def listLoadedObjects(self) -> dict:
        return self.objects

    # getObject(objcategory, objname)
    # objcategory is str and objname is str
    # Return an object designated by its category and name
    def getObject(self, objcategory: str, objname: str):
        return self.objects[objcategory][objname]

    # getCategoryObjects(objcategory)
    # objcategory is str
    # Return all objects existing in category objcategory
    def getCategoryObjects(self, objcategory: str) -> dict:
        return self.objects[objcategory]

    # createObject(objcategory, objname)
    # objcategory is str and objname is str
    # Create object objname in category objcategory from configuration (objcategory and objectname should exist in configuration)
    def createObject(self, objcategory: str, objname: str, objmodule: str, args: list) -> None:
        self.logger.debug(f'Creating Object {objname} in category {objcategory} with module {objmodule}. Object args : {args}')
        module = self.getModule(objmodule)
        self.objects[objcategory][objname] = module(*args)

    # createObjectsCategory(objcategory)
    # objcategory is str
    # Create all objects in category objcategory from configuration (objcategory should exist in configuration)
    def createObjectsCategory(self, objcategory: str) -> None:
        objectsconfigfile = self.config.getConfigSection("OBJECTS")[objcategory]["configfile"]
        self.logger.debug(f'Creating objects from category {objcategory} from configuration file {objectsconfigfile}')
        objectsconfigdir = f'{self.configdir}'
        objectsconfig = SimOpIntConfig(objectsconfigdir, objectsconfigfile)

        if objectsconfig:
            self.logger.debug(f'Reading Objects Configurations : {objectsconfig.getConfig()}')
            self.objects[objcategory] = {}
            objmodule = objectsconfig.getConfigParameter('CONF', 'class')
            propkeys = sorted(objectsconfig.getConfigSection('PROPERTIES').keys())
            self.logger.debug(f'Category objects properties keys :{propkeys}')
            for objname, objconfig in objectsconfig.getConfigSection('OBJECTS').items():
                self.logger.debug(f'Object {objname} : {objconfig}')

                args = []

                for prop in propkeys:
                    propname = objectsconfig.getConfigParameter('PROPERTIES', prop)
                    propvalue = objconfig[propname]

                    if propname == 'device':
                        propvalue = self.getDevice(propvalue)
                    else:
                        propvalue = objconfig[propname]

                    args.append(propvalue)

                self.createObject(objcategory, objname, objmodule, args)

                if self.getObject(objcategory, objname).IsCommand():
                    obj = self.getObject(objcategory, objname)
                    objdevice = obj.getDevice()
                    if objdevice.getDeviceType() == 'MCP23017':
                        self.logger.debug(f'Need to insert Object {objname} into Interrupt Dictionary. IsCommand : {obj.IsCommand()}. Pins : {obj.getPins()}.')
                        for name, params in obj.getPins().items():
                            channel = objdevice.getIntPortGPIO(params['port'])
                            self.logger.debug(f"Pin {name} => Port {params['port']} Pin Num {params['pin']} => Channel : {channel}")
                            self.interrupt[channel]['objects'][params['pin']] = objname

        else:
            self.logger.error(f'Error when loading configuration file  {objectsconfigfile}')

    # createObjects()
    # Create all objects define in configuration
    def createObjects(self) -> None:
        objectsconfig = self.config.getConfigSection('OBJECTS')
        self.logger.debug(f'Objects configuration : {objectsconfig}')
        for objcategory in objectsconfig:
            self.createObjectsCategory(objcategory)

    ###################################
    # Main Loop Interface
    ###################################

    def mainLoop(self):

        while self.intstate != 0:

            while self.running:
                self.logger.debug(f'Main loop running ....')

                time.sleep(1)

            time.sleep(5)

        # sys.exit()
