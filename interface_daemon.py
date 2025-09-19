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
from SimOpInt.SimOpIntServer import SimOpIntServer

# Logger Creation
"""
int_simopint_logger = logging.getLogger('SimOpInt',)
logfile = 'Logs/simopint.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
int_simopint_logger.addHandler(filehandler)
"""

int_simopintsrv_logger = logging.getLogger('SimOpInt.SimOpIntServer')
logfile = 'Logs/interface_simopintd.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
int_simopintsrv_logger.addHandler(filehandler)
int_simopintsrv_logger.propagate = False

# SimOpInt Daemon Creation (Ex SimOpIntServer(configfile='SimOpIntTestSrv.json', debug=logging.INFO) - configfile & debug facultatif
simopintd = SimOpIntServer(configfile='SimOpIntTestSrv.json')

# SimOpInt Daemon loop thread creation
simopintd_thread = threading.Thread(target=simopintd.mainLoop)
simopintd_thread.start()

# Waiting for Opened Socket
while simopintd.getSrvStatus() != 1:
    time.sleep(1)

# Starting SimOpInt Daemon Loop
simopintd.startSrvLoop()

