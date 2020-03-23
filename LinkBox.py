from __future__ import print_function
import sys
import signal
import logging
from PyQt5 import QtCore, QtGui, QtWidgets

from addons.hw_proxy.controllers.main import drivers
from ui.main import Ui_Dialog
from odoo.thread import WebThread
from odoo.ui import SystemTrayIcon
from static.images import xpm

from state import StateManager
from devices import FindPrinters


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


class LinkBox(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(LinkBox, self).__init__(parent)
        self.state = StateManager.getInstance()
        self.state.set_dialog(self)
        self.setupUi(self)
        self._register_thread()
        self._register_signal()

        # attribute registration
        self.printer_zpl_model = QtGui.QStandardItemModel()
        self.printer_escpos_model = QtGui.QStandardItemModel()

        # update status
        self._init_ui()

    # --------------------------------------------------------------------------------
    # ********************* All functions shown to user is here *********************|
    # --------------------------------------------------------------------------------
    def _init_ui(self):
        # set spinbox
        self.spnPort.setValue(self.state.web_service.port)
        # set combobox
        self.cmbZPL.setModel(self.printer_zpl_model)
        self.cmbESCPOS.setModel(self.printer_escpos_model)
        # trigger printers
        self._reload_printers()
        # web_service
        self.txtPort.setText('%d' % self.state.web_service.port)

    # --------------------------------------------------------------------------------
    # ****************** All threads must register on this section ******************|
    # --------------------------------------------------------------------------------
    def _register_thread(self):
        self.web_thread = WebThread()
        self.web_thread.start()
        # run all driver
        for key in drivers.keys():
            attr_name = 'driver_%s_thread' % key
            setattr(self, attr_name, drivers[key])
            getattr(self, attr_name).start()

    # --------------------------------------------------------------------------------
    # ****************** All signals must register on this section ******************|
    # --------------------------------------------------------------------------------
    def _register_signal(self):
        self.btnClose.clicked.connect(self.on_click_button)
        self.btnApply.clicked.connect(self.on_click_button)
        self.btnReload.clicked.connect(self.on_click_button)
        self.btnTestZPL.clicked.connect(self.on_click_button)
        self.btnTestESCPOS.clicked.connect(self.on_click_button)
        self.cmbZPL.currentIndexChanged[int].connect(self.on_combobox_index_changed)
        self.cmbESCPOS.currentIndexChanged[int].connect(self.on_combobox_index_changed)
        # register signal for printer driver
        # the following section required for update printer connected status
        for key in drivers.keys():
            attr_name = 'driver_%s_thread' % key
            getattr(getattr(self, attr_name), 'printer_status_signal').connect(self.update_printer_status)

    # --------------------------------------------------------------------------------
    # ******************** Callback function for signals is here ********************|
    # --------------------------------------------------------------------------------
    def update_printer_status(self, printer_type, status):
        printer_type, status = (int(printer_type), int(status))
        if printer_type == StateManager.ZPL_PRINTER:
            zpl_printer_connected = True if status else False
            self.txtPrinterZPL.setText(self.state.printer_zpl.get_status_display())
            colorZPL = 'green' if zpl_printer_connected else 'red'
            self.txtPrinterZPL.setStyleSheet('color: %s' % colorZPL)
            self.btnTestZPL.setEnabled(zpl_printer_connected)
            return
        if printer_type == StateManager.ESCPOS_PRINTER:
            escpos_printer_connected = True if status else False
            self.txtPrinterESCPOS.setText(self.state.printer_escpos.get_status_display())
            colorESCPOS = 'green' if escpos_printer_connected else 'red'
            self.txtPrinterESCPOS.setStyleSheet('color: %s' % colorESCPOS)
            self.btnTestESCPOS.setEnabled(escpos_printer_connected)
            return

    @QtCore.pyqtSlot(int)
    def on_combobox_index_changed(self, row):
        cmbID = self.sender().objectName()
        if cmbID == 'cmbZPL':
            # prevent same printer selected
            if row > 0 and self.cmbESCPOS.currentIndex() == row:
                self.cmbESCPOS.setCurrentIndex(0)
        if cmbID == 'cmbESCPOS':
            # prevent same printer selected
            if row > 0 and self.cmbZPL.currentIndex() == row:
                self.cmbZPL.setCurrentIndex(0)
        self.changed()

    def on_click_button(self):
        btnID = self.sender().objectName()
        if btnID == 'btnClose':
            self.hide()
            return
        if btnID == 'btnApply':
            self._apply_config()
            return
        if btnID == 'btnReload':
            self._reload_printers()
            return
        if btnID == 'btnTestZPL':
            self.state.printer_zpl.print_test_request = True
            return
        if btnID == 'btnTestESCPOS':
            self.state.printer_escpos.print_test_request = True
            return

    # --------------------------------------------------------------------------------
    # *************************** Other function is here *************************** |
    # --------------------------------------------------------------------------------
    def _apply_config(self):
        for printer_type in [StateManager.ZPL_PRINTER, StateManager.ESCPOS_PRINTER]:
            printer = None
            if printer_type == StateManager.ZPL_PRINTER:
                printer = self.get_combobox_object(self.cmbZPL, self.printer_zpl_model)
            if printer_type == StateManager.ESCPOS_PRINTER:
                printer = self.get_combobox_object(self.cmbESCPOS, self.printer_escpos_model)

            if printer_type in [StateManager.ZPL_PRINTER, StateManager.ESCPOS_PRINTER] and printer:
                self.state.set_printer(printer_type, printer)

        self.btnApply.setEnabled(False)
        self._reload_printers()

    def _reload_printers(self):
        self.cmbZPL.clear()
        self.cmbESCPOS.clear()
        printers = [printer for printer in FindPrinters()]
        if self.state.printer_zpl not in printers:
            printers.append(self.state.printer_zpl)
        if self.state.printer_escpos not in printers:
            printers.append(self.state.printer_escpos)

        # add printers to combobox
        for printer in printers:
            zpl_item = QtGui.QStandardItem(printer.description)
            zpl_item.setData(printer)
            self.printer_zpl_model.appendRow(zpl_item)
            escpos_item = QtGui.QStandardItem(printer.description)
            escpos_item.setData(printer)
            self.printer_escpos_model.appendRow(escpos_item)

        self.cmbZPL.setCurrentIndex(printers.index(self.state.printer_zpl))
        self.cmbESCPOS.setCurrentIndex(printers.index(self.state.printer_escpos))

    def get_combobox_object(self, combobox, model):
        index = combobox.currentIndex()
        if index >= 0:
            return model.item(index).data()

    def changed(self):
        change_statuses = []

        for printer_type in [StateManager.ZPL_PRINTER, StateManager.ESCPOS_PRINTER]:
            ui = None
            config = None
            if printer_type == StateManager.ZPL_PRINTER:
                ui = self.get_combobox_object(self.cmbZPL, self.printer_zpl_model)
                config = self.state.printer_zpl
            if printer_type == StateManager.ESCPOS_PRINTER:
                ui = self.get_combobox_object(self.cmbESCPOS, self.printer_escpos_model)
                config = self.state.printer_escpos

            if ui and config:
                change_statuses.append(ui == config)

        self.btnApply.setEnabled(False in change_statuses)


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)

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
