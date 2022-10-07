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
                print(f'Killed {process.name()} process')
            except AccessDenied as ex:
                print(f'ERROR: {format_exception_only(ex)[0]}')
            except NoSuchProcess:
                pass
