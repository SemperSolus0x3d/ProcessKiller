import predicates

class PredicatesConstructionService:
    _predicate_type_by_path = {
        ('by-name', 'verbatim'): predicates.VerbatimByNamePredicate,
        ('by-name', 'regex-patterns'): predicates.RegexByNamePredicate,
        ('by-name', 'glob-patterns'): predicates.GlobByNamePredicate
    }

    def construct_predicates(self, predicates_dict):
        return self._do_construct_predicates(predicates_dict)

    def construct_ignores(self, ignores_dict):
        return self._do_construct_predicates(ignores_dict)

    def _do_construct_predicates(self, predicates_dict):
        result = []

        for path, type in self._predicate_type_by_path.items():
            for pred in self._get_predicates_by_path(predicates_dict, path):
                result.append(type(pred))

        return result

    def _get_predicates_by_path(
        self,
        dictionary,
        path: tuple[str]
    ):
        if len(path) == 1:
            return dictionary[path[0]]
        else:
            return self._get_predicates_by_path(
                dictionary[path[0]], path[1:]
            )
