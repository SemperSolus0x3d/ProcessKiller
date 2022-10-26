import time

from psutil import Process

_EVICTION_TIMEOUT = 5 * 60 # 5 minutes

class _CacheEntry:
    def __init__(self, process: Process, match_result):
        self._pid = process.pid
        self._create_time = process.create_time()
        self._match_result = match_result
        self._process_hash = self._hash_process(process)
        self._update_last_usage_time()

    @property
    def key(self):
        return (self._pid, self._create_time)

    @property
    def match_result(self):
        self._update_last_usage_time()
        return self._match_result

    @property
    def last_usage_time(self):
        return self._last_usage_time

    def is_up_to_date(self, process: Process) -> bool:
        self._update_last_usage_time()
        return self._hash_process(process) == self._process_hash

    def update(self, process: Process, match_result: bool):
        self._update_last_usage_time()
        self._process_hash = self._hash_process(process)
        self._match_result = match_result

    def _hash_process(self, process: Process):
        return hash((
            process.name(),
            ' '.join(process.cmdline())
        ))

    def _update_last_usage_time(self):
        self._last_usage_time = time.time()

class ProcessCacheService:
    def __init__(self):
        self._cache: dict[tuple[int, float], _CacheEntry] = {}
        self._hits = 0
        self._misses = 0

    @property
    def hits(self):
        return self._hits

    @property
    def misses(self):
        return self._misses

    def query(self, process: Process) -> bool | None:
        key = self._create_key(process)

        if key in self._cache:
            entry = self._cache[key]
            if entry.is_up_to_date(process):
                self._hits += 1
                return entry.match_result

        self._misses += 1

    def update(self, process: Process, match_result: bool):
        key = self._create_key(process)

        if key in self._cache:
            entry = self._cache[key]
            entry.update(process, match_result)
        else:
            self._cache[key] = _CacheEntry(process, match_result)

    def evict(self):
        keys_to_delete = []

        for k, v in self._cache.items():
            if time.time() - v.last_usage_time >= _EVICTION_TIMEOUT:
                keys_to_delete.append(k)

        for key in keys_to_delete:
            del self._cache[key]

    def reset_statistics(self):
        self._hits = 0
        self._misses = 0

    def _create_key(self, process: Process):
        return (process.pid, process.create_time())
