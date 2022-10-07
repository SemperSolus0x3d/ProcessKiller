from psutil import Process

from predicates_mixins import (
    ByNamePredicate,
    VerbatimPredicate,
    RegexPredicate,
    GlobPatternPredicate
)

class Predicate:
    def match(self, process: Process):
        raise Exception('Not supported')

class VerbatimByNamePredicate(ByNamePredicate, VerbatimPredicate, Predicate):
    def __init__(self, name):
        ByNamePredicate.__init__(self, name)

class RegexByNamePredicate(ByNamePredicate, RegexPredicate, Predicate):
    def __init__(self, name):
        ByNamePredicate.__init__(self, name)

class GlobByNamePredicate(ByNamePredicate, GlobPatternPredicate, Predicate):
    def __init__(self, name):
        ByNamePredicate.__init__(self, name)
