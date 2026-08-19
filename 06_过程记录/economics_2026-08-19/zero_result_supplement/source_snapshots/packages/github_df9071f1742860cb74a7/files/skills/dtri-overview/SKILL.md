---
name: dtri-overview
description: Comprehensive guide to the Regional Digital Trade Integration Index (RDTII 2.1) framework, methodology, and economy-level data access for Asia-Pacific digital trade analysis.
version: 1.0.0
metadata:
  priority: 100
  filePattern: "**/*.{ts,js,py,md}"
  bashPattern: "(dtri|rdtii|trade.*integration)"
topics:
  - dtri
  - rdtii
  - digital-trade
  - un-escap
---

# DTRI Overview: Regional Digital Trade Integration Index

## What is RDTII?

The **Regional Digital Trade Integration Index (RDTII)** is a composite index developed by ESCAP to measure the readiness of Asia-Pacific economies for digital trade. Version 2.1 (2025) provides a comprehensive framework covering 12 pillars across 4 key dimensions.

**Official Source**: https://dtri.uneca.org/escap/trade-integration

### Key Resources

| Resource | URL |
|----------|-----|
| RDTII 2.1 Methodology Guide | https://dtri.uneca.org/assets/data/publications/ESCAP-2025-MN-RDTII-2.1-guide-en.pdf |
| DTRI Main Portal | https://dtri.uneca.org/ |
| ESCAP Dashboard | https://www.unescap.org/projects/rcdtra |

## RDTII 2.1 Framework

### Four Dimensions, Twelve Pillars

```
RDTII 2.1
├── Digital Trade Environment (Pillars 1-3)
│   ├── Pillar 1: Digital Trade Policies
│   ├── Pillar 2: Digital Trade Agreements
│   └── Pillar 3: Digital Infrastructure
│
├── Digital Trust & Environment (Pillars 4-7)
│   ├── Pillar 4: Cybersecurity
│   ├── Pillar 5: Data Governance
│   ├── Pillar 6: Digital Identity
│   └── Pillar 7: Consumer Protection
│
├── Business & Regulatory Environment (Pillars 8-10)
│   ├── Pillar 8: E-commerce Regulations
│   ├── Pillar 9: Competition Policy
│   └── Pillar 10: Digital Payments
│
└── Innovation & Capacity (Pillars 11-12)
    ├── Pillar 11: Digital Skills
    └── Pillar 12: Innovation Ecosystem
```

## Methodology

### Scoring System

- **Scale**: 0 to 100
- **0-20**: Very Low Readiness
- **21-40**: Low Readiness
- **41-60**: Medium Readiness
- **61-80**: High Readiness
- **81-100**: Very High Readiness

### Data Sources

1. **Primary Data Sources**
   - ESCAP Regional Databank
   - WTO Trade Policy Reviews
   - UNCTAD B2C E-commerce Index
   - ITU ICT Development Index
   - World Bank Doing Business
   - Global Cybersecurity Index

2. **Secondary Validation**
   - Government official publications
   - Regional organization reports
   - Industry association surveys

### Weighting Approach

- **Equal Weighting**: Each pillar contributes equally (1/12) to the overall index
- **Sub-indicator Weighting**: Within each pillar, indicators are weighted based on data availability and relevance
- **Missing Data Handling**: Imputation methods used for economies with incomplete data

## Economy Data Access

### Covered Economies

RDTII 2.1 covers **53 economies** across the Asia-Pacific region:

| Subregion | Economies |
|-----------|-----------|
| East & North-East Asia | China, Japan, Republic of Korea, Mongolia, DPR Korea, Taiwan Province of China |
| South-East Asia | ASEAN-10 + Timor-Leste |
| South & South-West Asia | Bangladesh, Bhutan, India, Iran, Maldives, Nepal, Pakistan, Sri Lanka |
| North & Central Asia | Armenia, Azerbaijan, Georgia, Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan |
| Pacific | Australia, New Zealand, Pacific Island States (14 economies) |
| Developed Economies | United States, Canada, Russian Federation (for comparative analysis) |

### Accessing Economy-Specific Data

To access data for a specific economy:

1. **Visit DTRI Portal**: https://dtri.uneca.org/escap/trade-integration
2. **Use Interactive Dashboard**: Select economy from dropdown
3. **Download Economy Profile**: Each economy has a downloadable PDF profile
4. **API Access**: Contact ESCAP for programmatic access (rdtii@un.org)

### Data Availability Notes

- **2025 Update**: Data reflects policies as of December 2024
- **Frequency**: Biennial updates (odd-numbered years)
- **Historical Data**: RDTII 1.0 (2019) and 2.0 (2022) available for trend analysis
- **Currency**: All monetary values in USD

## Regional Trends (2025)

### Top Performers (RDTII Score > 75)
- Singapore
- Republic of Korea
- Hong Kong, China
- Australia
- New Zealand

### Fastest Improvers (2022-2025)
- Vietnam (+8.2 points)
- Thailand (+6.5 points)
- Indonesia (+5.8 points)
- Bangladesh (+5.2 points)

### Key Challenges
- Digital infrastructure gaps in least developed countries
- Data governance framework fragmentation
- Cross-border data flow restrictions
- Digital skills shortage in rural areas

## Skill Dependencies

This overview skill provides context for domain-specific skills:

- `dtri-trade-policy` - Pillars 1, 2, 4 (Trade policies, agreements, cybersecurity)
- `dtri-infrastructure` - Pillar 3 (Digital infrastructure)
- `dtri-digital-trust` - Pillars 5, 6, 7 (Data governance, identity, consumer protection)
- `dtri-business-framework` - Pillars 8, 9, 10 (E-commerce, competition, payments)
- `dtri-innovation-capacity` - Pillars 11, 12 (Skills, innovation)

## Analysis Guidance

### Comparing Economies

When comparing RDTII scores across economies:

1. **Consider Economy Size**: Large economies may have different structural challenges
2. **Account for Income Level**: Adjust expectations based on development status
3. **Look at Sub-scores**: Overall scores may mask pillar-level strengths/weaknesses
4. **Check Trend Analysis**: Movement over time is more informative than static rankings

### Interpreting Scores

- **Score gaps > 20 points**: Indicate significant policy or infrastructure differences
- **Pillar-level variance**: Scores within 10 points across pillars indicate balanced development
- **Rapid score changes**: Usually reflect major policy reforms or infrastructure investments
- **Stagnation**: May indicate structural barriers or implementation gaps

### Common Use Cases

1. **Policy Benchmarking**: Compare against regional averages and top performers
2. **Investment Prioritization**: Identify gaps for resource allocation
3. **Trade Negotiation Support**: Use data to inform digital trade agreements
4. **Development Planning**: Set targets based on regional best practices
5. **Academic Research**: Source for econometric studies on digital trade

## Limitations

1. **Data Lag**: Some indicators may be 1-2 years behind current conditions
2. **Subjectivity**: Qualitative assessments introduce measurement bias
3. **Regulatory Change**: Frequent policy updates may not be captured immediately
4. **Cross-cutting Issues**: Some digital trade aspects span multiple pillars
5. **Subnational Variation**: Country-level scores may mask regional disparities

## Contact & Support

- **RDTII Team**: rdtii@un.org
- **ESCAP Trade, Investment & Innovation Division**: rcdtra@un.org
- **Mailing Address**: United Nations ESCAP, Rajadamnern Nok Avenue, Bangkok 10200, Thailand
