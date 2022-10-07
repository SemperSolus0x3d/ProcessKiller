import re
import toml

import predicates

CONFIG_FILE = 'config.toml'

class ConfigService:
    config = None
    _default_config = {
        'interval': '1s',
        'predicates': {
            'by-name': {
                'verbatim': [],
                'regex-patterns': [],
                'glob-patterns': []
            }
        }
    }

    def __init__(self):
        self.config = self._read_config()
        self._set_defaults()
        self._validate_config()
        self._parse_interval()

    def get_interval(self):
        return self._parsed_interval

    def get_predicates(self):
        result = []

        type_by_path = {
            ('by-name', 'verbatim'): predicates.VerbatimByNamePredicate,
            ('by-name', 'regex-patterns'): predicates.RegexByNamePredicate,
            ('by-name', 'glob-patterns'): predicates.GlobByNamePredicate
        }

        predicates_dict = self.config['predicates']

        for path, type in type_by_path.items():
            for pred in self._get_predicates_by_path(predicates_dict, path):
                result.append(type(pred))

        return result

    def _get_predicates_by_path(
        self,
        dictionary,
        path: tuple[str]
    ):
        if len(path) == 1:
            return dictionary[path[0]]
        else:
            return self._get_predicates_by_path(
                dictionary[path[0]], path[1:]
            )

    def _read_config(self):
        try:
            return toml.load(CONFIG_FILE)
        except FileNotFoundError as ex:
            raise RuntimeError(f'Config file {CONFIG_FILE} not found') from ex

    def _set_defaults(self):
        self._set_defaults_recursive(self.config, ())

    def _set_defaults_recursive(self, dictionary, keys):
        self._set_defaults_to_dict(keys)

        for k, v in dictionary.items():
            if isinstance(v, dict):
                self._set_defaults_recursive(v, keys + (k,))

    def _set_defaults_to_dict(self, keys):
        defaults = self._default_config
        config = self.config

        for key in keys:
            defaults = defaults[key]
            config = config[key]
        
        for k, v in defaults.items():
            config.setdefault(k, v)

    def _validate_config(self):
        self._validate_interval()

    def _validate_interval(self):
        interval = self.config['interval']
        regex = r'([0-9]+s)?([0-9]+m)?([0-9]+h)?'

        if re.fullmatch(regex, interval) is None:
            raise ValueError(f'Invalid interval: {interval}')

    def _parse_interval(self):
        interval_str = self.config['interval']

        seconds = self._parse_interval_component(interval_str, 's')
        minutes = self._parse_interval_component(interval_str, 'm')
        hours   = self._parse_interval_component(interval_str, 'h')

        minutes += hours * 60
        seconds += minutes * 60

        self._parsed_interval = seconds


    def _parse_interval_component(self, interval_str, component):
        match = re.search(rf'([0-9.]+){component}', interval_str)

        return float(match.group(1)) if match is not None else 0.
