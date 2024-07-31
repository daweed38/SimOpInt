##################################################
# FarmerSoft Open Interface Qt Gui Class
##################################################
# Add Interface Dialog Class
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
# import sys
import logging
# import os
import json
import os

# Pyside6 Module Import
from PySide6.QtWidgets import QDialog, QListWidgetItem, QMessageBox
from PySide6.QtCore import Qt

# SimOpInt Module Import

# SimOpIntUi Module Import
from SimOpIntUi.ui_InterfaceDialog import Ui_InterfaceDialog


class InterfaceDialog(QDialog):

    ###################################
    # Class Description
    ###################################

    def __str__(self) -> str:
        return 'This the Sim Open Interface Add / Edit Dialog Class'

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

        self.action = ''

        self.InterfaceDialog = Ui_InterfaceDialog()
        self.InterfaceDialog.setupUi(self)

        self.InterfaceDialog.BtnOk.clicked.connect(self.acceptChoice)
        self.InterfaceDialog.BtnCancel.clicked.connect(self.cancelChoice)

        self.logger.debug(f'Sim Open Interface Dialog initialized')

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

    # Return Interface Name from dialog
    def getInterfaceName(self) -> str:
        return self.InterfaceDialog.InterfaceName.text()

    # Return Interface Host from dialog
    def getInterfaceAddr(self) -> str:
        return self.InterfaceDialog.InterfaceAddr.text()

    # Return Interface Port from dialog
    def getInterfacePort(self) -> int:
        return int(self.InterfaceDialog.InterfacePort.text())

    # Show AddInterface Dialog
    def showInterfaceDialog(self, action) -> bool:
        self.action = action
        if self.action == 'add':
            self.InterfaceDialog.DialogTitle.setText(f'Adding Interface')
            self.InterfaceDialog.InterfaceName.clear()
            self.InterfaceDialog.InterfaceAddr.clear()
            self.InterfaceDialog.InterfacePort.setText('49500')
            self.InterfaceDialog.InterfaceName.setFocus()
            if self.exec():
                self.logger.debug(f'True Returned (add show)')
                return True
            else:
                self.logger.debug(f'False Returned (add show)')
                return False
        elif self.action == 'edit':
            intname = self.parent().InterfaceMngtDialog.InterfaceList.currentItem().text()
            interface = self.parent().interfaces[intname]['interface']
            intaddr = interface.getInterfaceAddr()
            intport = interface.getInterfacePort()
            self.InterfaceDialog.DialogTitle.setText(f'Editing Interface {intname}')
            self.InterfaceDialog.InterfaceName.setText(intname)
            self.InterfaceDialog.InterfaceAddr.setText(intaddr)
            self.InterfaceDialog.InterfacePort.setText(str(intport))
            self.InterfaceDialog.InterfaceName.setFocus()
            if self.exec():
                self.logger.debug(f'True Returned (edit show)')
                return True
            else:
                self.logger.debug(f'False Returned (edit show)')
                return False
        else:
            self.logger.error(f'Action {self.action} is not recognized !')
            self.logger.debug(f'False Returned')
            return False

    # Interface Ok Button Method
    def acceptChoice(self) -> None:
        if self.action == 'add':
            self.logger.debug(f'Action {self.action}. Adding New Interface')
            if self.addInterface():
                self.logger.debug(f'True Returned (add accept)')
                self.accept()
        elif self.action == 'edit':
            self.logger.debug(f'Action {self.action}. Editing Interface')
            if self.editInterface():
                self.logger.debug(f'True Returned (edit accept)')
                self.accept()
        else:
            self.logger.error(f'Action {self.action} is not recognized !')
            self.logger.debug(f'False Returned')

    # Interface Cancel Button Method
    def cancelChoice(self) -> None:
        self.logger.debug(f'Action {self.action} Cancelled')
        self.logger.debug(f'False Returned (cancel)')
        self.close()

    # Adding Interface Management
    def addInterface(self) -> bool:
        intexistcheck = len(self.parent().InterfaceMngtDialog.InterfaceList.findItems(self.getInterfaceName(), Qt.MatchFixedString))
        if intexistcheck == 0:
            interface = {'INTERFACE': {'intname': self.getInterfaceName()}, 'NETWORK': {'intaddr': self.getInterfaceAddr(), 'intport': self.getInterfacePort()}}
            self.logger.debug(f'Creating Interface {self.getInterfaceName()} with the following parameter {interface}')
            item = QListWidgetItem(self.getInterfaceName(), self.parent().InterfaceMngtDialog.InterfaceList)
            self.parent().InterfaceMngtDialog.InterfaceList.setCurrentItem(item)
            with open(f'Config/Interfaces/{self.getInterfaceName()}.json', 'w') as intfile:
                json.dump(interface, intfile)
            self.close()
            return True
        elif intexistcheck == 1:
            interfaceitem = self.parent().InterfaceMngtDialog.InterfaceList.findItems(self.getInterfaceName(), Qt.MatchFixedString)[0]
            interfacerow = self.parent().InterfaceMngtDialog.InterfaceList.row(interfaceitem)
            self.logger.warning(f'Interface already exist : {interfaceitem.text()} [ Row {interfacerow} ]')
            alertdialog = QMessageBox(self)
            alertdialog.setWindowTitle('Existing Interface !')
            alertdialog.setText(f'Interface {interfaceitem.text()} already exist')
            alertdialog.setStandardButtons(QMessageBox.Ok)
            alertdialog.setIcon(QMessageBox.Warning)
            alertdialog.exec()
        else:
            self.logger.error(f'Interface existing check error ({intexistcheck} found)')
            alertdialog = QMessageBox(self)
            alertdialog.setWindowTitle('Interface Check Error !')
            alertdialog.setText(f'More than one Interface found ({intexistcheck}) !')
            alertdialog.setStandardButtons(QMessageBox.Ok)
            alertdialog.setIcon(QMessageBox.Critical)
            alertdialog.exec()

    # Editing Interface Management
    def editInterface(self) -> bool:
        oldintname = self.parent().InterfaceMngtDialog.InterfaceList.currentItem().text()
        interface = {'INTERFACE': {'intname': self.getInterfaceName()}, 'NETWORK': {'intaddr': self.getInterfaceAddr(), 'intport': self.getInterfacePort()}}
        if oldintname != self.getInterfaceName():
            intexistcheck = len(self.parent().InterfaceMngtDialog.InterfaceList.findItems(self.getInterfaceName(), Qt.MatchExactly))
            if intexistcheck == 0:
                self.logger.debug(f'Renaming Interface {oldintname} to {self.getInterfaceName()} with the following parameters {interface}')
                os.rename(f'Config/Interfaces/{oldintname}.json', f'Config/Interfaces/{self.getInterfaceName()}.json')
                self.parent().InterfaceMngtDialog.InterfaceList.currentItem().setText(self.getInterfaceName())
                self.close()
            elif intexistcheck == 1:
                interfaceitem = self.parent().InterfaceMngtDialog.InterfaceList.findItems(self.getInterfaceName(), Qt.MatchExactly)[0]
                interfacerow = self.parent().InterfaceMngtDialog.InterfaceList.row(interfaceitem)
                self.logger.warning(f'Interface already exist : {interfaceitem.text()} [ Row {interfacerow} ]')
                alertdialog = QMessageBox(self)
                alertdialog.setWindowTitle('Existing Interface !')
                alertdialog.setText(f'Interface {interfaceitem.text()} already exist')
                alertdialog.setStandardButtons(QMessageBox.Ok)
                alertdialog.setIcon(QMessageBox.Warning)
                alertdialog.exec()
            else:
                self.logger.error(f'Interface existing check error ({intexistcheck} found)')
                alertdialog = QMessageBox(self)
                alertdialog.setWindowTitle('Interface Check Error !')
                alertdialog.setText(f'More than one Interface found ({intexistcheck}) !')
                alertdialog.setStandardButtons(QMessageBox.Ok)
                alertdialog.setIcon(QMessageBox.Critical)
                alertdialog.exec()
        else:
            self.logger.debug(f'Updating Interface {self.getInterfaceName()} with the following parameters {interface}')
            self.close()
        with open(f'Config/Interfaces/{self.getInterfaceName()}.json', 'w') as intfile:
            json.dump(interface, intfile)
        return True
