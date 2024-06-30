##############################
# Sim Open Interface Daemon
##############################

# System Modules Import
# import sys
import logging

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntClient import SimOpIntClient

configdir = 'Config'
configfile = 'configcli.ini'
configtype = 'INI'

logger = logging.getLogger('SimOpInt')
logfile = 'Logs/simopintclient.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
logger.addHandler(filehandler)

config = SimOpIntConfig(configdir, configfile, configtype)

srvname = config.getConfigParameter('NETWORK', 'srvname')['srvname']
srvaddr = config.getConfigParameter('NETWORK', 'srvaddr')['srvaddr']
srvport = config.getConfigParameter('NETWORK', 'srvport')['srvport']
cliname = config.getConfigParameter('NETWORK', 'cliname')['cliname']

simopintcli = SimOpIntClient(cliname, srvname, srvaddr, srvport, logging.DEBUG)

simopintcli.openCliSocket()
simopintcli.connectClient()
simopintcli.closeCliSocket()
