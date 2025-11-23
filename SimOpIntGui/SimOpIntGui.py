##################################################
# FarmerSoft SimOpInt Main Gui Class
##################################################
# Class TimeMachineGui
# FarmerSoft © 2025
# By Daweed
##################################################

# Standard Modules Import
import os
import sys
import logging

#  PySide6 Module Import
from PySide6.QtWidgets import QMainWindow
# from PySide6.QtGui import QAction
# from PySide6.QtGui import QIcon, QPixmap, QListWidgetItem

# SimOpIntUi Module Import
from SimOpIntUi.Ui_SimOpIntGui import Ui_SimOpIntGui


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

        self.debug = debug

        # Ui Creation
        self.setupUi(self)

        # Logging Management
        # Get Logger
        self.logger = logging.getLogger('SimOpIntGui.SimOpIntGui')

        if self.logger.getEffectiveLevel() != self.debug:
            self.logger.setLevel(self.debug)

        # File Menu
        self.actionQuit.triggered.connect(self.closeApps)

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

    def closeApps(self) -> None:
        self.logger.debug(f'Closing App')
        self.close()