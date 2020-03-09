# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(640, 640)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.formLayout = QtGui.QFormLayout(self.frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.groupBox = QtGui.QGroupBox(self.frame)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(64, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setMinimumSize(QtCore.QSize(64, 0))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cmbThermal = QtGui.QComboBox(self.groupBox)
        self.cmbThermal.setMinimumSize(QtCore.QSize(250, 0))
        self.cmbThermal.setObjectName(_fromUtf8("cmbThermal"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmbThermal)
        self.cmbLabel = QtGui.QComboBox(self.groupBox)
        self.cmbLabel.setMinimumSize(QtCore.QSize(250, 0))
        self.cmbLabel.setObjectName(_fromUtf8("cmbLabel"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmbLabel)
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.frame)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setMinimumSize(QtCore.QSize(64, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.spnPort = QtGui.QSpinBox(self.groupBox_2)
        self.spnPort.setMinimum(1024)
        self.spnPort.setMaximum(65535)
        self.spnPort.setProperty("value", 8080)
        self.spnPort.setObjectName(_fromUtf8("spnPort"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.spnPort)
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(self.frame)
        self.groupBox_3.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 9px;\n"
"    margin-top: 0.5em;\n"
"    background-color: #ffffff;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
"}"))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.txtPort = QtGui.QLabel(self.groupBox_3)
        self.txtPort.setObjectName(_fromUtf8("txtPort"))
        self.gridLayout.addWidget(self.txtPort, 0, 2, 1, 1)
        self.txtPrinterLabel = QtGui.QLabel(self.groupBox_3)
        self.txtPrinterLabel.setObjectName(_fromUtf8("txtPrinterLabel"))
        self.gridLayout.addWidget(self.txtPrinterLabel, 1, 2, 1, 1)
        self.txtPrinterThermal = QtGui.QLabel(self.groupBox_3)
        self.txtPrinterThermal.setObjectName(_fromUtf8("txtPrinterThermal"))
        self.gridLayout.addWidget(self.txtPrinterThermal, 2, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.groupBox_3)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(Dialog)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.btnReload = QtGui.QPushButton(self.frame_2)
        self.btnReload.setObjectName(_fromUtf8("btnReload"))
        self.horizontalLayout.addWidget(self.btnReload)
        self.btnApply = QtGui.QPushButton(self.frame_2)
        self.btnApply.setObjectName(_fromUtf8("btnApply"))
        self.horizontalLayout.addWidget(self.btnApply)
        self.btnClose = QtGui.QPushButton(self.frame_2)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox.setTitle(_translate("Dialog", "Printer", None))
        self.label_2.setText(_translate("Dialog", "Label", None))
        self.label_3.setText(_translate("Dialog", "Thermal", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Sevices", None))
        self.label.setText(_translate("Dialog", "Port", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Status", None))
        self.label_4.setText(_translate("Dialog", "Running Port", None))
        self.label_5.setText(_translate("Dialog", "Printer Label", None))
        self.label_6.setText(_translate("Dialog", "Printer Thermal", None))
        self.txtPort.setText(_translate("Dialog", "N/A", None))
        self.txtPrinterLabel.setText(_translate("Dialog", "N/A", None))
        self.txtPrinterThermal.setText(_translate("Dialog", "N/A", None))
        self.btnReload.setText(_translate("Dialog", "Reload", None))
        self.btnApply.setText(_translate("Dialog", "Apply", None))
        self.btnClose.setText(_translate("Dialog", "Close", None))

