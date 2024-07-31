# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_InterfaceMngt.ui'
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
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_InterfaceMngtDialog(object):
    def setupUi(self, InterfaceMngtDialog):
        if not InterfaceMngtDialog.objectName():
            InterfaceMngtDialog.setObjectName(u"InterfaceMngtDialog")
        InterfaceMngtDialog.resize(400, 300)
        self.layoutWidget = QWidget(InterfaceMngtDialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(15, 10, 380, 258))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.DialogNameLbl = QLabel(self.layoutWidget)
        self.DialogNameLbl.setObjectName(u"DialogNameLbl")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DialogNameLbl.sizePolicy().hasHeightForWidth())
        self.DialogNameLbl.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.DialogNameLbl.setFont(font)

        self.verticalLayout_2.addWidget(self.DialogNameLbl)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.InterfaceList = QListWidget(self.layoutWidget)
        self.InterfaceList.setObjectName(u"InterfaceList")

        self.horizontalLayout.addWidget(self.InterfaceList)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.BtnAddInterface = QPushButton(self.layoutWidget)
        self.BtnAddInterface.setObjectName(u"BtnAddInterface")
        self.BtnAddInterface.setStyleSheet(u"text-align:left;")

        self.verticalLayout.addWidget(self.BtnAddInterface)

        self.BtnEditInterface = QPushButton(self.layoutWidget)
        self.BtnEditInterface.setObjectName(u"BtnEditInterface")
        self.BtnEditInterface.setStyleSheet(u"text-align:left;")

        self.verticalLayout.addWidget(self.BtnEditInterface)

        self.BtnRemoveInterface = QPushButton(self.layoutWidget)
        self.BtnRemoveInterface.setObjectName(u"BtnRemoveInterface")
        self.BtnRemoveInterface.setStyleSheet(u"text-align:left;")

        self.verticalLayout.addWidget(self.BtnRemoveInterface)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(InterfaceMngtDialog)
        self.buttonBox.accepted.connect(InterfaceMngtDialog.accept)
        self.buttonBox.rejected.connect(InterfaceMngtDialog.reject)

        QMetaObject.connectSlotsByName(InterfaceMngtDialog)
    # setupUi

    def retranslateUi(self, InterfaceMngtDialog):
        InterfaceMngtDialog.setWindowTitle(QCoreApplication.translate("InterfaceMngtDialog", u"Dialog", None))
        self.DialogNameLbl.setText(QCoreApplication.translate("InterfaceMngtDialog", u"Interface Management ...", None))
        self.BtnAddInterface.setText(QCoreApplication.translate("InterfaceMngtDialog", u"Add Interface ...", None))
        self.BtnEditInterface.setText(QCoreApplication.translate("InterfaceMngtDialog", u"Edit Interface ...", None))
        self.BtnRemoveInterface.setText(QCoreApplication.translate("InterfaceMngtDialog", u"Remove Interface ...", None))
    # retranslateUi

