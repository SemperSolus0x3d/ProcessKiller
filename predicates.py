from predicates_mixins import (
    ByNamePredicateMixin,
    VerbatimPredicateMixin,
    RegexPredicateMixin,
    GlobPatternPredicateMixin
)

PREDICATE_TYPE_BY_PATH = {}

_MIXIN_CONFIG_NAME_BY_BY_XXX_MIXIN = {
    ByNamePredicateMixin: 'by-name'
}

_MIXIN_CONFIG_NAME_BY_OTHER_MIXIN = {
    VerbatimPredicateMixin: 'verbatim',
    RegexPredicateMixin: 'regex-patterns',
    GlobPatternPredicateMixin: 'glob-patterns'
}

class Predicate:
    def match(self, _):
        raise Exception('Not supported')

for by_xxx_mixin, by_xxx_mixin_config_name in _MIXIN_CONFIG_NAME_BY_BY_XXX_MIXIN.items():
    for other_mixin, other_mixin_config_name in _MIXIN_CONFIG_NAME_BY_OTHER_MIXIN.items():

        def constructor(self, predicate_value):
            by_xxx_mixin.__init__(self, predicate_value)

        key = (by_xxx_mixin_config_name, other_mixin_config_name)
        name = f'{other_mixin.__name__}{by_xxx_mixin.__name__}Predicate'
        bases = (by_xxx_mixin, other_mixin, Predicate)
        attributes = { '__init__': constructor }

        PREDICATE_TYPE_BY_PATH[key] = type(name, bases, attributes)
