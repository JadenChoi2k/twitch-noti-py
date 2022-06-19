import configparser
from config.app.const import CONFIG_FILE_NAME, APP_CONFIG_CONSTANTS, APP_DEFAULT_SETTINGS, VALUE_PARSER


class AppConfiguration:
    # singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._cp = configparser.ConfigParser()
        # if not file exist
        if not self._cp.read(CONFIG_FILE_NAME):
            self.set_default_and_save()
        # if invalid config value
        if not self.validate_config():
            self.set_default_and_save()

    def validate_config(self):
        cp_section_names = self._cp.sections()
        for section_name, config_dict in APP_CONFIG_CONSTANTS.items():
            if section_name not in cp_section_names:
                return False
            section = self._cp[section_name]
            for k, v in config_dict.items():
                cp_val = section.get(k)
                if not cp_val:
                    return False
                try:
                    cp_val = int(cp_val)
                except (ValueError, TypeError):
                    return False
                if not (0 <= cp_val < len(v)):
                    return False
        return True

    def set_default_and_save(self):
        self._cp.read_dict(APP_DEFAULT_SETTINGS)
        self.save()

    def save(self):
        with open(CONFIG_FILE_NAME, 'w') as f:
            self._cp.write(f)

    def update(self, update_dict: dict):
        for sec, option_dict in update_dict.items():
            if sec not in self._cp.sections():
                raise AttributeError('not exist section')
            if not isinstance(option_dict, dict):
                raise TypeError('option type must be dict')
            for opt, idx in option_dict.items():
                try:
                    idx = int(idx)
                except (ValueError, TypeError):
                    raise TypeError('option value must be index of list')
                if idx >= len(APP_CONFIG_CONSTANTS[sec][opt]):
                    raise IndexError('option index out of range')
                self._cp[sec][opt] = idx

    def get(self, section, option):
        idx = self._cp.getint(section, option)
        val = APP_CONFIG_CONSTANTS[section][option][idx]
        parser = VALUE_PARSER[section][option]
        return parser(val)
