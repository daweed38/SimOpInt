##################################################
# FarmerSoft Open Interface Add Dialog Class
##################################################
# AddIntDialog Class
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import logging
import os.path

# Pyside6 Module Import
# from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog

# Pyside6 Module Import
# from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog

# SimOpInt Module Import

# SimOpIntUi Module Import
from SimOpIntUi.ui_AddIntDialog import Ui_AddInterface


class AddIntDialog(QDialog):

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

        # Add Interface Form Ui
        self.AddInterfaceForm = Ui_AddInterface()
        self.AddInterfaceForm.setupUi(self)

    ###################################
    # Destructor
    ###################################

    def __del__(self) -> None:
        pass

    ###################################
    # System Method
    ###################################

    ###################################
    # Interfaces Method
    ###################################

    ###################################
    # Ui Methods
    ###################################
