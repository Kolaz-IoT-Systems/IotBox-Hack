import sys
import signal
import logging

from PyQt4 import QtCore, QtGui

from addons.hw_proxy.controllers.main import drivers
from odoo.thread import WebThread
from odoo.ui import SystemTrayIcon
from static.images import xpm
from ui.main import Ui_Dialog

from state import StateManager
from printer import FindPrinters


def setup_log():
    state = StateManager.getInstance()
    logformat = '%(asctime)s - %(funcName)s - %(levelname)s: %(message)s'

    if state.is_frozen is False:
        logging.basicConfig(
            format=logformat,
            level=state.log.level,
            handlers=[logging.StreamHandler()]
        )
    else:
        logging.basicConfig(
            format=logformat,
            level=state.log.level,
            filename=state.get_log().filename,
            filemode='a'
        )


class LinkBox(QtGui.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(LinkBox, self).__init__(parent)
        StateManager.getInstance().set_dialog(self)
        self.setupUi(self)

        self.web_thread = WebThread()
        self.web_thread.start()

        # run all driver
        for key in drivers.keys():
            drivers[key].start()

        # update status
        self.update_status()

        # button signal handlers
        self.btnClose.clicked.connect(self.on_click_button)
        self.btnApply.clicked.connect(self.on_click_button)
        self.btnReload.clicked.connect(self.on_click_button)

        # printer object handler
        self.printer_model = QtGui.QStandardItemModel()
        for printer in FindPrinters():
            printer_item = QtGui.QStandardItem(printer.description)
            printer_item.setData(printer)
            self.printer_model.appendRow(printer_item)
        self.cmbLabel.setModel(self.printer_model)
        self.cmbThermal.setModel(self.printer_model)

        # combobox signal handlers
        self.cmbLabel.currentIndexChanged[int].connect(self.on_combobox_index_changed)
        self.cmbThermal.currentIndexChanged[int].connect(self.on_combobox_index_changed)

    def update_status(self):
        self.txtPort.setText('%d' % StateManager.getInstance().web_service.port)

    @QtCore.pyqtSlot(int)
    def on_combobox_index_changed(self, row):
        cmbID = self.sender().objectName()
        if cmbID == 'cmbLabel':
            return
        if cmbID == 'cmbThermal':
            return

    def on_click_button(self):
        btnID = self.sender().objectName()
        if btnID == 'btnClose':
            self.hide()
            return
        if btnID == 'btnApply':
            cmbLabelIDx = self.cmbLabel.currentIndex()
            cmbThermalIDx = self.cmbThermal.currentIndex()
            selected_label_printer = self.printer_model.item(cmbLabelIDx).data().toPyObject()
            # selected_thermal_printer = self.printer_model.item(cmbThermalIDx).data().toPyObject()
            StateManager.getInstance().set_label_printer(selected_label_printer)
            return
        if btnID == 'btnReload':
            return


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)

    # show system try icon
    systemTryIcon = SystemTrayIcon(QtGui.QIcon(QtGui.QPixmap(xpm.icon_64)))
    systemTryIcon.show()
    # ui dialog
    dialog = LinkBox()
    dialog.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    setup_log()
    main()
