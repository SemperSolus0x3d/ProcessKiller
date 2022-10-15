import sys
import time
import traceback
import inject
import logging as log

from di_configurer import DIConfigurer
from config import Config
from process_kill_service import ProcessKillService
from process_discovery_service import ProcessDiscoveryService
from utils import log_execution_time

class Program:
    @inject.autoparams()
    def __init__(
        self,
        config: Config,
        process_kill_service: ProcessKillService,
        process_discovery_service: ProcessDiscoveryService
    ) -> None:
        self._config = config
        self._process_kill_service = process_kill_service
        self._process_discovery_service = process_discovery_service

    def run(self):
        interval = self._config.interval

        while True:
            self._run_iteration()
            time.sleep(interval)

    @log_execution_time
    def _run_iteration(self):
        processes = self._process_discovery_service.get_matching_processes()
        self._process_kill_service.kill_processes(processes)

def configure_logging():
    log.basicConfig(
        format='{asctime} [{levelname}]: {message}',
        style='{',
        level=log.INFO,
        stream=sys.stderr
    )

if __name__ == '__main__':
    try:
        configure_logging()
        DIConfigurer().configure()
        Program().run()
    except KeyboardInterrupt:
        log.info('Keyboard interrupt received. Exiting gracefully')
    except Exception as ex:
        log.critical(f'{traceback.format_exception_only(ex)}')
        input()
