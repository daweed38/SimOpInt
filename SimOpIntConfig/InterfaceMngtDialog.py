##################################################
# FarmerSoft Open Interface Qt Gui Class
##################################################
# Add Interface Management Class
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
# import sys
import logging
import os

# Pyside6 Module Import
from PySide6.QtWidgets import QDialog, QListWidgetItem

# SimOpInt Module Import
from SimOpInt.SimOpInt import SimOpInt

# SimOpIntConfig Module Import
from SimOpIntConfig.InterfaceDialog import InterfaceDialog

# SimOpIntUi Module Import
from SimOpIntUi.ui_InterfaceMngt import Ui_InterfaceMngtDialog


class InterfaceMngtDialog(QDialog):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return 'This the Sim Open Interface Management Dialog Class'

    ###################################
    # Properties
    ###################################

    ###################################
    # Constructor
    ###################################

    def __init__(self, parent, debug: int = logging.WARNING) -> None:
        super().__init__(parent)

        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        self.interfaces = {}
        self.interfacesloaded = False
        self.configdir = 'Config/Interfaces'

        self.InterfaceMngtDialog = Ui_InterfaceMngtDialog()
        self.InterfaceMngtDialog.setupUi(self)

        if self.loadInterfaces():
            self.interfacesloaded = True

        if self.InterfaceMngtDialog.InterfaceList.count() == 0:
            self.InterfaceMngtDialog.BtnRemoveInterface.setEnabled(False)
            self.InterfaceMngtDialog.BtnEditInterface.setEnabled(False)

        self.InterfaceDialog = InterfaceDialog(self)

        self.InterfaceMngtDialog.BtnAddInterface.clicked.connect(self.openAddInterfaceGui)
        self.InterfaceMngtDialog.BtnEditInterface.clicked.connect(self.openEditInterfaceGui)
        self.InterfaceMngtDialog.BtnRemoveInterface.clicked.connect(self.removeInterface)

        if self.interfacesloaded:
            self.logger.debug(f'Sim Open Interface Management Dialog Gui initialized')

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Method
    ###################################

    # Return Interfaces Dictionary
    def getInterfaces(self) -> dict:
        return self.interfaces

    # Return Interface intname from self.interfaces
    def getInterface(self, intname) -> SimOpInt:
        return self.interfaces[intname]['interface']

    # Create Interface from configuration file and store in self.interfaces
    def createInterface(self, intname) -> None:
        interface = SimOpInt(self.configdir, f'{intname}.json', 'json')
        self.interfaces[interface.getName()] = {'interface': interface}
        self.logger.debug(f'New Interface object created : {interface.getName()} and added to Interface Dict : {self.interfaces}')

    # Remove Interface intname from self.interfaces
    def deleteInterface(self, intname) -> None:
        del self.interfaces[intname]
        self.logger.debug(f'Selected interface {intname} removed from self.interfaces {self.interfaces}')

    ###################################
    # Ui Methods
    ###################################

    # Show InterfaceMngtDialog
    def showInterfaceMngtDialog(self) -> None:
        self.show()

    # Load Interfaces from Config Directory
    def loadInterfaces(self) -> bool:
        if os.path.exists(f'{self.configdir}'):
            self.logger.debug(f'Loading interface from {self.configdir}')
            with os.scandir(self.configdir) as configfiles:
                for configfile in configfiles:
                    if configfile.name.endswith('.json') and configfile.is_file():
                        self.logger.debug(configfile.name)
                        interface = SimOpInt(self.configdir, configfile.name, 'json', logging.DEBUG)
                        self.interfaces[interface.getName()] = {'interface': interface}
                        QListWidgetItem(interface.getName(), self.InterfaceMngtDialog.InterfaceList)
                        self.parent().interfacesList.addItem(interface.getName())
            return True
        else:
            self.logger.error(f'Loading interface Error : {self.configdir} does not exist')
            return False

    # Open Interface Dialog in Adding Mode Action
    def openAddInterfaceGui(self) -> None:
        dialogRC = self.InterfaceDialog.showInterfaceDialog('add')
        self.logger.debug(f'Return Code from Add Interface Dialog : {dialogRC}')
        if dialogRC:
            intname = self.InterfaceMngtDialog.InterfaceList.currentItem().text()
            self.createInterface(intname)
            self.parent().interfacesList.addItem(intname)
            if self.InterfaceMngtDialog.InterfaceList.count() != 0 and not self.InterfaceMngtDialog.BtnEditInterface.isEnabled():
                self.InterfaceMngtDialog.BtnEditInterface.setEnabled(True)
                self.InterfaceMngtDialog.BtnRemoveInterface.setEnabled(True)
            self.parent().interfacesList.setCurrentText(intname)

    # Open Interface Dialog in Editing Mode Action
    def openEditInterfaceGui(self) -> None:
        oldintname = self.InterfaceMngtDialog.InterfaceList.currentItem().text()
        dialogRC = self.InterfaceDialog.showInterfaceDialog('edit')
        self.logger.debug(f'Return Code from Edit Interface Dialog : {dialogRC}')
        if dialogRC:
            intname = self.InterfaceMngtDialog.InterfaceList.currentItem().text()
            self.deleteInterface(oldintname)
            self.createInterface(intname)
            if intname != oldintname:
                itemrow = self.parent().interfacesList.findText(oldintname)
                self.logger.debug(f'Item row to rename {itemrow}')
                self.parent().interfacesList.setItemText(itemrow, intname)
            self.logger.debug(f'ComboBox Current Index : {self.parent().interfacesList.currentIndex()} {self.parent().interfacesList.currentText()}')
            self.parent().loadSelectedInterface(self.parent().interfacesList.currentIndex())

    # Delete Interface Action
    def removeInterface(self) -> None:
        intname = self.InterfaceMngtDialog.InterfaceList.currentItem().text()
        introw = self.InterfaceMngtDialog.InterfaceList.currentRow()
        comboitemrow = self.parent().interfacesList.findText(intname)
        self.InterfaceMngtDialog.InterfaceList.takeItem(introw)
        self.logger.debug(f'Selected interface {intname} [ Row {introw} ] removed')
        self.parent().interfacesList.removeItem(comboitemrow)
        self.logger.debug(f'Item row in QComboBox removed: {comboitemrow}')
        self.deleteInterface(intname)
        if os.path.exists(f'{self.configdir}/{intname}.json'):
            os.remove(f'{self.configdir}/{intname}.json')
            self.logger.debug(f'Interface configuration file {self.configdir}/{intname}.json removed')
            if self.InterfaceMngtDialog.InterfaceList.count() == 0 and self.InterfaceMngtDialog.BtnEditInterface.isEnabled():
                self.InterfaceMngtDialog.BtnEditInterface.setEnabled(False)
                self.InterfaceMngtDialog.BtnRemoveInterface.setEnabled(False)
        else:
            self.logger.error(f'Interface configuration file {self.configdir}/{intname}.json not found')
