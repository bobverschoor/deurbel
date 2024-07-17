from configuration import ConfigurationException
from utils.requests_wrapper import RequestWrapper, RequestException


class Esp32CamException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Esp32Cam:
    CONFIG_URL = 'url'
    CONFIG_CAPTURE_PATH = 'capture_path'
    CONFIG_CONTROL_PATH = 'control_path'
    CONFIG_STATUS_PATH = 'status_path'
    CONFIG_CONTROL_PARAMETERS = 'control_parameters'
    CONFIG_CONTROL_VARIABELE = 'var'
    CONFIG_CONTROL_VALUE = 'val'
    DEFAULT = {"xclk": 20, "pixformat": 4, "framesize": 8, "quality": 20, "brightness": 0, "contrast": 0,
               "saturation": 0, "sharpness": 0, "special_effect": 0, "wb_mode": 0, "awb": 1, "awb_gain": 1, "aec": 1,
               "aec2": 0, "ae_level": 0, "aec_value": 168, "agc": 1, "agc_gain": 0, "gainceiling": 0, "bpc": 0,
               "wpc": 1, "raw_gma": 1, "lenc": 1, "hmirror": 0, "dcw": 1, "colorbar": 0, "led_intensity": 0,
               "face_detect": 0}

    def __init__(self, config):
        self._config = config
        self._control_url = ""
        self._control_parameters = []
        self._capture_url = ""
        self._status_url = ""
        self._request = RequestWrapper(timeout=5, origin=str(self))

    def setup(self):
        try:
            self._control_url = self._config[self.CONFIG_URL] + "/" + self._config[self.CONFIG_CONTROL_PATH]
            self._capture_url = self._config[self.CONFIG_URL] + "/" + self._config[self.CONFIG_CAPTURE_PATH]
            self._status_url = self._config[self.CONFIG_URL] + "/" + self._config[self.CONFIG_STATUS_PATH]
            self.set_to_default()
            for parameter in self._config[self.CONFIG_CONTROL_PARAMETERS]:
                self._control_parameters.append(parameter)
                [(k, v)] = parameter.items()
                self.set_control_parameter(k, v)
        except KeyError as e:
            raise ConfigurationException(str(e) + " from Esp32Cam setup")
        except RequestException as e:
            raise ConfigurationException(str(e) + " from Esp32Cam setup")

    def set_to_default(self):
        current_state = self._request.http_get_json(self._status_url)
        for key, value in self.DEFAULT.items():
            if key in current_state:
                if value != current_state[key]:
                    self.set_control_parameter(key, self.DEFAULT[key])

    def set_control_parameter(self, key, value):
        parameter = {'var': key, 'val': value}
        self._request.http_get_text(self._control_url, parameters=parameter)

    def capture(self, photo_filename):
        photo_filename = photo_filename + ".jpg"
        try:
            with open(photo_filename, 'wb') as f:
                f.write(self._request.http_get_stream(self._capture_url))
        except RequestException as e:
            raise Esp32CamException(str(e) + " from Esp32Cam capture")
        return photo_filename

    def __str__(self):
        return "Esp32Cam"
