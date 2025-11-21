# Pyside6 Module Import
from PySide6.QtWidgets import QMessageBox


# Create a Message Box Dialog
def createMessageBoxDialog(title: str, message: str, buttons, dialogtype) -> QMessageBox:
    msgBoxDialog = QMessageBox()
    msgBoxDialog.setWindowTitle(title)
    msgBoxDialog.setText(message)
    msgBoxDialog.setStandardButtons(buttons)
    msgBoxDialog.setIcon(dialogtype)
    return msgBoxDialog
