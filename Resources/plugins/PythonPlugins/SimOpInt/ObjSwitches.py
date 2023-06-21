# System Modules Import
from datetime import datetime
# Device Base Import
from ObjBase import ObjBase
# MCP23017 Import
from DeviceMCP23017 import MCP23017

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Switch Class REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class Switch(ObjBase):
    """
    This class allow Simple Switch management (Off / On)
    based on hardware driver MCP23017
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: str, values: str, valuestype: str, output: bool = False, command: bool = False, debug: bool = False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)
        # ----- Object properties -----
        self.objtype = 'Switch'
        self.device = device
        self.port = str(port)
        self.pin = int(pin)
        self.values = values
        self.valuestype = valuestype

        if self.debug:
            print("######################################################################")
            print("{} Object {} creation".format(self.objtype, self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # Destructor
    ########################################

    def __del__(self) -> None:
        if self.debug:
            print("######################################################################")
            print("# {} Object {} removed".format(self.objtype, self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # System Methods
    ########################################

    def getTypedData(self, data) -> int | str | bool:
        if self.valuestype == 'string':
            return str(data)
        elif self.valuestype == 'int':
            return int(data)
        elif self.valuestype == 'bool':
            return bool(data)
        else:
            return data

    def getValueType(self) -> str:
        return self.valuestype

    ########################################
    # Object Status & Value
    ########################################

    # Method getInputState()
    # Return Switch GPIO Pin Status
    def getSwitchState(self) -> int | str | bool:
        if self.device.readGpioPin(self.port, self.pin) == 1:
            return self.values[1]
        else:
            return self.values[0]

    ########################################
    # Object Methods
    ########################################

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Switch Class REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class DoubleSwitch(ObjBase):
    """
    This class allow Double Switch management (On / Off / On)
    based on hardware driver MCP23017
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin1: str, pin2: str, values: str, valuestype: str, output: bool = False, command: bool = False, debug: bool = False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)
        # ----- Object properties -----
        self.objtype = 'Double Switch'
        self.device = device
        self.port = str(port)
        self.pin1 = int(pin1)
        self.pin2 = int(pin2)
        self.values = values
        self.valuestype = valuestype
        self.state = ''
        self.noderef = {}

        if self.debug:
            print("######################################################################")
            print("{} Object {} creation".format(self.objtype, self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # Destructor
    ########################################

    def __del__(self) -> None:
        if self.debug:
            print("######################################################################")
            print("# {} Object {} removed".format(self.objtype, self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # System Methods
    ########################################

    def getTypedData(self, data) -> int | str | bool:
        if self.valuestype == 'string':
            return str(data)
        elif self.valuestype == 'int':
            return int(data)
        elif self.valuestype == 'bool':
            return bool(data)
        else:
            return data

    def getValueType(self) -> str:
        return self.valuestype

    ########################################
    # Object Status & Value
    ########################################

    def getSwitchState(self):
        return self.state

    def readSwitch(self) -> int | str | bool | None:
        if self.device.readGpioPin(self.port, self.pin1) == 1:
            status = self.values[0]
        elif self.device.readGpioPin(self.port, self.pin2) == 1:
            status = self.values[2]
        else:
            status = self.values[1]

        if self.debug:
            print(f"Pin 1 {self.device.readGpioPin(self.port, self.pin1)} Pin2 {self.device.readGpioPin(self.port, self.pin2)} Status {status}")

        if status != self.state:
            self.state = status
            return self.state
        else:
            return None

    ########################################
    # Object Methods
    ########################################

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Switch Class REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class RotarySwitch(ObjBase):
    """
    This class allow Rotary Switch management (N position)
    based on hardware driver MCP23017
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pins: str, values: str, valuestype: str, bincode: str, output: bool = False, command: bool = False, debug: bool = False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)
        # ----- Object properties -----
        self.objtype = 'Rotary Switch'
        self.device = device
        self.port = str(port)
        self.pins = {}
        self.values = values
        self.valuestype = valuestype
        self.bincode = bincode
        self.swstate = None
        self.position = 0
        self.direction = None

        self.createPins(pins)

        # self.getSwitchState()

        if self.debug:
            print("######################################################################")
            print("{} Object {} creation".format(self.objtype, self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # Destructor
    ########################################

    def __del__(self) -> None:
        if self.debug:
            print("######################################################################")
            print("# {} Object {} removed".format(self.objtype, self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # System Methods Override
    ########################################

    # Method getAllNodes()
    # Return Nodes Dictionary
    def getAllNodes(self) -> dict:
        return self.node

    # Method getNode(direction)
    # Return Object Node
    def getNode(self, direction: str) -> str:
        return self.node[direction]

    # Method setNode(direction, node)
    # Set Object Node to node
    # node is str
    def setNode(self, node: str, direction: str) -> None:
        self.node[direction] = node

    # Method getNodeRef(direction)
    # Return X-Plane Node Reference
    def getNodeRef(self, direction: str) -> object:
        return self.noderef[direction]

    # Method setNodeRef(direction, noderef)
    # Set X-Plane Node Reference to noderef
    # noderef is an X-Plane DataRef Object
    def setNodeRef(self, noderef, direction: str) -> None:
        self.noderef[direction] = noderef

    ########################################
    # Data Methods
    ########################################

    def getTypedData(self, data) -> int | str | bool:
        if self.valuestype == 'string':
            return str(data)
        elif self.valuestype == 'int':
            return int(data)
        elif self.valuestype == 'bool':
            return bool(data)
        else:
            return data

    def getValueType(self) -> str:
        return self.valuestype

    ########################################
    # Object Status & Value
    ########################################

    def getSwitchState(self) -> str | int | tuple | None:
        for i in range(0, len(self.pins)):
            port = self.pins[i]['port']
            pin = self.pins[i]['pin']
            if self.device.readGpioPin(port, pin) == 1:
                self.swstate = self.values[i]
                if self.getNodeType() == 'cmd':
                    if i > self.position:
                        self.direction = 'right'
                        self.position = i
                    elif i < self.position:
                        self.direction = 'left'
                        self.position = i
                    else:
                        self.direction = None
                else:
                    if self.position != i:
                        self.swstate = self.values[i]
                        self.position = i
                    else:
                        self.swstate = None

        """
        if (self.bincode == 1):
            #print("Reading Rotary Binary Code Switches")
            if len(self.pinA) > 0:
                #print("Reading Port A")
                #print(bin(self.device.getRegister('gpioa')))
                #print(bin(self.device.getRegister('gpioa') & self.maskA))
                swportAval = self.device.getRegister('gpioa') & self.maskA
                if swportBval > 0:
                    #print("Switch Value != 0 : {} | {}".format(bin(swportAval), self.pinA[0]['pin']))
                    strmask = int(self.pinA[0]['pin']) - 1
                    idxval = int(bin(swportAval)[:-strmask], 2)
                else:
                    #print("Switch Value = 0 :{}".format(bin(swportAval)))
                    idxval = 0
            elif len(self.pinB) > 0:
                #print("Reading Port B")
                #print(bin(self.device.getRegister('gpiob')))
                #print(bin(self.device.getRegister('gpiob') & self.maskB))
                swportBval = self.device.getRegister('gpiob') & self.maskB
                if swportBval > 0:
                    #print("Switch Value != 0 : {} | {}".format(bin(swportBval), self.pinB[0]['pin']))
                    strmask = int(self.pinB[0]['pin']) - 1
                    idxval = int(bin(swportBval)[:-strmask], 2)
                else:
                    #print("Switch Value = 0 :{}".format(bin(swportBval)))
                    idxval = 0
            #print("Index Value : {} Len Value : {}".format(idxval, len(self.values)))
            #print(self.values[idxval])
            if (idxval <= (len(self.values) - 1)):
               self.swstate = self.values[idxval]
        else:
            for i in range(0, self.nbpos):
                port = self.pins[i]['port']
                pin = int(self.pins[i]['pin'])
                if self.device.getPin(port, pin) == 1:
                    self.swstate = self.values[i]
        #print(self.swstate)
        """

        if self.getNodeType() == 'cmd':
            if self.direction is not None:
                return self.swstate, self.direction
            else:
                return None
        elif self.getNodeType() == 'dref':
            return self.swstate
        else:
            return None

    def getCurrentPosition(self):
        return self.position

    def getDirection(self):
        return self.direction

    ########################################
    # Object Methods
    ########################################

    def createPins(self, pins) -> None:
        for pin in range(len(pins)):
            pininfos = pins[pin]
            self.pins[pin] = {}
            self.pins[pin]['port'] = pininfos[0]
            self.pins[pin]['pin'] = int(pininfos[1])

    def getPins(self) -> dict:
        return self.pins

    def getPin(self, pin) -> dict:
        return self.pins[pin]

    def getPinPort(self, pin) -> str:
        return self.pins[pin]['port']

    def getPinInput(self, pin) -> int:
        return self.pins[pin]['input']

##################################################
# FarmerSoft Sim Open Interface
##################################################
# PushButtonSwitch Class (Push Button) REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class PushButtonSwitch(ObjBase):
    """
    This class allow Simple Push Button management
    based on hardware driver MCP23017
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin: str, values: dict, valuestype: str, output: bool = False, command: bool = False, debug: bool = False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, output, command, debug)
        self.objtype = 'Push Button'
        self.device = device
        self.port = str(port)
        self.pin = int(pin)
        self.values = values
        self.valuestype = valuestype
        self.timestamp = datetime.now()
        self.bouncetime = 250
        self.status = 0
        self.value = 0

        """
        self.swstate = initstate
        self.swstate = self.getTypedData(initstate)
        """

        if self.debug:
            print("######################################################################")
            print("# Create Push Button Switch {} On Port {} On Device {}".format(self.name, self.port, self.device.getName()))
            print("######################################################################")
            print("\r")

    ########################################
    # Destructor
    ########################################

    def __del__(self) -> None:
        if self.debug:
            print("######################################################################")
            print("# ush Button Switch {} Removed".format(self.name))
            print("######################################################################")
            print("\r")

    ########################################
    # System Methods
    ########################################

    def getTypedData(self, data) -> int | str | bool:
        if self.valuestype == 'string':
            return str(data)
        elif self.valuestype == 'int':
            return int(data)
        elif self.valuestype == 'bool':
            return bool(data)
        else:
            return data

    def getValueType(self) -> str:
        return self.valuestype

    ########################################
    # Object Status & Value
    ########################################

    def getValue(self) -> int | str:
        return self.value

    def setValue(self, value: int | str) -> None:
        self.value = value

    def getStatus(self) -> int | str:
        return self.status

    def setStatus(self, status: int | str) -> None:
        self.status = status

    ########################################
    # Object Methods
    ########################################

    def getBounceTime(self):
        return self.bouncetime

    def setBounceTime(self, bouncetime):
        self.bouncetime = bouncetime

    def getTimeStamp(self):
        return self.timestamp

    def setTimeStamp(self):
        self.timestamp = datetime.now()

    def getMillis(self) -> float:
        dt = datetime.now() - self.timestamp
        ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
        return ms

    # Method getSwitchState()
    # Return Switch GPIO Pin Status
    def getInputState(self) -> int | bool:
        return self.device.readGpioPin(self.port, self.pin)

    def getSwitchState(self):
        if self.getMillis() > self.getBounceTime() and self.getInputState() == 1:
            self.setTimeStamp()
            return self.values['pushed']
        else:
            return self.values['released']
