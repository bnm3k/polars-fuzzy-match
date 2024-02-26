import polars as pl
from polars_fuzzy_match import fuzzy_match


def main():
    df = pl.DataFrame(
        {
            "strs": ["foo", "barz", "quz", "foobar", "for"],
        }
    )
    needle = "foo"
    out = df.with_columns(score=fuzzy_match(pl.col("strs"), needle))
    print(out)


if __name__ == "__main__":
    main()
