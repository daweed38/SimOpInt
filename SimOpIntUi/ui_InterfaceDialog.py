# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_InterfaceDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import simopintui_rc

class Ui_InterfaceDialog(object):
    def setupUi(self, InterfaceDialog):
        if not InterfaceDialog.objectName():
            InterfaceDialog.setObjectName(u"InterfaceDialog")
        InterfaceDialog.resize(398, 186)
        icon = QIcon()
        icon.addFile(u":/imgs/interface.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        InterfaceDialog.setWindowIcon(icon)
        self.layoutWidget = QWidget(InterfaceDialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 21, 361, 148))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.DialogTitle = QLabel(self.layoutWidget)
        self.DialogTitle.setObjectName(u"DialogTitle")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DialogTitle.sizePolicy().hasHeightForWidth())
        self.DialogTitle.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.DialogTitle.setFont(font)

        self.verticalLayout_3.addWidget(self.DialogTitle)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.InterfaceNameLbl = QLabel(self.layoutWidget)
        self.InterfaceNameLbl.setObjectName(u"InterfaceNameLbl")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.InterfaceNameLbl.sizePolicy().hasHeightForWidth())
        self.InterfaceNameLbl.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.InterfaceNameLbl.setFont(font1)

        self.verticalLayout.addWidget(self.InterfaceNameLbl)

        self.InterfaceAddrLbl = QLabel(self.layoutWidget)
        self.InterfaceAddrLbl.setObjectName(u"InterfaceAddrLbl")
        sizePolicy1.setHeightForWidth(self.InterfaceAddrLbl.sizePolicy().hasHeightForWidth())
        self.InterfaceAddrLbl.setSizePolicy(sizePolicy1)
        self.InterfaceAddrLbl.setFont(font1)

        self.verticalLayout.addWidget(self.InterfaceAddrLbl)

        self.InterfacePortLbl = QLabel(self.layoutWidget)
        self.InterfacePortLbl.setObjectName(u"InterfacePortLbl")
        sizePolicy1.setHeightForWidth(self.InterfacePortLbl.sizePolicy().hasHeightForWidth())
        self.InterfacePortLbl.setSizePolicy(sizePolicy1)
        self.InterfacePortLbl.setFont(font1)

        self.verticalLayout.addWidget(self.InterfacePortLbl)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.InterfaceName = QLineEdit(self.layoutWidget)
        self.InterfaceName.setObjectName(u"InterfaceName")

        self.verticalLayout_2.addWidget(self.InterfaceName)

        self.InterfaceAddr = QLineEdit(self.layoutWidget)
        self.InterfaceAddr.setObjectName(u"InterfaceAddr")

        self.verticalLayout_2.addWidget(self.InterfaceAddr)

        self.InterfacePort = QLineEdit(self.layoutWidget)
        self.InterfacePort.setObjectName(u"InterfacePort")

        self.verticalLayout_2.addWidget(self.InterfacePort)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.BtnOk = QPushButton(self.layoutWidget)
        self.BtnOk.setObjectName(u"BtnOk")

        self.horizontalLayout_2.addWidget(self.BtnOk)

        self.BtnCancel = QPushButton(self.layoutWidget)
        self.BtnCancel.setObjectName(u"BtnCancel")

        self.horizontalLayout_2.addWidget(self.BtnCancel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.retranslateUi(InterfaceDialog)

        QMetaObject.connectSlotsByName(InterfaceDialog)
    # setupUi

    def retranslateUi(self, InterfaceDialog):
        InterfaceDialog.setWindowTitle(QCoreApplication.translate("InterfaceDialog", u"Dialog", None))
        self.DialogTitle.setText(QCoreApplication.translate("InterfaceDialog", u"DialogName", None))
        self.InterfaceNameLbl.setText(QCoreApplication.translate("InterfaceDialog", u"Interface Name :", None))
        self.InterfaceAddrLbl.setText(QCoreApplication.translate("InterfaceDialog", u"Interface Host :", None))
        self.InterfacePortLbl.setText(QCoreApplication.translate("InterfaceDialog", u"Interface Port :", None))
        self.InterfacePort.setText(QCoreApplication.translate("InterfaceDialog", u"49500", None))
        self.BtnOk.setText(QCoreApplication.translate("InterfaceDialog", u"OK", None))
        self.BtnCancel.setText(QCoreApplication.translate("InterfaceDialog", u"Cancel", None))
    # retranslateUi

