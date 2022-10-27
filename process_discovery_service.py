from typing import Generator
import psutil
import inject
import logging as log
from config import Config
from process_cache_service import ProcessCacheService

_NAMES_TO_SKIP = {
    '',
    'Secure System',
    'Registry',
    'LsaIso.exe',
    'MemCompression',
    'vmmem'
}

class ProcessDiscoveryService:
    @inject.autoparams()
    def __init__(self, config: Config, cache_service: ProcessCacheService):
        self._predicates = config.predicates
        self._ignores = config.ignores
        self._cache_service = cache_service
        self._iterations_passed = 0

    def get_matching_processes(self) -> Generator[psutil.Process, None, None]:
        for process in psutil.process_iter():
            with process.oneshot():
                if self._should_be_included(process):
                    yield process

        self._evict_cache_if_needed()
        self._log_and_reset_cache_statistics()

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
            process.name() in _NAMES_TO_SKIP
        ):
            return True

        return False

    def _match_predicates(self, process: psutil.Process):
        try:
            return (
                self._is_matching(process) and
                not self._is_ignored(process)
            )
        except psutil.AccessDenied:
            log.error(f'Access denied while matching process: {process}')
        except psutil.NoSuchProcess:
            pass

        return False

    def _should_be_included(self, process: psutil.Process):
        if self._should_be_skipped(process):
            return False

        cache_query_result = self._cache_service.query(process)

        if cache_query_result is not None:
            return cache_query_result

        match_result = self._match_predicates(process)
        self._cache_service.update(process, match_result)

        return match_result

    def _evict_cache_if_needed(self):
        self._iterations_passed += 1

        if self._iterations_passed >= 10:
            self._iterations_passed = 0
            self._cache_service.evict()

    def _log_and_reset_cache_statistics(self):
        hits = self._cache_service.hits
        misses = self._cache_service.misses
        log.debug(f'Cache statistics: hits: {hits}; misses: {misses}')
        self._cache_service.reset_statistics()
