---
name: ai-quant-engineering
description: >
  AI Quant Engineering — specializes in AI/ML for quantitative finance within the
  Fincept Terminal Desktop project. Activate when working on quant model development,
  ML pipelines, Qlib/RD-Agent integration, LLM-powered finance, backtesting,
  reinforcement learning for trading, multi-agent systems, Python venv management
  (numpy1/numpy2), or the AI Quant Lab services.
---

# AI Quant Engineering

You are an AI/ML quantitative finance specialist embedded in the Fincept Terminal
Desktop codebase. Your role is to guide the development of machine learning pipelines,
quant models, LLM integrations, backtesting systems, and the AI Quant Lab services.

---

## 1. Quant Model Development

### 1.1 Factor Mining

**Process:**

1. **Hypothesis**: Start with an economic intuition (e.g., "stocks with accelerating earnings revisions outperform").
2. **Feature construction**: Translate hypothesis into a computable feature from available data.
3. **Univariate test**: Compute IC (Information Coefficient) = rank correlation between factor and forward returns.
4. **Decay analysis**: How fast does the signal decay? IC at lag 1, 5, 20 days.
5. **Turnover**: How often does the factor-implied portfolio rebalance? High turnover = high transaction costs.
6. **Orthogonality**: Regress against known factors (Fama-French, momentum). Is there residual alpha?

**Good factor properties:**

- IC > 0.02 (consistent across time periods)
- IC decay is gradual (not a spike at lag 1 that disappears)
- Monotonic quintile returns (Q1 < Q2 < ... < Q5 or reverse)
- Stable across market regimes (bull, bear, sideways)

### 1.2 Alpha Generation

```python
# Alpha = Factor exposure × Factor return prediction
# Composite alpha from multiple signals:

def combine_alphas(signals: list[pd.Series], weights: list[float]) -> pd.Series:
    """Combine multiple alpha signals with specified weights."""
    combined = sum(w * s.rank(pct=True) for w, s in zip(weights, signals))
    return combined.rank(pct=True)  # Re-rank for uniform distribution
```

**Alpha combination methods:**

- **Equal weight**: Simple average of ranked signals.
- **IC-weighted**: Weight by each signal's recent Information Coefficient.
- **Optimization**: Mean-variance optimization of signal weights (careful of overfitting).
- **ML-based**: Use a model to learn non-linear signal combinations.

### 1.3 Signal Combination

- Normalize all signals to z-scores or percentile ranks before combining.
- Handle missing data: fill forward (limited), cross-sectional median, or exclude.
- Winsorize extreme values (e.g., clip at +/- 3 sigma) to reduce outlier influence.
- Re-evaluate signal weights periodically (e.g., quarterly) using walk-forward IC.

---

## 2. ML Pipeline Patterns

### 2.1 Data Preparation

```python
# Standard pipeline for financial ML

# 1. Raw data → Clean data
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=['close', 'volume'])          # Drop rows with missing essential fields
    df = df[df['volume'] > 0]                           # Remove zero-volume bars
    df = df.drop_duplicates(subset=['timestamp'])       # Deduplicate
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df

# 2. Feature engineering
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df['ret_1d'] = df['close'].pct_change(1)
    df['ret_5d'] = df['close'].pct_change(5)
    df['vol_20d'] = df['ret_1d'].rolling(20).std()
    df['rsi_14'] = compute_rsi(df['close'], 14)
    df['macd'] = compute_macd(df['close'])
    df['volume_ratio'] = df['volume'] / df['volume'].rolling(20).mean()
    df['bb_position'] = (df['close'] - df['close'].rolling(20).mean()) / (2 * df['close'].rolling(20).std())
    return df

# 3. Label construction
def create_labels(df: pd.DataFrame, horizon: int = 5) -> pd.DataFrame:
    df['forward_ret'] = df['close'].shift(-horizon) / df['close'] - 1
    df['label'] = (df['forward_ret'] > 0).astype(int)  # Binary classification
    return df
```

### 2.2 Feature Engineering Best Practices

**Do:**
- Use returns (not prices) as features — prices are non-stationary.
- Normalize features cross-sectionally (z-score within each timestamp across assets).
- Include technical indicators with varied lookback periods.
- Add volume-based features (OBV, volume ratio, VWAP deviation).
- Use rolling statistics (mean, std, skew, kurtosis) of returns.

**Don't:**
- Use raw prices as features (non-stationary).
- Use future information in feature construction (lookahead bias).
- Create too many features without regularization (overfitting).
- Ignore transaction costs in the label (a 0.01% alpha is meaningless with 0.1% round-trip costs).

### 2.3 Train/Validate/Test Split

**Time-series splits — never random splits for financial data:**

```
|--- Train ---|-- Validate --|--- Test ---|
  2015-2019      2020           2021

Purging: Remove samples within N days of the train/validate boundary
  to prevent information leakage from overlapping labels.

Embargo: Skip M days between train and validate sets.
```

**Walk-Forward Optimization:**

```
Fold 1: Train [2015-2017] → Validate [2018]
Fold 2: Train [2015-2018] → Validate [2019]
Fold 3: Train [2015-2019] → Validate [2020]
Final:  Train [2015-2020] → Test [2021]

Report average and std of metrics across folds.
```

- **Expanding window**: Training set grows with each fold. More data, potential regime change.
- **Rolling window**: Fixed-size training window. Adapts to recent regime, less data.
- **Combinatorial purged cross-validation**: Multiple test sets with purging. Most robust.

---

## 3. Framework-Specific Guidance

### 3.1 Qlib (Microsoft)

Fincept integrates Qlib via the AI Quant Lab (`resources/scripts/ai_quant_lab/`).

**Services available (15 scripts):**

| Service | File | Purpose |
|---------|------|---------|
| Core Service | `qlib_service.py` | Initialization, data loading, basic model training |
| Strategy | `qlib_strategy.py` | Strategy backtesting with TopkDropout |
| Feature Engineering | `qlib_feature_engineering.py` | Alpha158, custom expressions |
| Advanced Models | `qlib_advanced_models.py` | LightGBM, XGBoost, deep learning |
| Advanced Backtest | `qlib_advanced_backtest.py` | Multi-frequency, cost modeling |
| Evaluation | `qlib_evaluation.py` | IC, ICIR, sharpe, ranking metrics |
| Portfolio Optimization | `qlib_portfolio_opt.py` | Mean-variance, risk parity |
| Rolling Retraining | `qlib_rolling_retraining.py` | Walk-forward model updates |
| Reporting | `qlib_reporting.py` | Tearsheet generation, analysis |
| High Frequency | `qlib_high_frequency.py` | HF data handling, features |
| Online Learning | `qlib_online_learning.py` | Incremental model updates |
| Meta Learning | `qlib_meta_learning.py` | Model selection, task adaptation |
| Data Processors | `qlib_data_processors.py` | Custom data handlers |
| Reinforcement Learning | `qlib_rl.py` | RL-based trading agents |
| RD-Agent | `rd_agent_service.py` | Research & Development automation |

**Qlib data format:**

```python
import qlib
qlib.init(provider_uri="~/.qlib/qlib_data/cn_data")

# Qlib expressions for features
FEATURES = [
    "$close/Ref($close, 1) - 1",        # 1-day return
    "Mean($close, 5) / Mean($close, 20)",  # MA ratio
    "Std($close, 20)",                    # 20-day volatility
    "Rsquare($close, 20)",               # R-squared of linear fit
    "Resi($close, 20) / $close",         # Residual of linear fit
]
```

### 3.2 RD-Agent

Fincept wraps RD-Agent for automated quant research (`resources/scripts/ai_quant_lab/rdagent/`):

- `hypothesis_gen.py`: LLM-based hypothesis generation for factor ideas.
- `knowledge_base.py`: Storage and retrieval of research findings.
- `proposal_system.py`: Structured proposals for factor research.

### 3.3 scikit-learn / LightGBM / XGBoost

```python
# Standard pattern for tree-based models in quant
from lightgbm import LGBMClassifier

model = LGBMClassifier(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_samples=50,     # Prevent overfitting on small groups
    reg_alpha=0.1,            # L1 regularization
    reg_lambda=1.0,           # L2 regularization
    random_state=42,
    n_jobs=-1,
)

# IMPORTANT: Use time-series cross-validation, not random
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
```

### 3.4 PyTorch

```python
# Sequence model for financial time series
import torch
import torch.nn as nn

class FinancialTransformer(nn.Module):
    def __init__(self, n_features, d_model=64, nhead=4, num_layers=2, dropout=0.1):
        super().__init__()
        self.input_proj = nn.Linear(n_features, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward=256, dropout=dropout)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        self.output_head = nn.Linear(d_model, 1)

    def forward(self, x):  # x: (batch, seq_len, n_features)
        x = self.input_proj(x)
        x = x.permute(1, 0, 2)  # (seq_len, batch, d_model)
        x = self.transformer(x)
        x = x[-1]               # Take last timestep
        return self.output_head(x)
```

---

## 4. LLM Integration for Finance

### 4.1 Multi-Provider Support

Fincept supports multiple LLM providers. Configuration pattern:

```python
PROVIDERS = {
    "openai": {"models": ["gpt-4o", "gpt-4o-mini"], "api_key_env": "OPENAI_API_KEY"},
    "anthropic": {"models": ["claude-sonnet-4-20250514"], "api_key_env": "ANTHROPIC_API_KEY"},
    "google": {"models": ["gemini-2.0-flash"], "api_key_env": "GOOGLE_API_KEY"},
    "groq": {"models": ["llama-3.3-70b-versatile"], "api_key_env": "GROQ_API_KEY"},
    "ollama": {"models": ["llama3.1", "mistral"], "base_url": "http://localhost:11434"},
}
```

### 4.2 MCP Tool System

Model Context Protocol tools for financial agents:

```python
# Tools that LLM agents can call
FINANCIAL_TOOLS = [
    {"name": "get_stock_price", "params": {"symbol": "str"}},
    {"name": "get_historical_data", "params": {"symbol": "str", "period": "str"}},
    {"name": "compute_indicator", "params": {"indicator": "str", "symbol": "str", "params": "dict"}},
    {"name": "get_news_sentiment", "params": {"symbol": "str", "lookback_hours": "int"}},
    {"name": "analyze_portfolio", "params": {"holdings": "list"}},
    {"name": "backtest_strategy", "params": {"strategy_code": "str", "period": "str"}},
]
```

### 4.3 Agent Orchestration

The Agno trading framework (`resources/scripts/agno_trading/`) provides:

**Core modules:**

| Module | File | Purpose |
|--------|------|---------|
| Base Agent | `core/base_agent.py` | Abstract base class for all trading agents |
| Agent Manager | `core/agent_manager.py` | Lifecycle, creation, selection of agents |
| Agent Evolution | `core/agent_evolution.py` | Genetic/evolutionary improvement of agent strategies |
| Debate Orchestrator | `core/debate_orchestrator.py` | Multi-agent debate for consensus decisions |
| Auto Trader | `core/auto_trader.py` | Autonomous trading loop |
| Trade Executor | `core/trade_executor.py` | Order submission and tracking |
| Workflow Engine | `core/workflow_engine.py` | DAG-based multi-step workflow execution |

**Framework modules:**

| Module | File | Purpose |
|--------|------|---------|
| Decision Coordinator | `framework/decision_coordinator.py` | Aggregates agent opinions into actions |
| LLM Composer | `framework/llm_composer.py` | Composes LLM prompts for trading analysis |
| Competition Runtime | `framework/competition_runtime.py` | Agent vs. agent competition |
| Features Pipeline | `framework/features_pipeline.py` | Real-time feature computation |
| Paper Execution | `framework/paper_execution.py` | Simulated order execution |
| Portfolio Service | `framework/portfolio_service.py` | Portfolio tracking and rebalancing |
| Market Data Source | `framework/market_data_source.py` | Unified market data interface |

**Tools:**

- `tools/market_data.py` — Price and OHLCV data fetching.
- `tools/technical_indicators.py` — Indicator computation wrappers.
- `tools/news_sentiment.py` — News analysis and sentiment scoring.
- `tools/portfolio_tools.py` — Portfolio analytics functions.
- `tools/kraken_api.py` — Kraken exchange API integration.

---

## 5. Backtesting Best Practices

### 5.1 Avoiding Lookahead Bias

**Common sources of lookahead bias:**

| Source | Problem | Fix |
|--------|---------|-----|
| Random train/test split | Test data temporally before training data | Use time-series split only |
| Feature uses future data | e.g., `df['ma'] = df['close'].rolling(20).mean()` includes current bar | Use `.shift(1)` for all features |
| Survivor bias | Only testing on stocks that exist today | Include delisted stocks in universe |
| Point-in-time violation | Using data that wasn't available at decision time | Use as-of-date data snapshots |
| Label leakage | Forward return overlaps with feature window | Purge overlapping samples |

### 5.2 Proper Benchmarking

```python
def backtest_report(returns: pd.Series, benchmark: pd.Series):
    """Generate proper backtest metrics."""
    excess = returns - benchmark

    metrics = {
        "Total Return": (1 + returns).prod() - 1,
        "Annualized Return": (1 + returns).prod() ** (252 / len(returns)) - 1,
        "Annualized Volatility": returns.std() * np.sqrt(252),
        "Sharpe Ratio": returns.mean() / returns.std() * np.sqrt(252),
        "Sortino Ratio": returns.mean() / returns[returns < 0].std() * np.sqrt(252),
        "Max Drawdown": compute_max_drawdown(returns),
        "Calmar Ratio": annualized_return / abs(max_drawdown),
        "Win Rate": (returns > 0).mean(),
        "Profit Factor": returns[returns > 0].sum() / abs(returns[returns < 0].sum()),
        "Alpha": excess.mean() * 252,
        "Beta": returns.cov(benchmark) / benchmark.var(),
        "Information Ratio": excess.mean() / excess.std() * np.sqrt(252),
    }
    return metrics
```

### 5.3 Slippage Modeling

```python
def estimate_slippage(order_size: float, adv: float, spread: float) -> float:
    """
    Estimate market impact slippage.

    order_size: Number of shares
    adv: Average Daily Volume
    spread: Bid-ask spread in price units
    """
    participation_rate = order_size / adv
    # Square-root market impact model (Almgren-Chriss)
    impact = spread * 0.5 + spread * 10 * np.sqrt(participation_rate)
    return impact
```

### 5.4 Transaction Cost Modeling

```python
COST_MODEL = {
    "commission_per_share": 0.005,      # $0.005 per share
    "commission_minimum": 1.00,          # $1.00 minimum per order
    "exchange_fee_per_share": 0.003,     # Exchange/SEC fees
    "spread_cost_bps": 5,               # Half-spread in basis points
    "slippage_bps": 2,                   # Additional market impact
    "short_borrow_annual_bps": 50,       # Annual short borrow cost
}
```

---

## 6. Reinforcement Learning for Trading

### 6.1 Environment Design (Gymnasium)

```python
import gymnasium as gym
import numpy as np

class TradingEnv(gym.Env):
    """
    Observation: [price_features..., position, pnl, cash]
    Action: Discrete(3) = {0: hold, 1: buy, 2: sell}
           or Box(-1, 1) for continuous position sizing
    Reward: Change in portfolio value (PnL-based)
    """

    def __init__(self, data: pd.DataFrame, initial_cash: float = 100_000):
        super().__init__()
        self.data = data
        self.initial_cash = initial_cash

        n_features = 10  # price features
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(n_features + 3,), dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(3)

    def reset(self, seed=None):
        self.step_idx = self.lookback
        self.cash = self.initial_cash
        self.position = 0
        self.portfolio_value = self.initial_cash
        return self._get_obs(), {}

    def step(self, action):
        # Execute action, compute reward, advance time
        prev_value = self.portfolio_value
        self._execute_action(action)
        self.step_idx += 1
        self.portfolio_value = self.cash + self.position * self._current_price()
        reward = self.portfolio_value - prev_value  # Dollar PnL
        done = self.step_idx >= len(self.data) - 1
        return self._get_obs(), reward, done, False, {}
```

### 6.2 Reward Function Design

**Options and tradeoffs:**

| Reward | Formula | Pros | Cons |
|--------|---------|------|------|
| PnL | delta_portfolio_value | Simple, intuitive | Ignores risk, rewards volatility |
| Sharpe-based | mean(ret) / std(ret) over window | Risk-adjusted | Sparse signal, hard to learn |
| Differential Sharpe | Incremental Sharpe update | Dense signal, risk-aware | Requires careful hypertuning |
| Log returns | log(V_t / V_{t-1}) | Penalizes large losses | May underweight small gains |
| Risk-adjusted PnL | PnL - lambda * drawdown | Balances return and risk | Lambda is a hyperparameter |

### 6.3 RL Agents

- **DQN**: Discrete actions. Good for simple buy/hold/sell. Use prioritized replay, double DQN.
- **PPO**: Works for both discrete and continuous. Stable, good default choice.
- **SAC**: Continuous actions (position sizing). Maximum entropy for exploration.
- **A2C**: Simpler than PPO, faster training, less stable.

**Training tips:**
- Normalize observations (z-score with running statistics).
- Use frame stacking (last N observations) for temporal context.
- Train on multiple assets simultaneously for generalization.
- Evaluate on held-out time periods, not held-out random episodes.
- Add transaction costs to the environment — agents must learn to avoid churning.

---

## 7. Multi-Agent Trading Systems

### 7.1 Competition Frameworks

Fincept's Agno framework supports agent competitions (`framework/competition_runtime.py`):

```python
# Each agent manages its own portfolio
# Agents compete on the same market data
# Leaderboard tracks: return, sharpe, drawdown, win rate

class Competition:
    agents: list[TradingAgent]
    market_data: MarketDataSource
    duration: timedelta
    scoring: Callable  # Custom scoring function

    def run(self):
        for timestep in self.market_data.stream():
            for agent in self.agents:
                decision = agent.decide(timestep)
                self.execute(agent, decision)
            self.update_leaderboard()
```

### 7.2 Debate Orchestrators

From `core/debate_orchestrator.py`:

- Multiple LLM agents analyze the same market situation.
- Each agent presents its thesis (bullish/bearish/neutral) with reasoning.
- Orchestrator synthesizes views, identifies consensus and dissent.
- Final decision weighted by agent track record and confidence.

### 7.3 Agent Evolution

From `core/agent_evolution.py`:

- **Genetic algorithm**: Evolve strategy parameters (indicator periods, thresholds).
- **Tournament selection**: Top performers reproduce, bottom performers are replaced.
- **Mutation**: Random perturbation of parameters within bounds.
- **Crossover**: Combine parameters from two successful agents.
- **Fitness function**: Risk-adjusted return (Sharpe, Sortino, or custom).

---

## 8. Python Virtual Environment Management

### 8.1 Dual venv Architecture

Fincept uses two separate Python virtual environments due to NumPy binary incompatibility:

**numpy1 venv** (legacy packages):
```
Packages requiring NumPy < 2.0:
  - vectorbt         (vectorized backtesting)
  - backtesting      (backtesting.py library)
  - financepy        (derivatives pricing)

Python: 3.10 or 3.11
NumPy: 1.26.x (latest 1.x)
```

**numpy2 venv** (modern packages):
```
Packages compatible with NumPy >= 2.0:
  - qlib             (Microsoft Qlib)
  - torch / pytorch  (deep learning)
  - vnpy             (event-driven trading framework)
  - scikit-learn     (latest)
  - lightgbm         (latest)
  - xgboost          (latest)

Python: 3.11 or 3.12
NumPy: 2.x
```

### 8.2 venv Selection Logic

```python
# The Rust backend selects the correct venv based on the service being called

NUMPY1_SERVICES = {"vectorbt_backtest", "backtesting_run", "financepy_pricing"}
NUMPY2_SERVICES = {"qlib_*", "torch_*", "rdagent_*", "agno_*"}

def get_python_path(service: str) -> str:
    if service in NUMPY1_SERVICES:
        return "resources/venvs/numpy1/Scripts/python.exe"
    else:
        return "resources/venvs/numpy2/Scripts/python.exe"
```

### 8.3 Dependency Isolation

- Each venv has its own `requirements.txt`.
- Services communicate via JSON over stdout/stderr (subprocess calls from Rust).
- Never import packages across venv boundaries.
- Pin exact versions in requirements files to prevent unexpected upgrades.

---

## 9. Fincept AI Quant Lab Architecture

### 9.1 Service Communication Pattern

```
Tauri Frontend (React/TypeScript)
  ↓ IPC command
Rust Backend (src-tauri/)
  ↓ subprocess spawn with correct venv
Python Service (resources/scripts/ai_quant_lab/*.py)
  ↓ JSON result on stdout
Rust Backend
  ↓ IPC response
Tauri Frontend
```

### 9.2 Agent Streaming Mechanism

For long-running agent tasks (training, backtesting), use streaming:

```python
# Python side: emit progress as JSON lines
import json, sys

def emit_progress(step: int, total: int, message: str, data: dict = None):
    payload = {"type": "progress", "step": step, "total": total, "message": message}
    if data:
        payload["data"] = data
    print(json.dumps(payload), flush=True)

def emit_result(result: dict):
    print(json.dumps({"type": "result", **result}), flush=True)
```

```rust
// Rust side: read stdout line by line, forward to frontend
// Use tauri::command with streaming response or event emission
```

### 9.3 Error Handling

```python
# Standard error response format
def emit_error(error: str, details: dict = None):
    payload = {"type": "error", "error": error}
    if details:
        payload["details"] = details
    print(json.dumps(payload), flush=True)
    sys.exit(1)

# Always wrap service entry point
def main():
    try:
        args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
        result = run_service(**args)
        emit_result(result)
    except Exception as e:
        emit_error(str(e), {"traceback": traceback.format_exc()})
```

---

## 10. Model Governance

### 10.1 Model Registry

Track all trained models with metadata:

```python
MODEL_METADATA = {
    "model_id": "lgbm_alpha158_v3",
    "training_date": "2024-01-15",
    "training_period": "2018-01-01 to 2023-12-31",
    "validation_ic": 0.038,
    "test_ic": 0.031,
    "features": ["alpha158"],
    "hyperparameters": {...},
    "data_hash": "sha256:...",         # Reproducibility
    "code_version": "git:abc123",
}
```

### 10.2 Model Monitoring

- Track live IC vs. backtest IC. Alert if degradation > 50%.
- Monitor feature drift: KL divergence between training and live feature distributions.
- Track prediction distribution shift.
- Automatic retraining trigger when performance drops below threshold.

### 10.3 Experiment Tracking

- Log all experiments: parameters, metrics, artifacts.
- Use deterministic seeds for reproducibility.
- Version data alongside code (data hash in model metadata).
- Compare experiments on standardized metrics.
