---
name: financial-engineering
description: >
  수리금융·금융공학 기법을 사용한 모델 개발 및 실증 검증 스킬. 옵션 프라이싱, 신용리스크,
  포트폴리오 이론, 팩터 모델, 부도확률(PD) 추정, 텍스트 기반 금융 신호 추출 등을 수행한다.
  학술 논문 수준의 모델 설계 및 Python/R 구현을 제공하며, 어떤 금융 주제에도 적용 가능.
---

# Financial Engineering

수리금융 모델 설계부터 실증 구현까지 담당하는 스킬.

## 방법론 레퍼토리

### 1. 신용리스크 & 부도확률 (PD) 모델

#### 1-1. 구조 모델 (Structural Models)

**Merton (1974) 모델:**
```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import fsolve

def merton_model(V, sigma_V, D, r, T):
    """
    V: 자산가치, sigma_V: 자산변동성, D: 부채(액면가)
    r: 무위험이자율, T: 만기
    """
    d1 = (np.log(V/D) + (r + 0.5*sigma_V**2)*T) / (sigma_V * np.sqrt(T))
    d2 = d1 - sigma_V * np.sqrt(T)
    
    E = V * norm.cdf(d1) - D * np.exp(-r*T) * norm.cdf(d2)  # 주식가치
    DD = d2  # Distance to Default
    PD = norm.cdf(-d2)  # 위험중립 부도확률
    
    return E, DD, PD

def implied_asset_value(E_obs, sigma_E_obs, D, r, T):
    """관측된 주식가치/변동성으로 내재 자산가치 역산 (KMV 방식)"""
    def equations(params):
        V, sigma_V = params
        d1 = (np.log(V/D) + (r + 0.5*sigma_V**2)*T) / (sigma_V * np.sqrt(T))
        d2 = d1 - sigma_V * np.sqrt(T)
        eq1 = V * norm.cdf(d1) - D * np.exp(-r*T) * norm.cdf(d2) - E_obs
        eq2 = V * norm.cdf(d1) * sigma_V - E_obs * sigma_E_obs
        return [eq1, eq2]
    
    V0, sigma_V0 = E_obs + D, 0.3
    return fsolve(equations, [V0, sigma_V0])
```

#### 1-2. 축약 모델 (Reduced-Form): Logit/Probit 기반 PD

```python
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.calibration import calibration_curve
import statsmodels.api as sm

# Altman Z-Score (1968) 변수 구성
def altman_zscore(df):
    """
    A = Working Capital / Total Assets
    B = Retained Earnings / Total Assets
    C = EBIT / Total Assets
    D = Market Cap / Total Liabilities
    E = Sales / Total Assets
    """
    df['A'] = df['working_capital'] / df['total_assets']
    df['B'] = df['retained_earnings'] / df['total_assets']
    df['C'] = df['ebit'] / df['total_assets']
    df['D'] = df['market_cap'] / df['total_liabilities']
    df['E'] = df['sales'] / df['total_assets']
    df['zscore'] = 1.2*df['A'] + 1.4*df['B'] + 3.3*df['C'] + 0.6*df['D'] + 1.0*df['E']
    return df

# Logit PD 모델
features = ['leverage', 'roa', 'liquidity', 'volatility', 'zscore', 'interest_coverage']
X = df[features]
y = df['default']  # 0/1

logit = sm.Logit(y, sm.add_constant(X)).fit()
print(logit.summary())

# PD 예측 및 보정 검증
pd_pred = logit.predict(sm.add_constant(X_test))
auc = roc_auc_score(y_test, pd_pred)
brier = brier_score_loss(y_test, pd_pred)

# 호스머-레메쇼 검정 (캘리브레이션)
from scipy.stats import chi2
def hosmer_lemeshow(y_true, y_pred, g=10):
    df_hl = pd.DataFrame({'y': y_true, 'pred': y_pred})
    df_hl['decile'] = pd.qcut(df_hl['pred'], g, labels=False)
    grouped = df_hl.groupby('decile').agg({'y': ['sum', 'count'], 'pred': 'mean'})
    obs1 = grouped['y']['sum']
    exp1 = grouped['pred']['mean'] * grouped['y']['count']
    obs0 = grouped['y']['count'] - obs1
    exp0 = grouped['y']['count'] - exp1
    hl_stat = ((obs1 - exp1)**2/exp1 + (obs0 - exp0)**2/exp0).sum()
    p_val = 1 - chi2.cdf(hl_stat, g-2)
    return hl_stat, p_val
```

---

### 2. 팩터 모델 & 알파 발굴

#### 2-1. Fama-French 팩터 구성

```python
import pandas as pd
import numpy as np

def construct_ff_factors(df_monthly):
    """
    df_monthly: columns=['date', 'ticker', 'ret', 'mktcap', 'bm_ratio', 'op_ratio', 'inv_ratio']
    Returns: SMB, HML, RMW, CMA, MOM
    """
    results = []
    for date, grp in df_monthly.groupby('date'):
        # 시가총액 기준 분류 (Median)
        med_size = grp['mktcap'].median()
        grp['size'] = np.where(grp['mktcap'] <= med_size, 'Small', 'Big')
        
        # BM 기준 3분위
        grp['bm_rank'] = pd.qcut(grp['bm_ratio'], 3, labels=['Low', 'Mid', 'High'])
        
        # 6개 포트폴리오 수익률 (Value-weighted)
        portfolios = grp.groupby(['size', 'bm_rank']).apply(
            lambda x: np.average(x['ret'], weights=x['mktcap'])
        )
        
        SMB = (portfolios[('Small', 'Low')] + portfolios[('Small', 'Mid')] + 
               portfolios[('Small', 'High')]) / 3 - \
              (portfolios[('Big', 'Low')] + portfolios[('Big', 'Mid')] + 
               portfolios[('Big', 'High')]) / 3
        
        HML = (portfolios[('Small', 'High')] + portfolios[('Big', 'High')]) / 2 - \
              (portfolios[('Small', 'Low')] + portfolios[('Big', 'Low')]) / 2
        
        results.append({'date': date, 'SMB': SMB, 'HML': HML})
    
    return pd.DataFrame(results)

# Fama-MacBeth 크로스섹션 회귀
def fama_macbeth(df):
    """두 단계: 1) 시계열 베타 추정, 2) 크로스섹션 회귀"""
    # Step 1: 롤링 베타 추정 (36개월 윈도우)
    betas = df.groupby('ticker').apply(
        lambda x: x[['market', 'SMB', 'HML']].rolling(36).corr(x['ret'])
    )
    # Step 2: 매월 크로스섹션 회귀
    lambdas = []
    for date in df['date'].unique():
        cross = df[df['date'] == date].merge(betas[betas['date'] == date], on='ticker')
        model = sm.OLS(cross['ret_next'], sm.add_constant(cross[['beta_mkt', 'beta_smb', 'beta_hml']]))
        lambdas.append(model.fit().params)
    return pd.DataFrame(lambdas).mean(), pd.DataFrame(lambdas).sem()  # 리스크 프리미엄
```

#### 2-2. 포트폴리오 백테스팅

```python
import vectorbt as vbt  # pip install vectorbt
import backtrader as bt  # pip install backtrader

def long_short_backtest(signals_df, returns_df, n_long=30, n_short=30, rebal_freq='M'):
    """
    signals_df: 각 종목의 알파 시그널 (높을수록 매수)
    returns_df: 수익률 데이터
    """
    portfolio_returns = []
    
    for date in signals_df.resample(rebal_freq).last().index:
        scores = signals_df.loc[date].dropna()
        longs = scores.nlargest(n_long).index
        shorts = scores.nsmallest(n_short).index
        
        # 다음 기간 수익률
        next_ret = returns_df.loc[date:date + pd.DateOffset(months=1)].mean()
        long_ret = next_ret[longs].mean()
        short_ret = next_ret[shorts].mean()
        portfolio_returns.append({
            'date': date, 'long': long_ret, 'short': short_ret,
            'ls': long_ret - short_ret
        })
    
    port = pd.DataFrame(portfolio_returns).set_index('date')
    
    # 성과 지표
    sharpe = port['ls'].mean() / port['ls'].std() * np.sqrt(12)
    max_dd = (port['ls'].cumsum() - port['ls'].cumsum().cummax()).min()
    
    return port, {'sharpe': sharpe, 'max_drawdown': max_dd, 
                  'annual_return': port['ls'].mean() * 12}
```

#### 2-3. 알파 팩터 검증 프레임워크

```python
# Alphalens 기반 팩터 분석
import alphalens

# IC (Information Coefficient) 분석
factor_data = alphalens.utils.get_clean_factor_and_forward_returns(
    factor=signals, prices=prices, periods=(1, 5, 21)
)
alphalens.tears.create_full_tear_sheet(factor_data)

# t-통계 (Newey-West 표준오차)
from statsmodels.stats.sandwich_covariance import cov_hac
model = sm.OLS(factor_data['1D'], sm.add_constant(factor_data['factor']))
res = model.fit()
nw_se = np.sqrt(np.diag(cov_hac(res, nlags=6)))
t_stats = res.params / nw_se
```

---

### 3. 옵션 프라이싱 & 변동성 모델

```python
from scipy.stats import norm
from scipy.optimize import brentq
import numpy as np

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    return K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def implied_volatility(market_price, S, K, T, r, option_type='call'):
    """이분법으로 내재 변동성 계산"""
    objective = lambda sigma: black_scholes(S, K, T, r, sigma, option_type) - market_price
    return brentq(objective, 1e-6, 10.0)

# 몬테카를로 시뮬레이션 (복잡한 페이오프)
def mc_option_price(S0, K, T, r, sigma, n_paths=100000, option_type='asian'):
    dt = T / 252
    paths = S0 * np.exp(np.cumsum(
        (r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*np.random.randn(n_paths, 252), axis=1
    ))
    if option_type == 'asian':
        payoff = np.maximum(paths.mean(axis=1) - K, 0)
    elif option_type == 'barrier_up_out':
        barrier = 1.2 * S0
        alive = (paths.max(axis=1) < barrier)
        payoff = np.maximum(paths[:, -1] - K, 0) * alive
    return np.exp(-r*T) * payoff.mean(), payoff.std() / np.sqrt(n_paths)
```

---

### 4. NLP / 텍스트 기반 금융 신호

#### 4-1. 금융 감성분석 (Sentiment Analysis)

```python
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch

# FinBERT (금융 도메인 특화 BERT)
# 출처: https://huggingface.co/ProsusAI/finbert
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def batch_sentiment(texts, batch_size=32):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        outputs = sentiment_pipeline(batch, truncation=True, max_length=512)
        results.extend(outputs)
    # positive=1, neutral=0, negative=-1
    score_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    return [score_map[r['label']] * r['score'] for r in results]

# 한국어: KR-FinBert-SC
# 출처: https://huggingface.co/snunlp/KR-FinBert-SC
kr_pipeline = pipeline("text-classification", model="snunlp/KR-FinBert-SC")
```

#### 4-2. 이벤트 텍스트 → 시장 반응 연구

```python
import re
from datetime import datetime, timedelta

def extract_events_from_text(texts_df):
    """
    texts_df: columns=['date', 'source', 'text', 'entity']
    유명인/기관의 발언 → 날짜별 집계 감성 점수
    """
    # 감성 점수 산출
    texts_df['sentiment_score'] = batch_sentiment(texts_df['text'].tolist())
    
    # 일별 집계 (엔티티별)
    daily_sentiment = texts_df.groupby(['entity', texts_df['date'].dt.date]).agg({
        'sentiment_score': ['mean', 'std', 'count'],
        'text': 'count'
    }).reset_index()
    
    return daily_sentiment

def text_signal_to_alpha(sentiment_df, returns_df, lags=[1, 3, 5]):
    """감성 시그널 → 미래 수익률 예측력 검증 (Panel 회귀)"""
    merged = sentiment_df.merge(returns_df, on=['entity', 'date'])
    for lag in lags:
        merged[f'ret_{lag}d'] = merged.groupby('entity')['return'].shift(-lag)
    
    # Fama-MacBeth
    results = {}
    for lag in lags:
        valid = merged.dropna(subset=[f'ret_{lag}d', 'sentiment_score'])
        fm_results = []
        for date in valid['date'].unique():
            cross = valid[valid['date'] == date]
            if len(cross) < 5:
                continue
            ols = sm.OLS(cross[f'ret_{lag}d'], sm.add_constant(cross['sentiment_score']))
            fm_results.append(ols.fit().params['sentiment_score'])
        results[f'lag_{lag}'] = {
            'mean_lambda': np.mean(fm_results),
            't_stat': np.mean(fm_results) / (np.std(fm_results) / np.sqrt(len(fm_results)))
        }
    return results
```

#### 4-3. Named Entity Recognition (NER) & 토픽 모델링

```python
import spacy
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from bertopic import BERTopic

# NER — 인물/기업/이벤트 추출
nlp = spacy.load("ko_core_news_lg")  # 한국어 모델

def extract_entities(text):
    doc = nlp(text)
    return {
        'persons': [ent.text for ent in doc.ents if ent.label_ == 'PS'],
        'organizations': [ent.text for ent in doc.ents if ent.label_ == 'OG'],
        'dates': [ent.text for ent in doc.ents if ent.label_ == 'DT']
    }

# BERTopic — 동적 토픽 모델링 (시간별 토픽 변화)
topic_model = BERTopic(language="multilingual", calculate_probabilities=True)
topics, probs = topic_model.fit_transform(texts)
topics_over_time = topic_model.topics_over_time(texts, timestamps)
```

---

### 5. 리스크 측정

```python
def calculate_var_es(returns, confidence=0.99, method='historical'):
    """
    VaR (Value at Risk) 및 ES (Expected Shortfall / CVaR) 계산
    """
    if method == 'historical':
        var = np.percentile(returns, (1 - confidence) * 100)
        es = returns[returns <= var].mean()
    elif method == 'parametric':
        mu, sigma = returns.mean(), returns.std()
        var = norm.ppf(1 - confidence, mu, sigma)
        es = mu - sigma * norm.pdf(norm.ppf(1 - confidence)) / (1 - confidence)
    elif method == 'cornish_fisher':  # 비정규 분포 보정
        from scipy.stats import skew, kurtosis
        s = skew(returns)
        k = kurtosis(returns)  # excess kurtosis
        z = norm.ppf(1 - confidence)
        z_cf = z + (z**2 - 1)*s/6 + (z**3 - 3*z)*k/24 - (2*z**3 - 5*z)*s**2/36
        var = returns.mean() + z_cf * returns.std()
        es = None  # 별도 계산 필요
    return {'VaR': var, 'ES': es}

# Kupiec POF 백테스트 (VaR 유효성 검증)
def kupiec_test(returns, var_series, confidence=0.99):
    exceedances = (returns < var_series).sum()
    T = len(returns)
    p = 1 - confidence
    LR_uc = -2 * (np.log(p**exceedances * (1-p)**(T-exceedances)) - 
                   np.log((exceedances/T)**exceedances * (1-exceedances/T)**(T-exceedances)))
    from scipy.stats import chi2
    p_val = 1 - chi2.cdf(LR_uc, df=1)
    return {'exceedances': exceedances, 'LR': LR_uc, 'p_value': p_val}
```

---

## 모델 검증 체크리스트

| 검증 항목 | 방법 | 기준 |
|-----------|------|------|
| 예측력 (분류) | AUROC | > 0.7 (우수), > 0.8 (탁월) |
| 캘리브레이션 | Hosmer-Lemeshow | p > 0.05 |
| 과적합 여부 | Out-of-sample / K-Fold CV | In-sample ≈ Out-of-sample |
| 경제적 유의성 | 알파 크기 vs 거래비용 | 거래비용 차감 후 양수 |
| 팩터 IC | 월별 IC > 0.05 | ICIR > 0.5 |
| VaR 백테스트 | Kupiec, Christoffersen | p > 0.05 |

---

## 산출물 저장 경로

```
/Users/pc/Documents/sr_research_centre/workspace/research/YYYY-MM-DD_{paper-slug}/
├── paper/
│   ├── draft.md
│   └── appendix.md
├── models/
│   ├── {model_name}.py        ← 모델 구현 코드
│   ├── {model_name}_results.csv  ← 추정 결과
│   └── figures/               ← 모델 성과 시각화
└── data/
    ├── raw/
    └── processed/
```

**raw CSV 출처 주석 (REQUIRED):**
```csv
# source: 기관명
# url: https://실제URL
# retrieved: YYYY-MM-DD
```
