---
name: matlab-backtest-workflow
description: >
  Portfolio backtesting workflow for MATLAB — strategy design, analysis protocol,
  and result interpretation. Use when deciding which allocation strategies to compare,
  structuring a backtest from requirements to final report, or interpreting Sharpe
  ratio, drawdown, turnover, and transaction cost outputs. Pairs with
  matlab-backtest-api (inject both) for complete, runnable output.
license: MIT
metadata:
  author: carreychen
  version: "1.0"
---

# Portfolio Backtesting Workflow

A 5-phase protocol for designing and running a rigorous portfolio backtest in MATLAB.
For API-level correctness (function signatures, gotchas), also inject `matlab-backtest-api`.

## When to Use

- Structuring a backtest from scratch (what strategies, what data, what to report)
- Comparing allocation strategies: equal-weight, momentum, inverse-variance, mean-variance, robust
- Deciding rebalance frequency, lookback window, and transaction cost structure
- Interpreting and presenting backtest results professionally

## When NOT to Use

- You already know the strategy and just need to write correct MATLAB code → use `matlab-backtest-api` alone
- Options/derivatives pricing → separate skill
- Real-time live trading → this framework is simulation-only

## Strategy Selection Guide

| Strategy | When to Use | Key Parameter | Requires |
|----------|-------------|---------------|----------|
| Equal-Weight | Baseline, no estimation risk | — | Nothing extra |
| Inverse-Variance | Risk-weighted, simple | `LookbackWindow` for vol estimate | `cov()` |
| Momentum | Trend-following signal | Lookback for return period | `tick2ret` |
| Max Sharpe | Best Sharpe in-sample | `Portfolio` object | Financial Toolbox |
| Markowitz | Controlled risk-return tradeoff | `lambda` risk-aversion | Optimization Toolbox |
| Robust Optimization | Uncertainty-aware Markowitz | `k` robustness factor | Optimization Toolbox |

**Rule of thumb:** always include Equal-Weight as a benchmark. In-sample Max Sharpe often underperforms out-of-sample ("past performance ≠ future results").

## 5-Phase Workflow

### Phase 1: Clarify Requirements

Before writing code, confirm:
- **Assets**: instruments, count, real data or simulated?
- **Strategy logic**: how weights are determined at each rebalance
- **Rebalance frequency**: integer steps (daily=1, weekly≈5, monthly≈21)
- **Transaction costs**: bps per trade, tiered, or zero?
- **Signals**: external signal timetable needed?
- **Warmup period**: rows needed before first real rebalance (typically 20–126 days)

### Phase 2: Prepare Data

Data must be a timetable with datetime row times and one column per asset.
Load or simulate; always verify row count. See `matlab-backtest-api` for code patterns.

**Warmup pattern (official MathWorks):**
```matlab
warmupPeriod = 40;
warmupTT = pricesTT(1:warmupPeriod, :);
init_w = myStratFcn(zeros(1, nAssets), warmupTT);   % pre-compute initial weights
```

### Phase 3: Implement Rebalance Functions

One local function per strategy, placed at the bottom of the .m file.
Each function must:
1. Guard against insufficient data (`if height(priceWindow) < minRows`): return equal weights
2. Compute weights using the chosen method
3. Normalize: `w = max(w,0); w = w/sum(w);`
4. Return correct output shape (1×N row vector)

See `matlab-backtest-api` for exact signatures and verified patterns.

### Phase 4: Configure and Run

```matlab
% One backtestStrategy object per strategy
strat = backtestStrategy("Name", @fcn, ...
    RebalanceFrequency=21, LookbackWindow=[40 126], ...
    TransactionCosts=0.005, InitialWeights=init_w);

% Engine (strategies first — no prices here)
engine = backtestEngine([s1, s2, s3], RiskFreeRate=0.01);

% Run — skip warmup rows with Start=
engine = runBacktest(engine, pricesTT, Start=warmupPeriod);
```

### Phase 5: Analyze and Report

**Minimum required output:**
```matlab
tbl = summary(engine);
disp(tbl)
equityCurve(engine)
```

**Keep the deliverable minimal.** Do NOT hand-roll position tables or custom equity
curves — `engine.Returns`, `engine.Positions`, `engine.Turnover` are already available.
Hand-written extra code is where new bugs enter.

**What to report for each strategy:**

| Metric | Interpretation | Good threshold |
|--------|----------------|----------------|
| `TotalReturn` | Cumulative return | > benchmark |
| `SharpeRatio` | Risk-adjusted return (annualized, uses `RiskFreeRate`) | > 0.5 |
| `MaxDrawdown` | Worst peak-to-trough loss | < 20% |
| `AverageTurnover` | Fraction of portfolio traded per rebalance | < 30% for cost efficiency |
| `AverageBuyCost` / `AverageSellCost` | Total cost per rebalance in dollars | Compare across strategies |
| `Volatility` | Annualized return vol | Lower = more stable |

**Extended metrics** (add manually if needed):
```matlab
% Calmar ratio = AverageReturn / MaxDrawdown
calmar = tbl.AverageReturn ./ tbl.MaxDrawdown;

% Sortino ratio (downside deviation)
for i = 1:numel(strategies)
    r = engine.Returns.(strategies(i).Name).Variables;
    dd = r(r < 0);
    sortino(i) = mean(r) / std(dd) * sqrt(252);
end

% Statistical test: are two strategies significantly different?
[~, p] = ttest2(engine.Returns.(s1).Variables, engine.Returns.(s2).Variables);
fprintf("p-value for return difference: %.4f\n", p)
```

## References

| Load when... | File |
|---|---|
| Writing any rebalance function (code-level) | inject `matlab-backtest-api` |
| Interpreting summary() fields in detail | `references/performance-guide.md` |

----

Copyright 2025 carreychen. MIT License.

----
