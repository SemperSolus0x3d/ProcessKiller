from datetime import datetime
from psutil import (
    Process,
    NoSuchProcess,
    AccessDenied
)

from traceback import format_exception_only

class ProcessKillService:
    def kill_processes(self, processes: list[Process]):
        for process in processes:
            try:
                process.kill()
                self._report_kill(process.name())
            except AccessDenied as ex:
                print(f'ERROR: {format_exception_only(ex)[0]}')
            except NoSuchProcess:
                pass

    def _report_kill(self, process_name):
        datetime_str = datetime.strftime(
            datetime.now(), '%H:%M:%S.%f'
        )

        print(f'[{datetime_str}] Killed {process_name} process')
