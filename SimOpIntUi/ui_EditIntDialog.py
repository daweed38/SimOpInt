# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_EditIntDialog.ui'
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
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)
import SimOpIntUi.simopintui_rc

class Ui_EditInterface(object):
    def setupUi(self, EditInterface):
        if not EditInterface.objectName():
            EditInterface.setObjectName(u"EditInterface")
        EditInterface.resize(400, 508)
        icon = QIcon()
        icon.addFile(u":/imgs/interface.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        EditInterface.setWindowIcon(icon)
        self.EditIntBtnBox = QDialogButtonBox(EditInterface)
        self.EditIntBtnBox.setObjectName(u"EditIntBtnBox")
        self.EditIntBtnBox.setGeometry(QRect(40, 460, 341, 32))
        self.EditIntBtnBox.setOrientation(Qt.Orientation.Horizontal)
        self.EditIntBtnBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.FormInterfaceLbl = QLabel(EditInterface)
        self.FormInterfaceLbl.setObjectName(u"FormInterfaceLbl")
        self.FormInterfaceLbl.setGeometry(QRect(20, 26, 111, 20))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.FormInterfaceLbl.setFont(font)
        self.FormInterfaceNameLbl = QLabel(EditInterface)
        self.FormInterfaceNameLbl.setObjectName(u"FormInterfaceNameLbl")
        self.FormInterfaceNameLbl.setGeometry(QRect(130, 26, 231, 20))
        self.FormInterfaceNameLbl.setFont(font)
        self.layoutWidget = QWidget(EditInterface)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 60, 371, 83))
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

        self.treeWidget = QTreeWidget(EditInterface)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setIcon(0, icon);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        icon1 = QIcon()
        icon1.addFile(u":/imgs/device.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon2 = QIcon()
        icon2.addFile(u":/imgs/display_green.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon3 = QIcon()
        icon3.addFile(u":/imgs/indicator.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon4 = QIcon()
        icon4.addFile(u":/imgs/switch.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon5 = QIcon()
        icon5.addFile(u":/imgs/toogleswitch.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon6 = QIcon()
        icon6.addFile(u":/imgs/encoder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        __qtreewidgetitem1 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem1.setIcon(0, icon1);
        __qtreewidgetitem2 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem2.setIcon(0, icon2);
        __qtreewidgetitem3 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem3.setIcon(0, icon3);
        __qtreewidgetitem4 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem4.setIcon(0, icon4);
        __qtreewidgetitem5 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem5.setIcon(0, icon5);
        __qtreewidgetitem6 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem6.setIcon(0, icon6);
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(20, 160, 371, 291))

        self.retranslateUi(EditInterface)
        self.EditIntBtnBox.accepted.connect(EditInterface.accept)
        self.EditIntBtnBox.rejected.connect(EditInterface.reject)

        QMetaObject.connectSlotsByName(EditInterface)
    # setupUi

    def retranslateUi(self, EditInterface):
        EditInterface.setWindowTitle(QCoreApplication.translate("EditInterface", u"Edit Interface Dialog", None))
        self.FormInterfaceLbl.setText(QCoreApplication.translate("EditInterface", u"Edit Interface", None))
        self.FormInterfaceNameLbl.setText(QCoreApplication.translate("EditInterface", u"InterfaceName", None))
        self.InterfaceNameLbl.setText(QCoreApplication.translate("EditInterface", u"Interface Name : ", None))
        self.InterfacHostLbl.setText(QCoreApplication.translate("EditInterface", u"Interface Host Address :", None))
        self.InterfacePortLbl.setText(QCoreApplication.translate("EditInterface", u"Interface Host Port :", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("EditInterface", u"InterfaceName", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("EditInterface", u"Devices", None));
        ___qtreewidgetitem2 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("EditInterface", u"7 Seg Displays", None));
        ___qtreewidgetitem3 = self.treeWidget.topLevelItem(2)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("EditInterface", u"Annunciators", None));
        ___qtreewidgetitem4 = self.treeWidget.topLevelItem(3)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("EditInterface", u"Switches", None));
        ___qtreewidgetitem5 = self.treeWidget.topLevelItem(4)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("EditInterface", u"Push Buttons", None));
        ___qtreewidgetitem6 = self.treeWidget.topLevelItem(5)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("EditInterface", u"Encoders", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

