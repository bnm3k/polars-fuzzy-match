use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use pyo3_polars::export::polars_core::utils::CustomIterTools;
use serde::Deserialize;

#[derive(Deserialize)]
struct FuzzyMatchKwargs {
    needle: String,
}

// exact match
#[polars_expr(output_type=Boolean)]
fn fuzzy_match(haystack: &[Series], kwargs: FuzzyMatchKwargs) -> PolarsResult<Series> {
    let ca = (&haystack[0]).str()?;
    let needle = kwargs.needle;
    let out: BooleanChunked = ca
        .into_iter()
        .map(|v: Option<&str>| {
            if let Some(s) = v {
                Some(s == &needle)
            } else {
                None
            }
        })
        .collect_trusted();

    Ok(out.into_series())
}
