import time
import traceback

from config_service import ConfigService
from process_discovery_service import ProcessDiscoveryService
from process_kill_service import ProcessKillService

class Program:
    def __init__(self) -> None:
        self._config_service = ConfigService()
        self._process_kill_service = ProcessKillService()

        predicates = self._config_service.config.predicates
        ignores = self._config_service.config.ignores

        self._process_discovery_service = \
            ProcessDiscoveryService(predicates, ignores)


    def run(self):
        interval = self._config_service.config.interval

        while True:
            processes = self._process_discovery_service.get_matching_processes()
            self._process_kill_service.kill_processes(processes)

            time.sleep(interval)

if __name__ == '__main__':
    try:
        Program().run()
    except KeyboardInterrupt:
        print('Keyboard interrupt received. Exiting gracefully')
    except Exception as ex:
        print(f'FATAL: {traceback.format_exception_only(ex)}')
        input()
