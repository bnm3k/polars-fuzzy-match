use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use pyo3_polars::export::polars_core::utils::CustomIterTools;

use nucleo::Utf32Str;
use nucleo_matcher::pattern::{CaseMatching, Normalization};
use serde::Deserialize;

#[derive(Deserialize, Debug)]
struct FuzzyMatchKwargs {
    pattern: String,
}

// exact match
#[polars_expr(output_type=UInt32)]
fn fuzzy_match_score(haystack: &[Series], kwargs: FuzzyMatchKwargs) -> PolarsResult<Series> {
    let ca = (&haystack[0]).str()?;

    let pattern = {
        nucleo::pattern::Pattern::parse(&kwargs.pattern, CaseMatching::Smart, Normalization::Smart)
    };

    // config
    let config = nucleo::Config::DEFAULT;
    let mut matcher = nucleo::Matcher::new(config);
    let mut buf = Vec::new();
    let out: UInt32Chunked = ca
        .into_iter()
        .map(|v: Option<&str>| {
            if let Some(s) = v {
                let haystack = Utf32Str::new(s, &mut buf);
                pattern.score(haystack, &mut matcher).map(|v| v as u32)
            } else {
                None
            }
        })
        .collect_trusted();
    Ok(out.into_series())
}
