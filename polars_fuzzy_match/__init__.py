from enum import Enum
from typing import Optional

import polars as pl
from polars.type_aliases import IntoExpr
from polars.utils.udfs import _get_shared_lib_location

from polars_fuzzy_match.util import parse_into_expr

lib = _get_shared_lib_location(__file__)


class Normalization(Enum):
    """
    For configuring handling of unicode normalization when matching against a
    pattern.

    NEVER: Neither the pattern nor the string being search is normalized.
    Characters do not match against their normalized version (a != ä).

    SMART: This is the default. The pattern is not normalized but the string being
    searched is normalized. If the pattern is 'äää' and the string being
    searched is 'aaa', it does not match. However if the pattern is 'aaa' and
    the string being search is 'äää', the string is then normalized to 'aaa'
    and then matched
    """

    NEVER = "Never"
    SMART = "Smart"

    def __str__(self) -> str:
        return self.value


class CaseMatching(Enum):
    RESPECT = "Respect"
    IGNORE = "Ignore"
    SMART = "Smart"

    """
    For configuring case mismatch between characters

    RESPECT: the pattern matches case exactly

    IGNORE: both the pattern and the string being searched for the pattern are
    converted to lowercase before carrying out the search.

    SMART:
    """

    def __str__(self) -> str:
        return self.value


def fuzzy_match_score(
    expr: IntoExpr,
    pattern: str,
    normalization: Normalization = Normalization.SMART,
    case_matching: CaseMatching = CaseMatching.SMART,
) -> pl.Expr:
    expr = parse_into_expr(expr)
    return expr.register_plugin(
        lib=lib,
        symbol="fuzzy_match_score",
        is_elementwise=True,
        kwargs={
            "pattern": pattern,
            "normalization": str(normalization),
            "case_matching": str(case_matching),
        },
    )
