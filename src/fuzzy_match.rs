use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use pyo3_polars::export::polars_core::utils::CustomIterTools;

// if len of str is less than or equal to 3, return True
// otherwise return false
#[polars_expr(output_type=Boolean)]
fn fuzzy_match(inputs: &[Series]) -> PolarsResult<Series> {
    let ca = (&inputs[0]).str()?;
    let out: BooleanChunked = ca
        .into_iter()
        .map(|v: Option<&str>| {
            if let Some(s) = v {
                Some(s.len() <= 3)
            } else {
                None
            }
        })
        .collect_trusted();

    Ok(out.into_series())
}
