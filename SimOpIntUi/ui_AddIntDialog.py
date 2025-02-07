# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_AddIntDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QLineEdit, QSizePolicy,
    QWidget)
import SimOpIntUi.simopintui_rc

class Ui_AddInterface(object):
    def setupUi(self, AddInterface):
        if not AddInterface.objectName():
            AddInterface.setObjectName(u"AddInterface")
        AddInterface.resize(400, 220)
        icon = QIcon()
        icon.addFile(u":/imgs/interface.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        AddInterface.setWindowIcon(icon)
        self.AddIntBtnBox = QDialogButtonBox(AddInterface)
        self.AddIntBtnBox.setObjectName(u"AddIntBtnBox")
        self.AddIntBtnBox.setGeometry(QRect(40, 170, 341, 32))
        self.AddIntBtnBox.setOrientation(Qt.Orientation.Horizontal)
        self.AddIntBtnBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.FormNameLbl = QLabel(AddInterface)
        self.FormNameLbl.setObjectName(u"FormNameLbl")
        self.FormNameLbl.setGeometry(QRect(21, 22, 145, 22))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.FormNameLbl.setFont(font)
        self.layoutWidget = QWidget(AddInterface)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(21, 60, 371, 83))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.InterfaceNameLbl = QLabel(self.layoutWidget)
        self.InterfaceNameLbl.setObjectName(u"InterfaceNameLbl")
        font1 = QFont()
        font1.setPointSize(10)
        self.InterfaceNameLbl.setFont(font1)

        self.gridLayout.addWidget(self.InterfaceNameLbl, 0, 0, 1, 1)

        self.InterfaceName = QLineEdit(self.layoutWidget)
        self.InterfaceName.setObjectName(u"InterfaceName")
        self.InterfaceName.setFont(font1)

        self.gridLayout.addWidget(self.InterfaceName, 0, 1, 1, 1)

        self.InterfacHostLbl = QLabel(self.layoutWidget)
        self.InterfacHostLbl.setObjectName(u"InterfacHostLbl")
        self.InterfacHostLbl.setFont(font1)

        self.gridLayout.addWidget(self.InterfacHostLbl, 1, 0, 1, 1)

        self.InterfaceHost = QLineEdit(self.layoutWidget)
        self.InterfaceHost.setObjectName(u"InterfaceHost")
        self.InterfaceHost.setFont(font1)

        self.gridLayout.addWidget(self.InterfaceHost, 1, 1, 1, 1)

        self.InterfacePortLbl = QLabel(self.layoutWidget)
        self.InterfacePortLbl.setObjectName(u"InterfacePortLbl")
        self.InterfacePortLbl.setFont(font1)

        self.gridLayout.addWidget(self.InterfacePortLbl, 2, 0, 1, 1)

        self.InterfacePort = QLineEdit(self.layoutWidget)
        self.InterfacePort.setObjectName(u"InterfacePort")
        self.InterfacePort.setFont(font1)

        self.gridLayout.addWidget(self.InterfacePort, 2, 1, 1, 1)


        self.retranslateUi(AddInterface)
        self.AddIntBtnBox.accepted.connect(AddInterface.accept)
        self.AddIntBtnBox.rejected.connect(AddInterface.reject)

        QMetaObject.connectSlotsByName(AddInterface)
    # setupUi

    def retranslateUi(self, AddInterface):
        AddInterface.setWindowTitle(QCoreApplication.translate("AddInterface", u"Add Interface Dialog", None))
        self.FormNameLbl.setText(QCoreApplication.translate("AddInterface", u"Adding Interface ...", None))
        self.InterfaceNameLbl.setText(QCoreApplication.translate("AddInterface", u"Interface Name : ", None))
        self.InterfacHostLbl.setText(QCoreApplication.translate("AddInterface", u"Interface Host Address :", None))
        self.InterfacePortLbl.setText(QCoreApplication.translate("AddInterface", u"Interface Host Port :", None))
    # retranslateUi

