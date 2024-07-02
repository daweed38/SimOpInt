##############################
# Sim Open Interface Daemon
##############################

# System Modules Import
# import sys
import logging
import threading

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntServer import SimOpIntServer

configdir = 'Config'
configfile = 'config.ini'
configtype = 'INI'

# Logger Creation
logger = logging.getLogger('SimOpInt')
logfile = 'Logs/simopintd.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
logger.addHandler(filehandler)

config = SimOpIntConfig(configdir, configfile, configtype)

srvname = config.getConfigParameter('NETWORK', 'srvname')['srvname']
srvaddr = config.getConfigParameter('NETWORK', 'srvaddr')['srvaddr']
srvport = config.getConfigParameter('NETWORK', 'srvport')['srvport']

simopintd = SimOpIntServer(srvname, srvaddr, srvport, logging.INFO)

simopintd_thread = threading.Thread(target=simopintd.mainLoop)

simopintd_thread.start()

simopintd.startSrvLoop()
