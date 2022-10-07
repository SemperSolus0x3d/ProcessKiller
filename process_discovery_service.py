import psutil

from predicates import Predicate

class ProcessDiscoveryService:
    def __init__(self, predicates: list[Predicate], ignores: list[Predicate]):
        self._predicates = predicates
        self._ignores = ignores

    def get_matching_processes(self) -> list[psutil.Process]:
        processes = []

        for process in psutil.process_iter():
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

    def _should_be_included(self, process: psutil.Process):
        return self._is_matching(process) and not self._is_ignored(process)
