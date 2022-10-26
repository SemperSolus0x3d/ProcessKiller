import re
import toml
import inject

from config import Config
from predicates_construction_service import PredicatesConstructionService

CONFIG_FILE = 'config.toml'

class ConfigService:
    @inject.autoparams()
    def __init__(
        self,
        predicate_construction_service: PredicatesConstructionService
    ):
        self.config = Config()

        self._predicate_construction_service = predicate_construction_service
        self._raw_config = self._read_config()

        self._validate_config()
        self._parse_interval()
        self._construct_predicates()
        self._construct_ignores()

    def _read_config(self):
        try:
            return toml.load(CONFIG_FILE)
        except FileNotFoundError as ex:
            raise RuntimeError(f'Config file {CONFIG_FILE} not found') from ex

    def _validate_config(self):
        self._validate_interval()

    def _validate_interval(self):
        interval = self._raw_config['interval']
        regex = r'([0-9.]+s)?([0-9.]+m)?([0-9.]+h)?'

        if re.fullmatch(regex, interval) is None:
            raise ValueError(f'Invalid interval: {interval}')

    def _parse_interval(self):
        interval_str = self._raw_config['interval']

        seconds = self._parse_interval_component(interval_str, 's')
        minutes = self._parse_interval_component(interval_str, 'm')
        hours   = self._parse_interval_component(interval_str, 'h')

        minutes += hours * 60
        seconds += minutes * 60

        self.config.interval = seconds


    def _parse_interval_component(self, interval_str, component):
        match = re.search(rf'([0-9.]+){component}', interval_str)

        return float(match.group(1)) if match is not None else 0.

    def _construct_predicates(self):
        service = self._predicate_construction_service
        self.config.predicates = \
            service.construct_predicates(self._raw_config['predicates'])

    def _construct_ignores(self):
        service = self._predicate_construction_service
        self.config.ignores = \
            service.construct_ignores(self._raw_config['ignores'])
