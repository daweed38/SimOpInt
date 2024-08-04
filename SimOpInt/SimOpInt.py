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
        if self.config:
            self.intname = self.config.getConfigParameter('INTERFACE', 'intname')
            self.intaddr = self.config.getConfigParameter('NETWORK', 'intaddr')
            self.intport = self.config.getConfigParameter('NETWORK', 'intport')

            if 'DEVICES' in self.config.getConfig():
                devicesconfig = self.config.getConfigSection('DEVICES')
                if devicesconfig:
                    # self.logger.debug(f'Loading devices from configuration {devicesconfig} {type(devicesconfig)} {bool(devicesconfig)}')
                    self.loadDevices()
                else:
                    self.logger.warning(f'No devices configuration found to load ...')

            """
            if 'MODULES' in self.config.getConfig():
                modulesconfig = self.config.getConfigSection('MODULES')
                if modulesconfig:
                    self.logger.debug(f'Loading Modules from Configuration {modulesconfig} {type(modulesconfig)} {bool(modulesconfig)}')
                else:
                    self.logger.warning(f'No modules configuration found to load ...')

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
    # Devices Methods
    ###################################

    # Load Devices Defines in configuration file
    def loadDevices(self) -> None:
        intconfigdir = f'Config/Interfaces/{self.getName()}'
        deviceconfigfile = self.config.getConfigSection('DEVICES')['configfile']
        devicesconfig = SimOpIntConfig(intconfigdir, deviceconfigfile, 'JSON')
        devicedict = devicesconfig.getConfig()["DEVICES"]
        self.logger.debug(f'Interface Configuration Directory : {intconfigdir} | Device Configuration File : {deviceconfigfile} => {devicesconfig.getConfig()["DEVICES"]}')
        for device in devicesconfig.getConfig()['DEVICES']:
            self.logger.debug(
                f'Loading {devicesconfig.getConfig()["DEVICES"][device]["devicename"]} with following parameters : '
                f'Device Address {devicesconfig.getConfig()["DEVICES"][device]["deviceaddr"]} '
                f'Device Type {devicesconfig.getConfig()["DEVICES"][device]["devicetype"]}'
            )

    ###################################
    # Modules Methods
    ###################################

    ###################################
    # Objects Methods
    ###################################
