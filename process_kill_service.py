import logging as log
from datetime import datetime
from psutil import (
    Process,
    NoSuchProcess,
    AccessDenied
)

class ProcessKillService:
    def kill_processes(self, processes: list[Process]):
        for process in processes:
            try:
                process.kill()
                log.info(f'Killed process: {process.name()}')
            except AccessDenied as ex:
                log.error(f'Access denied while killing process: {process.name}')
            except NoSuchProcess:
                pass
