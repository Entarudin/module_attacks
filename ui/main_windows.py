# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windows.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(700, 500)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_select_the_attacks = QLabel(self.centralwidget)
        self.label_select_the_attacks.setObjectName(u"label_select_the_attacks")
        self.label_select_the_attacks.setGeometry(QRect(10, 30, 681, 61))
        font = QFont()
        font.setPointSize(14)
        self.label_select_the_attacks.setFont(font)
        self.label_select_the_attacks.setAlignment(Qt.AlignCenter)
        self.button_start_testing_system = QPushButton(self.centralwidget)
        self.button_start_testing_system.setObjectName(u"button_start_testing_system")
        self.button_start_testing_system.setGeometry(QRect(160, 350, 361, 61))
        self.button_start_testing_system.setFont(font)
        self.check_box_syn_flood = QCheckBox(self.centralwidget)
        self.check_box_syn_flood.setObjectName(u"check_box_syn_flood")
        self.check_box_syn_flood.setGeometry(QRect(60, 140, 231, 51))
        font1 = QFont()
        font1.setPointSize(18)
        self.check_box_syn_flood.setFont(font1)
        self.check_box_udp_flood = QCheckBox(self.centralwidget)
        self.check_box_udp_flood.setObjectName(u"check_box_udp_flood")
        self.check_box_udp_flood.setGeometry(QRect(60, 200, 231, 41))
        self.check_box_udp_flood.setFont(font1)
        self.check_box_brute_force = QCheckBox(self.centralwidget)
        self.check_box_brute_force.setObjectName(u"check_box_brute_force")
        self.check_box_brute_force.setGeometry(QRect(60, 250, 251, 61))
        self.check_box_brute_force.setFont(font1)
        self.check_box_arp_spoofing = QCheckBox(self.centralwidget)
        self.check_box_arp_spoofing.setObjectName(u"check_box_arp_spoofing")
        self.check_box_arp_spoofing.setGeometry(QRect(330, 140, 261, 51))
        self.check_box_arp_spoofing.setFont(font1)
        self.check_box_dhcp_spoofing = QCheckBox(self.centralwidget)
        self.check_box_dhcp_spoofing.setObjectName(u"check_box_dhcp_spoofing")
        self.check_box_dhcp_spoofing.setGeometry(QRect(330, 200, 311, 41))
        self.check_box_dhcp_spoofing.setFont(font1)
        self.check_box_dhcp_starvation = QCheckBox(self.centralwidget)
        self.check_box_dhcp_starvation.setObjectName(u"check_box_dhcp_starvation")
        self.check_box_dhcp_starvation.setGeometry(QRect(330, 250, 311, 61))
        self.check_box_dhcp_starvation.setFont(font1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 700, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Attack-vv", None))
        self.label_select_the_attacks.setText(QCoreApplication.translate("MainWindow", u"Select the attacks that will analyze the security of the system", None))
        self.button_start_testing_system.setText(QCoreApplication.translate("MainWindow", u"Start testing system", None))
        self.check_box_syn_flood.setText(QCoreApplication.translate("MainWindow", u"Syn flood attack", None))
        self.check_box_udp_flood.setText(QCoreApplication.translate("MainWindow", u"Udp flood attack", None))
        self.check_box_brute_force.setText(QCoreApplication.translate("MainWindow", u"Brute force attack", None))
        self.check_box_arp_spoofing.setText(QCoreApplication.translate("MainWindow", u"Arp spoofing attack", None))
        self.check_box_dhcp_spoofing.setText(QCoreApplication.translate("MainWindow", u"Dhcp spoofing attack", None))
        self.check_box_dhcp_starvation.setText(QCoreApplication.translate("MainWindow", u"Dhcp starvation attack", None))
    # retranslateUi

