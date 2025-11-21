# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_SimOpIntGui.ui'
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)
import SimOpIntUi.simopintui_rc

class Ui_SimOpIntGui(object):
    def setupUi(self, SimOpIntGui):
        if not SimOpIntGui.objectName():
            SimOpIntGui.setObjectName(u"SimOpIntGui")
        SimOpIntGui.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/imgs/simopintgui.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        SimOpIntGui.setWindowIcon(icon)
        self.actionQuit = QAction(SimOpIntGui)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionAdd = QAction(SimOpIntGui)
        self.actionAdd.setObjectName(u"actionAdd")
        self.centralwidget = QWidget(SimOpIntGui)
        self.centralwidget.setObjectName(u"centralwidget")
        SimOpIntGui.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SimOpIntGui)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menuConfiguration = QMenu(self.menubar)
        self.menuConfiguration.setObjectName(u"menuConfiguration")
        self.menuInterfaces = QMenu(self.menuConfiguration)
        self.menuInterfaces.setObjectName(u"menuInterfaces")
        icon1 = QIcon()
        icon1.addFile(u":/imgs/interface.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menuInterfaces.setIcon(icon1)
        SimOpIntGui.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SimOpIntGui)
        self.statusbar.setObjectName(u"statusbar")
        SimOpIntGui.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuConfiguration.menuAction())
        self.menu_File.addAction(self.actionQuit)
        self.menuConfiguration.addAction(self.menuInterfaces.menuAction())
        self.menuInterfaces.addAction(self.actionAdd)
        self.menuInterfaces.addSeparator()

        self.retranslateUi(SimOpIntGui)

        QMetaObject.connectSlotsByName(SimOpIntGui)
    # setupUi

    def retranslateUi(self, SimOpIntGui):
        SimOpIntGui.setWindowTitle(QCoreApplication.translate("SimOpIntGui", u"Sim Open Interface Editor", None))
        self.actionQuit.setText(QCoreApplication.translate("SimOpIntGui", u"&Quit", None))
        self.actionAdd.setText(QCoreApplication.translate("SimOpIntGui", u"Add ...", None))
        self.menu_File.setTitle(QCoreApplication.translate("SimOpIntGui", u"&File", None))
        self.menuConfiguration.setTitle(QCoreApplication.translate("SimOpIntGui", u"Configuration", None))
        self.menuInterfaces.setTitle(QCoreApplication.translate("SimOpIntGui", u"Interfaces", None))
    # retranslateUi

