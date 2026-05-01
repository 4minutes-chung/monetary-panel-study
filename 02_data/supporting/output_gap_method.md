# Output Gap Construction Note

For the short-run Phillips block, output gap is constructed from real GDP growth panel data using an annual HP filter approximation:

- country-level series sorted by year,
- log real GDP level proxied by cumulative sum of GDP growth where level is unavailable,
- HP filter smoothing parameter `lambda = 6.25` (annual frequency),
- output gap defined as `100 * (log_gdp_level - hp_trend)`.

Implementation intent in notebooks and rebuild scripts:

- require at least 10 annual observations per country to compute a stable trend,
- leave missing where country history is too short,
- use the same output-gap construction in baseline and robustness paths.

Robustness placeholder:

- Hamilton (2018) style filter can be added as a sensitivity check in a later cycle.
