# Standard Import
import time
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
        self.name = ''
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
                print("# Sim Open Interface {} initialized".format(self.name))
                print("######################################################################")
                print("\r")

    ###############
    # Destructor
    ###############
    def __del__(self):
        if self.debug == 3:
            print("######################################################################")
            print("# Sim Open Interface {} removed".format(self.name))
            print("######################################################################")
            print("\r")

    ###################################
    # System Methods
    ###################################
    # getName()
    # return the interface name
    def getName(self):
        return self.name

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
    # Data Methods
    ###################################

    # Method createNodeConds(nodeconds)
    # Return a formatted Dict Condition
    def createNodeConds(self, conditions):
        nodeconds = {}
        for nodecond in conditions.split(':'):
            nodeconds[nodecond.split(',')[0]] = {}
            nodeconds[nodecond.split(',')[0]]['node'] = nodecond.split(',')[1]
            nodeconds[nodecond.split(',')[0]]['noderefid'] = None

        return nodeconds

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
        self.config = self.tools.readConfigFile(self.configdir, self.configfile)
        if self.config:
            self.name = self.config['INT']['intname']
        else:
            print("##################################################")
            print("# Error reading Configuration file {}".format(self.getConfigFile()))
            print("##################################################")
            print("\r")

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
        for key, value in self.config['DEVICES'].items():
            # if int(self.getConfigOption('INT', 'dummydevice')) == 1:
            #     lib = 'DeviceDummy'
            #     package = 'Dummy'
            # else:
            #     lib = value.split(',')[0]
            #     package = value.split(',')[1]

            lib = value.split(',')[0]
            package = value.split(',')[1]

            if self.debug == 32:
                print("Device Type {} Lib {} Package {}".format(value.split(',')[1], lib, package))

            self.modules[value.split(',')[1]] = {}
            self.modules[value.split(',')[1]]['module'] = importlib.import_module(lib, package)
            self.modules[value.split(',')[1]]['package'] = package

        if self.debug == 32:
            print("\r")

    def getDevice(self, devicename):
        if devicename in self.devices:
            return self.devices[devicename]
        else:
            return False

    def createDevice(self, devicemod, devicename, deviceaddr):
        if self.debug == 32:
            print("Device : {} Device Addr : {} Module : {} Dummy Mode {}".format(devicename, deviceaddr, devicemod, self.dummy))
        self.devices[devicename] = self.getModule(devicemod)(devicename, deviceaddr, dummy=self.dummy)

    def createDevices(self):
        if self.debug == 32:
            print("Loading Devices ...")

        devices = self.tools.readConfigFile(self.configdir, 'devices.cfg')

        for devicename, deviceconf in devices.items():
            self.createDevice(deviceconf['devicetype'], deviceconf['devicename'], deviceconf['deviceaddr'])

        if self.debug == 32:
            print("\r")

    ###################################
    # Modules Methods
    ###################################
    def listLoadedModules(self):
        return self.modules

    def loadModule(self, module, package):
        self.modules[package] = {}
        self.modules[package]['module'] = importlib.import_module(module, package)
        self.modules[package]['package'] = package

    def loadModules(self):
        if self.debug == 33:
            print("Loading Modules ...")
        for key, value in self.config['MODULES'].items():
            package = value.split(',')[1]
            module = value.split(',')[0]
            if self.debug == 33:
                print("Module {} : Lib {} Class {}".format(key, module, package))
            self.loadModule(module, package)

        if self.debug == 33:
            print("\r")

    def getModule(self, modulename):
        return getattr(self.modules[modulename]['module'], self.modules[modulename]['package'])

    ###################################
    # Objects Methods
    ###################################
    def listObjects(self):
        return self.objects

    def listExportedObjects(self):
        expobject = {}
        for objtype in self.listObjects():
            if self.getObjectConfOfType(objtype)['export'] == 'yes':
                expobject[objtype] = {}
                for objname, obj in self.getObjectOfType(objtype).items():
                    expobject[objtype][objname] = obj

        return expobject

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

    def createObject(self, objectmodule, objecttype, objectname, args):
        if self.debug == 34:
            print("Creating Object {} {} with Args {}".format(objectmodule, objectname, args))
            print("\r")

        module = self.getModule(objectmodule)

        self.objects[objecttype]['OBJECTS'][objectname] = module(*args)

        if self.debug == 34:
            print(module)

    def createObjectOfType(self, objecttype, objectsfile):
        if self.debug == 34:
            print("Reading {} configuration for Object Type {}".format(objectsfile, objecttype))
            print("\r")

        self.objects[objecttype] = {}
        objects = self.tools.readConfigFile(self.configdir, objectsfile)
        objectsconf = {confsection: confdata for confsection, confdata in objects.items() if confsection in ['CONF', 'PROPERTIES']}

        if self.debug == 34:
            for objectsconfsection, objectsconfdata in objectsconf.items():
                print("Object Type {} Conf Section {} : {}".format(objecttype, objectsconfsection, objectsconfdata))
            print("\r")

        self.objects[objecttype]['CONF'] = objectsconf['CONF']
        self.objects[objecttype]['OBJECTS'] = {}

        objectsdata = {confsection: confdata for confsection, confdata in objects.items() if confsection not in ['CONF', 'PROPERTIES']}

        for objectname, objectdata in objectsdata.items():
            if self.debug == 34:
                print("Object {} : {}".format(objectname, objectdata))

            propskey = sorted(objectsconf['PROPERTIES'].keys())

            args = []
            for prop in propskey:
                propname = objectsconf['PROPERTIES'][prop]
                propvalue = objectdata[propname]

                if self.debug == 34:
                    print("Prop {} Value {}".format(propname, propvalue))

                if propname == 'device':
                    propvalue = self.getDevice(propvalue)

                if propname == 'node':
                    if propvalue == 'None':
                        propvalue = None

                if propname == 'nodecond':
                    if propvalue != 'None':
                        propvalue = self.createNodeConds(propvalue)
                    else:
                        propvalue = None

                args.append(propvalue)

            objectmodule = objectsconf['CONF']['module']

            self.createObject(objectmodule, objecttype, objectname, args)

    def createObjects(self):
        if self.debug == 34:
            print("Creating Objects ...")
            print("\r")
        for objecttype, objecttypefile in self.getConfigSection('OBJECTS').items():
            self.createObjectOfType(objecttype, objecttypefile)

        if self.debug == 34:
            print("\r")
