##################################################
# FarmerSoft Open Interface Qt Gui Class
##################################################
# Main Window Class
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
# import sys
import logging

#  PySide6 Module Import
from PySide6.QtWidgets import QMainWindow, QTreeWidgetItem
from PySide6.QtGui import QIcon, QPixmap

# SimOpInt Module Import
from SimOpInt.SimOpIntConfig import SimOpIntConfig

# SimOpIntConfig Module Import
from SimOpIntConfig.InterfaceMngtDialog import InterfaceMngtDialog

# SimOpIntUi Module Import
from SimOpIntUi.ui_MainWindowGui import Ui_MainWindowGui


class MainWindowGui(QMainWindow, Ui_MainWindowGui):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return 'This the main Sim Open Interface Configuration Window Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, debug: int = logging.WARNING) -> None:
        super().__init__()

        self.setupUi(self)

        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.branchesloaded = False

        # Interface Management Dialog Ui creation
        self.InterfaceMngtDialog = InterfaceMngtDialog(self, logging.DEBUG)

        # File Menu Management
        self.actionQuit.triggered.connect(self.close)

        # Settings Menu Management
        self.actionInterfaceManagement.triggered.connect(self.InterfaceMngtDialog.showInterfaceMngtDialog)

        # Interfaces List Management
        self.interfacesList.currentIndexChanged.connect(self.loadSelectedInterface)
        self.configBranch = SimOpIntConfig('Config/Gui', 'branches.json', 'JSON')
        self.loadObjectBranch()

        # Interface Connexion Button
        self.connectBtn.clicked.connect(self.connectInterface)
        self.logger.debug(f'Sim Open Interface Main Config Gui initialized')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Method
    ###################################

    ###################################
    # Ui Methods
    ###################################

    # Tree Branch Loading & Creation
    def loadObjectBranch(self) -> None:
        self.logger.debug(f'Config Branch : {self.configBranch.getConfig()}')
        self.objectsTree.clear()
        branchconfig = self.configBranch.getConfig()
        for branch in branchconfig:
            item = QTreeWidgetItem(self.objectsTree, 1)
            item.setText(0, branchconfig[branch]['name'])
            icon = QIcon(QPixmap(":/imgs/"+branchconfig[branch]['icon']))
            item.setIcon(0, icon)
            item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)
        if self.interfacesList.count() > 0:
            self.loadSelectedInterface(0)

    # Load Selected Interface in the InterfaceTree
    def loadSelectedInterface(self, index):
        if self.interfacesList.count() > 0:
            intname = self.interfacesList.currentText()
            interface = self.InterfaceMngtDialog.interfaces[intname]['interface']
            self.logger.debug(f'Interface selected : {index} {intname} {interface.getAddr()} {interface.getPort()}')
            self.hostValue.setText(str(interface.getAddr()))
            self.portValue.setText(str(interface.getPort()))
        else:
            self.hostValue.clear()
            self.portValue.clear()

    def connectInterface(self):
        intname = self.interfacesList.currentText()
        interface = self.InterfaceMngtDialog.getInterface(intname)
        self.logger.debug(f'Connecting to Interface {interface.getName()} at {self.hostValue.text()} on port {self.portValue.text()}')
