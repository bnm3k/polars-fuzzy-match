import polars as pl
from polars.type_aliases import IntoExpr
from polars.utils.udfs import _get_shared_lib_location

from polars_fuzzy_match.util import parse_into_expr

lib = _get_shared_lib_location(__file__)


def noop(expr: IntoExpr) -> pl.Expr:
    expr = parse_into_expr(expr)
    return expr.register_plugin(
        lib=lib,
        symbol="noop",
        is_elementwise=True,
    )
