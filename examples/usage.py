import polars as pl
from polars_fuzzy_match import fuzzy_match_score, Normalization


def main():
    df = pl.DataFrame(
        {
            "strs": ["aaa", "aää"],
        }
    )
    pattern = "aaa"
    out = (
        df.with_columns(
            score=fuzzy_match_score(
                pl.col("strs"), pattern, normalization=Normalization.SMART
            )
        )
        .filter(pl.col("score").is_not_null())
        .sort(by="score", descending=True)
    )
    print(out)


if __name__ == "__main__":
    main()
