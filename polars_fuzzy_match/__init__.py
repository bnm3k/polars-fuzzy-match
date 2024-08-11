from enum import Enum
from pathlib import Path
import polars as pl
from polars.type_aliases import IntoExpr
from polars.plugins import register_plugin_function

from polars_fuzzy_match.util import parse_into_expr



class Normalization(Enum):
    """
    Enum representing different values for configuring handling of unicode
    normalization when matching against a pattern.

    Attributes:
        NEVER:
            Neither the pattern nor the string being search is normalized.
            Characters do not match against their normalized version (a != ä).

        SMART:
            The pattern is not normalized but the string being searched is
            normalized. If the pattern is 'äää' and the string being searched is
            'aaa', both do not match. However if the pattern is 'aaa' and the string
            being search is 'äää', the string is normalized to 'aaa' and then
            matched
    """

    NEVER = 'Never'
    SMART = 'Smart'

    def __str__(self) -> str:
        return self.value


class CaseMatching(Enum):
    """
    Enum representing different values for configuring case mismatch (how to
    treat uppercase and lowercase characters when searching)

    Attributes:
        RESPECT:
            the pattern matches case exactly

        IGNORE:
            both the pattern and the string being searched for the pattern
            are lowercased before carrying out the search.

        SMART:
            If the pattern contains only lowercase letters, then the string
            being search is lowercased before search. If the pattern contains
            one or more uppercase letters, the pattern matches case exactly
    """

    RESPECT = 'Respect'
    IGNORE = 'Ignore'
    SMART = 'Smart'

    def __str__(self) -> str:
        return self.value


def fuzzy_match_score(
    expr: IntoExpr,
    pattern: str,
    normalization: Normalization = Normalization.SMART,
    case_matching: CaseMatching = CaseMatching.SMART,
) -> pl.Expr:
    expr = parse_into_expr(expr)
    return register_plugin_function(
        plugin_path=Path(__file__).parent,
        function_name="fuzzy_match_score",
        is_elementwise=True,
        args=expr,
        kwargs={
            "pattern": pattern,
            "normalization": str(normalization),
            "case_matching": str(case_matching),
        },
    )

