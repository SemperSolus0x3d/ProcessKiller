import time
import traceback

from config_service import ConfigService
from process_discovery_service import ProcessDiscoveryService
from process_kill_service import ProcessKillService
from predicates_construction_service import PredicatesConstructionService

class Program:
    def __init__(self) -> None:
        self._config_service = ConfigService()
        self._process_kill_service = ProcessKillService()
        self._predicates_construction_service = PredicatesConstructionService()

        predicates, ignores = self._construct_predicates_and_ignores()

        self._process_discovery_service = \
            ProcessDiscoveryService(predicates, ignores)


    def run(self):
        interval = self._config_service.get_interval()

        while True:
            processes = self._process_discovery_service.get_matching_processes()
            self._process_kill_service.kill_processes(processes)

            time.sleep(interval)

    def _construct_predicates_and_ignores(self):
        predicates_dict = self._config_service.config['predicates']
        ignores_dict = self._config_service.config['ignores']

        predicates = (self._predicates_construction_service.
            construct_predicates(predicates_dict))

        ignores = (self._predicates_construction_service.
            construct_predicates(ignores_dict))

        return (predicates, ignores)

if __name__ == '__main__':
    try:
        Program().run()
    except KeyboardInterrupt:
        print('Keyboard interrupt received. Exiting gracefully')
    except Exception as ex:
        print(f'FATAL: {traceback.format_exception_only(ex)}')
        input()
