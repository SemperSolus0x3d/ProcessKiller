import re
from fnmatch import fnmatch
from psutil import Process

class ByNamePredicate:
    def __init__(self, name):
        self._name = name

    def _get_predicate_value(self):
        return self._name

    def _get_value(self, process: Process):
        return process.name()

class VerbatimPredicate:
    def match(self, process: Process):
        value = self._get_value(process)
        pred_value = self._get_predicate_value()
        return value == pred_value

class RegexPredicate:
    def match(self, process: Process):
        value = self._get_value(process)
        pred_value = self._get_predicate_value()
        return re.fullmatch(pred_value, value) is not None

class GlobPatternPredicate:
    def match(self, process: Process):
        value = self._get_value(process)
        pred_value = self._get_predicate_value()
        return fnmatch(value, pred_value)
