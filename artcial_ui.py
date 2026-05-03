# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'artcial_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(833, 625)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 20, 121, 41))
        self.pushButton_log = QPushButton(Dialog)
        self.pushButton_log.setObjectName(u"pushButton_log")
        self.pushButton_log.setGeometry(QRect(180, 20, 91, 31))
        self.pushButton_reg = QPushButton(Dialog)
        self.pushButton_reg.setObjectName(u"pushButton_reg")
        self.pushButton_reg.setGeometry(QRect(320, 20, 91, 31))
        self.pushButton_opfile = QPushButton(Dialog)
        self.pushButton_opfile.setObjectName(u"pushButton_opfile")
        self.pushButton_opfile.setGeometry(QRect(50, 80, 341, 31))
        self.label_user_name = QLabel(Dialog)
        self.label_user_name.setObjectName(u"label_user_name")
        self.label_user_name.setGeometry(QRect(490, 40, 181, 21))
        self.lineEdit_title = QLineEdit(Dialog)
        self.lineEdit_title.setObjectName(u"lineEdit_title")
        self.lineEdit_title.setGeometry(QRect(150, 180, 471, 20))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u9759\u6001\u535a\u5ba2\u7ba1\u7406\u7cfb\u7edf", None))
        self.pushButton_log.setText(QCoreApplication.translate("Dialog", u"\u767b\u5f55", None))
        self.pushButton_reg.setText(QCoreApplication.translate("Dialog", u"\u6ce8\u518c", None))
        self.pushButton_opfile.setText(QCoreApplication.translate("Dialog", u"\u6253\u5f00\u6587\u4ef6", None))
        self.label_user_name.setText(QCoreApplication.translate("Dialog", u"user_name", None))
    # retranslateUi

