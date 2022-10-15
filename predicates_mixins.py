import re
import fnmatch
from psutil import Process

class ByNamePredicateMixin:
    def __init__(self, name):
        self._name = self._init_predicate_value(name)

    def _get_predicate_value(self):
        return self._name

    def _get_value(self, process: Process):
        return process.name()

class ByCmdLinePredicateMixin:
    def __init__(self, cmd):
        self._cmd = self._init_predicate_value(cmd)

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

    def _init_predicate_value(self, value):
        return value

class RegexPredicateMixin:
    def match(self, process: Process):
        value = self._get_value(process)
        regex = self._get_predicate_value()
        return regex.fullmatch(value) is not None

    def _init_predicate_value(self, value):
        return re.compile(value)

class GlobPatternPredicateMixin(RegexPredicateMixin):
    def _init_predicate_value(self, value):
        return re.compile(fnmatch.translate(value))
