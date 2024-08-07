##################################################
# FarmerSoft Open Interface Class
##################################################
# SimOpInt Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
# import sys
# import os
import logging
import importlib

# SimOpInt Module Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig


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

    def __init__(self, configdir: str, configfilename: str, configfiletype: str, debug: int = 30) -> None:

        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.configdir = configdir
        self.configfilename = configfilename
        self.configfiletype = configfiletype
        self.dummy = False
        self.modules = {}
        self.devices = {}
        self.objects = {}

        self.config = SimOpIntConfig(self.configdir, self.configfilename, self.configfiletype)
        self.logger.debug(f'Interface Config : {self.config.getConfig()}')

        if self.config:
            self.intname = self.config.getConfigParameter('INTERFACE', 'intname')
            self.intaddr = self.config.getConfigParameter('NETWORK', 'intaddr')
            self.intport = self.config.getConfigParameter('NETWORK', 'intport')

            if 'MODULES' in self.config.getConfig():
                self.logger.debug(f'--- Modules Configuration Management ---')
                modulesconfig = self.config.getConfigSection('MODULES')

                if modulesconfig:
                    self.logger.debug(f'Loading Modules from Configuration {modulesconfig}')
                    for modulesection, modulesconfig in modulesconfig.items():
                        if len(modulesconfig) > 0:
                            self.logger.debug(f'Module Section : {modulesection} : {modulesconfig}')
                            for modulename, moduledata in modulesconfig.items():
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


            self.logger.debug(f'--- Sim Open Interface {self.getName()} initialized ---')
        else:
            self.logger.debug(f'Sim Open Interface initialisation error ...')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

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
    def setName(self, intname) -> None:
        self.intname = intname

    # getAddr()
    # Return interface address (int)
    def getAddr(self) -> str:
        return self.intaddr

    # setAddr(intaddr)
    # intaddr is int
    # Set interface address to intaddr
    def setAddr(self, intaddr) -> None:
        self.intaddr = intaddr

    # getPort()
    # Return interface port (int)
    def getPort(self) -> int:
        return self.intport

    # setPort(intport)
    # intport is int
    # Set interface port to intport
    def setPort(self, intport) -> None:
        self.intport = intport

    ###################################
    # Configuration Methods
    ###################################

    # getConfigFile()
    # Return config file name (str)
    def getConfigFileName(self) -> str:
        return self.configfilename

    # setConfigFile(configfilename, configfiletype)
    # configfilename is str
    # configfiletype is str (possible value are json or ini)
    # Set Config file name to configfilename & Config file type to configfiletype
    def setConfigFileName(self, configfilename, configfiletype) -> None:
        self.configfilename = configfilename
        self.configfiletype = configfiletype

    # getConfig()
    # Return interface configuration (SimOpIntConfig Class)
    def getConfig(self) -> SimOpIntConfig:
        return self.config

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
    # Devices Methods
    ###################################

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
    def createDevice(self, devicename: str, deviceaddr: str, devicemodule: str):
        devicemod = self.getModule(devicemodule)
        self.devices[devicename] = devicemod(devicename, deviceaddr)
        self.logger.debug(f'Creating Device {devicename} with following parameter : Address : {deviceaddr} Module : {devicemodule} [{devicemod}] Object: {self.devices[devicename]}')

    # createDevices()
    # Create Devices objects from configuration file and store them into self.devices
    def createDevices(self):
        self.logger.debug(f'Create All devices from configuration')
        deviceconfigdir = f'{self.configdir}/{self.intname}'
        devicesconfigfile = self.config.getConfigSection("DEVICES")["configfile"]
        devicesconfig = SimOpIntConfig(deviceconfigdir, devicesconfigfile, 'JSON')

        if devicesconfig:
            for devicename, deviceconfig in devicesconfig.getConfig().items():
                self.createDevice(devicename, deviceconfig['deviceaddr'], deviceconfig['devicemodule'])
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
        pass

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
        objectsconfigdir = f'{self.configdir}/{self.intname}'
        objectsconfig = SimOpIntConfig(objectsconfigdir, objectsconfigfile, 'JSON')

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

                    args.append(propvalue)

                self.createObject(objcategory, objname, objmodule, args)
        else:
            self.logger.error(f'Error when loading configuration file  {objectsconfigfile}')

    # createObjects()
    # Create all objects define in configuration
    def createObjects(self) -> None:
        self.logger.debug(f'Objects configuration : {self.config.getConfigSection('OBJECTS')}')
        for objcategory in self.config.getConfigSection('OBJECTS'):
            self.createObjectsCategory(objcategory)

