# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'result_windows.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QTextBrowser, QWidget)

class Ui_ResultWindowTesting(object):
    def setupUi(self, ResultWindowTesting):
        if not ResultWindowTesting.objectName():
            ResultWindowTesting.setObjectName(u"ResultWindowTesting")
        ResultWindowTesting.resize(684, 800)
        ResultWindowTesting.setMinimumSize(QSize(684, 800))
        ResultWindowTesting.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.button_save_on_file_system = QPushButton(ResultWindowTesting)
        self.button_save_on_file_system.setObjectName(u"button_save_on_file_system")
        self.button_save_on_file_system.setGeometry(QRect(80, 670, 241, 71))
        font = QFont()
        font.setPointSize(15)
        self.button_save_on_file_system.setFont(font)
        self.button_send_on_server = QPushButton(ResultWindowTesting)
        self.button_send_on_server.setObjectName(u"button_send_on_server")
        self.button_send_on_server.setGeometry(QRect(360, 670, 231, 71))
        self.button_send_on_server.setFont(font)
        self.label_result_testing = QLabel(ResultWindowTesting)
        self.label_result_testing.setObjectName(u"label_result_testing")
        self.label_result_testing.setGeometry(QRect(240, 30, 361, 41))
        font1 = QFont()
        font1.setPointSize(24)
        self.label_result_testing.setFont(font1)
        self.text_area_result_testing = QTextBrowser(ResultWindowTesting)
        self.text_area_result_testing.setObjectName(u"text_area_result_testing")
        self.text_area_result_testing.setGeometry(QRect(80, 90, 511, 551))

        self.retranslateUi(ResultWindowTesting)

        QMetaObject.connectSlotsByName(ResultWindowTesting)
    # setupUi

    def retranslateUi(self, ResultWindowTesting):
        ResultWindowTesting.setWindowTitle(QCoreApplication.translate("ResultWindowTesting", u"Result Testing", None))
        self.button_save_on_file_system.setText(QCoreApplication.translate("ResultWindowTesting", u"Save on file system", None))
        self.button_send_on_server.setText(QCoreApplication.translate("ResultWindowTesting", u"Send on server", None))
        self.label_result_testing.setText(QCoreApplication.translate("ResultWindowTesting", u"Result Testing", None))
    # retranslateUi

