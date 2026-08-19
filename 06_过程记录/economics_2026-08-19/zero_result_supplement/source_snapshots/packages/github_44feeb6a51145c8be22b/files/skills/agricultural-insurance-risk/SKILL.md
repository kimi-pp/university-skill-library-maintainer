---
name: agricultural-insurance-risk
description: "Use when assessing ag insurance risk. Payouts, modeling."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [agriculture, insurance, risk-assessment, actuarial, modeling]
    related_skills: [crop-yield-modeling, precision-agriculture]
---

# Agricultural Insurance Risk Assessment

## Overview
Design and implement agricultural insurance products using satellite data, weather stations, predictive modeling, and actuarial science. Covers parametric insurance, index-based payouts, risk pooling, claims processing automation, and actuarial reserve calculations for crop, livestock, and weather risk products.

## When to Use
- "Design parametric crop insurance product"
- "Calculate actuarial reserves for insurance portfolio"
- "Build weather index-based insurance model"
- "Automate agricultural claims processing"
- "Assess farmer-level insurance risk"

## Parametric Insurance Design

### Index-Based Insurance Framework
```python
import numpy as np
import pandas as pd
from scipy.stats import norm

def design_weather_index_insurance(historical_weather_data, threshold, payout_rate):
    """
    Design weather-based parametric insurance
    
    Args:
        historical_weather_data: daily weather observations (10+ years)
        threshold: trigger threshold (e.g., rainfall < 10mm during growing season)
        payout_rate: payout per unit threshold deviation
    
    Returns:
        Actuarially fair premium, payout probabilities
    """
    # Calculate historical probability of trigger event
    trigger_events = sum(
        1 for day in historical_weather_data 
        if day['rainfall'] < threshold
    )
    prob_trigger = trigger_events / len(historical_weather_data)
    
    # Expected payout
    expected_payout = prob_trigger * payout_rate
    
    # Standard deviation of payouts (for risk loading)
    payouts = [
        payout_rate if day['rainfall'] < threshold else 0
        for day in historical_weather_data
    ]
    payout_std = np.std(payouts)
    
    # Actuarially fair premium + risk loading
    risk_loading = 0.3  # 30% above expected value
    fair_premium = expected_payout * (1 + risk_loading)
    
    return {
        'trigger_probability': round(prob_trigger * 100, 2),
        'expected_payout': round(expected_payout, 2),
        'fair_premium': round(fair_premium, 2),
        'payout_volatility': round(payout_std, 2),
        'value_at_risk_99': round(
            expected_payout + 2.33 * payout_std, 2
        )
    }
```

## Satellite Data Integration

### Crop Health Monitoring for Claims
```python
def satellite_claim_verification(field_boundary, planting_date, expected_crop):
    """
    Use satellite NDVI to verify crop damage claims
    """
    # Get historical NDVI pattern for this crop/field
    normal_growth_pattern = get_historical_ndvi_curve(
        field_id, crop_type=expected_crop, years=5
    )
    
    # Get actual NDVI during growing season
    actual_ndvi = get_current_season_ndvi(
        field_boundary, planting_date
    )
    
    # Calculate deviation from normal
    deviation = compare_ndvi_patterns(actual_ndvi, normal_growth_pattern)
    
    # Insurance payout calculation
    if deviation['deviation_pct'] > 30:
        # Severe stress — likely insurance claim valid
        return {
            'claim_status': 'APPROVED',
            'damage_severity': 'SEVERE' if deviation['deviation_pct'] > 50 else 'MODERATE',
            'payout_percentage': min(deviation['deviation_pct'] / 100, 0.9),
            'confidence': deviation['confidence']
        }
    elif deviation['deviation_pct'] > 15:
        return {
            'claim_status': 'PENDING_INSPECTION',
            'damage_severity': 'MILD',
            'payout_percentage': 0.1,
            'confidence': deviation['confidence']
        }
    else:
        return {
            'claim_status': 'REJECTED',
            'damage_severity': 'NONE',
            'payout_percentage': 0.0,
            'confidence': deviation['confidence']
        }

def get_historical_ndvi_curve(field_id, crop_type, years):
    """
    Retrieve historical NDVI data for comparison
    """
    import ee  # Google Earth Engine
    
    # Query satellite archive (MODIS/Sentinel-2)
    collection = ee.ImageCollection('MODIS/006/MOD13Q1').filter(
        ee.DateRange(
            datetime(2020, 1, 1),
            datetime(2024, 12, 31)
        )
    ).select('NDVI')
    
    # Extract time series for field boundary
    ts = collection.getRegion(
        geometry=field_boundary,
        scale=250  # 250m resolution for MODIS
    )
    
    return ts  # Array of [timestamp, NDVI, lat, lon] tuples
```

## Actuarial Reserve Modeling

### Portfolio Reserve Calculation
```python
class InsuranceReserveCalculator:
    def __init__(self, portfolio_data, historical_claims):
        self.portfolio = portfolio_data
        self.claims_history = historical_claims
        
    def calculate_solvency_reserves(self, confidence_level=0.99):
        """
        Calculate reserves needed for solvency at given confidence level
        """
        # Aggregate claims distribution
        portfolio_claims = []
        
        for farm in self.portfolio:
            farm_risk_profile = self.get_farm_risk(farm)
            expected_claims = farm_risk_profile['expected_annual_claims']
            claim_volatility = farm_risk_profile['claim_volatility']
            
            # Monte Carlo simulation of farm-level claims
            simulated_claims = np.random.normal(
                expected_claims, 
                claim_volatility, 
                10000
            )
            portfolio_claims.extend(simulated_claims)
        
        # Portfolio-level statistics
        total_claims = np.array(portfolio_claims)
        portfolio_expected = np.mean(total_claims)
        portfolio_std = np.std(total_claims)
        
        # Solvency reserve (Value at Risk)
        var_threshold = np.percentile(total_claims, confidence_level * 100)
        
        return {
            'expected_annual_claims': round(portfolio_expected, 2),
            'solvency_reserve_99': round(var_threshold, 2),
            'capital_requirement': round(var_threshold * 1.2, 2),  # 20% buffer
            'risk_margin_ratio': round(portfolio_std / portfolio_expected, 3)
        }
```

## Claims Processing Automation

### Automated Claim Workflow
```python
class AutomatedClaimProcessor:
    def __init__(self, risk_models):
        self.risk_models = risk_models
        
    def process_claim(self, claim_data):
        """
        Automated claim assessment and processing
        """
        # Step 1: Verify farmer policy status
        policy_valid = verify_policy(claim_data['farmer_id'], claim_data['date'])
        if not policy_valid:
            return {"status": "REJECTED", "reason": "Policy expired or invalid"}
        
        # Step 2: Damage assessment
        satellite_analysis = satellite_claim_verification(
            claim_data['field_boundary'],
            claim_data['planting_date'],
            claim_data['crop_type']
        )
        
        # Step 3: Weather verification
        weather_data = get_weather_during_claim_period(
            claim_data['location'],
            claim_data['incident_date']
        )
        
        # Step 4: Calculate payout
        if satellite_analysis['claim_status'] == 'APPROVED':
            payout_amount = calculate_payout(
                claim_data['insured_value'],
                satellite_analysis['payout_percentage'],
                weather_data['severity_factor']
            )
            
            return {
                'status': 'APPROVED',
                'payout_amount': round(payout_amount, 2),
                'processing_time_hours': 2,
                'automated': True
            }
        
        elif satellite_analysis['claim_status'] == 'PENDING_INSPECTION':
            return {
                'status': 'MANUAL_REVIEW',
                'reason': 'Field inspection required',
                'estimated_processing_days': 5
            }
        
        else:
            return {
                'status': 'REJECTED',
                'reason': 'Satellite data shows no significant damage',
                'confidence_threshold': 0.85
            }
```

## Risk Pooling & Reinsurance

### Diversification Strategies
| Pool Type | Geography | Crops | Risk Correlation | Premium Reduction |
|-----------|-----------|-------|------------------|-------------------|
| Regional | Same state | Multiple | Medium | 15-25% |
| National | Country-wide | All crops | Low | 30-45% |
| Index-based | Global | Weather-index | Very low | 40-60% |
| Reinsurer | Multiple pools | All | Lowest | 50-70% |

## Common Pitfalls
1. **Inadequate historical data** — need 10+ years of weather/satellite records
2. **Basis risk** — weather station data doesn't match actual farm conditions
3. **Overfitting to recent weather patterns** — climate change shifts norms
4. **Not accounting for correlation** — drought affecting entire region simultaneously
5. **Satellite cloud cover gaps** — missing data during critical periods
6. **Too many manual claims** — defeats automation purpose
7. **Ignoring reinsurance needs** — catastrophic loss exceeds reserves
8. **Poor risk segmentation** — treating all farms as identical risk
9. **Not updating actuarial models** — premiums become inaccurate
10. **Regulatory compliance gaps** — state/country insurance regulations

## Verification Checklist
- [ ] Historical weather data spans ≥10 years for all regions
- [ ] Satellite data validated against ground truth measurements
- [ ] Basis risk quantified and disclosed to customers
- [ ] Correlation coefficients calculated between farms/regions
- [ ] Reinsurance agreements in place for catastrophic losses
- [ ] Automated claims accuracy ≥90% vs manual review
- [ ] Actuarial models updated annually with new claims data
- [ ] Regulatory filings current for all operating jurisdictions
- [ ] Reserve calculations meet solvency requirements (≥99% confidence)
- [ ] Customer communication protocol for claim status and payouts established