import os
import sys
import logging
import ConfigParser


# the singleton config class
class StateManager(ConfigParser.RawConfigParser):
    is_frozen = False
    base_path = None
    config_file = None
    dialog = None
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if StateManager.__instance is None:
            StateManager()
        return StateManager.__instance

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)

        self.is_frozen = getattr(sys, 'frozen', False)
        if self.is_frozen:
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.config_file = os.path.join(self.base_path, 'config.ini')
        """ Virtually private constructor. """
        if StateManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            try:
                if os.path.exists(self.config_file):
                    self.readfp(open(self.config_file))
                else:
                    self._create_config()
                    self.readfp(open(self.config_file))
            except ConfigParser.ParsingError:
                self._create_config()

            StateManager.__instance = self

    def _create_config(self):
        for section in self.sections():
            self._remove_section(section)
        with open(self.config_file, "wb") as config_file:
            self.write(config_file)

    def _write_config(self, section, option, value):
        with open(self.config_file, "wb") as config_file:
            self.set(section, option, value)
            self.write(config_file)

    def _remove_section(self, section):
        self.remove_section(section)

    def set_dialog(self, dialog):
        self.dialog = dialog

    def show_dialog(self):
        self.dialog.show()

    def get_service_port(self):
        serviceport = 8080
        try:
            serviceport = self.getint('SERVICE', 'port')
            if not 1024 <= serviceport <= 65535:
                serviceport = 8080
                raise ValueError('port must be 1024-65535')
        except ConfigParser.NoSectionError:
            self.add_section('SERVICE')
            self._write_config('SERVICE', 'port', serviceport)
        except ConfigParser.NoOptionError:
            self._write_config('SERVICE', 'port', serviceport)
        except ValueError:
            self._write_config('SERVICE', 'port', serviceport)

        return serviceport

    def get_log_level(self):
        loglevel = 'ERROR'
        try:
            loglevel = self.get('LOG', 'level')
            all_levels = [fmt for fmt in logging._levelNames if isinstance(fmt, str)]
            if loglevel.upper() not in all_levels:
                loglevel = 'ERROR'
                self._write_config('LOG', 'level', loglevel)
        except ConfigParser.NoSectionError:
            self.add_section('LOG')
            self._write_config('LOG', 'level', loglevel)
        except ConfigParser.NoOptionError:
            self._write_config('LOG', 'level', loglevel)

        return loglevel

    def get_log_name(self):
        logname = 'odoo.log'
        try:
            logname = self.get('LOG', 'name')
        except ConfigParser.NoSectionError:
            self.add_section('LOG')
            self._write_config('LOG', 'name', logname)
        except ConfigParser.NoOptionError:
            self._write_config('LOG', 'name', logname)

        return logname

    def get_log_file(self):
        logpath = os.path.join(self.base_path, 'logs')
        if not os.path.exists(logpath):
            os.makedirs(logpath)
        logfile = os.path.join(logpath, self.get_log_name())
        return logfile
