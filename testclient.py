##############################
# Sim Open Interface Daemon
##############################

# System Modules Import
# import sys
import logging
import datetime
import json

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntClient import SimOpIntClient

testdict = {'command': {'name': {'args': {'arg1': True, 'arg2': False}}}}

jsondata = open('Config/data.json')
jsondict = dict(json.load(jsondata))
jsondata.close()

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

simopintcli = SimOpIntClient(cliname, srvname, srvaddr, srvport, logging.INFO)

simopintcli.openCliSocket()
simopintcli.connectClient()
simopintcli.receiveMessage()
simopintcli.sendMessage(f'Message Test {datetime.datetime.now()}')
simopintcli.sendMessage(f'Message Test {testdict}')
simopintcli.sendMessage(f'Message Test {jsondict}')
simopintcli.closeCliSocket()
