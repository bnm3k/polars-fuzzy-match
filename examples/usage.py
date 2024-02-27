import polars as pl
from polars_fuzzy_match import fuzzy_match


def main():
    df = pl.DataFrame(
        {
            "strs": ["foo", "barz", "quz", "barfoo", "foro"],
        }
    )
    needle = "foo"
    out = (
        df.with_columns(score=fuzzy_match(pl.col("strs"), needle))
        .filter(pl.col("score").is_not_null())
        .sort(by="score", descending=True)
    )
    print(out)


if __name__ == "__main__":
    main()
