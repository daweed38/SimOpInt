##################################################
# FarmerSoft Open Interface Config Gui
##################################################
# FarmerSoft © 2024
# By Daweed
##################################################
import logging
# Standard Modules Import
import sys
# import logging

# PySide6 Module Import
from PySide6.QtWidgets import QApplication

# SimOpInt Module Import
from SimOpInt.SimOpIntLogger import SimOpIntLogger

# SimOpIntConfig Module Import
from SimOpIntGui.SimOpIntGui import SimOpIntGui

# Logger Creation
simopintlogger = SimOpIntLogger('SimOpInt', 'Logs', 'simopint.log')
simopintconfiglogger = SimOpIntLogger('SimOpIntGui', 'Logs', 'SimOpIntGui.log')

# Qapplication Creation
app = QApplication(sys.argv)

window = SimOpIntGui(logging.DEBUG)
window.show()

# Starting Event Loop
app.exec()

# logger.warning(f'Application ended at {datetime.datetime.now()}')
