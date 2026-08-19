---
name: solar-energy-modeling
description: "Build solar panel soiling trackers, cleaning ROI optimizers, and energy-yield monitoring tools. Covers soiling physics (PM2.5, PM10, pollen, rain), panel degradation by type, inverter health, energy price lookups, and cross-session persistence."
version: 1.0.0
author: user-defined
platforms: [linux, macos, windows]
---

# Solar Energy Modeling — Soiling, Degradation & Cleaning ROI

Build data-driven solar panel monitoring tools that combine environmental data, panel physics, and energy economics.

## Core Architecture

A solar soiling optimizer follows a daily-step accumulation pattern:

```
Daily Inputs (PM2.5, PM10, pollen, rain, humidity, energy price)
    ↓
Soiling Accumulation (log-linear model, 0.02–1.5%/day)
    ↓
Rain Cleaning (if ≥15mm, intensity/duration factor)
    ↓
Age Degradation (by panel type: 0.4–1.2%/yr)
    ↓
Power Output = capacity × moduleEff × ageEff × soilingEff × inverterEff
    ↓
Revenue Loss = (theoretical - actual) × peakSunHours × energyPrice
    ↓
Cleaning Decision = lossOver30Days > cleaningCost (with rain postponement)
```

## Data Sources

| Data | Source | Free? | API Key? |
|------|--------|-------|----------|
| PM2.5 | Open-Meteo Air Quality API | ✅ | No |
| PM10 | Open-Meteo Air Quality API | ✅ | No |
| Pollen (grass, birch, ragweed, alder, mugwort) | Open-Meteo Air Quality API | ✅ | No |
| Temperature, humidity | Open-Meteo Weather API | ✅ | No |
| Rain forecast + hourly precipitation | Open-Meteo Weather API | ✅ | No |
| Geocoding (city → lat/lon) | Open-Meteo Geocoding API | ✅ | No |
| Historical weather (past 14 days) | Open-Meteo API | ✅ | No |
| Energy prices | Static lookup table (EIA, IEA, Statista) | ✅ | No — see pitfalls |
| Gemini commentary | Google Gemini API | ❌ Free tier available | Optional, paste in UI |

## Soiling Model

### Soiling Rate (daily %)

```
base_rate = 0.05 × ln(PM2.5 + 1)                         // fine particles
coarse_term = PM10 > PM25 ? 0.02 × ln(PM10 - PM25 + 1) : 0  // dust, sand
pollen_term = totalPollen > 0 ? 0.03 × ln(totalPollen + 1) : 0  // sticky binders
humidity_term = 0.02 × (RH / 100)                           // adhesion
rate = clamp(base_rate + coarse_term + pollen_term + humidity_term, 0.02, 1.5)  // % per day
```

At PM2.5=10: ~0.14%/day (clean suburban). At PM2.5=100: ~0.33%/day (unhealthy). Cap 30% total.

### Rain Cleaning

```
threshold = 15mm — below this, rain is ineffective (may redistribute dust)

baseEfficiency = 1 - exp(-0.1 × (rainfall - 15))

intensityFactor:
  < 1mm/hr (drizzle):     0.6–1.0×
  2–5mm/hr (moderate):    1.0× (optimal)
  5–10mm/hr (heavy):      0.8–1.0×
  > 10mm/hr (downpour):   0.7× (runoff waste)

durationFactor = min(1.2, 0.7 + (rainfall / intensity) × 0.05)

totalEfficiency = min(0.98, baseEfficiency × intensityFactor × durationFactor)
residualSoiling = 0.5 × (1 + PM2.5 / 100)  // sticky residues remain
```

### Panel Degradation by Type

| Type | Rate/yr | 25yr Retention | Source |
|------|---------|----------------|--------|
| Monocrystalline | 0.4% | 90% | NREL median |
| Polycrystalline | 0.65% | 84% | NREL + industry |
| Thin-film (CdTe, a-Si) | 1.2% | 70% | Oxford Academic |
| Bifacial (mono) | 0.4% | 90% | Similar to mono |

### Inverter Efficiency Penalties

```
voltage < 460V:       up to 30% penalty
frequency drift >0.5Hz: up to 30% penalty
temp > 60°C:         up to 30% penalty
string imbalance >15%: up to 40% penalty (per bad string)
fault condition:     30% penalty
```

All penalties multiply. Example: voltage 400V (0.93) × temp 75°C (0.82) × 1 bad string (0.85) = 65% inverter efficiency.

## Cleaning ROI Formula

```
projectedSoiling30d = currentSoiling + avgDailyRate × 30
avgSoiling = (currentSoiling + projectedSoiling30d) / 2
lossOver30Days = capacity × moduleEff × (avgSoiling/100) × peakSunHours × 30 × energyPrice
shouldClean = lossOver30Days > cleaningCost AND NOT rainImminent
```

Rain postponement: if rain forecast ≤7 days away AND ≥15mm expected, postpone cleaning.

## Energy Prices

Uses a static lookup table of 100+ countries/regions from EIA, IEA, and Statista data. National/state averages — NOT real-time, NOT time-of-use, NOT your specific tariff. Good enough for MVP decisions ($0.10 vs $0.30/kWh matters; $0.18 vs $0.19 doesn't). For production, wire a real energy price API.

## Cross-Session Persistence

Store soiling state in localStorage with `lastUpdateDate`. On next load, calculate days since last visit and run optimizer steps for each missed day using historical PM2.5 averages. Capped at 365 days catch-up. Soiling hard-capped at 30%.

## Pitfalls

- **Energy prices are static averages**, not real-time tariffs. Document this limitation explicitly.
- **Rain model needs hourly precipitation data**, not just daily totals. Open-Meteo's `hourly=precipitation` endpoint provides this.
- **Pollen data is seasonal** — API returns null outside pollen season. Handle gracefully.
- **PM10 is often null** in clean-air regions. The model treats null as "no coarse particles."
- **Server-side Gemini key storage**: save to `~/.<app>/config.json` with `chmod 600` so it survives restarts. Provide Test/Remove buttons in UI.
- **Geocoding debounce**: 400ms minimum to avoid rate limits on free geocoding APIs. Show "Searching..." while loading and "No locations found" on empty results.
- **String count dynamic**: When user changes number of strings, sync the telemetry array with useEffect — don't just reinitialize or you'll lose slider positions.
- **Master average slider**: When all strings are disabled (0A), dragging the master up should re-enable them rather than getting stuck.
