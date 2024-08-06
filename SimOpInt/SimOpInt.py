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
                modulesconfig = self.config.getConfigSection('MODULES')

                if modulesconfig:
                    self.logger.debug(f'Loading Modules from Configuration {modulesconfig}')
                    modules = [key for key, value in modulesconfig.items() if key not in ['CONF']]
                    for modulesection in modules:
                        if len(modulesconfig[modulesection]) > 0:
                            for modulename, moduledata in modulesconfig[modulesection].items():
                                self.logger.debug(f'Loading Module Name {modulename} : Module {moduledata["module"]} => Class {moduledata["class"]}')
                                module = f'SimOpInt.{moduledata["module"]}'
                                self.loadModule(modulename, module, moduledata['class'])
                    self.logger.debug(f'Loaded Modules : {self.listLoadedModules()}')
                else:
                    self.logger.warning(f'No modules configuration found to load ...')

            if 'DEVICES' in self.config.getConfig():
                deviceconfigdir = f'{self.configdir}/{self.intname}'
                devicesconfigfile = self.config.getConfigSection("DEVICES")["CONF"]["configfile"]
                devicesconfig = SimOpIntConfig(deviceconfigdir, devicesconfigfile, 'JSON')

                if devicesconfig:
                    self.logger.debug(f'Device Config File {devicesconfigfile} : {devicesconfig.getConfig()}')
                    for devicename, deviceconfig in devicesconfig.getConfig().items():
                        self.logger.debug(f'Loading Device {devicename} : {deviceconfig}')
                        self.devices[devicename] = deviceconfig
                    self.createDevices()
                    self.logger.debug(f'Loaded Devices : {self.getDevices()}')
                else:
                    self.logger.warning(f'No devices configuration found to load ...')

            """
            if 'OBJECTS' in self.config.getConfig():
                objectsconfig = self.config.getConfigSection('OBJECTS')
                if objectsconfig:
                    self.logger.debug(f'Loading Objects from Configuration {objectsconfig} {type(objectsconfig)} {bool(objectsconfig)}')
                else:
                    self.logger.warning(f'No objects configuration found to load ...')
            """

            self.logger.debug(f'Sim Open Interface {self.getName()} initialized ...')
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

    # loadModule(module, cls)
    # module is str / cls is str
    # Import Class (cls) from Module (module) and store it into self.modules
    def loadModule(self, modulename, module, cls) -> None:
        self.modules[modulename] = {}
        self.modules[modulename]["class"] = cls
        self.modules[modulename]["module"] = importlib.import_module(module, cls)

    # getModule(modulename)
    # modulename is str
    # return loaded module modulename
    def getModule(self, modulename):
        return getattr(self.modules[modulename]["module"], self.modules[modulename]["class"])

    ###################################
    # Devices Methods
    ###################################

    # getDevice(devicename)
    # Return device <devicename> from self.devices
    def getDevice(self, devicename):
        if devicename in self.devices:
            return self.devices[devicename]
        else:
            return False

    # getDeviceObj(devicename)
    # Return devices <devicename> object from self.devices
    def getDeviceObj(self, devicename):
        if devicename in self.devices:
            return self.devices[devicename]['deviceobj']
        else:
            return False

    # getDevices()
    # Return all loaded devices from self.devices
    def getDevices(self) -> dict:
        return self.devices

    # createDevice(devicename, deviceaddr, devicemodule [, debug ])
    # Create Device object and store it into self.devices
    def createDevice(self, devicename, deviceaddr, devicetype):
        devicemod = self.getModule(devicetype)
        self.devices[devicename]['deviceobj'] = devicemod(devicename, deviceaddr, self.debug)
        self.logger.debug(f'Creating Device {devicename} with following parameter : Address : {deviceaddr} Module : {devicetype} [{devicemod}] Object: {self.devices[devicename]["deviceobj"]}')

    # createDevices()
    # Create Devices from configuration file and store them into self.devices
    def createDevices(self):
        self.logger.debug(f'Create All devices defined in self.devices')
        for device, deviceconf in self.devices.items():
            self.createDevice(deviceconf['devicename'], deviceconf['deviceaddr'], deviceconf['devicetype'])

    ###################################
    # Objects Methods
    ###################################
