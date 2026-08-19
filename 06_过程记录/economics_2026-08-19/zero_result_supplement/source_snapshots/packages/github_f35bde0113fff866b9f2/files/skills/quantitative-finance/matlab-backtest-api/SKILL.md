---
name: matlab-backtest-api
description: >
  MATLAB Financial Toolbox backtesting API — runtime correctness guard.
  Use when writing MATLAB code that calls backtestStrategy, backtestEngine,
  runBacktest, or any rebalance function. Covers function signatures, argument
  placement, type constraints, and verified WRONG/CORRECT patterns for every
  known error mode. NOT a workflow guide — see matlab-backtest-workflow for
  strategy design and result interpretation.
license: MIT
metadata:
  author: carreychen
  version: "1.0"
---

# MATLAB Backtest API — Runtime Guard

Every rule in this skill came from a real execution failure, verified in R2026a.
Read `references/quick-ref/rebalance-function.md` before writing any code.

## When to Use

- Writing a `rebalanceFcn` of any kind (equal-weight, momentum, optimization)
- Setting up `backtestStrategy` / `backtestEngine` / `runBacktest`
- Modeling transaction costs (fixed, tiered, function handle)
- Integrating external signals (`signalTT`) or stateful `UserData`
- Loading price data from `dowPortfolio.xlsx` or simulated arrays

## When NOT to Use

- Deciding *which* strategy to use or *how* to interpret results → use `matlab-backtest-workflow`
- Options/derivatives pricing → separate skill
- Live trading execution → this framework is backtest-only

## GOLDEN TEMPLATE — script structure (copy this, do not deviate)

```matlab
% === MAIN SCRIPT BODY (no function definitions here) ===
T = readtable('dowPortfolio.xlsx');
% ... data loading ...

% ── STEP A: build signal timetable FIRST (before any strategy or warmup call) ──
% signalTT = buildMySignal(pricesTT);   % must exist before warmup
% warmupSignalTT = signalTT(1:warmupPeriod, :);

% ── STEP B: warmup weights (uses the already-built signal slice) ──
warmupPeriod = 40;
init_w1 = strategy1Fcn(zeros(1,nAssets), pricesTT(1:warmupPeriod,:));
% init_w2 = strategy2Fcn(zeros(1,nAssets), pricesTT(1:warmupPeriod,:), warmupSignalTT);

% ── STEP C: create strategies — NO SignalData property ──
strat1 = backtestStrategy("S1", @strategy1Fcn, RebalanceFrequency=21, InitialWeights=init_w1);
strat2 = backtestStrategy("S2", @strategy2Fcn, RebalanceFrequency=21, LookbackWindow=[40 126], InitialWeights=init_w2);
% NEVER: backtestStrategy(..., SignalData=signalTT)  ← 'SignalData' is NOT a valid property

% ── STEP D: run — pass signalTT as 3rd positional arg to runBacktest ──
engine = backtestEngine([strat1, strat2], RiskFreeRate=0.01);
engine = runBacktest(engine, pricesTT, signalTT, Start=warmupPeriod);
%                                      ^^^^^^^^ 3rd positional arg here, nowhere else
disp(summary(engine)); equityCurve(engine);

% === LOCAL FUNCTIONS (EACH DEFINED EXACTLY ONCE, at the bottom) ===
function w = strategy1Fcn(w, priceWindow)
    n = width(priceWindow);  % ALWAYS first line — local functions can't see workspace vars
    % ... never use nAssets/N/numAssets from script body; use n here
end

function w = strategy2Fcn(w, priceWindow)
    n = width(priceWindow);  % ALWAYS first line
    % ...
end
```

**Four rules derived from this template:**
1. **No `X = @(...)` variable** when there is also a `function X(...)` local function — name collision → script error.
2. **Each local function defined EXACTLY ONCE** — defining the same function in two places → "函数已在此作用域内声明" error.
3. **Reference local functions with `@funcName`** in `backtestStrategy` — never reassign them to variables.
4. **`n = width(priceWindow)` is the FIRST LINE of every local function** — workspace variables like `nAssets` are INVISIBLE inside `function...end` blocks → "无法识别" error.

## Critical Rules (memorize these)

- **`RebalanceFrequency` must be a positive integer** — `Inf` errors; use `99999` for buy-and-hold.
- **`rebalanceFcn` signature is VARIADIC** — mismatch is the #1 `runBacktest` error. See quick-ref.
- **`TransactionCosts` goes on `backtestStrategy`, never on `backtestEngine`.**
- **`tick2ret` on a timetable returns a timetable** — extract `{:,:}` before `cov()` or `estimateAssetMoments`.
- **`w` (current weights) is always 1×N** — use `numel(w)` inside functions, pass `zeros(1,N)` externally.
- **`optimvar` must be N×1 column** — `optimvar('x', N, 1, ...)`, not `(1, N, ...)`.

## Rebalance Function Signatures (variadic — must match config exactly)

| Configuration | Required signature | In/Out |
|---------------|--------------------|--------|
| Base (no extras) | `w = fcn(w, priceWindow)` | 2/1 |
| With `signalTT` | `w = fcn(w, priceWindow, signalWindow)` | 3/1 |
| With `UserData` (no signals) | `[w, ud] = fcn(w, priceWindow, ud)` | **3/2** |
| With both | `[w, ud] = fcn(w, priceWindow, signalWindow, ud)` | 4/2 |

Wrong arity → *"Too few outputs"* or *"not enough input arguments"*.

## Data Loading

```matlab
% From built-in dowPortfolio.xlsx (Financial Toolbox) — readtable returns datetime already
T = readtable('dowPortfolio.xlsx');
assets = ["AA","CAT","DIS","GM","HPQ","JNJ","MCD","MMM","MO","MRK","MSFT","PFE","PG","T","XOM"];
T = T(:, [{'Dates'}, cellstr(assets)]);
pricesTT = table2timetable(T, 'RowTimes', 'Dates');  % do NOT run datetime() on Dates again
% After table2timetable: width(pricesTT)==15 (only asset columns; Dates is now RowTimes, NOT a column)
% height(pricesTT)==251 (251 trading days in 2006); tick2ret gives 250 return rows
% Momentum/RSI windows: use ≤126 (6-month); a 252-day window has NO valid rows on this dataset
% Get RowTimes: pricesTT.Properties.RowTimes  ← always safe
%               pricesTT.Dates                ← also works (dimension named 'Dates')
%               pricesTT.Time                 ← WRONG: errors "无法识别 'Time'，请用 'Dates'"

% Simulated (avoids off-by-one)
nDays = 252; nA = 5;
priceMatrix  = 100 * cumprod(1 + 0.01*randn(nDays, nA));
tradingDates = (datetime(2023,1,2) + caldays(0:nDays-1))';
assert(size(priceMatrix,1) == numel(tradingDates));
pricesTT = array2timetable(priceMatrix, RowTimes=tradingDates, VariableNames="A"+string(1:nA));
```

## Strategy + Engine Setup

```matlab
% TransactionCosts / RebalanceFrequency / LookbackWindow — on STRATEGY
strat = backtestStrategy("Name", @myFcn, RebalanceFrequency=21, ...
    LookbackWindow=40, TransactionCosts=0.005, InitialWeights=init_w);

% backtestEngine — strategies first, no prices, no TransactionCosts
engine = backtestEngine([strat1, strat2], RiskFreeRate=0.01);

% runBacktest — prices here; Start skips warmup rows
engine = runBacktest(engine, pricesTT, Start=warmupPeriod);

% Results
tbl = summary(engine);
equityCurve(engine);
```

## Common Gotchas

| Mistake | Fix |
|---------|-----|
| `RebalanceFrequency=Inf` | Use `99999` for buy-and-hold |
| 4-arg signature when only `UserData` set | UserData-only = 3-in/2-out: `[w,ud]=fcn(w,priceWindow,ud)` |
| `UserData` set but returning only `w` | Must return `[w,ud]` — else "Too few outputs" |
| `TransactionCosts` on `backtestEngine` | Strategy property only; engine takes `RiskFreeRate`, `CashBorrowRate`, `InitialPortfolioValue` |
| `price2ret(...)` | Needs Econometrics Toolbox (not installed) — use `tick2ret` |
| `cov(tick2ret(priceWindow))` | `tick2ret` returns timetable → extract: `cov(tick2ret(priceWindow){:,:})` |
| `estimateAssetMoments(p, tick2ret(x))` | Same — pass `{:,:}` not the timetable |
| `estimateMaxSharpeRatio(p)` | Returns N×1 column — transpose: `w = estimateMaxSharpeRatio(p)'` |
| `datetime(T.Dates,'ConvertFrom','datenum')` | `readtable` already returns datetime; use `table2timetable` directly |
| `variableTransactionCosts` returning vectors | Engine needs scalar `[buy,sell]` — add `sum()`: `buy=sum(...); sell=sum(...);` |
| `backtestEngine(pricesTT, strats, ...)` | Strategies first, no prices: `backtestEngine([s1,s2], RiskFreeRate=0.01)` |
| `Portfolio` bounds via `setBounds(p,LowerBound=0)` | Set in constructor: `Portfolio('NumAssets',n,'LowerBound',0,'UpperBound',0.1,'LowerBudget',1,'UpperBudget',1)` |
| `mu' * w` when `mu` is 1×N | N×N outer product — use `mu * w` (scalar) |
| `mu * x` when `mu` is N×1 column | N×1 × N×1 = dimension error — use `mu' * x` OR keep mu as 1×N row |
| anonymous var + local function same name | `X = @(...);` and `function X(...)` in same file → error; pick one approach |
| local function defined twice | defining same function inline AND at the bottom → "函数已在此作用域内声明" error; define each ONCE |
| `pricesTT.Time` on dowPortfolio timetable | RowTimes dimension is named 'Dates' not 'Time' → error; use `pricesTT.Properties.RowTimes` or `pricesTT.Dates` |
| `width(pricesTT) - 1` after table2timetable | Dates column becomes RowTimes and disappears; `width()` already gives only asset columns |
| `pricesTT(1:end, 2:end)` to drop Dates column | Same issue: no Dates column after table2timetable; use `pricesTT` directly |
| `SignalData=signalTT` on `backtestStrategy` | 'SignalData' is NOT a valid property → error; pass signalTT as 3rd positional arg to `runBacktest(engine, pricesTT, signalTT, Start=N)` |
| `@equalWeightFcn` when `equalWeightFcn = @(...)` is a variable | `@varName` looks for a function not a variable → "函数不存在"; pass the variable directly: `backtestStrategy(..., equalWeightFcn, ...)` (no `@`) |
| `timetable{rows,:}.Variables` | `{rows,:}` already extracts a numeric matrix; `.Variables` on a double fails → use `timetable{rows,:}` directly |
| `tbl.SharpeRatio` on `summary(engine)` output | `summary()` returns a table with **metrics as rows** and **strategies as columns**; access with `tbl{'SharpeRatio',:}` or `tbl.MonthlyEqW{'SharpeRatio'}` — NOT `tbl.SharpeRatio` |
| signalTT when momentum computable from priceWindow | momentum computed from priceWindow (price history) needs NO external signalTT; only use signalTT for signals from external sources (e.g., analyst scores, RSI pre-computed outside). A 2-arg `momentumFcn(w, priceWindow)` computes momentum internally — do NOT pass signalTT to `runBacktest` for this case |
| `movprod(x, k, 'WindowMethod','rolling')` | 'WindowMethod' is NOT a valid movprod option → error; use `movprod(x, k)` directly |
| `nAssets` (workspace var) inside local function | Local functions have NO access to workspace variables; use `width(priceWindow)` inside the function |
| `gains(i)` in loop when `gains = diff(prices)` | `diff` returns n-1 elements; loop index i goes 1:n → out of bounds at i=n; use `gains(i-1)` |
| `tick2ret(prices')` with prices as column | Transposing a 251×1 column to 1×251 row makes tick2ret think 251 = assets, 1 = time → "observations >= 2" error; keep prices as column (no `'`) |
| `signalMatrix(1:252,:) = 0` when data has 251 rows | MATLAB auto-expands matrix beyond its size; then RowTimes has 251 elements but matrix is 252×N → mismatch error; use `min(window, nDays)`: `signalMatrix(1:min(window,nDays),:) = 0` |
| Momentum window > nDays-1 with dowPortfolio | dowPortfolio has 251 rows (2006 trading days); tick2ret gives 250 returns; 252-day window has NO data rows → all signals stay 0. Use window ≤ 126 (6-month) for this dataset. |
| `optimvar('x', 1, N, ...)` | Must be column: `optimvar('x', N, 1, ...)` |
| `zeros(N,1)` as initial weights | `w` is always 1×N row; use `zeros(1,N)` and `numel(w)` inside functions |
| Missing `...` on continued line | "Unexpected end of line" — end every continued line with `...` or keep call on one line |
| `signalTT` fewer rows than `pricesTT` | Must have identical row count — build both on same date vector |
| `LookbackWindow` ≤ return lookback | `tick2ret` drops one row; guard `height(priceWindow) > returnLookback` |
| Off-by-one in `array2timetable` | `size(prices,1)` must equal `numel(dates)` — use `cumprod(1+randn(N,nA))` for exactly N rows |
| Passing matrix as `pricesTT` | Wrap with `array2timetable` first |
| Weights not summing to 1 | Normalize: `w = w / sum(w)` |

## References

| Need | File |
|------|------|
| All rebalance patterns + WRONG/CORRECT blocks | `references/quick-ref/rebalance-function.md` |
| `summary()` fields, Sharpe/Sortino/Calmar | `references/performance-metrics.md` |

----

Copyright 2025 carreychen. MIT License.

----
