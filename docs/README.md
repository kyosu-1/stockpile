# Stockpile Documentation

## Structure

```
docs/
├── README.md                 # This file
├── design.md                 # Design document (JP)
├── design_en.md              # Design document (EN)
├── methodology/              # Analysis methodology (reusable)
│   ├── financial_metrics.md  # Financial metrics definitions and formulas
│   └── screening_criteria.md # Screening criteria for stock selection
└── reports/                  # Time-series analysis reports
    └── YYYY/
        └── MM/
            └── topic.md      # Individual report
```

## How to Add Reports

Reports are organized by date: `reports/YYYY/MM/topic.md`

Each report should include:
- Date of analysis
- Tickers analyzed
- Commands used to fetch data
- Key findings
- Methodology reference (link to `methodology/`)

## Reports Index

### 2026

- [2026/03 - GAFAM + TSLA/NVDA Financial Analysis](reports/2026/03/us_bigtech_comparison.md)
- [2026/03 - Japanese Blue Chip Screening](reports/2026/03/jp_bluechip_screening.md)
