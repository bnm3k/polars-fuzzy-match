use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use pyo3_polars::export::polars_core::utils::CustomIterTools;

use nucleo::Utf32Str;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
struct FuzzyMatchKwargs {
    needle: String,
}

#[polars_expr(output_type=UInt32)]
fn fuzzy_match(haystack: &[Series], kwargs: FuzzyMatchKwargs) -> PolarsResult<Series> {
    let ca = (&haystack[0]).str()?;

    let mut nucleo = nucleo::Matcher::new(nucleo::Config::DEFAULT.match_paths());
    let needle = Utf32Str::Ascii(kwargs.needle.as_bytes());
    let mut buf = Vec::new();
    let out: UInt32Chunked = ca
        .into_iter()
        .map(|v: Option<&str>| {
            if let Some(s) = v {
                let haystack = Utf32Str::new(s, &mut buf);
                nucleo.fuzzy_match(haystack, needle).map(|v| v as u32)
            } else {
                None
            }
        })
        .collect_trusted();
    Ok(out.into_series())
}
