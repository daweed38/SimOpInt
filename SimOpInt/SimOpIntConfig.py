##################################################
# FarmerSoft Open Interface Configuration Class
##################################################
# SimOpIntConfig Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import os
import logging
import json

# SimOpInt Modules Import

# SimOpIntConfig Modules Import


class SimOpIntConfig:

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return 'This is the Sim Open Interface Configuration Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, configdir: str, configfile: str, debug: int = 30) -> None:
        self.debug = debug
        self.logger = logging.getLogger(__name__)

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.configdir = configdir
        self.configfile = configfile
        self.configfmt = 'json'
        self.newconfig = False
        self.configdict = {}

        self.logger.debug(f'Config Dir {self.configdir} / Config File {self.configfile} / Config Type {self.configfmt}')

        # Loading configuration
        if os.path.isfile(self.configdir+'/'+self.configfile):
            self.logger.debug(f'Trying to read configuration file {self.configfile} in directory {self.configdir}')
            if self.configfile.endswith('.json'):
                self.readJsonConfigFile()
                self.logger.debug(f'Sim Open Interface configuration Class initialized')
            else:
                self.logger.critical(f'Configuration file format is not recognized (Only JSON configuration files are supported')
        else:
            if not os.path.isdir(self.configdir):
                self.logger.debug(f'Creating new configuration directory {self.configdir}')
                os.mkdir(self.configdir)
            self.newconfig = True

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    def isNewConfig(self) -> bool:
        return self.newconfig

    def setNewConfig(self, status):
        self.newconfig = status

    def getConfigFile(self) -> str:
        return self.configfile

    def setConfigFile(self, configfile: str) -> None:
        self.configfile = configfile

    def getConfigDir(self) -> str:
        return self.configdir

    def setConfigDir(self, configdir: str) -> None:
        self.configdir = configdir

    ###################################
    # Common Config Methods
    ###################################

    # getConfig()
    # Return Configuration (dict)
    def getConfig(self) -> dict:
        return self.configdict

    # setConfig(configdict)
    # Set Configuration to configdict (dict)
    def setConfig(self, configdict: dict):
        self.configdict = configdict

    # getConfigSection(section)
    # section is str
    # Return config section from self.config (dict)
    def getConfigSection(self, section: str) -> bool | dict:
        if section in self.getConfig():
            return self.configdict[section]
        else:
            self.logger.error(f'Section {section} not found in configuration {self.getConfig()}')
            return False

    # setConfigSection(section, data)
    # section is str
    # data is dict
    # set config section in self.config to data
    def setConfigSection(self, section: str, data: dict) -> None:
        if section in self.getConfig():
            self.configdict[section] = data
        else:
            self.logger.error(f'Section {section} not found in configuration {self.getConfig()}')

    # setConfigParameter(section, parameter, data)
    # section is str
    # parameter is str
    # Set config parameter in section from self.config to data (bool | dict | int | str)
    def setConfigParameter(self, section: str, parameter: str, data: bool | dict | int | str) -> None:
        if section in self.getConfig():
            if parameter in self.getConfigSection(section):
                self.configdict[section][parameter] = data
            else:
                self.logger.error(f'Parameter {parameter} not found in section {section} : {self.getConfigSection(section)}')
        else:
            self.logger.error(f'Section {section} not found in configuration {self.getConfig()}')

    # setConfigParameter(section, parameter, data)
    # section is str
    # parameter is str
    # Return config parameter from self.config (dict | int | str)
    def getConfigParameter(self, section: str, parameter: str) -> bool | dict | int | str:
        if section in self.getConfig():
            if parameter in self.getConfigSection(section):
                return self.configdict[section][parameter]
            else:
                self.logger.error(f'Parameter {parameter} not found in section {section} : {self.getConfigSection(section)}')
                return False
        else:
            self.logger.error(f'Section {section} not found in configuration {self.getConfig()}')
            return False

    ###################################
    # JSON Files Methods
    ###################################

    # readJsonConfigFile()
    # JSON Configuration File Reader
    def readJsonConfigFile(self) -> None:
        if os.path.exists(self.configdir + '/' + self.configfile):
            self.logger.debug(f'Reading Configuration JSON file {self.configfile} in directory {self.configdir}')
            try:
                with open(self.configdir + '/' + self.configfile, 'r') as filedesc:
                    self.configdict = json.load(filedesc)

            except json.decoder.JSONDecodeError:
                self.configdict = False
                self.logger.critical(f"{self.configfile} in dir {self.configdir} is invalid")
        else:
            self.logger.critical(f'Error : Configuration file {self.configfile} not found in directory {self.configdir}')
            self.configdict = False
            raise FileNotFoundError()

    # writeJsonConfigFile()
    # JSON Configuration File Writer
    def writeJsonConfigFile(self) -> None:
        self.logger.debug(f'Writing data {self.getConfig()} to JSON file {self.configfile} in {self.configdir}')
        with open(f'{self.configdir}/{self.configfile}', 'w') as outfile:
            json.dump(self.getConfig(), outfile, indent=2)