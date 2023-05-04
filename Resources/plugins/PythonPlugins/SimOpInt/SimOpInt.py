# Standard Import
import importlib

# FarmerSoft Modules Import
from SimOpIntTools import SimOpIntTools

###################################
# FarmerSoft Sim Open Interface
###################################
# SimOpInt Class
# FarmerSoft © 2023
# By Daweed
###################################


class SimOpInt:
    """
    This Class is the main interface structure class
    From this Class all object are available
    The SimOpInt object is created regarding the configuration files
    Debug Level are set as :
    Level 3 : SimOpInt General Debug Level
    Level 31 : SimOpInt Configuration Debug Level
    Level 32 : SimOpInt Devices Debug Level
    Level 33 : SimOpInt Module Debug Level
    Level 34 : SimOpInt Object Debug Level
    """

    ###############
    # Properties
    ###############

    ###############
    # Constructor
    ###############
    def __init__(self, configdir, configfile, debug=0):
        self.debug = int(debug)
        self.globaldebug = False
        self.configdir = configdir
        self.configfile = configfile
        self.dummy = False
        self.intname = ''
        self.cliname = ''
        self.cliaddr = ''
        self.cliport = ''
        self.srvname = ''
        self.srvaddr = ''
        self.srvport = 0
        
        self.config = {}
        self.modules = {}
        self.devices = {}
        self.objects = {}

        self.tools = SimOpIntTools(debug)

        if self.debug == 3:
            print("######################################################################")
            print("# Sim Open Interface initialization")
            print("######################################################################")
            print("\r")

        self.readConfig()

        if self.config:
            self.intname = self.config['INT']['intname']
            self.cliname = self.config['NETWORK']['cliname']
            self.cliaddr = self.config['NETWORK']['cliaddr']
            self.cliport = self.config['NETWORK']['cliport']
            self.srvname = self.config['NETWORK']['srvname']
            self.srvaddr = self.config['NETWORK']['srvaddr']
            self.srvport = self.config['NETWORK']['srvport']

            if int(self.getConfigOption('INT', 'dummydevice')):
                self.dummy = True

            if self.getConfig():

                if 'DEVICES' in self.config:
                    self.loadDevicesModule()
                    self.createDevices()

                if 'MODULES' in self.config:
                    self.loadModules()

                if 'OBJECTS' in self.config:
                    self.createObjects()

                if self.debug == 3:
                    print("######################################################################")
                    print("# Sim Open Interface {} initialized".format(self.intname))
                    print("######################################################################")
                    print("\r")

        else:
            if self.debug == 3:
                print("######################################################################")
                print("# Sim Open Interface {} initialisation error")
                print("######################################################################")
                print("\r")

    ###############
    # Destructor
    ###############
    def __del__(self):
        if self.debug == 3:
            print("######################################################################")
            print("# Sim Open Interface {} removed".format(self.intname))
            print("######################################################################")
            print("\r")

    ###################################
    # System Methods
    ###################################
    # getName()
    # return the interface name
    def getName(self):
        return self.intname

    def getCliName(self):
        return self.cliname

    def getCliAddr(self):
        return self.cliaddr

    def getCliPort(self):
        return self.cliport

    def getSrvName(self):
        return self.srvname

    def getSrvAddr(self):
        return self.srvaddr

    def getSrvPort(self):
        return self.srvport

    def getDebugLevel(self):
        return self.debug

    def setDebugLevel(self, debuglevel):
        if self.debug in [3, 31, 32, 33, 34]:
            print("##################################################")
            print("# Set Debug Level to {}".format(int(debuglevel)))
            print("##################################################")
            print("\r")

        self.debug = int(debuglevel)

    ###################################
    # Configuration Methods
    ###################################
    # getConfigFile()
    # return configuration file name
    def getConfigFile(self):
        return self.configfile

    def getConfigDir(self):
        return self.configdir

    def readConfig(self):
        self.config = self.tools.readJsonFile(self.configdir, self.configfile)

    # getConfig()
    # return Interface Configuration
    def getConfig(self):
        return self.config

    # getConfigSection(section)
    # return interface section config
    def getConfigSection(self, section):
        return self.config[section]

    # getOption(section, option)
    # return interface option config
    def getConfigOption(self, section, option):
        return self.config[section][option]

    ###################################
    # Devices Methods
    ###################################
    def listDevices(self):
        return self.devices

    def loadDevicesModule(self):
        if self.debug == 32:
            print("Loading Devices Modules .... ")
        for devicemod, modconf in self.getConfigOption('DEVICES', 'modules').items():

            mod = modconf['module']
            cls = modconf['class']

            if self.debug == 32:
                print("Key : {} Package : {} Class : {}".format(devicemod, mod, cls))

            self.modules[cls] = {}
            self.modules[cls]['class'] = cls
            self.modules[cls]['module'] = importlib.import_module(mod, cls)

        if self.debug == 32:
            print("\r")

    def getDevice(self, devicename):
        if devicename in self.devices:
            return self.devices[devicename]
        else:
            return False

    def createDevice(self, devicename, devicemod, deviceaddr):
        if self.debug == 32:
            print("Device : {} Device Addr : {} Module : {} Dummy Mode {}".format(devicename, deviceaddr, devicemod, self.dummy))
        self.devices[devicename] = self.getModule(devicemod)(devicename, deviceaddr, dummy=self.dummy)

    def createDevices(self):
        if self.debug == 32:
            print("Loading Devices ...")

        devices = self.tools.readJsonFile(self.configdir, 'devices.json')

        for devicename, deviceconf in devices.items():
            self.createDevice(deviceconf['devicename'], deviceconf['devicetype'], deviceconf['deviceaddr'])

        if self.debug == 32:
            print("\r")

    ###################################
    # Modules Methods
    ###################################
    def listLoadedModules(self):
        return self.modules

    def loadModule(self, module, cls):
        self.modules[cls] = {}
        self.modules[cls]['class'] = cls
        self.modules[cls]['module'] = importlib.import_module(module, cls)

    def loadModules(self):
        if self.debug == 33:
            print("Loading Modules ...")

        for mod, modconf in self.config['MODULES'].items():
            if self.debug == 33:
                print("Module {} : Lib {} Class {}".format(mod, modconf['module'], modconf['class']))
            self.loadModule(modconf['module'], modconf['class'])

        if self.debug == 33:
            print("\r")

    def getModule(self, modulename):
        return getattr(self.modules[modulename]['module'], self.modules[modulename]['class'])

    ###################################
    # Objects Methods
    ###################################
    def listObjects(self):
        return self.objects

    def listExportedObjects(self):
        expobjects = {}
        for objtype in self.listObjects():
            if self.getObjectConfOfType(objtype)['export'] == 'yes':
                expobjects[objtype] = {}
                for objname, obj in self.getObjectOfType(objtype).items():
                    if obj.getExpStatus():
                        expobjects[objtype][objname] = obj

        return expobjects

    def listImportedObjects(self):
        impobjects = {}
        for objtype in self.listObjects():
            if self.getObjectConfOfType(objtype)['import'] == 'yes':
                impobjects[objtype] = {}
                for objname, obj in self.getObjectOfType(objtype).items():
                    impobjects[objtype][objname] = obj

        return impobjects

    def getObject(self, objecttype, objectname):
        if objecttype in self.objects:
            if objectname in self.objects[objecttype]['OBJECTS']:
                return self.objects[objecttype]['OBJECTS'][objectname]
            else:
                return False
        else:
            return False

    def getObjectConfOfType(self, objecttype):
        return self.objects[objecttype]['CONF']

    def getObjectOfType(self, objecttype):
        return self.objects[objecttype]['OBJECTS']

    def createObject(self, objmodule, objtype, objname, args):
        module = self.getModule(objmodule)

        if self.debug == 34:
            print("Creating Object {} {} with Args {} from Module {}".format(objmodule, objname, args, module))
            print("\r")

        # self.objects[objtype]['OBJECTS'][objname] = module(*args)
        self.objects[objtype]['OBJECTS'][args[0]] = module(*args)

    def createObjectOfType(self, objtype, objfile):
        if self.debug == 34:
            print("Reading {} configuration for Object Type {}".format(objfile, objtype))

        self.objects[objtype] = {}

        objects = self.tools.readJsonFile(self.configdir, objfile)

        if self.debug == 34:
            print("Objects Type {} Data : {}".format(objtype, objects))

        self.objects[objtype]['CONF'] = objects['CONF']
        self.objects[objtype]['OBJECTS'] = {}

        propkeys = sorted(objects['PROPERTIES'].keys())

        if self.debug == 34:
            print("Properties Keys : {}".format(propkeys))

        for objname, objdata in objects['OBJECTS'].items():
            if self.debug == 34:
                print("Object {} [{}] : Config : {}".format(objname, objtype, objdata))

            args = []
            for prop in propkeys:
                propname = objects['PROPERTIES'][prop]
                propvalue = objdata[propname]

                if self.debug == 34:
                    print("Prop {} Value {}".format(propname, propvalue))

                if propname == 'device':
                    propvalue = self.getDevice(propvalue)

                if propname == 'node':
                    if propvalue == 'None':
                        propvalue = None

                if propname == 'nodetype':
                    if propvalue == 'None':
                        propvalue = None

                if propname == 'nodeconds':
                    if propvalue == 'None':
                        propvalue = None

                if propname == 'exported':
                    if propvalue == 'True':
                        propvalue = True
                    else:
                        propvalue = False

                args.append(propvalue)

            if self.debug == 34:
                print("Args : {}".format(args))

            objmodule = objects['CONF']['module']

            self.createObject(objmodule, objtype, objname, args)

    def createObjects(self):
        if self.debug == 34:
            print("Creating Objects ...")
        for objecttype, objecttypefile in self.getConfigSection('OBJECTS').items():
            self.createObjectOfType(objecttype, objecttypefile)

    ###################################
    # Data Methods
    ###################################
