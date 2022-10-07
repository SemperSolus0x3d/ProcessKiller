from predicates_mixins import (
    ByNamePredicateMixin,
    ByCmdLinePredicateMixin,
    VerbatimPredicateMixin,
    RegexPredicateMixin,
    GlobPatternPredicateMixin
)

PREDICATE_TYPE_BY_PATH = {}

_MIXIN_CONFIG_NAME_BY_BY_XXX_MIXIN = {
    ByNamePredicateMixin: 'by-name',
    ByCmdLinePredicateMixin: 'by-cmd-line'
}

_MIXIN_CONFIG_NAME_BY_OTHER_MIXIN = {
    VerbatimPredicateMixin: 'verbatim',
    RegexPredicateMixin: 'regex-patterns',
    GlobPatternPredicateMixin: 'glob-patterns'
}

class Predicate:
    def match(self, _):
        raise Exception('Not supported')

def _strip_suffix(name: str):
    return name.removesuffix('PredicateMixin')

for by_xxx_mixin, by_xxx_mixin_config_name in _MIXIN_CONFIG_NAME_BY_BY_XXX_MIXIN.items():
    for other_mixin, other_mixin_config_name in _MIXIN_CONFIG_NAME_BY_OTHER_MIXIN.items():
        def _dummy():
            global PREDICATE_TYPE_BY_PATH

            by_xxx_mixin_copy = by_xxx_mixin

            def constructor(self, predicate_value):
                by_xxx_mixin_copy.__init__(self, predicate_value)

            name = (
                f'{_strip_suffix(other_mixin.__name__)}'
                f'{_strip_suffix(by_xxx_mixin.__name__)}'
                'Predicate'
            )

            key = (by_xxx_mixin_config_name, other_mixin_config_name)
            bases = (by_xxx_mixin, other_mixin, Predicate)
            attributes = { '__init__': constructor }

            PREDICATE_TYPE_BY_PATH[key] = type(name, bases, attributes)

        _dummy()
