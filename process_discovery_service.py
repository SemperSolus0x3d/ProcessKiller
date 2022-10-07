import psutil

from predicates import Predicate

class ProcessDiscoveryService:
    def __init__(self, predicates: list[Predicate]):
        self._predicates = predicates

    def get_matching_processes(self) -> list[psutil.Process]:
        processes = []

        for process in psutil.process_iter():
            for pred in self._predicates:
                if pred.match(process):
                    processes.append(process)

        return processes
