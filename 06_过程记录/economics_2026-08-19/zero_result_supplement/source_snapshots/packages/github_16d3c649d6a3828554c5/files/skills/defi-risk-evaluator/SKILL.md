---
name: defi-risk-evaluator
description: Use this skill when asked to evaluate economic, mathematical, and financial risk in DeFi protocols — including perpetual DEXs, AMMs, lending markets, options vaults, CDPs, and tokenomics. Covers funding rate dynamics, impermanent loss, liquidation cascades, death spirals, collateral quality, yield sustainability, and contagion risk. Do NOT evaluate smart contract code, technical bugs, or security vulnerabilities.
license: MIT
metadata:
  author: auralshin
  version: "1.0.0"
---

# DeFi Economic & Financial Risk Evaluation Guidelines

## PURPOSE

Analyze decentralized finance strictly from an economic and financial engineering perspective. Focus on financial mathematics, incentive structures, capital efficiency, and systemic market risk. Do NOT evaluate smart contract architecture, code-level vulnerabilities, or technical exploits.

---

## 1. Oracle & Data Feed Economics

Assess the economic vulnerability of how the protocol ingests off-chain pricing.

* **Manipulation Cost:** Estimate the capital required to move the oracle price (e.g., flash loan + TWAP manipulation) vs. the extractable profit. If attack profit > attack cost, the oracle is economically broken.
* **DEX Depth Dependency:** For on-chain oracles, assess the spot liquidity depth of the underlying market. Thin markets = cheap manipulation.
* **Latency Arbitrage:** Evaluate financial losses from stale prices during high-volatility events (e.g., gap risk between index and mark price on a perp).

---

## 2. Perpetual DEX & Leverage Risk

Analyze the financial stability of the derivatives engine.

* **Funding Rate Dynamics:** Examine historical funding rates for sustained imbalances. Persistent positive funding = crowded long, creating squeeze risk for the short side (insurance fund).
* **Mark vs. Index Divergence:** Quantify the spread between mark price and index price. Large divergence causes unfair liquidations and adversarial arbitrage.
* **Liquidation Cascade Risk:** Model the concentration of open interest near key price levels. Identify if a single move of X% would trigger a chain of liquidations that amplifies the move.
* **Insurance Fund Solvency:** Evaluate capitalization as a % of open interest. Assess depletion rate under historical worst-case scenarios (e.g., 3σ move). Below ~0.5% of OI is a warning threshold.
* **Socialized Loss Mechanism:** Determine if and how losses are mutualized when the insurance fund is depleted. Quantify the per-user haircut risk.

---

## 3. Options & Hedging Exposure

Assess derivatives pricing and vault mechanics.

* **Greek Exposure:** Calculate net Delta, Gamma, Theta, and Vega for the vault or strategy. Flag unhedged tail exposure.
* **Assignment & Settlement Risk:** Analyze the financial impact of ITM settlement — specifically, whether the vault has sufficient collateral to cover max loss at expiry.
* **Hedge Decay Thresholds:** For delta-neutral strategies, compute the exact price level at which the hedge breaks down. Express as: *"The hedge fails if the underlying moves more than ±X% within T days."*
* **Volatility Mispricing:** Compare implied volatility (IV) to realized volatility (RV). If IV < RV persistently, the vault is systematically underpricing risk and selling options too cheaply.

---

## 4. Liquidity & AMM Risk

Evaluate the financial mechanics of automated market makers.

* **Impermanent Loss (IL):** Calculate the price divergence ratio required to fully offset projected fee yield.
  * Standard formula: $IL = \frac{2\sqrt{k}}{1+k} - 1$ where $k$ is the price ratio $\frac{P_{new}}{P_{initial}}$
* **Fee Yield Viability:** Assess volume-to-TVL ratio. Below ~0.05x daily is a warning that fee income cannot compensate LP risk.
* **Concentrated Liquidity Range Risk:** For Uniswap v3-style pools, estimate the probability of price leaving the active range given historical volatility. Out-of-range positions earn zero fees while remaining fully exposed to IL.
* **JIT Liquidity & MEV Extraction:** Identify if JIT (Just-In-Time) liquidity provision is economically cannibalizing passive LPs — a structural yield drain.
* **Pool Depth vs. Trade Size:** Evaluate price impact for representative trade sizes. High slippage signals shallow liquidity that degrades trader experience and TVL retention.

---

## 5. Lending Protocol & Credit Risk

Evaluate the solvency mechanics of borrowing and lending markets.

* **Utilization Rate Risk:** High utilization (>90%) traps depositors who cannot withdraw and triggers rate spikes that cause mass borrower liquidations.
  * Optimal utilization threshold (kink point) is typically 80%. Above this, borrow rates become punitive.
* **Interest Rate Model:** Assess whether the rate curve adequately incentivizes liquidity supply at high utilization. Flat curves at high utilization = systemic risk.
* **Collateral Factor & Bad Debt:** Evaluate whether collateral factors (LTV ratios) are calibrated to the liquidity depth of the collateral asset. For illiquid collateral, a liquidation discount may not fully cover the shortfall — creating bad debt socialized to depositors.
* **Health Factor Distribution:** Assess the concentration of positions near liquidation thresholds. A cluster of positions at health factor ~1.05 means a small price drop triggers mass liquidations.
* **Liquidation Incentive Economics:** Check if the liquidation bonus is sufficient to attract liquidators in a falling market while not being so large it over-penalizes borrowers.

---

## 6. Tokenomic & Economic Risk

Analyze incentive structures through a financial engineering lens.

* **Emission Schedules & Inflation:** Map token unlock cliffs and vesting schedules. Quantify the sell pressure in $/day at current prices. Flag if emission rate > protocol revenue.
* **FDV / Revenue Ratio:** Compute fully diluted valuation divided by annualized protocol revenue. Above 100x is speculative; above 500x suggests Ponzi-dynamics.
* **Value Accrual Mechanism:** Determine if the token captures real cash flows (fee switch, buybacks, staking yield from revenue) or relies purely on governance speculation.
* **Death Spiral Analysis:** Stress-test reflexive mechanics under a −50% token price scenario:
  * Algorithmic stablecoins: does seigniorage mint rate exceed absorptive demand?
  * Dual-token models: does the yield token maintain peg when reserve token crashes?
  * Collateralized CDPs: at what collateral price does the system become undercollateralized?
* **Mercenary Capital Risk:** Estimate what % of TVL and yield is driven by token incentives vs. organic demand. High mercenary capital = TVL cliff risk when emissions drop.

---

## 7. Yield Sustainability Analysis

Decompose the source and durability of advertised yields.

* **Yield Decomposition:** Break APY into components — trading fees, token emissions, real protocol revenue, and external subsidies. Flag any component that is time-limited or reflexive.
* **Sustainable Yield Floor:** Estimate the baseline APY if all token incentives were removed. If the floor is near 0%, the protocol is entirely dependent on inflation to attract capital.
* **Ponzi vs. Real Yield Test:** Does the protocol pay yield from external revenue (trading fees, interest, liquidation fees) or from newly minted tokens recycled to depositors? The latter is not sustainable.
* **Incentive Duration:** Calculate how many months the current emission rate can continue at current TVL before the treasury is depleted.

---

## 8. Composability & Contagion Risk

Evaluate financial exposure to external protocols and systemic linkages.

* **Collateral Quality:** Analyze the peg stability and market liquidity depth of wrapped assets, LSTs (Liquid Staking Tokens), and bridged tokens used as collateral. A depeg in collateral = instant bad debt.
* **Protocol Dependency Graph:** Map the chain of dependencies (e.g., Protocol A uses Protocol B's LP token as collateral, which uses Protocol C's stablecoin). A single failure propagates.
* **Economic Contagion Scenarios:** Model the downstream financial impact if a major dependency (lending market, yield aggregator, stablecoin) experiences a liquidity crisis. Quantify the maximum loss exposure.
* **Bridge & Cross-Chain Risk:** For multi-chain protocols, assess the economic risk of bridged asset depegs — particularly for assets where the bridge TVL is small relative to the collateral usage on the destination chain.

---

## REQUIRED OUTPUT FORMAT

Always structure the final economic risk report using this schema:

```json
{
  "protocol_type": "[Perp DEX / Options Vault / AMM / Lending / CDP / Yield Aggregator]",
  "risk_score": "[1-10, where 10 = highest risk]",
  "risk_summary": "[2-3 sentence narrative of the most critical economic vulnerabilities]",
  "primary_economic_risk": "[The single biggest financial/economic vulnerability]",
  "oracle_dependency": "[Oracle type, manipulation cost estimate, latency exposure]",
  "liquidation_risk": "[Cascade potential, insurance fund health, bad debt likelihood]",
  "tokenomic_vulnerability": "[Inflation rate, FDV/revenue, death spiral triggers]",
  "yield_sustainability": "[Real yield floor, mercenary capital %, emission runway]",
  "delta_exposure": "[Directional risk, IL at key price levels, hedge decay threshold]",
  "contagion_exposure": "[Key protocol dependencies and max loss from a single failure]",
  "tail_risk_scenario": "[Specific market event or sequence that financially breaks the protocol]"
}
```
