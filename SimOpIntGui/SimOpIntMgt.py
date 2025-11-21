##################################################
# FarmerSoft Open Interface Management Class
##################################################
# SimOpIntMgt Class
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging
import os.path

# Pyside6 Module Import
from PySide6.QtCore import Slot
# from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog
# from PySide6.QtWidgets import QDialog, QMenu
# from PySide6.QtGui import QAction

# SimOpInt Module Import
from SimOpInt.SimOpInt import SimOpInt
# from SimOpInt.SimOpIntConfig import SimOpIntConfig

# SimOpIntGui Module Import
from SimOpIntGui.UiStaticFunc import *
from SimOpIntGui.AddIntDialog import AddIntDialog
from SimOpIntGui.EditIntDialog import EditIntDialog


class SimOpIntMgt(QDialog):

    ###################################
    # Class Description
    ###################################

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, parent, debug: int = logging.WARNING) -> None:
        super().__init__(parent)

        # Debug Management
        self.debug = debug
        self.logger = logging.getLogger(__name__)

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.intconfigdir = 'Config/Interfaces'
        self.interfaces = {}

        self.loadInterfaces()

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Method
    ###################################

    # Return Interface Config Directory
    def getIntConfigDir(self):
        return self.intconfigdir

    ###################################
    # Interfaces Method
    ###################################

    # Load Interfaces found in configuration directory
    def loadInterfaces(self) -> None:
        for intname in os.listdir(self.intconfigdir):
            self.logger.debug(f'Found directory {intname} in {self.intconfigdir}')
            self.logger.debug(f'Checking if interface configuration {intname}.json file exist in {self.intconfigdir}/{intname}')
            if os.path.isfile(f'{self.intconfigdir}/{intname}/{intname}.json'):
                self.logger.debug(f'Interface {intname} configuration file found')
                self.createInterface(f'{intname}')
            else:
                self.logger.debug(f'Interface {intname} configuration file not found')

    # Return loaded interface(s) dictionary
    # getLoadedInterfaces()
    def getLoadedInterfaces(self) -> dict:
        return self.interfaces

    # Return interface <intname> from self.interfaces dictionary
    # getInterface(intname)
    # intname is the interface name (str) that should exist in self.interfaces
    def getInterface(self, intname: str) -> SimOpInt:
        return self.interfaces[intname]

    # Add interface <intname> in self.interfaces
    # intname is a string defining the interface name
    # intdata is a dictionary which contain interface definition
    def addInterface(self, intname: str, intdata: dict) -> None:
        self.interfaces[intname] = intdata

    # Load Interface <intname> from configuration files
    # reloadInterface(intname)
    # intname is the interface name (str) that should exist in self.interfaces
    @Slot(str)
    def reloadInterface(self, intname) -> None:
        self.logger.debug(f'Load interface {intname}')

    # Create SimOpInt interface <intname> from configuration files
    # intname is the interface name (str) and configuration directory & json configuration files should exist in
    # interfaces configuration directory
    def createInterface(self, intname: str) -> None:
        self.interfaces[intname] = SimOpInt(f'{self.getIntConfigDir()}/{intname}', f'{intname}.json')

    # Edit Interface <intname> from in self.interfaces
    # editInterface(intname)
    # intname is the interface name (str) that should exist in self.interfaces
    def editInterface(self, intname) -> None:
        self.logger.debug(f'Edit interface {intname}')

    # Connect to Interface <intname>
    # connectInterface(intname)
    # intname is the interface name (str) that should exist in self.interfaces
    def connectInterface(self, intname):
        self.logger.debug(f'Connect interface {intname}')

    # Start Interface <intname>
    # startInterface(intname)
    # intname is the interface name (str) that should exist in self.interfaces
    def startInterface(self, intname) -> None:
        self.logger.debug(f'Starting interface {intname}')

    # Stop Interface <intname>
    # stopInterface(intname)
    # intname is the interface name (str) that should exist in self.interfaces
    def stopInterface(self, intname) -> None:
        self.logger.debug(f'Stopping interface {intname}')

    ###################################
    # Ui Methods
    ###################################

    def openAddIntDialog(self) -> None:
        self.logger.debug(f'openAddIntDialog method called.')
        intform = AddIntDialog(self, logging.DEBUG)
        if intform.exec():
            self.logger.debug(f'Interface Add Form : Button OK Clicked.')
            intname = intform.AddInterfaceForm.InterfaceName.text()
            inthost = intform.AddInterfaceForm.InterfaceHost.text()
            intport = intform.AddInterfaceForm.InterfacePort.text()
            self.logger.debug(f'Interface Name : {intname}')
            self.logger.debug(f'Interface Name : {inthost}')
            self.logger.debug(f'Interface Name : {intport}')
            if os.path.isdir(f'Config/Interfaces/{intname}'):
                self.logger.debug(f'Interface configuration found in Configuration directory')
                loaddlg = createMessageBoxDialog(
                    f'Load Interface Configuration ?',
                    f'Do you want to load {intname} configuration ?',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Warning
                )

                if loaddlg.exec() == QMessageBox.Yes:
                    if os.path.isfile(f'Config/Interfaces/{intname}/{intname}.json'):
                        self.logger.debug(f'Loading Interface {intname} configuration !')
                        # intconfig = SimOpIntConfig(f'Config/Interfaces/{intname}', f'{intname}.json').getConfig()
                        # print(f'Config : {intconfig}')
                    else:
                        self.logger.error(f'Main Interface {intname} configuration file Config/Interfaces/{intname}/{intname}.json not found!')
                else:
                    self.logger.debug(f'Interface {intname} configuration not loaded!')
            else:
                self.logger.debug(f'Interface configuration not found in Configuration directory')
                createdlg = createMessageBoxDialog(
                    f'Create Interface Configuration ?',
                    f'Do you want to create {intname} configuration ?',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Warning
                )

                if createdlg.exec() == QMessageBox.Yes:
                    self.logger.debug(f'Creating Interface {intname} configuration !')
                else:
                    self.logger.debug(f'Interface {intname} configuration not created !')
        else:
            self.logger.debug(f'Interface Add Form : Button Cancel Clicked.')

    def openEditIntDialog(self, intname: str) -> None:
        self.logger.debug(f'openEditIntDialog method called.')
        interface = self.getInterface(intname)
        intform = EditIntDialog(self, logging.DEBUG)
        intform.EditInterfaceForm.InterfaceName.setText(f'{interface.getName()}')
        intform.EditInterfaceForm.InterfaceHost.setText(f'{interface.getAddr()}')
        intform.EditInterfaceForm.InterfacePort.setText(f'{interface.getPort()}')
        if intform.exec():
            self.logger.debug(f'Interface Edit Form : Button OK Clicked.')
            formintname = intform.EditInterfaceForm.InterfaceName.text()
            forminthost = intform.EditInterfaceForm.InterfaceHost.text()
            formintport = intform.EditInterfaceForm.InterfacePort.text()
            self.logger.debug(f'Interface Name : {formintname}')
            self.logger.debug(f'Interface Name : {forminthost}')
            self.logger.debug(f'Interface Name : {formintport}')
        else:
            self.logger.debug(f'Interface Edit Form : Button Cancel Clicked.')