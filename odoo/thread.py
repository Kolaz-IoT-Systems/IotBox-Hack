from bottle import Bottle
from odoo.http import EnableCors, Controller
from PyQt4.QtCore import QThread


class Thread(QThread):

    def lockedstart(self):
        if not self.isRunning():
            self.start()


class WebThread(Thread):

    def run(self):
        app = Bottle()

        # register all controller
        controllers = [cls() for cls in Controller.__subclasses__()]
        for controller in controllers:
            controller.register(app)

        app.install(EnableCors())
        app.run(host='localhost', port=8080, debug=False)
