##################################################
# FarmerSoft Open Interface Client Test Script
##################################################
# Test Client Script
# FarmerSoft © 2024
# By Daweed
##################################################

# System Modules Import
import logging
import threading
import time

# Standard Modules Import
import json

# Sim Open Interface Import
# from SimOpInt.SimOpIntConfig import SimOpIntConfig
from SimOpInt.SimOpIntClient import SimOpIntClient

testdict = {'type': 'cmd', 'name': 'read', 'args': {'object': 'config', 'filter': 'simopintd'}}

jsondata = open('Config/Client/data.json')
jsondict = dict(json.load(jsondata))
jsondata.close()

configdir = 'Config/Client'
configfile = 'configcli.json'
# configtype = 'json'

clientrun = True

logger = logging.getLogger('SimOpInt')
logfile = 'Logs/simopint.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
logger.addHandler(filehandler)

simopintsrv_logger = logging.getLogger('SimOpInt.SimOpIntClient')
logfile = 'Logs/simopintcli.log'
filehandler = logging.FileHandler(filename=logfile, mode='w')
fileformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
filehandler.setFormatter(fileformat)
simopintsrv_logger.addHandler(filehandler)
simopintsrv_logger.propagate = False

# config = SimOpIntConfig(configdir, configfile, configtype)
# config = SimOpIntConfig(configdir, configfile)
# srvname = config.getConfigParameter('SERVER', 'srvname')
# srvaddr = config.getConfigParameter('SERVER', 'srvaddr')
# srvport = config.getConfigParameter('SERVER', 'srvport')
# cliname = config.getConfigParameter('CLIENT', 'cliname')

# SimOpInt Client Creation
# simopintcli = SimOpIntClient(cliname, srvname, srvaddr, srvport, logging.INFO)
simopintcli = SimOpIntClient(logging.INFO)

# simopintcli.openCliSocket()
# simopintcli.connectClient()
# simopintcli.receiveMessage()
# simopintcli.sendMessage(f'Message Test {datetime.datetime.now()}')
# simopintcli.sendMessage(f'Message Test {testdict}')
# simopintcli.sendMessage(f'Message Test {jsondict}')
# simopintcli.sendMessage(testdict)
# simopintcli.closeCliSocket()

# SimOpInt Daemon loop thread creation
simopint_thread = threading.Thread(target=simopintcli.mainLoop)
simopint_thread.start()

# Waiting for Opened Socket
while simopintcli.getCliStatus() != 1:
    time.sleep(1)

# Starting SimOpInt Daemon Loop
simopintcli.startCliLoop()
