## [Main title](../README.md)
### [Interview questions](full.md)

# Statistics and Experimentation for Data Engineers
+ [Why do averages lie and how do percentiles fix that](#Why-do-averages-lie-and-how-do-percentiles-fix-that)
+ [How do you summarize a distribution with descriptive statistics](#How-do-you-summarize-a-distribution-with-descriptive-statistics)
+ [How do distributions and skew affect engineering decisions](#How-do-distributions-and-skew-affect-engineering-decisions)
+ [How do you sample data without bias](#How-do-you-sample-data-without-bias)
+ [How do you interpret a confidence interval](#How-do-you-interpret-a-confidence-interval)
+ [How do you run a t test and a proportion test](#How-do-you-run-a-t-test-and-a-proportion-test)
+ [How do you use a chi square test on categorical data](#How-do-you-use-a-chi-square-test-on-categorical-data)
+ [What do p values actually mean and how do multiple comparisons break them](#What-do-p-values-actually-mean-and-how-do-multiple-comparisons-break-them)
+ [How do you calculate statistical power and sample size](#How-do-you-calculate-statistical-power-and-sample-size)
+ [How do you design an A B test for a data platform](#How-do-you-design-an-A-B-test-for-a-data-platform)
+ [What is sample ratio mismatch and how do you detect it](#What-is-sample-ratio-mismatch-and-how-do-you-detect-it)
+ [What are guardrail metrics and novelty effects](#What-are-guardrail-metrics-and-novelty-effects)
+ [What is sequential testing and why does peeking inflate false positives](#What-is-sequential-testing-and-why-does-peeking-inflate-false-positives)
+ [Bayesian vs frequentist approaches to experiments](#Bayesian-vs-frequentist-approaches-to-experiments)
+ [How do you distinguish correlation from causation and handle confounding](#How-do-you-distinguish-correlation-from-causation-and-handle-confounding)
+ [What is Simpson's paradox](#What-is-Simpsons-paradox)
+ [How do you detect anomalies with z score IQR and MAD](#How-do-you-detect-anomalies-with-z-score-IQR-and-MAD)
+ [How do you decompose a time series into trend and seasonality](#How-do-you-decompose-a-time-series-into-trend-and-seasonality)
+ [What are stationarity and moving averages](#What-are-stationarity-and-moving-averages)
+ [How do you bootstrap a confidence interval](#How-do-you-bootstrap-a-confidence-interval)
+ [How do you plan capacity with percentiles](#How-do-you-plan-capacity-with-percentiles)
+ [How do you implement statistics in SQL](#How-do-you-implement-statistics-in-SQL)
+ [How do you implement statistics in Python with numpy pandas and scipy](#How-do-you-implement-statistics-in-Python-with-numpy-pandas-and-scipy)
+ [Real world use cases for statistics in data engineering](#Real-world-use-cases-for-statistics-in-data-engineering)

## Why do averages lie and how do percentiles fix that
Averages are dragged by the tail while percentiles describe the shape users actually feel. A p50 of 14 ms with a p99 of 900 ms means one request in a hundred is unusable even though the mean looks acceptable.

```text
latencies = [10, 12, 13, 15, 20, 900]
mean = 161.7, p50 = 14, p95 = 900, p99 = 900
```

```python
import statistics

def percentile(ordered: list[float], pct: float) -> float:
    # Nearest-rank definition: the smallest value at or above the pct-th rank.
    rank = max(1, int(-(-pct / 100 * len(ordered) // 1)))
    return ordered[rank - 1]

def summarize(values: list[float]) -> dict[str, float]:
    if not values:
        raise ValueError("empty sample")
    ordered = sorted(values)
    return {
        "n": len(ordered),
        "mean": statistics.fmean(ordered),
        "p50": percentile(ordered, 50),
        "p95": percentile(ordered, 95),
        "p99": percentile(ordered, 99),
        "max": ordered[-1],
    }
```

Interpretation: report p50 with p95 and p99, never the mean alone. Edge cases: percentiles are not additive, so p95 of a day is not the average of p95 per hour; with fewer than 100 samples p99 is the maximum; a bimodal distribution has a meaningless mean even when the tails look fine.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you summarize a distribution with descriptive statistics
Statement: before testing anything, describe center, spread, and shape. Standard deviation measures absolute spread; the coefficient of variation makes spread comparable across metrics with different units.

```text
values = [2, 4, 4, 4, 5, 5, 7, 9] -> mean 5.0, stdev 2.14, cv 0.43
```

```python
import math
import statistics

def describe(values: list[float]) -> dict[str, float]:
    n = len(values)
    if n < 2:
        raise ValueError("need at least two observations")
    mean = statistics.fmean(values)
    stdev = statistics.stdev(values)
    centered = [(value - mean) / stdev for value in values]
    skew = n / ((n - 1) * (n - 2)) * sum(c**3 for c in centered) if n > 2 else 0.0
    return {
        "n": n,
        "mean": mean,
        "median": statistics.median(values),
        "stdev": stdev,
        "variance": statistics.variance(values),
        "cv": stdev / mean if mean else math.inf,
        "min": min(values),
        "max": max(values),
        "skew": skew,
    }
```

Interpretation: compare mean and median to see skew — `mean > median` means a right tail, so a small group of large values dominates. Edge cases: `stdev` uses the sample denominator `n - 1` while `pstdev` uses `n`, and mixing them changes the answer; a zero mean makes the coefficient of variation infinite, so use it only for ratio-scale metrics; `statistics.variance` needs at least two points.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do distributions and skew affect engineering decisions
Heavy-tailed metrics break the intuition built on normal distributions. Latency, revenue per user, and file sizes are right-skewed: most values are small, a few are huge, and the mean sits above the median.

```text
normal mean == median, thin tails, 3-sigma rule applies
log-normal mean > median, heavy right tail, 3-sigma rule fails
```

```python
import math
import statistics

def compare_tail_models(values: list[float]) -> dict[str, float]:
    mean = statistics.fmean(values)
    median = statistics.median(values)
    stdev = statistics.stdev(values)
    beyond = sum(1 for value in values if abs(value - mean) > 3 * stdev) / len(values)
    logged = [math.log1p(value) for value in values]
    return {
        "mean_over_median": mean / median if median else math.inf,
        "share_beyond_3sigma": beyond,
        "logged_mean": statistics.fmean(logged),
        "logged_stdev": statistics.stdev(logged),
    }
```

Interpretation: when the mean-to-median ratio is well above 1 and the share beyond three sigma is far above the expected 0.3%, the metric is heavy-tailed. Aggregate on the log scale or on quantiles, and use medians for per-tenant comparisons. Edge cases: log of zero or negative values (`log1p` still fails on negatives); a heavy tail makes standard tests underpowered, so prefer the Mann-Whitney U test or a bootstrap; averaging ratios such as revenue per session is biased, so aggregate numerator and denominator separately.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you sample data without bias
A sample is only useful if it is representative. Simple random sampling is the default; stratified sampling guarantees coverage of small segments; and cluster sampling is for when rows arrive in groups such as files.

```text
population: 1M users, 5% enterprise
bad sample: first 10k by user_id -> 0% enterprise (ids are created in cohort order)
good sample: stratified, 2k per segment
```

```python
import random
from collections import defaultdict
from collections.abc import Iterable, Sequence
from typing import Any, TypeVar

T = TypeVar("T")

def simple_random(rows: Sequence[T], size: int, seed: int = 7) -> list[T]:
    return random.Random(seed).sample(rows, min(size, len(rows)))

def stratified(rows: Iterable[dict[str, Any]], stratum: str, per_stratum: int, seed: int = 7) -> list[dict[str, Any]]:
    buckets: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[row[stratum]].append(row)
    rng = random.Random(seed)
    return [row for bucket in buckets.values() for row in rng.sample(bucket, min(per_stratum, len(bucket)))]

```

Interpretation: fix and record the seed and the salt so the sample is reproducible and backfills do not reshuffle. Edge cases: sampling the first N rows of a time-ordered table biases toward old records; filtering the population after sampling breaks the ratio; a hash sample is consistent across jobs but is not exactly uniform at small sizes; a segment that appears in 0.1% of rows needs stratification or it disappears.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you interpret a confidence interval
A 95% confidence interval is a range that would contain the true parameter in 95% of repeated samples. It is not a 95% probability that the parameter is in this particular interval, which is the most common interview mistake.

```text
n = 100, mean = 20, stdev = 10 -> 95% CI = [18.04, 21.96]
```

```python
import math
import statistics

def ci_mean(values: list[float], z: float = 1.959964) -> tuple[float, float]:
    n = len(values)
    if n < 2:
        raise ValueError("need at least two observations")
    mean = statistics.fmean(values)
    standard_error = statistics.stdev(values) / math.sqrt(n)
    return mean - z * standard_error, mean + z * standard_error

```

Interpretation: the interval narrows with the square root of n, so quadrupling the sample halves the width. Overlapping intervals are not a valid significance test, because each interval carries its own error; run the two-sample test instead. Edge cases: the normal approximation for a proportion is unreliable when `n * p < 5`, so use Wilson or Clopper-Pearson; the z multiplier is wrong for small n, where a t distribution is needed; clustering (many rows per user) inflates the effective variance, so compute the interval on per-user aggregates.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you run a t test and a proportion test
The t test compares two means; the two-proportion z test compares two conversion rates. Both ask the same question: is the observed difference large relative to the noise?

```text
control:   mean 20.0 (n=500), treatment: mean 21.5 (n=500)
proportion: 10/100 vs 18/100 -> z = 1.63, p = 0.104
```

```python
import math

from scipy import stats

def welch_t_test(control: list[float], treatment: list[float]) -> dict[str, float]:
    # Welch does not assume equal variances, which is the safe default.
    result = stats.ttest_ind(control, treatment, equal_var=False)
    return {"t": float(result.statistic), "p_value": float(result.pvalue)}

def two_proportion_z(success_a: int, n_a: int, success_b: int, n_b: int) -> dict[str, float]:
    p_a, p_b = success_a / n_a, success_b / n_b
    pooled = (success_a + success_b) / (n_a + n_b)
    standard_error = math.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    if standard_error == 0:
        return {"z": 0.0, "p_value": 1.0}
    z = (p_b - p_a) / standard_error
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return {"z": z, "p_value": p_value, "absolute_lift": p_b - p_a}
```

Interpretation: report the effect size with the p-value; a tiny but real lift is still not worth shipping. Edge cases: the t test assumes independent observations, so repeated rows per user understate the variance; the proportion test needs at least about 5 successes and 5 failures per arm; one-sided tests double the false-positive risk if the direction was chosen after looking at the data; use the Mann-Whitney U test when the metric is heavy-tailed.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you use a chi square test on categorical data
The chi-square test compares observed counts to the counts expected under independence. It answers questions like "is the conversion rate different across channels" or "are missing values evenly distributed across tenants".

```text
             converted  not converted
control            200            800
treatment          250            750
chi2 = 8.0, dof = 1, p = 0.0047, Cramer's V = 0.063
```

```python
from scipy.stats import chi2_contingency

def chi_square(table: list[list[int]]) -> dict[str, float]:
    chi2, p_value, dof, expected = chi2_contingency(table, correction=False)
    n = sum(sum(row) for row in table)
    cramers_v = (chi2 / (n * (min(len(table), len(table[0])) - 1))) ** 0.5
    return {"chi2": float(chi2), "p_value": float(p_value), "dof": dof, "cramers_v": float(cramers_v)}

def expected_counts(table: list[list[int]]) -> list[list[float]]:
    _chi2, _p, _dof, expected = chi2_contingency(table, correction=False)
    return [[round(value, 2) for value in row] for row in expected]
```

Interpretation: Cramer's V gives effect size, since a large table makes chi-square large even for trivial associations. Edge cases: any expected cell below 5 invalidates the approximation, so merge categories or use Fisher's exact test; the test needs counts, not percentages; a significant result on a 10x10 table does not say which cell drove it, so inspect standardized residuals; repeated measures violate independence.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## What do p values actually mean and how do multiple comparisons break them
A p-value is the probability of data at least this extreme if the null hypothesis were true. It is not the probability that the null is true, and it is not the probability that a result replicates.

```text
20 independent A/A tests at alpha = 0.05 -> expect ~1 false positive
bonferroni: alpha / 20 = 0.0025 per test
```

```python
def benjamini_hochberg(p_values: list[float], alpha: float = 0.05) -> dict[str, list]:
    # Controls the false discovery rate, which is usually the right target.
    m = len(p_values)
    ranked = sorted(enumerate(p_values), key=lambda item: item[1])
    threshold_rank = 0
    for rank, (_index, p_value) in enumerate(ranked, start=1):
        if p_value <= rank / m * alpha:
            threshold_rank = rank
    rejected = [index for index, _p in ranked[:threshold_rank]]
    return {"rejected": rejected, "cutoff": ranked[threshold_rank - 1][1] if threshold_rank else None}

def bonferroni(p_values: list[float], alpha: float = 0.05) -> list[int]:
    cutoff = alpha / len(p_values)
    return [index for index, p_value in enumerate(p_values) if p_value <= cutoff]
```

Interpretation: with many metrics, always correct for multiplicity; Bonferroni controls the chance of any false positive and is conservative, while Benjamini-Hochberg controls the share of false discoveries and is the better default for dashboards. Edge cases: correlated metrics make the correction overly conservative, so a permutation test that preserves correlation is more accurate; p-values depend on sample size, so a huge dataset makes trivial differences significant; a p-value with no effect size and no confidence interval is incomplete.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you calculate statistical power and sample size
Power is the probability of detecting a real effect of a given size. Sample size, effect size, variance, and alpha trade off against each other; fixing three determines the fourth.

```text
baseline 10%, target 12%, alpha 0.05, power 0.80 -> ~3,842 per arm
baseline 10%, target 11% -> ~14,750 per arm
```

```python
import math

Z_ALPHA = 1.959964  # two-sided alpha = 0.05
Z_POWER = 0.8416212  # power = 0.80

def sample_size_proportion(p1: float, p2: float, alpha: float = 0.05, power: float = 0.8) -> int:
    z_alpha = 1.959964 if abs(alpha - 0.05) < 1e-9 else 2.5758293
    z_power = 0.8416212 if abs(power - 0.8) < 1e-9 else 1.2815516
    pooled = (p1 + p2) / 2
    numerator = (z_alpha * math.sqrt(2 * pooled * (1 - pooled)) + z_power * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(numerator / (p2 - p1) ** 2)

```

Interpretation: halving the detectable effect quadruples the sample, which is why small improvements need long experiments or a larger randomization unit. Edge cases: the formula assumes independent Bernoulli observations and understates n for ratios or clustered data; never compute power after seeing the result to justify a non-significant test (observed power is a function of the p-value); multiple metrics and repeated looks each need their own correction.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you design an A B test for a data platform
An experiment is only valid if assignment is random, stable, and independent of the metric. The randomization unit must match the unit of analysis: users for retention, sessions for click-through, clusters when users can leak between variants.

```text
unit: user_id; variants: control/treatment; hash(user_id, salt) -> bucket
```

```python
import hashlib

def assign(unit_id: str, experiment: str, buckets: int = 100, salt: str = "v1") -> int:
    digest = hashlib.sha256(f"{experiment}:{salt}:{unit_id}".encode()).hexdigest()
    return int(digest[:8], 16) % buckets

def variant(unit_id: str, experiment: str, traffic_split: float = 0.5) -> str:
    bucket = assign(unit_id, experiment)
    return "treatment" if bucket < traffic_split * 100 else "control"

```

Interpretation: specify the primary metric, the guardrails, the randomization unit, the minimum detectable effect, and the analysis window before launch; adding a metric after launch invalidates the p-value. Edge cases: the same user touching two variants contaminates the comparison; changing the salt mid-experiment reshuffles users and destroys the sample; network effects between users break the independence assumption; ramp-ups that expose heavy users first create a novelty-driven sample bias.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## What is sample ratio mismatch and how do you detect it
Sample ratio mismatch (SRM) means the observed traffic split differs from the intended split by more than chance allows. It is the single most useful health check because it is evidence that assignment or logging is broken.

```text
intended 50/50, observed control = 49,100, treatment = 50,900, n = 100,000
chi2 = 32.4, p = 1.2e-08 -> SRM: do not trust the result
```

```python
from scipy.stats import chisquare

def srm_check(counts: dict[str, int], ratios: dict[str, float], alpha: float = 0.001) -> dict[str, float]:
    total = sum(counts.values())
    observed = [counts[name] for name in counts]
    expected = [ratios[name] * total for name in counts]
    statistic, p_value = chisquare(observed, expected)
    return {"total": total, "chi2": float(statistic), "p_value": float(p_value), "srm": float(p_value) < alpha}

```

Interpretation: run the check overall and per platform, device, and country, because a global 50/50 can hide a broken split inside one segment. Edge cases: a strict alpha such as 0.001 avoids false alarms from routine checks; a real SRM means the experiment is invalid, not that a correction is needed; a small SRM can be caused by bot traffic or by a logging pipeline that drops one variant; bot filtering and assignment must use the same key or the counts never match.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## What are guardrail metrics and novelty effects
Guardrails are metrics that must not degrade even if the primary metric improves: latency, error rate, refunds, unsubscribe rate, data freshness. Novelty effects are temporary behavior changes caused by the newness of the treatment rather than the treatment itself.

```text
primary: conversion rate +1.5%
guardrail: p99 latency +40% -> do not ship even though the primary metric won
```

```python
def guardrail_breach(control: list[float], treatment: list[float], tolerance: float = 0.0) -> dict[str, float]:
    mean_control = sum(control) / len(control)
    mean_treatment = sum(treatment) / len(treatment)
    relative = (mean_treatment - mean_control) / mean_control if mean_control else 0.0
    return {"control_mean": mean_control, "treatment_mean": mean_treatment, "relative_change": relative, "breached": relative > tolerance}

```

Interpretation: pre-register guardrails with thresholds and hold the launch decision on them; a positive early lift that decays over two weeks is usually novelty, and the analysis should use the mature window rather than the whole run. Edge cases: guardrails with low traffic need longer windows before they can detect a regression; multiple guardrails need multiplicity control; a seasonal week can mimic a novelty decay; stopping early on a guardrail is itself a peeking problem, so use sequential methods.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## What is sequential testing and why does peeking inflate false positives
Checking a test every day and stopping when p < 0.05 turns a 5% false-positive rate into a much larger one. Sequential methods hold the overall error rate while allowing valid interim looks.

```text
fixed-horizon alpha = 0.05; ten daily looks with naive peeking -> far above 0.05
use an alpha-spending boundary or a sequential test instead
```

```python
import numpy as np
from scipy.stats import chi2_contingency, norm

def peek_false_positive_rate(looks: int = 10, per_look: int = 1000, baseline: float = 0.1, trials: int = 2000, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    false_positives = 0
    for _ in range(trials):
        control = rng.binomial(1, baseline, looks * per_look).cumsum()
        treatment = rng.binomial(1, baseline, looks * per_look).cumsum()
        for look in range(1, looks + 1):
            k = look * per_look
            table = [[control[k - 1], k - control[k - 1]], [treatment[k - 1], k - treatment[k - 1]]]
            _chi2, p_value, _dof, _expected = chi2_contingency(table, correction=False)
            if p_value < 0.05:
                false_positives += 1
                break
    return false_positives / trials

def alpha_spending_thresholds(looks: int, alpha: float = 0.05) -> list[float]:
    # Pocock-style constant boundary approximation for illustration.
    z = norm.ppf(1 - alpha / (2 * looks))
    return [round(float(z), 3)] * looks
```

Interpretation: decide the look schedule before launch and use a boundary that accounts for it; a sequential test spends alpha across looks so the final decision is still valid. Edge cases: the simulation above runs an A/A test, so any rejection is by construction a false positive; unequal look sizes and unequal traffic need the boundary recomputed; peeking at many metrics multiplies the problem; a Bayes factor or an always-valid confidence sequence is an alternative that needs no fixed schedule.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## Bayesian vs frequentist approaches to experiments
Frequentist inference fixes the parameter and treats the data as random; Bayesian inference fixes the data and treats the parameter as uncertain. Bayesian results answer the question decision-makers actually ask: "what is the probability that B is better?"

```text
A: 100/1000, B: 130/1000 -> P(B > A) ~ 0.98, expected loss ~ 0.006
```

```python
import numpy as np

def posterior_samples(successes: int, n: int, draws: int = 200_000, seed: int = 0) -> np.ndarray:
    # Beta(1, 1) prior keeps the model equivalent to add-one smoothing.
    rng = np.random.default_rng(seed)
    return rng.beta(successes + 1, n - successes + 1, draws)

def prob_b_beats_a(success_a: int, n_a: int, success_b: int, n_b: int, draws: int = 200_000, seed: int = 0) -> float:
    a = posterior_samples(success_a, n_a, draws, seed)
    b = posterior_samples(success_b, n_b, draws, seed + 1)
    return float((b > a).mean())

```

Interpretation: the posterior probability is easy to explain but depends on the prior and is not a guarantee; the frequentist p-value has a precise long-run meaning but is easy to misread. Edge cases: a weakly informative prior still moves the answer when traffic is low; Bayesian credible intervals are not confidence intervals, so do not swap the labels; optional stopping is more defensible under a Bayesian model but the expected loss still needs a decision threshold; simulation cost grows with the number of metrics.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you distinguish correlation from causation and handle confounding
Correlation is a measure of linear association; causation needs a mechanism plus a design that removes confounding. A confounder changes both the treatment and the outcome, and it creates a correlation where none is causal.

```text
ice cream sales correlate with drownings; the confounder is temperature
revenue correlates with support tickets; the confounder is customer size
```

```python
import numpy as np

def correlation(x: list[float], y: list[float]) -> float:
    return float(np.corrcoef(x, y)[0, 1])

def partial_correlation(x: list[float], y: list[float], z: list[float]) -> float:
    # Correlate x and y after linearly removing the confounder z from each.
    design = np.column_stack([np.ones(len(z)), z])
    residual_x = np.asarray(x) - design @ np.linalg.lstsq(design, np.asarray(x), rcond=None)[0]
    residual_y = np.asarray(y) - design @ np.linalg.lstsq(design, np.asarray(y), rcond=None)[0]
    return float(np.corrcoef(residual_x, residual_y)[0, 1])

```

Interpretation: report correlation with a scatter plot and the confounders you adjusted for; a large drop from correlation to partial correlation is evidence that z explains the association. Edge cases: adjusting for a mediator removes a real causal effect, and adjusting for a collider creates a fake one; Pearson correlation misses non-linear relationships, so check Spearman and the plot; regression controls only for measured confounders, so unmeasured ones still bias the estimate; the only clean proof of causation is a randomized experiment or a credible quasi-experimental design.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## What is Simpson's paradox
An association that holds in every subgroup can reverse when the subgroups are combined, because the groups differ in size and in baseline rate. It is a warning that aggregated metrics are not automatically safe.

```text
group A: control 1/10, treatment 2/10   (treatment better)
group B: control 50/100, treatment 40/100 (treatment worse)
aggregate: control 51/110, treatment 42/110 -> treatment appears better
```

```python
def simpson_check(groups: list[dict]) -> dict[str, float | int]:
    treatment_n = sum(group["treatment_n"] for group in groups)
    treatment_success = sum(group["treatment_success"] for group in groups)
    control_n = sum(group["control_n"] for group in groups)
    control_success = sum(group["control_success"] for group in groups)
    aggregate = treatment_success / treatment_n - control_success / control_n
    total = treatment_n + control_n
    weighted = sum(
        (group["treatment_n"] + group["control_n"]) / total
        * (group["treatment_success"] / group["treatment_n"] - group["control_success"] / group["control_n"])
        for group in groups
    )
    signs_differ = (aggregate > 0) != (weighted > 0)
    return {"aggregate_lift": aggregate, "stratum_weighted_lift": weighted, "reversal": int(signs_differ)}
```

Interpretation: when exposure is uneven across strata, report the stratum-weighted or stratified estimate and state the weighting scheme. Edge cases: the paradox is not a statistical error but a real feature of unequal group sizes; the correct weight depends on the target population, so weighting by traffic answers a different question than weighting by users; a change in the mix of traffic over time can produce a false trend; a confounded experiment that lands unevenly across segments produces the same pattern.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you detect anomalies with z score IQR and MAD
Anomaly detection compares a value to what is normal for its context. The z-score assumes a roughly normal distribution, the IQR is robust to mild outliers, and MAD is the most robust to extreme ones.

```text
[10, 11, 12, 12, 13, 900] -> z-score flags 900; IQR flags 900; MAD flags 900
[10, 11, 12, 12, 13, 14] -> nothing flagged
```

```python
import statistics

def zscore_flags(values: list[float], threshold: float = 3.0) -> list[int]:
    mean = statistics.fmean(values)
    stdev = statistics.stdev(values)
    if stdev == 0:
        return []
    return [index for index, value in enumerate(values) if abs(value - mean) / stdev > threshold]

def iqr_flags(values: list[float], k: float = 1.5) -> list[int]:
    quantiles = statistics.quantiles(values, n=4)
    q1, q3 = quantiles[0], quantiles[2]
    low, high = q1 - k * (q3 - q1), q3 + k * (q3 - q1)
    return [index for index, value in enumerate(values) if value < low or value > high]

def mad_flags(values: list[float], threshold: float = 3.5) -> list[int]:
    median = statistics.median(values)
    mad = statistics.median([abs(value - median) for value in values]) or 1e-9
    return [index for index, value in enumerate(values) if 0.6745 * abs(value - median) / mad > threshold]
```

Interpretation: MAD is the right default for metrics with a heavy tail because a single extreme value barely moves the median and the MAD. Edge cases: all three methods fail on a seasonal metric unless the value is compared to the same season; a slow drift produces no individual outlier, so pair point detection with a rolling baseline; `statistics.quantiles` needs enough points for a meaningful Q1 and Q3; a constant series has a zero MAD, hence the epsilon; alert thresholds need a minimum effect size as well as a statistical cutoff.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you decompose a time series into trend and seasonality
Decomposition splits a series into trend, seasonal, and residual components. The additive form fits constant seasonal amplitude; the multiplicative form fits amplitude that grows with the level, and it becomes additive after a log transform.

```text
values by week: [10, 12, 15, 11, 13, 16, 12, 14, 17], period = 3
trend = centered moving average; seasonal = mean detrended value per phase
```

```python
def centered_moving_average(values: list[float], period: int) -> list[float | None]:
    half = period // 2
    trend: list[float | None] = [None] * len(values)
    for index in range(half, len(values) - half):
        window = values[index - half: index + half + 1]
        trend[index] = sum(window) / len(window)
    return trend

def seasonal_indices(values: list[float], period: int) -> list[float]:
    trend = centered_moving_average(values, period)
    buckets: list[list[float]] = [[] for _ in range(period)]
    for index, value in enumerate(values):
        if trend[index] is not None:
            buckets[index % period].append(value - trend[index])
    means = [sum(bucket) / len(bucket) if bucket else 0.0 for bucket in buckets]
    overall = sum(means) / period
    return [mean - overall for mean in means]

```

Interpretation: read the residual for anomalies, the seasonal index for capacity planning, and the trend for growth; a strong seasonal index means year-over-year comparisons, not week-over-week. Edge cases: a period that does not divide the series leaves the ends without a trend estimate; holidays and promotions must be handled as events, not as seasonality; an additive model on a multiplicative series leaves structure in the residuals; a real decomposition tool such as STL handles changing seasonality, which this simple version does not.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## What are stationarity and moving averages
A stationary series has a constant mean and variance over time. Most business series are not stationary: they trend, they have weekly seasonality, and their variance grows with volume, which breaks tests that assume stationarity.

```text
[1, 2, 3, 4, 5, 6] -> non-stationary (mean drifts)
[3, 2, 4, 3, 3, 4] -> roughly stationary
```

```python
def moving_average(values: list[float], window: int) -> list[float | None]:
    out: list[float | None] = []
    total = 0.0
    for index, value in enumerate(values):
        total += value
        if index >= window:
            total -= values[index - window]
        out.append(total / window if index >= window - 1 else None)
    return out

def stationarity_check(values: list[float], parts: int = 4) -> dict[str, float]:
    # A quick diagnostic; a real ADF or KPSS test is the formal answer.
    chunk = max(1, len(values) // parts)
    means = [sum(values[i * chunk:(i + 1) * chunk]) / len(values[i * chunk:(i + 1) * chunk]) for i in range(parts)]
    variances = []
    for i in range(parts):
        piece = values[i * chunk:(i + 1) * chunk]
        mean = sum(piece) / len(piece)
        variances.append(sum((value - mean) ** 2 for value in piece) / max(1, len(piece) - 1))
    return {"mean_drift": max(means) - min(means), "variance_ratio": max(variances) / (min(variances) or 1e-9)}

```

Interpretation: a drifting mean or a variance ratio far from 1 signals non-stationarity; differencing removes a trend and a log transform stabilizes a growing variance. Edge cases: a moving average lags the series and is not a forecast; a centered versus trailing window answers different questions; a short series cannot support four chunks; seasonality is not removed by first differencing alone, so use a seasonal difference.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you bootstrap a confidence interval
The bootstrap resamples the observed data with replacement to approximate the sampling distribution of any statistic. It is the pragmatic answer for medians, ratios, and p99s, where a closed-form interval does not exist.

```text
values = [10, 12, 13, 15, 20, 900]; statistic = median
resample 10,000 times -> 95% CI around the median
```

```python
import numpy as np

def bootstrap_ci(values: list[float], draws: int = 10_000, alpha: float = 0.05, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    data = np.asarray(values)
    samples = np.array([np.median(rng.choice(data, size=data.size, replace=True)) for _ in range(draws)])
    return float(np.quantile(samples, alpha / 2)), float(np.quantile(samples, 1 - alpha / 2))

```

Interpretation: the interval is only as good as the sample; bootstrap assumes the sample is representative and the observations are independent. Edge cases: resampling rows instead of users understates the interval when users have many rows each, so resample the cluster (the user); a heavy tail needs more draws for a stable p99; the percentile interval is biased for small samples, where a BCa interval is better; stratification should be preserved inside each resample.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you plan capacity with percentiles
Capacity planning uses peak demand plus headroom, not the average. Size from a high percentile of traffic, correct for latency at that load, and re-derive the numbers as the traffic mix changes.

```text
peak 12,000 rps, p95 6,000 rps, per replica 2,000 rps, headroom 1.3
replicas = ceil(12,000 * 1.3 / 2,000) = 8
```

```python
import math

def replicas_for_peak(peak_rps: float, per_replica_rps: float, p99_ms: float, latency_budget_ms: float = 300.0, headroom: float = 1.3) -> dict[str, float]:
    # A replica that is slower than the budget serves proportionally less traffic.
    usable = per_replica_rps * min(1.0, latency_budget_ms / p99_ms)
    return {"usable_rps_per_replica": usable, "replicas": math.ceil(peak_rps * headroom / usable)}

```

Interpretation: size for the p95 or p99 of demand with explicit headroom, and treat the utilisation curve as non-linear — going from 70% to 90% utilisation more than doubles the queue. Edge cases: a daily peak is not a yearly peak, so use the seasonal maximum for provisioning; percentiles hide correlated bursts, so load-test the peak shape; autoscaling has a reaction delay, so the headroom must cover the scale-out time; a p99 that is latency-bound (for example a full garbage collection) does not scale linearly with replicas.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you implement statistics in SQL
Warehouses expose the same primitives as a stats library: `percentile_cont`, `stddev_samp`, `var_samp`, and histograms built with `width_bucket`. Push the aggregation into SQL so gigabytes do not move.

```sql
-- Percentiles and dispersion in one pass (PostgreSQL/Snowflake style)
select
  count(*)                                              as n,
  avg(latency_ms)                                       as mean,
  stddev_samp(latency_ms)                               as sd,
  var_samp(latency_ms)                                  as variance,
  percentile_cont(0.50) within group (order by latency_ms) as p50,
  percentile_cont(0.95) within group (order by latency_ms) as p95,
  percentile_cont(0.99) within group (order by latency_ms) as p99
from metrics.requests
where event_date between date '2026-09-01' and date '2026-09-30';
```

```sql
-- Histogram and a z-score based outlier flag
with buckets as (
  select width_bucket(latency_ms, 0, 1000, 20) as bucket, count(*) as requests
  from metrics.requests
  where event_date = current_date - 1
  group by 1
), stats as (
  select avg(latency_ms) as mean, stddev_samp(latency_ms) as sd from metrics.requests
)
select requests.event_id,
       (requests.latency_ms - stats.mean) / nullif(stats.sd, 0) as z_score
from metrics.requests cross join stats
where abs((requests.latency_ms - stats.mean) / nullif(stats.sd, 0)) > 3;
```

Interpretation: `percentile_cont` interpolates while `percentile_disc` returns an actual data point, so pick per the metric contract; `approx_percentile` trades a little accuracy for large speedups at scale. Edge cases: `stddev_samp` uses `n - 1` and `stddev_pop` uses `n`, and they differ most on small groups; percentiles cannot be averaged across partitions, so aggregate at the right grain; a z-score computed per partition must use the partition's own mean and standard deviation; NULLs are ignored by aggregates, which silently shrinks the denominator.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## How do you implement statistics in Python with numpy pandas and scipy
The Python stack splits cleanly: numpy for arrays and percentiles, pandas for grouped descriptive statistics, and scipy for tests and distributions.

```python
import numpy as np
import pandas as pd
from scipy import stats

latencies = np.array([10.0, 12.0, 13.0, 15.0, 20.0, 900.0])
summary = {
    "mean": float(np.mean(latencies)),
    "std": float(np.std(latencies, ddof=1)),
    "p50": float(np.percentile(latencies, 50)),
    "p95": float(np.percentile(latencies, 95)),
    "p99": float(np.percentile(latencies, 99)),
    "skew": float(stats.skew(latencies)),
    "kurtosis": float(stats.kurtosis(latencies)),
}

frame = pd.DataFrame({"channel": ["a", "a", "b", "b"], "revenue": [10.0, 12.0, 40.0, 44.0]})
by_channel = frame.groupby("channel")["revenue"].agg(["count", "mean", "std", "median"])

test = stats.ttest_ind([10.0, 12.0, 13.0], [11.0, 14.0, 15.0], equal_var=False)
interval = stats.norm.interval(0.95, loc=float(np.mean(latencies)), scale=float(stats.sem(latencies)))
```

Interpretation: `np.std` defaults to the population denominator `ddof=0`, so pass `ddof=1` to match `statistics.stdev` and SQL's `stddev_samp`; `scipy.stats` covers tests, distributions, and intervals. Edge cases: `np.percentile` interpolates by default, so it can differ from nearest-rank SQL; pandas `agg(["mean", "std"])` skips NaN and can hide missing data; SciPy tests still assume independent observations; a pandas frame loaded with `toPandas()` on a large Spark result can exhaust driver memory.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)

## Real world use cases for statistics in data engineering
### 1. Experimentation platform for a consumer app
The platform assigns users by hashing, checks for sample ratio mismatch on every dimension, and reports lift with a confidence interval and a guardrail dashboard. It blocks a launch when any pre-registered guardrail regresses.

```python
from scipy.stats import chisquare

counts = {"control": 49_100, "treatment": 50_900}
expected = [50_000, 50_000]
chi2, p_value = chisquare(list(counts.values()), expected)
assert p_value < 0.001  # SRM: the readout is not trustworthy
```

Why it matters: an automated SRM gate catches broken assignment and logging before a false result reaches a decision maker.

### 2. Data-quality thresholds derived from distributions
Instead of hard-coding "row count must be within 10%", the pipeline learns the distribution of each check over 90 days and alerts when today's value falls outside the 1st or 99th percentile.

```python
import numpy as np

def threshold_from_history(history: list[float], alpha: float = 0.01) -> tuple[float, float]:
    return float(np.quantile(history, alpha / 2)), float(np.quantile(history, 1 - alpha / 2))
```

Why it matters: distribution-based thresholds adapt to weekday and seasonal patterns and cut alert fatigue compared with fixed bounds.

### 3. Capacity planning for a streaming cluster
The team plots rps and consumer lag by percentile, models peak-plus-headroom, and reprovisions before a marketing event instead of after an incident.

```python
import math

def brokers_needed(peak_records_per_sec: float, records_per_broker: float, headroom: float = 1.4) -> int:
    return math.ceil(peak_records_per_sec * headroom / records_per_broker)
```

Why it matters: peak demand plus explicit headroom is defensible, whereas sizing on the average guarantees saturation during the daily peak.

### 4. Anomaly alerting on pipeline metrics
Freshness, null rate, and schema-drift counts are monitored with robust z-scores on a rolling baseline, so a single extreme day does not desensitize the detector.

```python
import statistics

def robust_flag(value: float, history: list[float], threshold: float = 3.5) -> bool:
    median = statistics.median(history)
    mad = statistics.median([abs(item - median) for item in history]) or 1e-9
    return 0.6745 * abs(value - median) / mad > threshold
```

Why it matters: median and MAD are unaffected by past outliers, which is exactly what an alerting baseline needs.

### 5. Marketing attribution and incrementality
Correlation between spend and revenue is not incremental revenue. The team runs geo holdouts and computes the lift with a difference-in-differences estimate instead of a raw spend correlation.

```python
def difference_in_differences(treat_pre: float, treat_post: float, control_pre: float, control_post: float) -> float:
    return (treat_post - treat_pre) - (control_post - control_pre)
```

Why it matters: a holdout removes the confounding that makes spend always look effective, and the estimator stays explainable to finance.

### 6. Fraud detection thresholds
The model scores transactions and the threshold is chosen from the precision-recall curve at the operating point that controls expected loss, not from accuracy on an imbalanced dataset.

```python
from sklearn.metrics import precision_recall_curve

def threshold_at_recall(y_true, scores, target_recall: float = 0.8) -> float:
    precision, recall, thresholds = precision_recall_curve(y_true, scores)
    eligible = [thresholds[i] for i in range(len(thresholds)) if recall[i] >= target_recall]
    return float(min(eligible)) if eligible else float(thresholds[-1])
```

Why it matters: fraud is rare, so a percentage accuracy of 99.9% is meaningless; precision and recall at a business-chosen operating point is the honest metric.

[Table of Contents](#Statistics-and-Experimentation-for-Data-Engineers)
