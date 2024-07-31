##################################################
# FarmerSoft Open Interface Configuration Class
##################################################
# SimOpIntConfig Class
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import os
import logging
import configparser
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

    def __init__(self, configdir: str, configfile: str, configtype: str, debug: int = 30) -> None:
        self.debug = debug
        self.logger = logging.getLogger(__name__)

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.configdir = configdir
        self.configfile = configfile
        self.configtype = configtype
        self.configdict = {}

        self.logger.debug(f'Config Dir {self.configdir} / Config File {self.configfile} / Config Type {self.configtype}')

        # Loading configuration
        if self.configtype.upper() == 'INI' or self.configtype.upper() == 'JSON':
            if self.configtype.upper() == 'INI':
                self.readIniConfigFile()
            else:
                self.readJsonConfigFile()
            self.logger.debug(f'Sim Open Interface configuration Class initialized')
        else:
            self.logger.critical(f'Configuration File Type {self.configtype} is not recognized')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # Common Config Methods
    ###################################

    # getConfig()
    # Return Configuration (dict)
    def getConfig(self) -> dict:
        return self.configdict

    # getConfigSection(section)
    # section is str
    # Return config section from self.config (dict)
    def getConfigSection(self, section: str) -> dict:
        return self.configdict[section]
        # return {section: self.configdict[section]}

    # getConfigParameter(section, parameter)
    # section is str
    # parameter is str
    # Return config parameter from self.config (dict | int | str)
    def getConfigParameter(self, section: str, parameter: str) -> dict | int | str:
        return self.configdict[section][parameter]
        # return {parameter: self.configdict[section][parameter]}

    ###################################
    # INI Files Methods
    ###################################

    # readIniConfigFile()
    # INI Configuration File Reader
    def readIniConfigFile(self) -> None:
        if os.path.exists(self.configdir + '/' + self.configfile):
            self.logger.debug(f'Reading Configuration INI file {self.configfile} in directory {self.configdir}')

            config = configparser.ConfigParser()
            config.read(self.configdir + "/" + self.configfile)

            for section in config.sections():
                self.logger.debug("# Section : {}".format(section))

                optiontab = {}
                for key, value in config.items(section):
                    self.logger.debug("{} => {} [{}]".format(key, value, type(value)))
                    optiontab[key] = value

                self.configdict[section] = optiontab
        else:
            self.logger.critical(f'Error : Configuration file {self.configfile} not found in directory {self.configdir}')
            self.configdict = False
            raise FileNotFoundError()

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
        pass

    """
    def writeJsonConfigFile(self, configdir: str, configfile: str, data: dict) -> None:
        if os.path.exists(configdir):
            self.logger.debug(f'Directory {configdir} exist ...')
            if os.path.exists(f'{configdir}/{configfile}'):
                self.logger.error(f'Interface configuration file {configfile} already exist in {configdir} directory ...')
            else:
                self.logger.error(f'Creating Interface configuration file {configfile} in {configdir} directory  ...')
                with open(f'{configdir}/{configfile}.json', 'w') as intfile:
                    json.dump(data, intfile)
        else:
            self.logger.debug(f' {configdir} directory does not exist ...')
    """