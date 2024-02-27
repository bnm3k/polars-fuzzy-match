import polars as pl
from polars_fuzzy_match import fuzzy_match_score


def main():
    df = pl.DataFrame(
        {
            "strs": ["foo test baaar", "foo hello-world bar"],
        }
    )
    pattern = "hello"
    out = (
        df.with_columns(score=fuzzy_match_score(pl.col("strs"), pattern))
        .filter(pl.col("score").is_not_null())
        .sort(by="score", descending=True)
    )
    print(out)


if __name__ == "__main__":
    main()
