from typing import Optional
import polars as pl
from polars.type_aliases import IntoExpr
from polars.utils.udfs import _get_shared_lib_location

from polars_fuzzy_match.util import parse_into_expr

lib = _get_shared_lib_location(__file__)


def fuzzy_match(
    expr: IntoExpr,
    needle: str,
    *,
    normalize=True,
    ignore_case=True,
    prefer_prefix=False,
    match_paths=False
) -> pl.Expr:
    expr = parse_into_expr(expr)
    return expr.register_plugin(
        lib=lib,
        symbol="fuzzy_match",
        is_elementwise=True,
        kwargs={
            "needle": needle,
            "normalize": normalize,
            "ignore_case": ignore_case,
            "prefer_prefix": prefer_prefix,
            "match_paths": match_paths,
        },
    )
