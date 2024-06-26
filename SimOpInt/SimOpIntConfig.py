# System Modules Import
import os
import logging

# Standard Modules Import
import configparser
import json

##################################################
# FarmerSoft Open Interface Configuration Class
##################################################
# SimOpIntConfig Class
# FarmerSoft © 2024
# By Daweed
##################################################


class SimOpIntConfig:
    """
    This is the Sim Open Interface Configuration Management Class
    Configuration can be read and write in two format :
    - INI
    - JSON
    Configurations files are stored in the Config Directory
    """

    #############################################
    # Class Description
    #############################################
    def __str__(self) -> str:
        return 'This is the Sim Open Interface Configuration Class'

    ##############################
    # Properties
    ##############################

    ##############################
    # Constructor
    ##############################
    def __init__(self, configdir: str, configfile: str, configtype: str, debug: int = 30) -> None:
        self.configdir = configdir
        self.configfile = configfile
        self.configtype = configtype
        self.debug = debug
        self.configdict = {}

        # Get Logger
        self.logger = logging.getLogger(__name__)
        self.logger.info(f'Sim Open Interface Configuration Class Intialisation')

        # Loading configuration
        if self.configtype.upper() == 'INI' or self.configtype.upper() == 'JSON':
            if self.configtype.upper() == 'INI':
                self.ReadIniConfigFile()
            else:
                self.ReadJsonConfigFile()
        else:
            self.logger.critical(f'Configuration File Type {self.configtype} is not recognized')

    #############################
    # Destructor
    ##############################
    def __del__(self) -> None:
        self.logger.info(f'Sim Open Interface Configuration Removed')

    ##############################
    # Common Config Methods
    ##############################

    # Get Configuration Dict
    def getConfig(self) -> dict:
        return self.configdict

    def getConfigSection(self, section: str) -> dict:
        return { section: self.configdict[section] }

    def getConfigParameter(self, section: str, parameter: str) -> dict:
        return { parameter: self.configdict[section][parameter] }

    ##############################
    # INI Files Methods
    ##############################

    # INI Configuration File Reader
    def ReadIniConfigFile(self) -> None:
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
            raise FileNotFoundError()

    ##############################
    # JSON Files Methods
    ##############################

    # JSON Configuration File Reader
    def ReadJsonConfigFile(self) -> None:
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
            raise FileNotFoundError()
