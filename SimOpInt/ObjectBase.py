##################################################
# FarmerSoft Sim Open Interface Object Class
##################################################
# Base Object Class REV 5.0
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging


class ObjectBase:

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return f'This is the Sim Open Interface Object Base Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, name: str, node: str | dict, nodetype: str, nodeformat: str, nodeconds: dict, export: bool = False, command: bool = False, debug: int = 30) -> None:
        # ----- standard properties -----
        self.objtype = 'Base'
        self.objname = name
        self.node = node
        self.nodetype = nodetype
        self.noderef = None
        self.nodeformat = nodeformat
        self.nodeconds = nodeconds
        self.export = export
        self.command = command
        self.debug = debug

        self.logger = logging.getLogger(__name__)
        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Methods
    ###################################

    # Method getName()
    # Return Object Name
    def getName(self) -> str:
        return self.objname

    # Method setName(name)
    # name is str
    # Set Object Name to name
    def setName(self, name: str) -> None:
        self.objname = name

    # Method setNode(node)
    # Set Object Node to node
    # node is str
    def setNode(self, node: str) -> None:
        self.node = node

    # Method getNodeType()
    # Return Object Node Type
    def getNodeType(self) -> str:
        return self.nodetype

    # Method setNodeType(nodetype)
    # Set Object Node Type to nodetype
    # nodetype is str
    def setNodeType(self, nodetype: str) -> None:
        self.nodetype = nodetype

    # Method getNodeRef()
    # Return X-Plane Node Reference
    def getNodeRef(self) -> object:
        return self.noderef

    # Method setNodeRef(noderef)
    # Set X-Plane Node Reference to noderef
    # noderef is an X-Plane DataRef Object
    def setNodeRef(self, noderef) -> None:
        self.noderef = noderef

    # Method getNodeFormat()
    # Return Node Format
    # Used when Getting or Setting DataType Data [32]
    def getNodeFormat(self) -> str:
        return self.nodeformat

    # Method setNodeFormat(nodeformat)
    # Set the Node Format to nodeformat
    # Used when Getting or Setting DataType Data [32]
    # nodeformat is str
    def setNodeFormat(self, nodeformat: str) -> None:
        self.nodeformat = nodeformat

    # Method getNodeConds()
    # Return Object Conditions Dict
    def getNodeConds(self) -> dict | bool:
        return self.nodeconds

    # Method getNodeCond(nodecond)
    # nodecond is str
    # Return Object Condition for Node nodecond
    def getNodeCond(self, nodecond: str) -> str:
        return self.nodeconds[nodecond]['node']

    # Method getNodeCondType()
    # nodecond is str
    # Return Object Condition Type for Node nodecond
    def getNodeCondType(self, nodecond: str) -> str:
        return self.nodeconds[nodecond]['nodetype']

    # Method getNodeCondRef(nodecond)
    # nodecond is str
    # Return X-Plane Node RefID Condition for nodecond
    def getNodeCondRef(self, nodecond: str) -> object:
        return self.nodeconds[nodecond]['noderefid']

    # Method setNodeCondRef(nodecond, noderefid)
    # Set X-Plane Node RefID Condition to noderefid for nodecond
    # nodecond is str and noderefid is an X-Plane DataRef Object
    def setNodeCondRef(self, nodecond: str, noderefid) -> None:
        self.nodeconds[nodecond]['noderefid'] = noderefid

    # Method getIsOutputStatus()
    # Return Object Export Status
    def getIsOutputStatus(self) -> bool:
        return self.export

    # Method setIsOutputStatus(exportstatus)
    # status is bool
    # Set Object Export Status
    def setIsOutputStatus(self, exportstatus: bool) -> None:
        self.export = exportstatus

    # Method getIsCommandStatus()
    # Return Object Export Status
    def getIsCommandStatus(self) -> bool:
        return self.command

    # Method setIsCommandStatus(cmdstatus)
    # status is bool
    # Set Object Export Status
    def setIsCommandStatus(self, cmdstatus: bool) -> None:
        self.command = cmdstatus
