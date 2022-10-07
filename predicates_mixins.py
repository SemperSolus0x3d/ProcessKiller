import re
from fnmatch import fnmatch
from psutil import Process

class ByNamePredicateMixin:
    def __init__(self, name):
        self._name = name

    def _get_predicate_value(self):
        return self._name

    def _get_value(self, process: Process):
        return process.name()

class ByCmdLinePredicateMixin:
    def __init__(self, cmd):
        self._cmd = cmd

    def _get_predicate_value(self):
        return self._cmd

    def _get_value(self, process: Process):
        return ' '.join(map(self._quote_str, process.cmdline()))

    def _quote_str(self, string):
        return f'"{string}"'

class VerbatimPredicateMixin:
    def match(self, process: Process):
        value = self._get_value(process)
        pred_value = self._get_predicate_value()
        return value == pred_value

class RegexPredicateMixin:
    def match(self, process: Process):
        value = self._get_value(process)
        pred_value = self._get_predicate_value()
        return re.fullmatch(pred_value, value) is not None

class GlobPatternPredicateMixin:
    def match(self, process: Process):
        value = self._get_value(process)
        pred_value = self._get_predicate_value()
        return fnmatch(value, pred_value)
