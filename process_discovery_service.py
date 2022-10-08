import psutil
import logging as log

from predicates import Predicate

class ProcessDiscoveryService:
    _names_to_skip = {
        'Registry',
        'LsaIso.exe',
        'MemCompression',
        'vmmem'
    }

    def __init__(self, predicates: list[Predicate], ignores: list[Predicate]):
        self._predicates = predicates
        self._ignores = ignores

    def get_matching_processes(self) -> list[psutil.Process]:
        processes = []

        for process in psutil.process_iter():
            with process.oneshot():
                if self._should_be_included(process):
                    processes.append(process)

        return processes

    def _is_matching(self, process: psutil.Process):
        result = False

        for pred in self._predicates:
            if pred.match(process):
                result = True
                break

        return result

    def _is_ignored(self, process: psutil.Process):
        result = False

        for pred in self._ignores:
            if pred.match(process):
                result = True
                break

        return result

    def _should_be_skipped(self, process: psutil.Process):
        if (
            process.status() != psutil.STATUS_RUNNING or
            process.name() in self._names_to_skip
        ):
            return True

        return False

    def _should_be_included(self, process: psutil.Process):
        try:
            return (
                not self._should_be_skipped(process) and
                self._is_matching(process) and
                not self._is_ignored(process)
            )
        except psutil.AccessDenied:
            log.error(f'Access denied while matching process: {process}')
        except psutil.NoSuchProcess:
            pass

        return False
