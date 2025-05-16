##################################################
# FarmerSoft Open Interface Daemon
##################################################
# FarmerSoft © 2025
# By Daweed
##################################################

# System Modules Import
import logging
import threading
import time

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntDaemon import SimOpIntDaemon
from SimOpInt.SimOpIntClient import SimOpIntClient

# Logger Creation
# simopint_logger = logging.getLogger('SimOpInt',)
# logfile = 'Logs/simopint.log'
# filehandler = logging.FileHandler(filename=logfile, mode='w')
# fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
# filehandler.setFormatter(fileformat)
# simopint_logger.addHandler(filehandler)

plugin_simopintsrv_logger = logging.getLogger('SimOpInt.SimOpIntServer')
logfile = 'Logs/plugin_simopintsrv.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
plugin_simopintsrv_logger.addHandler(filehandler)
plugin_simopintsrv_logger.propagate = False

plugin_simopintcli_logger = logging.getLogger('SimOpInt.SimOpIntClient')
logfile = 'Logs/plugin_simopintcli.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
plugin_simopintcli_logger.addHandler(filehandler)
plugin_simopintcli_logger.propagate = False

# SimOpInt Daemon Creation (Ex SimOpIntDaemon(configfile='SimOpIntTestSrv.json', debug=logging.INFO) - configfile & debug facultative
# simopintd = SimOpIntDaemon()
# simopintd = SimOpIntDaemon(debug=logging.INFO)
# simopintd = SimOpIntDaemon(configfile='SimOpIntTestSrv.json', debug=logging.INFO)
simopintd = SimOpIntDaemon(debug=logging.INFO)

# SimOpInt Daemon loop thread creation
simopintd_thread = threading.Thread(target=simopintd.mainLoop)
simopintd_thread.start()

# Waiting for Opened Socket
while simopintd.getSrvStatus() != 1:
    time.sleep(1)

# Starting SimOpInt Daemon Loop
simopintd.startSrvLoop()

# Starting SimOpInt Interface
# while simopintd.getSrvStatus() != 2:
#    time.sleep(1)

# simopintd.startInterface()
