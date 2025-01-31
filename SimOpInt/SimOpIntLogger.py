##################################################
# FarmerSoft Open Interface TCP Client Class
##################################################
# SimOpIntClient Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging


class SimOpIntLogger:

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return 'This is the main Sim Open Interface Custom Logger'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, loggername, logdir: str, logfile: str, debug: int = logging.WARNING) -> None:
        self.loggername = loggername
        self.logger = logging.getLogger(self.loggername)
        self.debug = debug
        self.logfile = f'{logdir}/{logfile}'
        filehandler = logging.FileHandler(filename=self.logfile, mode='w')
        fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
        filehandler.setFormatter(fileformat)
        self.logger.addHandler(filehandler)

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

    #############################################
    # Destructor
    #############################################

    def __del__(self) -> None:
        pass

    #############################################
    # System Method
    #############################################

    #############################################
    # Class Method
    #############################################

    # getLogger()
    # Return the logger
    def getLogger(self):
        return self.logger

    # getLoggerName()
    # Return the logger name
    def getLoggerName(self) -> str:
        return self.loggername

    # getLoggingLevel()
    # Return current logging level for this logger
    def getLoggingLevel(self) -> int:
        return self.logger.getEffectiveLevel()

    # setLoggingLevel(level)
    # level is int
    # Set logging level for this logger
    def setLoggingLevel(self, level) -> None:
        self.logger.setLevel(level)
        self.logger.debug(f'Updating {__name__} logger level to {logging.getLevelName(level)}')
