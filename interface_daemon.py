##################################################
# FarmerSoft Sim Open Interface Daemon
##################################################
# FarmerSoft © 2026
# By Daweed
##################################################

# System Modules Import
import logging

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntDaemon import SimOpIntDaemon

# Logger Creation
int_simopintsrv_logger = logging.getLogger('SimOpInt.SimOpIntDaemon')
logfile = 'Logs/interface_simopintd.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
int_simopintsrv_logger.addHandler(filehandler)
int_simopintsrv_logger.propagate = False

simopint_logger = logging.getLogger('SimOpInt.SimOpInt')
logfile = 'Logs/interface_simopint.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
simopint_logger.addHandler(filehandler)
simopint_logger.propagate = False

# SimOpInt Daemon Creation (Ex SimOpIntServer(configfile='SimOpIntTestSrv.json', debug=logging.INFO) - configfile & debug facultatif
simopintd = SimOpIntDaemon(configfile='SimOpIntTestSrv.json', debug=logging.INFO)

# Starting Server
# simopintd.startServer()
