##################################################
# FarmerSoft Open Interface Gui
##################################################
# FarmerSoft © 2024
# By Daweed
##################################################

# Standard Modules Import
import sys
import logging

# PySide6 Module Import
from PySide6.QtWidgets import QApplication

# SimOpInt Module Import
from SimOpInt.SimOpIntLogger import SimOpIntLogger

# SimOpIntConfig Module Import
from SimOpIntConfig.MainWindowGui import MainWindowGui

# Logger Creation
simopintlogger = SimOpIntLogger('SimOpInt', 'Logs', 'simopint.log')
simopintconfiglogger = SimOpIntLogger('SimOpIntConfig', 'Logs', 'simopintconfig.log')

# Qapplication Creation
app = QApplication(sys.argv)

window = MainWindowGui()
window.show()

# Starting Event Loop
app.exec()

# logger.warning(f'Application ended at {datetime.datetime.now()}')
