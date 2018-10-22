import sys
import time
import json
import usb

from bottle import response, request, route, run, hook

from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import QApplication, QMainWindow


class PrintingThread(QThread):

    def connected_usb_devices(self):
        connected = []

        # printers can either define bDeviceClass=7, or they can define one of
        # their interfaces with bInterfaceClass=7. This class checks for both.
        class FindUsbClass(object):
            def __init__(self, usb_class):
                self._class = usb_class
            def __call__(self, device):
                # first, let's check the device
                if device.bDeviceClass == self._class:
                    return True
                # transverse all devices and look through their interfaces to
                # find a matching class
                for cfg in device:
                    intf = usb.util.find_descriptor(cfg, bInterfaceClass=self._class)

                    if intf is not None:
                        return True

                return False

        printers = usb.core.find(find_all=True, custom_match=FindUsbClass(7))

        # if no printers are found after this step we will take the
        # first epson or star device we can find.
        # epson
        if not printers:
            printers = usb.core.find(find_all=True, idVendor=0x04b8)
        # star
        if not printers:
            printers = usb.core.find(find_all=True, idVendor=0x0519)

        for printer in printers:
            try:
                manufacture  = usb.util.get_string(printer, printer.iManufacturer)
                product = usb.util.get_string(printer, printer.iProduct)
                description = manufacture + " " + product
            except Exception as e:
                # _logger.error("Can not get printer description: %s" % e)
                description = 'Unknown printer'
            connected.append({
                'vendor': printer.idVendor,
                'product': printer.idProduct,
                'name': description
            })

        return connected

    def run(self):
        while True:
            time.sleep(1)


class WebThread(QThread):


    @staticmethod
    @hook('after_request')
    def enable_cors():
        '''Add headers to enable CORS'''
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, X-Debug-Mode'

    @staticmethod
    @route('/', method='OPTIONS')
    @route('/<path:path>', method='OPTIONS')
    def options_handler(path=None):
        return

    @staticmethod
    @route('/hw_proxy/hello')
    def hello():
        return "ping"

    @staticmethod
    @route('/hw_proxy/handshake', method='POST')
    def handshake():
        content_type = 'application/json'
        response.content_type = content_type

        data = {
            "jsonrpc": "2.0",
        }

        if request.content_type == content_type:
            data["id"] = request.json.get('id')
            data["result"] = True
        else:
            data["result"] = False
            response.status = 400

        return json.dumps(data)

    @staticmethod
    @route('/hw_proxy/status_json', method='POST')
    def status_json():
        content_type = 'application/json'
        response.content_type = content_type

        data = {
            "jsonrpc": "2.0",
        }

        if request.content_type == content_type:
            data["id"] = request.json.get('id')
        else:
            data["result"] = False
            response.status = 400

        return json.dumps(data)

    def run(self):
        run(host='localhost', port=8080, debug=True)


class OPrint(QMainWindow):

    def __init__(self, parent=None):
        super(OPrint, self).__init__(parent)

        # web service
        self.web_thread = WebThread()
        self.web_thread.start()

        # printing service
        self.print_thread = PrintingThread()
        self.print_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OPrint()
    window.show()
    app.exec_()
