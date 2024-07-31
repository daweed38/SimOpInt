##################################################
# FarmerSoft Open Interface Client Test Script
##################################################
# Test Client Script
# FarmerSoft © 2024
# By Daweed
##################################################

# System Modules Import
# import sys
import logging
import datetime
import json
import time

# Standard Modules Import

# Sim Open Interface Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntClient import SimOpIntClient

testdict = {'command': {'name': {'args': {'arg1': True, 'arg2': False}}}}

jsondata = open('Config/data.json')
jsondict = dict(json.load(jsondata))
jsondata.close()

configdir = 'Config/Client'
configfile = 'configcli.json'
configtype = 'json'

logger = logging.getLogger('SimOpInt')
logfile = 'Logs/simopintclient.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
logger.addHandler(filehandler)

config = SimOpIntConfig(configdir, configfile, configtype)

srvname = config.getConfigParameter('SERVER', 'srvname')
srvaddr = config.getConfigParameter('SERVER', 'srvaddr')
srvport = config.getConfigParameter('SERVER', 'srvport')
cliname = config.getConfigParameter('CLIENT', 'cliname')

simopintcli = SimOpIntClient(cliname, srvname, srvaddr, srvport, logging.INFO)

simopintcli.openCliSocket()
simopintcli.connectClient()
simopintcli.receiveMessage()
simopintcli.sendMessage(f'Message Test {datetime.datetime.now()}')
simopintcli.sendMessage(f'Message Test {testdict}')
simopintcli.sendMessage(f'Message Test {jsondict}')
simopintcli.closeCliSocket()