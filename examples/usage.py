import polars as pl
from polars_fuzzy_match import noop


def main():
    df = pl.DataFrame(
        {
            "strs": ["foo", "bar", "quz"],
        }
    )
    out = df.with_columns(noop(pl.col("strs")).name.suffix("_noop"))
    print(out)


if __name__ == "__main__":
    main()
