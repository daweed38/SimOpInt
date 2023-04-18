##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Base Class REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################

class ObjBase:
    """
    SimOpInt Object Base Class
    Copyright FarmerSoft © 2023
    By Daweed
    """

    ########################################
    # Properties
    ########################################

    ########################################
    # Constructor
    ########################################

    def __init__(self, name: str, node: str, nodetype: str, nodeformat: str, nodeconds: dict, debug=False) -> None:
        # ----- standard properties -----
        self.debug = debug
        self.objtype = 'Base'
        self.name = name
        self.node = node
        self.nodetype = nodetype
        self.noderef = None
        self.nodeformat = nodeformat
        self.nodeconds = nodeconds

        if self.debug:
            print("######################################################################")
            print("# {} Object {} creation".format(self.objtype, self.name))
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

    # Method getDebugLevel()
    # Return Debug Mode Status
    def getDebugLevel(self) -> bool:
        return self.debug

    # Method setDebugLevel(status)
    # Setup or Remove Debug Mode
    # status is bool
    def setDebugLevel(self, status: bool) -> None:
        self.debug = status

    # Method getName()
    # Return Object Name
    def getName(self) -> str:
        return self.name

    # Method setName(name)
    # Set Object Name to name
    # name is str
    def setName(self, name: str) -> None:
        self.name = name

    # Method getNode()
    # Return Object Node
    def getNode(self) -> str:
        return self.node

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
    def getNodeConds(self) -> dict:
        return self.nodeconds

    # Method getNodeCond(nodecond)
    # Return Object Condition for Node nodecond
    # nodecond is str
    def getNodeCond(self, nodecond: str) -> str:
        return self.nodeconds[nodecond]['node']

    # Method getNodeCondType()
    # Return Object Condition Type for Node nodecond
    # nodecond is str
    def getNodeCondType(self, nodecond: str) -> str:
        return self.nodeconds[nodecond]['nodetype']

    # Method getNodeCondRef(nodecond)
    # Return X-Plane Node RefID Condition for nodecond
    # nodecond is str
    def getNodeCondRef(self, nodecond: str) -> object:
        return self.nodeconds[nodecond]['noderefid']

    # Method setNodeCondRef(nodecond, noderefid)
    # Set X-Plane Node RefID Condition to noderefid for nodecond
    # nodecond is str and noderefid is an X-Plane DataRef Object
    def setNodeCondRef(self, nodecond: str, noderefid) -> None:
        self.nodeconds[nodecond]['noderefid'] = noderefid

    ########################################
    # Object Status & Value
    ########################################

    ########################################
    # Object Methods
    ########################################
