import psutil
import re
from contextlib import suppress

from predicates import Predicate

class ProcessDiscoveryService:
    _skipping_regexes = []

    def __init__(self, predicates: list[Predicate], ignores: list[Predicate]):
        self._predicates = predicates
        self._ignores = ignores

        self._compile_skipping_regexes()

    def get_matching_processes(self) -> list[psutil.Process]:
        processes = []

        for process in psutil.process_iter():
            with process.oneshot():
                if self._should_be_included(process):
                    processes.append(process)

        return processes

    def _compile_skipping_regexes(self):
        self._skipping_regexes = [re.compile(x) for x in [
            r'NT AUTHORITY\\SYSTEM',
            r'NT VIRTUAL MACHINE\\.*'
        ]]

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
        username = process.username()

        for pattern in self._skipping_regexes:
            if pattern.fullmatch(username) is not None:
                return True

        return False

    def _should_be_included(self, process: psutil.Process):
        with suppress(psutil.AccessDenied):
            return (
                not self._should_be_skipped(process) and
                self._is_matching(process) and
                not self._is_ignored(process)
            )

        return False
