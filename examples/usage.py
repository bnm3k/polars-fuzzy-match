import polars as pl
from polars_fuzzy_match import fuzzy_match_score


df = pl.DataFrame(
    {
        'strs': ['foo', 'foo quz BAR', 'baaarfoo', 'quz'],
    }
)
pattern = 'bar'
out = (
    df.with_columns(
        score=fuzzy_match_score(
            pl.col('strs'),
            pattern,
        )
    )
    .filter(pl.col('score').is_not_null())
    .sort(by='score', descending=True)
)
print(out)
