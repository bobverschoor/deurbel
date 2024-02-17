import logging
import os
import tomllib


class ConfigurationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Configuration:
    DEURBEL_KNOP = 'deurbel_knop'
    DEURBEL_GONG = 'deurbel_gong'
    MESSENGER = 'messenger'
    ENABLED = 'enabled'

    def __init__(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "rb") as f:
                    self._config = tomllib.load(f)
            except tomllib.TOMLDecodeError as e:
                raise ConfigurationException("Config script: " + filename + " has an invalid syntax: " + str(e))
        else:
            raise ConfigurationException("Unable to find: " + filename)
        self._modules = self._config["modules"]

    def get_log_filename(self):
        if "main" in self._config and "logfile" in self._config["main"]:
            return self._config["main"]["logfile"]
        else:
            raise ConfigurationException("Unable to find logfile in main section")

    def get_active_module_names(self):
        active_modules = []
        for modulenaam in self._modules:
            if self._config['modules'][modulenaam]["enabled"]:
                active_modules.append(modulenaam)
        return active_modules

    def get_module(self, name):
        if name in self._modules:
            return self._modules[name]
        else:
            return {name: {'enabled': False}}
