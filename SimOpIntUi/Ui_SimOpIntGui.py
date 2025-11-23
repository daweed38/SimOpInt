# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_SimOpIntGuiMain.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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

class Ui_SimOpIntGui(object):
    def setupUi(self, SimOpIntGui):
        if not SimOpIntGui.objectName():
            SimOpIntGui.setObjectName(u"SimOpIntGui")
        SimOpIntGui.resize(800, 600)
        self.actionQuit = QAction(SimOpIntGui)
        self.actionQuit.setObjectName(u"actionQuit")
        self.centralwidget = QWidget(SimOpIntGui)
        self.centralwidget.setObjectName(u"centralwidget")
        SimOpIntGui.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SimOpIntGui)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        SimOpIntGui.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SimOpIntGui)
        self.statusbar.setObjectName(u"statusbar")
        SimOpIntGui.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionQuit)

        self.retranslateUi(SimOpIntGui)

        QMetaObject.connectSlotsByName(SimOpIntGui)
    # setupUi

    def retranslateUi(self, SimOpIntGui):
        SimOpIntGui.setWindowTitle(QCoreApplication.translate("SimOpIntGui", u"MainWindow", None))
        self.actionQuit.setText(QCoreApplication.translate("SimOpIntGui", u"Quit&", None))
        self.menuFile.setTitle(QCoreApplication.translate("SimOpIntGui", u"File", None))
    # retranslateUi

