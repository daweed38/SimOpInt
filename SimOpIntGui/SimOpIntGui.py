##################################################
# FarmerSoft Open Interface Qt Gui Class
##################################################
# Main Window Class SimOpIntGui
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import os
# import sys
import logging

#  PySide6 Module Import
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QAction
# from PySide6.QtGui import QIcon, QPixmap, QListWidgetItem

# SimOpInt Module Import

# SimOpIntGui Module Import
from SimOpIntGui.SimOpIntMgt import SimOpIntMgt

# SimOpIntUi Module Import
from SimOpIntUi.ui_SimOpIntGui import Ui_SimOpIntGui


class SimOpIntGui(QMainWindow, Ui_SimOpIntGui):

    ###################################
    # Class Description
    ###################################

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, debug: int = logging.WARNING) -> None:
        super().__init__()

        self.setupUi(self)

        # Debug Management
        self.debug = debug
        self.logger = logging.getLogger(__name__)

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        # Interface Management Class (With Ui)
        self.SimOpIntMgt = SimOpIntMgt(self, logging.DEBUG)

        # Menus Action Management #
        # File Menu
        self.actionQuit.triggered.connect(self.close)

        # Menu Configuration / Interface
        self.actionAdd.triggered.connect(self.SimOpIntMgt.openAddIntDialog)

        # Loading Interfaces from Config Directory
        self.loadMenuInterfaces()
        self.logger.debug(f'Loaded Interface : {self.SimOpIntMgt.getLoadedInterfaces()}')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Method
    ###################################

    def loadMenuInterfaces(self) -> None:
        self.logger.debug(f'loadMenuInterfaces method called')
        # for intname, intobject in self.SimOpIntMgt.getLoadedInterfaces().items():
        for name in self.SimOpIntMgt.getLoadedInterfaces():
            self.logger.debug(f'Adding {name} to interfaces Menu')
            intmenu = self.menuInterfaces.addMenu(f'{name}')
            intreloadaction = QAction(f'Reload', self)
            # intreloadaction.setData(intobject)
            # intreloadaction.triggered.connect(self.reloadInterfaceFromMenu)
            intreloadaction.triggered.connect(lambda intname=name: self.SimOpIntMgt.reloadInterface(name))
            inteditaction = QAction(f'Edit', self)
            # inteditaction.setData(intobject)
            # inteditaction.triggered.connect(self.reloadInterfaceFromMenu)
            inteditaction.triggered.connect(lambda intname=name: self.SimOpIntMgt.openEditIntDialog(name))
            intconnectaction = QAction(f'Connect', self)
            # intconnectaction.setData(intobject)
            # intconnectaction.triggered.connect(self.connectInterfaceFromMenu)
            intconnectaction.triggered.connect(lambda intname=name: self.SimOpIntMgt.connectInterface(name))
            intstartaction = QAction(f'Start', self)
            # intstartaction.setData(intobject)
            # intstartaction.triggered.connect(self.startInterfaceFromMenu)
            intstartaction.triggered.connect(lambda intname=name: self.SimOpIntMgt.startInterface(name))
            intstopaction = QAction(f'Stop', self)
            # intstopaction.setData(intobject)
            # intstopaction.triggered.connect(self.stopInterfaceFromMenu)
            intstopaction.triggered.connect(lambda intname=name: self.SimOpIntMgt.stopInterface(name))
            intmenu.addAction(intreloadaction)
            intmenu.addAction(inteditaction)
            intmenu.addSeparator()
            intmenu.addAction(intconnectaction)
            intmenu.addAction(intstartaction)
            intmenu.addAction(intstopaction)

    ###################################
    # Ui Methods
    ###################################