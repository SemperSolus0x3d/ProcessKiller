from psutil import Process

from predicates_mixins import (
    ByNamePredicateMixin,
    VerbatimPredicateMixin,
    RegexPredicateMixin,
    GlobPatternPredicateMixin
)

class Predicate:
    def match(self, process: Process):
        raise Exception('Not supported')

class VerbatimByNamePredicate(ByNamePredicateMixin, VerbatimPredicateMixin, Predicate):
    def __init__(self, name):
        ByNamePredicateMixin.__init__(self, name)

class RegexByNamePredicate(ByNamePredicateMixin, RegexPredicateMixin, Predicate):
    def __init__(self, name):
        ByNamePredicateMixin.__init__(self, name)

class GlobByNamePredicate(ByNamePredicateMixin, GlobPatternPredicateMixin, Predicate):
    def __init__(self, name):
        ByNamePredicateMixin.__init__(self, name)
