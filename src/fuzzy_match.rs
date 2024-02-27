#![allow(clippy::unused_unit)]
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use pyo3_polars::export::polars_core::utils::CustomIterTools;

use nucleo::Utf32Str;
use nucleo_matcher::pattern::{CaseMatching, Normalization};
use serde::Deserialize;

#[derive(Deserialize, Debug)]
struct FuzzyMatchKwargs {
    pattern: String,
    normalization: Option<PatternNormalization>,
    case_matching: Option<PatternCaseMatching>,
}

impl FuzzyMatchKwargs {
    fn to_pattern(&self) -> nucleo_matcher::pattern::Pattern {
        let n = {
            use PatternNormalization::*;
            match self.normalization.as_ref().unwrap_or(&Smart) {
                Smart => Normalization::Smart,
                Never => Normalization::Never,
            }
        };
        let c = {
            use PatternCaseMatching::*;
            match self.case_matching.as_ref().unwrap_or(&Smart) {
                Respect => CaseMatching::Respect,
                Ignore => CaseMatching::Ignore,
                Smart => CaseMatching::Smart,
            }
        };
        nucleo::pattern::Pattern::parse(&self.pattern, c, n)
    }
}

#[derive(Deserialize, Debug)]
pub enum PatternNormalization {
    Never,
    Smart,
}

#[derive(Deserialize, Debug)]
pub enum PatternCaseMatching {
    Respect,
    Ignore,
    Smart,
}

// exact match
#[polars_expr(output_type=UInt32)]
fn fuzzy_match_score(haystack: &[Series], kwargs: FuzzyMatchKwargs) -> PolarsResult<Series> {
    let ca = haystack[0].str()?;

    // config
    let config = nucleo::Config::DEFAULT;
    let mut matcher = nucleo::Matcher::new(config);
    let pattern = kwargs.to_pattern();
    let mut buf = Vec::new();
    let out: UInt32Chunked = ca
        .into_iter()
        .map(|v: Option<&str>| {
            if let Some(s) = v {
                let haystack = Utf32Str::new(s, &mut buf);
                pattern.score(haystack, &mut matcher)
            } else {
                None
            }
        })
        .collect_trusted();
    Ok(out.into_series())
}
