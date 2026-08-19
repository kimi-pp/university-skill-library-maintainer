---
name: quantitative-finance-expert
description: Comprehensive quantitative finance expert covering alpha models, market making, derivatives pricing, risk management, execution algorithms, portfolio construction, backtesting, statistical arbitrage, event-driven models, and regime modeling — synthesized from the MIT Quant Bible and broader practice. Use when designing or reviewing trading strategies, solving quant interview problems, building pricing or risk models, deploying systematic trading systems, designing market-making books, validating backtests, sizing positions (Kelly / mean-variance / vol-targeting / risk-parity), constructing factor-neutral alpha, building execution algorithms (TWAP/VWAP/POV/IS), modeling adverse selection and inventory, or any time the work requires turning probability/statistics/ML/optimization/microstructure into deployable trading decisions. Implements the master Trading Edge Equation, the 9 questions every model must answer, full quant workflow (objective → payoff → edge source → model family → validation → deployment), probability foundations, distribution selection cheat sheet, statistics and inference (multiple testing, bootstrap), regression and conditional expectation, feature engineering for markets, ML for finance, econometrics and causality, market making (3-determinant quote model + adverse selection), microstructure, portfolio construction, risk management (VaR/ES/stress/kill switches), backtesting (purging/embargo/walk-forward/transaction costs), execution, derivatives and volatility (Greeks, surface, vol RV), fixed income, statistical arbitrage (pairs, cointegration, factor residual), event-driven models, Bayesian deployment templates, regime modeling, data infrastructure, production systems, four full strategy templates, research memo template, two checklists, common failure modes, and a complete formula reference.
---

# Quantitative Finance Expert Skill
**Version:** 1.0 | **Source:** MIT Quant Bible + Broader Quantitative Finance Practice

---

## PART 0 — IDENTITY & PURPOSE

You are a quantitative finance reasoning engine. Apply this skill when working on:

- Designing alpha models, market-making models, pricing models, risk models, execution algorithms, and portfolio-construction systems.
- Translating probability, statistics, machine learning, optimization, and market microstructure into deployable trading decisions.
- Reviewing or improving a backtest, research memo, trading strategy, or quantitative interview solution.
- Converting noisy market data into fair value, expected payoff, risk, sizing, and execution decisions.

### Master Trading Edge Equation

```
Trading edge = modeling edge + execution edge + risk-management edge + adaptation edge - costs - errors
```

### The 9 Questions Every Model Must Answer

```
1. What should be traded?
2. Why is the market mispricing it?
3. How large is the edge?
4. How uncertain is the edge?
5. What are the transaction costs and market-impact costs?
6. How should the position be sized?
7. How should the order be executed?
8. How can the strategy fail?
9. How will live performance be monitored and adapted?
```

A model is NOT a trading strategy until all 9 questions are answered.

---

## PART 1 — QUANTITATIVE FINANCE MINDSET

### 1.1 Think in Distributions, Not Point Estimates

A price forecast is incomplete without uncertainty. Always provide:

```
Expected return = 4 bps
Standard error = 1.5 bps
Downside tail = -20 bps under stress
Expected cost = 1.2 bps
Capacity = $40mm notional
```

A good quant answer includes: a probability model, expected payoff, variance/confidence interval, stated assumptions, and a deployment rule accounting for costs and risk.

### 1.2 Separate Fair Value from Tradeability

A model may estimate fair value well but still be unprofitable if spreads, fees, impact, borrow costs, latency, or risk limits eliminate the edge.

**Decision rule:**
```
Trade only if expected edge > explicit costs + implicit costs + uncertainty buffer + risk charge.

Buy edge  = Fair Value - Ask - Fees - Slippage - Impact - Risk Buffer
Sell edge = Bid - Fair Value - Fees - Slippage - Impact - Risk Buffer
```

For a market maker:
```
Quoted spread must compensate for volatility, adverse selection, inventory, funding, fees, latency, and desired profit.
```

### 1.3 Always State the Market Mechanism

Different markets require different models:

| Market Type | Key Modeling Considerations |
|---|---|
| Continuous limit-order books | Queue priority, spread capture, adverse selection, latency, cancellation |
| Auctions | Clearing price, imbalance, end-of-period demand, strategic placement |
| OTC/RFQ | Counterparty selection, quote shading, information asymmetry, inventory |
| Options | Volatility surface, Greeks, skew, term structure, jump risk, hedging costs |
| Fixed income | Yield curves, duration, convexity, funding, liquidity, credit, roll-down |
| Crypto | Fragmented venues, 24/7 trading, funding rates, basis, custody, exchange risk |
| Prediction/event | Binary/discrete payoffs, probability calibration, liquidity, settlement risk |

---

## PART 2 — CORE WORKFLOW FOR QUANT FINANCE PROBLEMS

### 2.1 Define the Objective

Specify all of:
```
Asset universe | Trading horizon | Target variable | Decision frequency
Holding period | Permitted instruments | Portfolio constraints
Risk budget | Cost model | Data sources | Evaluation metric
```

### 2.2 Define the Payoff (Write It Exactly)

```
Directional equity:  PnL = position * (future price - entry price) - costs
Call option:         Payoff = max(S_T - K, 0)
Put option:          Payoff = max(K - S_T, 0)
Binary event:        Payoff = 1 if event occurs, 0 otherwise; Fair Value = P(event)
Market making:       If client buys at Ask: PnL = Ask - V
                     If client sells at Bid: PnL = V - Bid
```

### 2.3 Identify the Source of Edge

Classify the edge type:
```
Informational: better data, faster signal, better inference
Structural: rebates, market access, internalization, superior routing, lower funding cost
Behavioral: predictable flows, slow-moving investors, forced rebalancing, overreaction
Risk-transfer: being paid to warehouse risk others cannot hold
Execution: better order placement, lower impact, better queue prediction
Modeling: better fair value, volatility, correlation, or regime model
```

**If the edge cannot be stated clearly, do not trust the backtest.**

### 2.4 Choose the Right Model Family

```
Bayesian update          → changing belief after signals or order flow
Expected-value model     → discrete payoff, event trade, games, options payoff
Regression               → conditional mean, fair value, alpha, impact, volatility
Classification           → up/down moves, fill/no-fill, event/no-event
Poisson/exponential      → order arrivals, fills, cancellations, jumps
Factor model             → risk, hedging, relative value, residual alpha
kNN/kernel model         → analog states, local nonlinear behavior
Regularized ML           → high-dimensional noisy predictors
Stochastic process       → diffusion, jump, volatility, rates, option pricing
Optimization             → portfolio weights, execution schedule, quote placement
```

### 2.5 Validate the Model (All Required)

```
Out-of-sample validation | Walk-forward validation | Transaction-cost-adjusted PnL
Capacity analysis | Regime robustness | Feature-leakage audit | Ablation tests
Stability of coefficients | PnL attribution | Drawdown and tail-risk analysis
Live paper-trading or shadow-mode validation
```

### 2.6 Deploy and Monitor

```
Signal generation | Order generation | Risk checks | Execution logic
Logging | Monitoring | Alerting | Kill switches
Post-trade analytics | Model retraining or recalibration schedule
```

---

## PART 3 — PROBABILITY FOUNDATIONS

### 3.1 Conditional Probability

```
P(A | B) = P(A ∩ B) / P(B)
```

Market examples: P(next return > 0 | order-book imbalance), P(deal closes | regulatory headline), P(counterparty is informed | they lift my offer), P(fill occurs | queue position, spread, volatility)

### 3.2 Bayes' Theorem

```
P(State | Signal) = P(Signal | State) × P(State) / P(Signal)
Posterior odds = Prior odds × Likelihood ratio
Likelihood ratio = P(Signal | State true) / P(Signal | State false)
```

**Practical rule:** Do not ignore the base rate. A signal that looks strong can still be weak if the prior probability is low.

Trading use cases: update fair value after one-sided order flow, update event probabilities after news, update whether a strategy is decaying, update whether a counterparty is informed, update whether volatility regime has changed.

### 3.3 Expected Value

```
E[X] = Σ p_i x_i   (discrete)
E[X] = ∫ x f(x) dx  (continuous)
E[PnL] = Σ P(state_i) × Payoff(state_i) - Costs
```

For a binary event contract paying 1 if event occurs:
```
Fair Value = P(event)
Buy if Fair Value > Ask + Costs
Sell if Fair Value < Bid - Costs
```

### 3.4 Linearity of Expectation

Works even when variables are dependent:
```
E[X_1 + ... + X_n] = E[X_1] + ... + E[X_n]
```

Trick: define indicator variables I_i = 1 if event i happens, then Expected count = Σ P(event_i)

### 3.5 Variance and Signal Quality

```
Var(X) = E[X^2] - E[X]^2
Var(X + Y) = Var(X) + Var(Y)  [independent]
Var(mean) = σ^2 / n
Signal-to-noise = Expected return / Standard deviation
```

### 3.6 Covariance and Correlation

```
Cov(X, Y) = E[XY] - E[X]E[Y]
Corr(X, Y) = Cov(X, Y) / sqrt(Var(X) Var(Y))
```

**Warning:** Independence implies zero covariance, but zero covariance does NOT imply independence. Markets often have nonlinear tail dependence even when linear correlation appears low.

---

## PART 4 — DISTRIBUTION SELECTION CHEAT SHEET

| Distribution | Formula | Market Use Cases |
|---|---|---|
| **Bernoulli** | P(X=1)=p, E=p, Var=p(1-p) | Trade wins/loses, fill/no-fill, deal closes/breaks, option ITM |
| **Binomial** | E=np, Var=np(1-p) | Winning trades out of n, fills across n orders, event contracts |
| **Poisson** | E=λ, Var=λ | Trades/minute, quote updates/second, news events/day, jumps |
| **Exponential** | E=1/λ, Var=1/λ² | Time to next fill, time to cancellation, time to news; memoryless |
| **Geometric** | E=1/p | Trials until first success, quote updates until fill |
| **Normal** | μ, σ² | Average return estimates, regression inference, aggregated PnL |
| **Lognormal** | Positive right-skewed | Prices under GBM, volume, market cap, trade sizes |
| **Power-law** | Heavy tails | Trade size spikes, drawdowns, crypto liquidations, vol jumps |

**Warning on Normal:** Raw market returns are often fat-tailed, skewed, autocorrelated, and volatility-clustered. Do not rely on normal tails without stress testing.

---

## PART 5 — STATISTICS AND INFERENCE

### 5.1 Key Concepts

- **Law of Large Numbers:** Sample mean converges to true mean — but trades are often not independent, regimes change, data may be biased, and capacity may decay.
- **Central Limit Theorem:** sqrt(n) × (sample_mean - true_mean) / σ → Normal(0,1). Use for confidence intervals, standard errors, t-statistics.
- **Confidence Intervals:** sample_mean ± z × sample_std / sqrt(n). z = 1.64 (90%), 1.96 (95%), 2.58 (99%).

### 5.2 Hypothesis Tests

```
t-stat = estimate / standard_error
|t-stat| > 2 ≈ approximate statistical significance
```

**Quant finance caveats:**
- Multiple testing inflates false discoveries
- Autocorrelation reduces effective sample size
- Fat tails invalidate naive standard errors
- High t-stat can still be untradable after costs
- Low t-stat may reflect insufficient data, not zero edge

### 5.3 Multiple Testing Correction

If thousands of signals are tested, some will look good by chance. Controls:
```
Holdout set | Walk-forward validation | False discovery rate
Bonferroni-style thresholds | Deflated Sharpe ratio
Reality check / bootstrap tests | Economic rationale filter
```

**Rule:** The more signals tested, the higher the evidence threshold required.

### 5.4 Bootstrap and Simulation

Use resampling when closed-form inference is unreliable. Applications: Sharpe confidence interval, drawdown distribution, strategy PnL stability, tail risk, event-probability calibration. Use **block bootstrap** for time series to preserve autocorrelation.

---

## PART 6 — REGRESSION AND CONDITIONAL EXPECTATION

### 6.1 Core Framework

Regression estimates E[Y | X]:
```
Y = future return, fair value, volatility, spread, fill probability, slippage, impact, or PnL
X = features observed before the decision
Y_hat = β_0 + β_1 X_1 + ... + β_p X_p
β_hat = (X^T X)^(-1) X^T y
```

### 6.2 Regression Alpha Template

```
Target:     next-period return r_{t+h}
Features:   X_t
Model:      r_hat_{t+h} = f(X_t)
Fair Value: FV_t = Price_t × (1 + r_hat_{t+h})
Trade if:   |r_hat_{t+h}| > expected costs + risk buffer
Size:       proportional to edge / risk
```

### 6.3 Residual Diagnostics

Check residuals for: centered near zero, autocorrelation, heteroskedasticity, fat tails, correlation with features, regime dependence.

### 6.4 Residualization (Factor-Neutral Alpha)

```
1. Regress signal S on known factors F.
2. Save residual S_resid = S - E[S | F].
3. Test whether S_resid predicts returns.
4. Trade only the residual edge.
```

Use for: factor-neutral alpha, pairs trading, sector-neutral signals, removing market beta, removing volatility/liquidity confounds.

### 6.5 Regression Variants

| Method | Formula | Use When |
|---|---|---|
| Ridge | β = (X^T X + λI)^(-1) X^T y | Correlated features, coefficient stability |
| Lasso | minimize RSS + λΣ\|β_j\| | Sparse features, automatic selection |
| Elastic Net | minimize RSS + λ[αΣ\|β_j\| + (1-α)Σβ_j²] | Sparsity + stability, correlated clusters |
| Logistic | P(Y=1\|X) = 1/(1+exp(-Xβ)) | Probabilities: up move, fill, adverse selection |
| Quantile | Minimize asymmetric loss | Tail risk, downside, conditional VaR |

**Multivariate warning:** A signal that looks predictive alone may disappear after controlling for market beta, sector, volatility, liquidity, or time of day.

---

## PART 7 — FEATURE ENGINEERING FOR MARKETS

### 7.1 Target Design

```
Forward return:       r_{t,t+h} = P_{t+h}/P_t - 1
Forward log return:   log(P_{t+h}/P_t)
Future mid move:      mid_{t+h} - mid_t
Realized volatility:  sqrt(Σ r_i^2)
Fill indicator:       1 if order filled within horizon
Adverse selection:    future mid move after fill
Slippage:             execution price - benchmark price
```

**Critical rule:** All features must be known BEFORE the decision timestamp. No label leakage.

### 7.2 Return Definitions

```
Log return:    log(P_t / P_{t-1})          ← use for additive time aggregation
Simple return: P_t / P_{t-1} - 1           ← use for actual percentage PnL
Mid return:    (bid + ask) / 2             ← use for intraday prediction
```

### 7.3 Microstructure Features

```
Bid-ask spread | Quoted depth at best bid/ask | Order-book imbalance
Queue position | Recent trade sign | Aggressive buy/sell volume
Cancel/replace intensity | Realized volatility | Trade count
Volume imbalance | Distance from VWAP | Time since last trade
Tick direction | Spread changes
```

Order-book imbalance:
```
OBI = (BidDepth - AskDepth) / (BidDepth + AskDepth)
Multi-level: OBI_L = (Σ BidDepth_l - Σ AskDepth_l) / (Σ BidDepth_l + Σ AskDepth_l)
```

### 7.4 Feature Engineering Rules

```
Time features:     encode cyclically: sin(2πt/T), cos(2πt/T)
Skewed variables:  log(1 + volume), log(spread), log(market_cap)
Normalization:     z-score, robust z-score, rank transform, winsorization
Rolling norm:      x_norm_t = (x_t - rolling_mean) / rolling_std  [no lookahead]
Interactions:      momentum × volatility, imbalance × spread, signal × liquidity
Lagging:           feature timestamp ≤ decision timestamp (always)
```

### 7.5 Signal Decay

Estimate half-life: signal_ic_lag_k = Corr(signal_t, return_{t+k}). Use decay to choose holding period and rebalance frequency.

---

## PART 8 — MACHINE LEARNING FOR QUANT FINANCE

### 8.1 Bias-Variance Tradeoff

```
Total error ≈ bias² + variance + irreducible noise
```

Guidance: Start simple. Add complexity only when out-of-sample performance improves. Prefer stable, explainable signals over fragile in-sample gains. Penalize high turnover and high complexity.

### 8.2 Model Selection Guide

| Model | Strengths | Risks |
|---|---|---|
| kNN / Kernel | Analog states, local nonlinear behavior | Curse of dimensionality, poor extrapolation |
| Ridge | Correlated features, coefficient stability | Cannot do feature selection |
| Lasso | Sparse features, interpretability | Unstable with highly correlated features |
| Elastic Net | Sparsity + stability | Requires tuning α and λ |
| Tree / Boosting | Nonlinear interactions, tabular data | Overfitting, poor extrapolation, hidden leakage |
| Neural Networks | LOB, text, sequences, option surfaces | Overfitting, nonstationarity, poor interpretability |
| PCA | Yield curve, vol surface, risk models | Loses interpretability of original features |

### 8.3 PCA Common Interpretations

```
Yield curve PC1: level
Yield curve PC2: slope
Yield curve PC3: curvature
```

### 8.4 Model Calibration

When model predicts 70%, event should occur ~70% of the time. Tools: reliability curves, Brier score, log loss, calibration by bucket, isotonic or Platt calibration.

---

## PART 9 — ECONOMETRICS AND CAUSALITY

### 9.1 Correlation Is Not Causality

A signal can be predictive for the wrong reason:
```
Proxies for volatility | Proxies for liquidity | Sector exposure
Market beta | Data selected after the fact
```

### 9.2 Key Biases to Eliminate

| Bias | Description | Fix |
|---|---|---|
| Selection bias | Treated/control groups differ for non-treatment reasons | Include all assets, not just survivors |
| Survivorship bias | Only surviving stocks in universe | Include delisted names |
| Omitted variable bias | Omitted variable affects both signal and return | Add control variables |
| Lookahead bias | Future data used in features | Strict timestamp discipline |

### 9.3 Difference-in-Differences

```
Effect = (Treated_after - Treated_before) - (Control_after - Control_before)
```

Applications: index inclusion effects, regulatory changes, exchange fee changes, tick-size pilots, corporate events. Key assumption: parallel trends between treated and control groups absent treatment.

### 9.4 Standard Control Variables

```
Market beta | Sector | Size | Value | Momentum | Volatility
Liquidity | Short interest | Time of day | News intensity | Borrow cost | Spread
```

---

## PART 10 — MARKET MAKING

### 10.1 Market-Making Objective

Quote bid and ask, earn spread, manage adverse selection and inventory.

```
Bid = price willing to buy
Ask = price willing to sell
Spread = Ask - Bid
Mid = (Bid + Ask) / 2
```

### 10.2 Three Core Quote Determinants

```
1. Theoretical value / fair value
2. Last traded price and order-flow information
3. Current inventory position
```

### 10.3 Quote Model

```
Quoted Mid = Fair Value + Flow Adjustment - Inventory Skew
Bid = Quoted Mid - Half Spread
Ask = Quoted Mid + Half Spread
Inventory Skew = λ × Inventory
```

If long inventory → lower quoted mid or make ask more attractive.
If short inventory → raise quoted mid or make bid more attractive.

### 10.4 Spread Components

```
Half Spread = base spread
            + volatility charge
            + adverse-selection charge
            + inventory charge
            + latency charge
            + fees/funding charge
            + profit margin
```

### 10.5 Adverse Selection

Adverse selection is the risk that traders hit your quote when they know something you do not.

Signals of informed flow:
```
One-sided aggressive flow | Price moves against you after fill
Large order relative to depth | News proximity | Rapid cancellations
```

Response:
```
Widen quotes | Reduce size | Shift fair value | Increase adverse-selection charge
```

### 10.6 Market-Making Pseudocode

```python
while market_open:
    fair_value = fv_model.predict(market_state)
    uncertainty = uncertainty_model.predict(market_state)
    toxicity = flow_model.toxicity(market_state)
    inventory = position_manager.current_inventory()

    half_spread = base_spread + uncertainty + toxicity + inventory_risk(inventory)
    mid = fair_value - inventory_skew(inventory) + flow_adjustment(market_state)

    bid = mid - half_spread
    ask = mid + half_spread

    quotes = risk_engine.validate_quotes(bid, ask, inventory)
    quote_engine.update(quotes)

    fills = execution_engine.get_fills()
    position_manager.update(fills)
    fv_model.update_from_fills(fills)
```

---

## PART 11 — MARKET MICROSTRUCTURE

### 11.1 Limit Order Book Concepts

```
Best bid | Best ask | Bid-ask spread | Depth | Queue priority
Order imbalance | Market orders | Limit orders | Cancellations
Hidden liquidity | Tick size
```

### 11.2 Spread Decomposition

Bid-ask spread compensates liquidity providers for: order-processing costs, inventory risk, adverse selection, competition and latency, exchange fees and rebates.

### 11.3 Fill Probability

```
P(fill by T) ≈ P(queue ahead is depleted before price moves away)
Expected time to fill ≈ Q / expected marketable volume rate
```

Adjust for cancellations ahead of you.

### 11.4 Flow Toxicity Features

```
VPIN-like volume imbalance | Short-horizon adverse price movement after fills
One-sided aggressive flow | Quote-stuffing or rapid cancellations | News proximity
```

### 11.5 Short-Horizon Alpha Signals

```
Order-book imbalance | Trade imbalance | Spread changes | Depth depletion
Queue imbalance | Cross-venue lead-lag | ETF/futures lead-lag
Volatility bursts | Auction imbalance
```

**Deployment rule:** Short-horizon alpha must exceed spread, fees, adverse selection, and latency costs.

---

## PART 12 — PORTFOLIO CONSTRUCTION

### 12.1 Core Formulas

```
Expected return = w^T μ
Variance = w^T Σ w
Volatility = sqrt(w^T Σ w)
Mean-variance objective: maximize w^T μ - λ w^T Σ w
```

### 12.2 Sizing Rules

```
Simple:       weight_i ∝ expected_edge_i / variance_i
Correlated:   w ∝ Σ^(-1) μ  (shrink μ and Σ heavily — expected returns are noisy)
Vol targeting: scale = target_vol / realized_vol; position = base_position × scale
```

### 12.3 Kelly Criterion

```
f* = p/a - q/b   (p = win prob, a = loss per unit, b = gain per unit)
f* = 2p - 1      (even-money payoff)
```

**Practical rule:** Use fractional Kelly because edge estimates are noisy and tail risks are underestimated.

### 12.4 Risk Parity

```
Risk contribution: RC_i = w_i × (Σw)_i / sqrt(w^T Σ w)
```

Allocate capital so each asset contributes similar risk.

### 12.5 Factor Neutrality

```
B^T w = 0   (B contains factor loadings)
```

Common neutralities: dollar, beta, sector, country, currency, duration, vega.

### 12.6 Portfolio Constraints

```
Σ w_i = 1 | Gross exposure ≤ G | Net exposure within bounds
Sector exposure limits | Factor exposure limits | Position limits
Turnover limits | Liquidity limits
```

---

## PART 13 — RISK MANAGEMENT

### 13.1 Risk Types

```
Market risk | Liquidity risk | Credit/counterparty risk | Funding risk
Model risk | Operational risk | Regulatory risk | Tail risk
Concentration risk | Correlation-breakdown risk | Crowding risk
```

### 13.2 Risk Metrics

```
VaR_α = loss level not exceeded with probability α
ES_α = E[Loss | Loss > VaR_α]   ← better for tail risk
Drawdown_t = current equity - previous peak equity
MDD = max peak-to-trough loss
```

**VaR limitations:** Does not show how bad losses are beyond threshold. Sensitive to distribution assumptions. Can understate risk in crises.

### 13.3 Stress Scenarios

```
Equity crash | Volatility spike | Rate shock | Credit spread widening
Liquidity freeze | Exchange outage | Currency devaluation
Correlation goes to one | Short squeeze | Borrow recall | Gap open after news
```

### 13.4 Risk Limits (Hard and Soft)

```
Max position | Max gross exposure | Max net exposure | Max factor exposure
Max order size | Max daily loss | Max drawdown | Max leverage
Max turnover | Max concentration | Max stale data age
```

### 13.5 Kill Switches — Stop Trading When

```
Market data is stale | Order acknowledgments fail | PnL breach occurs
Positions mismatch | Volatility exceeds threshold | Spread or impact exceeds threshold
Model output is outside expected range | Feature pipeline breaks | Exchange connectivity degrades
```

---

## PART 14 — BACKTESTING AND RESEARCH VALIDATION

### 14.1 What a Backtest Must Simulate

```
Signal timing | Data availability | Order generation | Execution price
Transaction costs | Slippage | Market impact | Borrow/funding
Risk limits | Portfolio constraints | Corporate actions
```

### 14.2 Common Backtest Biases (Check All)

```
Lookahead bias | Survivorship bias | Selection bias | Data snooping
Multiple testing | Timestamp errors | Forward-filled unavailable data
Corporate-action errors | Ignoring delistings | Ignoring borrow constraints
Ignoring market impact | Using close price when order could not execute at close
Overlapping labels without correction
```

### 14.3 Walk-Forward Validation (Preferred)

```
Train on [t0, t1], test on [t1, t2]
Train on [t0, t2], test on [t2, t3]
...
```

Use purging (remove overlapping-label observations) and embargo (remove observations near test window).

### 14.4 Transaction Cost Model

```
Cost = fixed_fee + half_spread + impact_coefficient × sqrt(order_size / ADV)
Impact ∝ volatility × sqrt(order_size / daily_volume)
```

Always analyze capacity: at what AUM does net alpha decay to zero?

### 14.5 Performance Metrics

```
Annualized return | Annualized volatility | Sharpe ratio | Sortino ratio
Max drawdown | Calmar ratio | Hit rate | Average win/loss | Profit factor
Turnover | Capacity | Skewness | Kurtosis | Tail loss | Exposure-adjusted PnL

Sharpe = E[R - R_f] / Std(R - R_f)
```

### 14.6 Signal Metrics

```
Information coefficient: Corr(signal, future return)
Rank IC: Corr(rank(signal), rank(future return))
IC decay by horizon | Hit rate by signal bucket
Return spread: top bucket - bottom bucket | Turnover by signal bucket
```

---

## PART 15 — EXECUTION

### 15.1 Execution Objective

Minimize implementation shortfall = difference between decision price and average execution price.

```
Implementation Shortfall = (Execution Price - Decision Price) × Direction
```

### 15.2 Execution Algorithms

| Algorithm | Use Case |
|---|---|
| TWAP | Time-weighted average price; simple, predictable |
| VWAP | Volume-weighted; tracks market volume profile |
| POV | Participate-on-volume; fixed % of market volume |
| IS | Implementation shortfall; balances urgency vs impact |
| Adaptive | Dynamic; adjusts to real-time liquidity and price |

### 15.3 Passive vs Aggressive Orders

```
Passive (limit order): earn spread, risk non-fill
Aggressive (market order): guarantee fill, pay spread

Use passive when: expected spread capture - adverse selection - nonfill risk > 0
Use aggressive when: urgency and price-risk exceed passive benefits
```

### 15.4 Execution PnL

```
E[Execution Benefit] = P(fill) × passive_savings
                     - P(fill) × adverse_selection
                     - P(no_fill) × opportunity_cost
```

### 15.5 Venue Selection Criteria

```
Fill probability | Adverse selection after fill | Fees/rebates
Latency | Queue priority rules | Hidden liquidity | Toxicity
Cancel behavior | Regulatory constraints
```

---

## PART 16 — DERIVATIVES AND VOLATILITY

### 16.1 Option Basics

```
Call payoff = max(S_T - K, 0)
Put payoff  = max(K - S_T, 0)
Key variables: Spot S, Strike K, Time T, Volatility σ, Rate r, Dividends q
```

### 16.2 Black-Scholes Assumptions (All Violated in Practice)

```
Continuous trading | Lognormal underlying | Constant volatility
Constant rates | No transaction costs | Frictionless markets
```

Real markets violate these → volatility surface modeling.

### 16.3 Greeks

```
Delta: ∂V/∂S          → sensitivity to underlying price
Gamma: ∂²V/∂S²        → sensitivity of delta to price
Vega:  ∂V/∂σ          → sensitivity to volatility
Theta: ∂V/∂t          → sensitivity to time decay
Rho:   ∂V/∂r          → sensitivity to interest rates
```

### 16.4 Volatility Surface

```
IV = f(strike or moneyness, maturity, underlying, regime)
Features: skew, smile, term structure, ATM vol, risk reversal, butterfly, forward vol
```

### 16.5 Volatility Trading Edges

```
Implied vol vs realized vol | Skew mispricing | Term-structure mispricing
Event volatility mispricing | Index vs constituent dispersion
Volatility risk premium | Surface mean reversion | Cross-asset vol relative value
```

### 16.6 Delta Hedging Intuition

```
Long gamma: profits from movement, pays theta
Short gamma: earns theta, loses on large movement
```

### 16.7 Option Risk Warnings

```
Gamma near expiry | Vega concentration | Jump risk | Pin risk
Early exercise risk | Dividend risk | Vol-of-vol | Liquidity | Wide markets
Model calibration errors
```

---

## PART 17 — FIXED INCOME AND RATES

### 17.1 Bond Pricing

```
Price = Σ CashFlow_t / (1 + yield_t)^t
ΔPrice / Price ≈ -Duration × ΔYield
ΔPrice / Price ≈ -D Δy + 0.5 C (Δy)²   [with convexity]
```

### 17.2 Yield Curve Factors

```
PC1: level | PC2: slope | PC3: curvature
```

Strategies: curve steepener/flattener, butterfly trades, roll-down, carry, cross-market relative value, swap spread trades.

### 17.3 Credit

```
Expected loss = Probability of default × Loss given default
Credit instruments add: default probability, recovery rate, credit spread, liquidity premium, seniority, covenants, correlation/default clustering
```

---

## PART 18 — STATISTICAL ARBITRAGE

### 18.1 Stat-Arb Concept

Seeks recurring mispricings with positive expected convergence:
```
Pairs trading | Index arbitrage | ETF vs constituents
Dual-listed shares | Factor residual mean reversion
Cross-sectional reversal | Cross-asset lead-lag
```

### 18.2 Pairs Trading Workflow

```
1. Select related assets
2. Estimate hedge ratio
3. Compute spread: spread_t = price_A_t - β × price_B_t
4. Test stationarity or mean reversion
5. Z-score: z_t = (spread_t - rolling_mean) / rolling_std
6. Signal: z_t > threshold → short A / long B; z_t < -threshold → long A / short B
7. Risk-manage breaks
```

### 18.3 Cointegration

A linear combination of nonstationary price series is stationary. Use for pairs selection, basket relative value, long-term spread models. **Warning:** Cointegration can break under structural changes.

### 18.4 Factor Residual Stat Arb

```
Return = factor_component + residual
1. Estimate factor model
2. Compute residual return
3. Identify extreme residuals
4. Construct factor-neutral portfolio
5. Exit on convergence or stop condition
```

---

## PART 19 — EVENT-DRIVEN QUANT MODELS

### 19.1 Event Fair Value

```
Fair Value = Σ P(outcome_i) × Payoff_i
```

### 19.2 Merger Arbitrage Template

```
FV = p_close × deal_value + (1 - p_close) × break_value
Edge = FV - current_price - costs - risk_buffer
```

### 19.3 Earnings Events

Inputs: historical earnings moves, implied volatility, options straddle price, analyst dispersion, short interest, guidance history, revenue/EPS surprise distribution, liquidity.

Trade types: directional surprise model, volatility over/underpricing, skew trades, post-earnings drift, pre-earnings run-up.

### 19.4 Index Events

```
Flow demand = benchmarked AUM × weight change
Expected impact = f(flow demand, liquidity, crowding, timing)
```

Events: index inclusion/deletion, rebalance, ETF creation/redemption, corporate action, dividend changes, splits.

---

## PART 20 — BAYESIAN DEPLOYMENT TEMPLATES

### 20.1 Signal Update Model

```
Prior: P(up)
Signal likelihoods: P(signal | up), P(signal | down)
Posterior: P(up | signal)
Expected return: posterior-weighted payoff
Trade if expected return exceeds costs
```

### 20.2 Informed-Flow Model

```
P(informed | fill) = P(fill | informed) × P(informed)
                     / [P(fill | informed)×P(informed) + P(fill | uninformed)×P(uninformed)]
```

If posterior informed probability rises: widen quotes, reduce size, shift fair value, increase adverse-selection charge.

### 20.3 Regime Posterior

```
P(regime_k | data_t) ∝ P(data_t | regime_k) × P(regime_k)
```

Use for: volatility regime switching, risk-on/risk-off classification, trend vs mean-reversion state, liquidity normal vs stressed.

---

## PART 21 — REGIME MODELING

### 21.1 Why Regimes Matter

```
Momentum works in trending regimes, fails in choppy regimes
Mean reversion works in stable liquidity, fails during crashes
Carry works until funding stress
Short volatility works until jumps
```

### 21.2 Regime Features

```
Realized volatility | Implied volatility | Credit spreads | Funding rates
Market breadth | Liquidity/spreads | Correlation level | Macro calendar
News intensity | Trend strength | Drawdown state
```

### 21.3 Regime-Aware Model

```
Prediction = f_regime(X)
```

Approaches: separate models by regime, include regime indicators and interactions, hidden Markov models, Bayesian model averaging, volatility-targeted exposure.

---

## PART 22 — DATA INFRASTRUCTURE

### 22.1 Data Quality Checks

```
Missing bars | Outlier prices | Zero or negative prices | Crossed markets
Locked markets | Bad ticks | Duplicate events | Timestamp ordering
Corporate action adjustments | Symbol changes | Venue outages
```

### 22.2 Corporate Action Adjustments

Adjust for: splits, dividends, mergers, spin-offs, ticker changes, delistings, rights offerings. Need both adjusted and raw prices depending on use case.

### 22.3 Storage Patterns

```
Columnar storage for research tables | Time-partitioned data
Symbol-partitioned data | Immutable historical snapshots
Data versioning | Feature store with point-in-time joins
```

### 22.4 Reproducibility Requirements

```
Code version | Data version | Parameter version | Random seed
Universe definition | Backtest date range | Costs and constraints
Model artifact
```

---

## PART 23 — PRODUCTION TRADING SYSTEMS

### 23.1 Architecture Components

```
Market data ingestion | Feature calculation | Model inference | Signal aggregation
Portfolio/risk engine | Order manager | Execution engine | Exchange/broker connectivity
Monitoring and alerting | PnL and position reconciliation | Research feedback loop
```

### 23.2 Latency Tiers

```
Ultra-low latency: nanoseconds/microseconds → hardware, colocation, FPGA/C++
Low latency: milliseconds → optimized event-driven systems
Intraday: seconds/minutes → robust data and execution
Daily/weekly: batch research, portfolio optimization, slower execution
```

### 23.3 Pre-Order Production Checks

```
Data freshness check | Feature sanity check | Model output range check
Position limit check | Order size check | Price collar check
Fat-finger check | Connectivity check | Duplicate-order check | Kill-switch status check
```

### 23.4 Post-Trade Analysis

```
Did the signal work? | Did execution add or subtract value?
Was slippage expected? | Was adverse selection high?
Were fills concentrated in toxic periods? | Did risk limits bind?
Was PnL from intended sources?
```

---

## PART 24 — STRATEGY TEMPLATES

### 24.1 Regression Alpha Strategy

```
1. Define future return target
2. Build point-in-time features
3. Fit regularized regression
4. Validate with walk-forward test
5. Convert predicted return to expected edge
6. Subtract costs
7. Rank assets by net edge
8. Build risk-constrained portfolio
9. Execute with cost-aware algorithm
10. Monitor IC, PnL, costs, and drift

Decision rule:
net_alpha_i = predicted_return_i - expected_cost_i
trade_i if |net_alpha_i| > threshold_i
```

### 24.2 Market-Making Strategy

```
1. Estimate fair value
2. Estimate volatility and uncertainty
3. Estimate fill probability by quote distance
4. Estimate adverse selection by flow type
5. Estimate inventory penalty
6. Optimize bid/ask
7. Update after fills and market moves
8. Hedge inventory when needed
9. Stop quoting during stale data or high toxicity

bid = FV - spread_component - inventory_adjustment
ask = FV + spread_component - inventory_adjustment
```

### 24.3 Event-Trade Strategy

```
1. Define event states and payoffs
2. Estimate probabilities from data and Bayesian updates
3. Compute fair value
4. Compare to market price
5. Subtract costs and risk buffer
6. Trade if edge exceeds threshold
7. Update as new information arrives
8. Exit at event resolution or stop condition
```

### 24.4 Alpha Signal to Orders (Pseudocode)

```python
for timestamp in trading_calendar:
    features = feature_store.get(timestamp)
    predictions = model.predict(features)
    expected_costs = cost_model.estimate(timestamp, universe)
    net_alpha = predictions - expected_costs

    desired_positions = optimizer.solve(
        alpha=net_alpha, risk_model=risk_model,
        constraints=constraints, current_positions=positions,
    )
    orders = order_generator.create(desired_positions, positions)
    orders = risk_engine.filter(orders)
    execution_engine.send(orders)
```

---

## PART 25 — RESEARCH MEMO TEMPLATE

```markdown
# Strategy Name

## Summary
One-paragraph explanation of the strategy, edge, horizon, and instruments.

## Hypothesis
What inefficiency exists and why should it persist?

## Universe
Assets, filters, liquidity constraints, dates.

## Data
Sources, point-in-time handling, cleaning, missingness, corporate actions.

## Target
Exact label definition and horizon.

## Features
Feature list, transformations, lagging, normalization.

## Model
Model class, parameters, training procedure, validation split.

## Costs
Fees, spread, slippage, impact, borrow, funding.

## Portfolio Construction
Sizing, constraints, risk model, hedging.

## Backtest Results
PnL, Sharpe, drawdown, turnover, capacity, hit rate, IC, cost-adjusted results.

## Robustness
Walk-forward, ablations, parameter sensitivity, regimes, stress tests.

## Risks
Model risk, market risk, liquidity risk, tail risk, operational risk.

## Deployment Plan
Execution logic, monitoring, kill switches, retraining.

## Decision
Deploy / paper trade / reject / needs more research.
```

---

## PART 26 — CHECKLISTS

### 26.1 Backtest Review Checklist

```
Was all data available at the decision timestamp?
Were delisted names included?
Were corporate actions handled correctly?
Were transaction costs realistic?
Was market impact included?
Was borrow/funding included?
Was the universe selected point-in-time?
Were parameters chosen on the test set?
Were labels overlapping?
Were multiple tests corrected?
Was performance stable by period and regime?
Did PnL come from intended exposures?
Is capacity realistic?
Does turnover make sense?
Did the strategy survive stress scenarios?
```

### 26.2 Pre-Trade Decision Checklist

```
What is my fair value?
What is the market price?
What is the expected edge after costs?
What is the uncertainty?
What is the downside?
What is my position size and why?
What risk am I unintentionally taking?
What hedge is needed?
What is the liquidity?
How will I execute?
What invalidates the trade?
Where do I exit?
```

---

## PART 27 — COMMON FAILURE MODES

### 27.1 Research Failure Modes

```
Overfitting | Lookahead bias | Survivorship bias | Data snooping
Weak economic rationale | Unstable feature importance | Ignoring costs
Ignoring capacity | Ignoring borrow/funding | Ignoring regime shifts
Using too many correlated signals
```

### 27.2 Trading Failure Modes

```
Oversizing | Ignoring tail risk | Averaging down without thesis
Trading stale signals | Failing to adapt quotes | Ignoring adverse selection
Failing to hedge inventory | Letting losses exceed risk budget
Assuming liquidity will be there in stress
```

### 27.3 Production Failure Modes

```
Stale market data | Bad timestamps | Duplicate orders | Position mismatch
Symbol mapping errors | Model artifact mismatch | Feature pipeline break
Exchange rejects | Latency spike | Kill switch disabled
```

---

## PART 28 — FORMULA REFERENCE

### Probability and Statistics

```
P(A | B) = P(A ∩ B) / P(B)
P(A | B) = P(B | A)P(A) / P(B)
E[X] = Σ p_i x_i
Var(X) = E[X²] - E[X]²
Cov(X,Y) = E[XY] - E[X]E[Y]
Corr(X,Y) = Cov(X,Y) / sqrt(Var(X)Var(Y))
SE(mean) = sample_std / sqrt(n)
t-stat = estimate / SE(estimate)
```

### Regression

```
β_hat = (X^T X)^(-1) X^T y
Ridge: β = (X^T X + λI)^(-1) X^T y
Lasso: minimize RSS + λΣ|β_j|
Elastic net: minimize RSS + λ[αΣ|β_j| + (1-α)Σβ_j²]
```

### Trading

```
Buy edge = FV - Ask - Costs - RiskBuffer
Sell edge = Bid - FV - Costs - RiskBuffer
Sharpe = mean(excess return) / std(excess return)
Portfolio variance = w^T Σ w
Mean-variance objective = maximize w^T μ - λ w^T Σ w
Kelly fraction = p/a - q/b
```

### Market Making

```
Mid = FV + FlowAdjustment - λInventory
Bid = Mid - HalfSpread
Ask = Mid + HalfSpread
HalfSpread = Uncertainty + AdverseSelection + Costs + InventoryRisk + Profit
```

### Options

```
Call payoff = max(S_T - K, 0)
Put payoff = max(K - S_T, 0)
Delta = ∂V/∂S | Gamma = ∂²V/∂S² | Vega = ∂V/∂σ | Theta = ∂V/∂t
```

---

## PART 29 — HOW TO ANSWER QUANT FINANCE REQUESTS

### When Analyzing a Strategy

```
Start with the hypothesis
Define the target and features
Identify the model and assumptions
Check for leakage and biases
Include costs and capacity
Evaluate risk-adjusted performance
Discuss deployment and monitoring
List failure modes
```

### When Solving a Probability Trading Puzzle

```
Define events and variables
Use conditional probability, expectation, or symmetry
Compute carefully
Translate result into fair value or optimal strategy
State uncertainty or risk preference when needed
```

### When Designing a Market-Making Strategy

```
Estimate fair value
Set confidence interval
Choose spread
Skew for inventory
Update from trades
Track PnL and breakeven
Discuss adverse selection
```

### When Asked for a Trading Edge

```
Do NOT simply provide a signal.
Explain: why the edge exists, why it persists, how to validate it, how to size it, and how it fails.
```

### Market-Making Interview Behavior

Say:
```
I will start with a simple model and refine it.
Here are my assumptions.
This is the fair value under those assumptions.
This is how uncertainty affects my quote.
This trade gives me information, so I will update.
This is my current position and breakeven.
```

Avoid:
```
Giving a number without assumptions | Ignoring uncertainty
Ignoring position after trades | Forgetting PnL
Keeping the same market after the counterparty trades
Making absurdly wide quotes that would never trade
```

---

## PART 30 — FINAL PRINCIPLE

The best quantitative-finance work combines:

```
Mathematical correctness
Statistical skepticism
Economic intuition
Market microstructure awareness
Cost realism
Risk discipline
Production reliability
Fast learning from feedback
```

**The deployable goal:**

```
Estimate fair value better than the market,
quote or trade only when the edge exceeds costs and uncertainty,
size positions according to risk,
execute efficiently,
and adapt continuously as new data arrives.
```

A model that predicts well but trades poorly is not enough.
A strategy that backtests well but cannot survive live costs is not enough.
A trade with edge but uncontrolled downside is not enough.
