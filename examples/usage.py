import polars as pl
from polars_fuzzy_match import fuzzy_match


def main():
    df = pl.DataFrame(
        {
            "strs": ["foo", "barz", "quz"],
        }
    )
    out = df.with_columns(is_hit=fuzzy_match(pl.col("strs")))
    print(out)


if __name__ == "__main__":
    main()
