##################################################
# FarmerSoft Open Interface Daemon
##################################################
# FarmerSoft © 2024
# By Daweed
##################################################

# System Modules Import
# import sys
import logging
import threading

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntServer import SimOpIntServer

configdir = 'Config/Server'
configfile = 'config.json'
configtype = 'json'

# Logger Creation
logger = logging.getLogger('SimOpInt')
logfile = 'Logs/simopintd.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
logger.addHandler(filehandler)

config = SimOpIntConfig(configdir, configfile, configtype)
srvconfig = config.getConfig()

srvname = config.getConfigParameter('SERVER', 'srvname')
srvaddr = config.getConfigParameter('SERVER', 'srvaddr')
srvport = config.getConfigParameter('SERVER', 'srvport')

simopintd = SimOpIntServer(srvname, srvaddr, srvport, logging.INFO)

simopintd_thread = threading.Thread(target=simopintd.mainLoop)

simopintd_thread.start()

simopintd.startSrvLoop()
