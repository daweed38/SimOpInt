# System Modules Import
import os

# Standard Modules Import
import configparser
import json


class SimOpIntTools:
    """
    This Class contain some useful tools
    """

    ##############################
    # Properties
    ##############################

    ##############################
    # Constructor
    ##############################
    def __init__(self, debug=0):
        self.debug = debug

    ##############################
    # Destructor
    ##############################
    def __del__(self):
        pass

    ##############################
    # Methods INI Files
    ##############################

    # readConfigFile()
    # read and return ini format configuration file into a dictionary
    def readConfigFile(self, configdir, configfile):
        configdict = {}

        if os.path.exists(configdir + '/' + configfile):

            if self.debug == 98:
                print("######################################################################")
                print("# Reading Configuration from file : {} in directory {}".format(configfile, configdir))
                print("######################################################################")
                print("\r")

            config = configparser.ConfigParser()
            config.read(configdir + "/" + configfile)

            for section in config.sections():
                if self.debug == 98:
                    print("# Section : {}".format(section))

                optiontab = {}
                for key, value in config.items(section):
                    if self.debug == 98:
                        print("{} => {} [{}]".format(key, value, type(value)))
                    optiontab[key] = value

                configdict[section] = optiontab

            if self.debug == 98:
                print("\r")

        else:
            if self.debug == 98:
                print("######################################################################")
                print("# Configuration File : {} Not Found in  {}".format(configfile, configdir))
                print("######################################################################")
                print("\r")

            configdict = False

        return configdict

    ##############################
    # Methods JSON Files
    ##############################

    # readJsonFile()
    # read and return json format configuration file into a dictionary
    def readJsonFile(self, configdir, configfile):
        if os.path.exists(configdir + '/' + configfile):
            if self.debug == 98:
                print("######################################################################")
                print("# Reading Configuration from file : {} in directory {}".format(configfile, configdir))
                print("######################################################################")
                print("\r")

            try:
                with open(configdir + '/' + configfile, 'r') as filedesc:
                    configdict = json.load(filedesc)
            except json.decoder.JSONDecodeError:
                configdict = False
                print("{} in dir {} is invalid".format(configfile, configdir))

        else:
            if self.debug == 98:
                print("######################################################################")
                print("# Configuration File : {} Not Found in  {}".format(configfile, configdir))
                print("######################################################################")
                print("\r")

            configdict = False

        return configdict
