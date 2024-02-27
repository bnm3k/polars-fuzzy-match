import polars as pl
from polars_fuzzy_match import fuzzy_match


def main():
    df = pl.DataFrame(
        {
            "strs": ["foo test baaar", "foo hello-world bar"],
        }
    )
    needle = "bar"
    out = (
        df.with_columns(
            score=fuzzy_match(pl.col("strs"), needle, ignore_case=False)
        )
        .filter(pl.col("score").is_not_null())
        .sort(by="score", descending=True)
    )
    print(out)


if __name__ == "__main__":
    main()
