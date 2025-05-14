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
# from SimOpInt.SimOpIntClient import SimOpIntClient

# Logger Creation
int_simopint_logger = logging.getLogger('SimOpInt',)
logfile = 'Logs/simopint.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
int_simopint_logger.addHandler(filehandler)

int_simopintsrv_logger = logging.getLogger('SimOpInt.SimOpIntServer')
logfile = 'Logs/interface_simopintd.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
int_simopintsrv_logger.addHandler(filehandler)
int_simopintsrv_logger.propagate = False

int_simopintcli_logger = logging.getLogger('SimOpInt.SimOpIntClient')
logfile = 'Logs/interface_simopintcli.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
int_simopintcli_logger.addHandler(filehandler)
int_simopintcli_logger.propagate = False

# SimOpInt Daemon Creation (Ex SimOpIntDaemon(configfile='SimOpIntTestSrv.json', debug=logging.INFO) - configfile & debug facultatif
# simopintd = SimOpIntDaemon()
# simopintd = SimOpIntDaemon(debug=logging.INFO)
# simopintd = SimOpIntDaemon(configfile='SimOpIntTestSrv.json', debug=logging.INFO)
simopintd = SimOpIntDaemon(configfile='SimOpIntTestSrv.json', debug=logging.INFO)

# SimOpInt Daemon loop thread creation
simopintd_thread = threading.Thread(target=simopintd.mainLoop)
simopintd_thread.start()

# Waiting for Opened Socket
while simopintd.getSrvStatus() != 1:
    time.sleep(1)

# Starting SimOpInt Daemon Loop
simopintd.startSrvLoop()

# SimOpInt Client Creation
# simopintcli = SimOpIntClient(cliname, srvname, srvaddr, srvport, logging.INFO)
# simopintcli = SimOpIntClient(debug=logging.INFO)

# SimOpInt Daemon loop thread creation
# simopintcli_thread = threading.Thread(target=simopintcli.mainLoop)
# simopintcli_thread.start()

# Starting SimOpInt Interface
# while simopintd.getSrvStatus() != 2:
#     time.sleep(1)

# simopintd.startInterface()
