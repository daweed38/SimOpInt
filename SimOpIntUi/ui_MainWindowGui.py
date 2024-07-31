# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_MainWindowGui.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)
import simopintui_rc

class Ui_MainWindowGui(object):
    def setupUi(self, MainWindowGui):
        if not MainWindowGui.objectName():
            MainWindowGui.setObjectName(u"MainWindowGui")
        MainWindowGui.resize(800, 500)
        MainWindowGui.setDocumentMode(False)
        self.actionAbout = QAction(MainWindowGui)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionQuit = QAction(MainWindowGui)
        self.actionQuit.setObjectName(u"actionQuit")
        icon = QIcon()
        icon.addFile(u":/imgs/exit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionQuit.setIcon(icon)
        self.actionInterfaceManagement = QAction(MainWindowGui)
        self.actionInterfaceManagement.setObjectName(u"actionInterfaceManagement")
        icon1 = QIcon()
        icon1.addFile(u":/imgs/param.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionInterfaceManagement.setIcon(icon1)
        self.centralwidget = QWidget(MainWindowGui)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(11, 14, 258, 431))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.interfacesList = QComboBox(self.widget)
        self.interfacesList.setObjectName(u"interfacesList")

        self.verticalLayout.addWidget(self.interfacesList)

        self.HostHoriLayout = QHBoxLayout()
        self.HostHoriLayout.setObjectName(u"HostHoriLayout")
        self.hostLabel = QLabel(self.widget)
        self.hostLabel.setObjectName(u"hostLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hostLabel.sizePolicy().hasHeightForWidth())
        self.hostLabel.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.hostLabel.setFont(font)

        self.HostHoriLayout.addWidget(self.hostLabel)

        self.hostValue = QLabel(self.widget)
        self.hostValue.setObjectName(u"hostValue")

        self.HostHoriLayout.addWidget(self.hostValue)


        self.verticalLayout.addLayout(self.HostHoriLayout)

        self.PortHoriLayout = QHBoxLayout()
        self.PortHoriLayout.setObjectName(u"PortHoriLayout")
        self.portLabel = QLabel(self.widget)
        self.portLabel.setObjectName(u"portLabel")
        sizePolicy.setHeightForWidth(self.portLabel.sizePolicy().hasHeightForWidth())
        self.portLabel.setSizePolicy(sizePolicy)
        self.portLabel.setFont(font)

        self.PortHoriLayout.addWidget(self.portLabel)

        self.portValue = QLabel(self.widget)
        self.portValue.setObjectName(u"portValue")

        self.PortHoriLayout.addWidget(self.portValue)


        self.verticalLayout.addLayout(self.PortHoriLayout)

        self.ConnectBtnHoriLayout = QHBoxLayout()
        self.ConnectBtnHoriLayout.setObjectName(u"ConnectBtnHoriLayout")
        self.connectBtn = QPushButton(self.widget)
        self.connectBtn.setObjectName(u"connectBtn")

        self.ConnectBtnHoriLayout.addWidget(self.connectBtn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ConnectBtnHoriLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.ConnectBtnHoriLayout)

        self.objectsTree = QTreeWidget(self.widget)
        icon2 = QIcon()
        icon2.addFile(u":/imgs/interface.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setIcon(0, icon2);
        self.objectsTree.setHeaderItem(__qtreewidgetitem)
        self.objectsTree.setObjectName(u"objectsTree")
        font1 = QFont()
        font1.setPointSize(10)
        self.objectsTree.setFont(font1)
        self.objectsTree.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.objectsTree.setFrameShape(QFrame.Shape.StyledPanel)
        self.objectsTree.setFrameShadow(QFrame.Shadow.Sunken)
        self.objectsTree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.objectsTree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.objectsTree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.objectsTree.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.objectsTree.setRootIsDecorated(True)
        self.objectsTree.setAnimated(True)

        self.verticalLayout.addWidget(self.objectsTree)

        MainWindowGui.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindowGui)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindowGui.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindowGui)
        self.statusbar.setObjectName(u"statusbar")
        MainWindowGui.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menu_File.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionInterfaceManagement)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindowGui)

        QMetaObject.connectSlotsByName(MainWindowGui)
    # setupUi

    def retranslateUi(self, MainWindowGui):
        MainWindowGui.setWindowTitle(QCoreApplication.translate("MainWindowGui", u"MainWindow", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindowGui", u"About", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindowGui", u"Quit", None))
        self.actionInterfaceManagement.setText(QCoreApplication.translate("MainWindowGui", u"Interface Management ...", None))
        self.hostLabel.setText(QCoreApplication.translate("MainWindowGui", u"Host :", None))
        self.hostValue.setText("")
        self.portLabel.setText(QCoreApplication.translate("MainWindowGui", u"Port :", None))
        self.portValue.setText("")
        self.connectBtn.setText(QCoreApplication.translate("MainWindowGui", u"Connect", None))
        ___qtreewidgetitem = self.objectsTree.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindowGui", u"Interfaces", None));
        self.menu_File.setTitle(QCoreApplication.translate("MainWindowGui", u"&File", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindowGui", u"Settings", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindowGui", u"Help", None))
    # retranslateUi

