# PolicyStack

**Indian government scheme tracker -- budgets, performance, and policy data.**

[![Part of OpenStacks](https://img.shields.io/badge/Part%20of-OpenStacks-blue)](https://openstacks.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Retired](https://img.shields.io/badge/Status-Retired-6b7280?style=flat-square)](https://github.com/Varnasr/OpenStacks-for-Change/blob/main/MAINTENANCE.md)

> Structured, open data on 15 flagship government schemes across health, education, gender, livelihoods, and climate.

> **Status: Retired.** This repository is archived and read-only. It holds the
> original static dataset: 15 flagship schemes with four years of budget data.
> [PolicyDhara](https://github.com/Varnasr/PolicyDhara) replaced it; it covers the
> same ground and updates itself. The code and data stay public so that links,
> citations and forks keep working. See the
> [maintenance policy](https://github.com/Varnasr/OpenStacks-for-Change/blob/main/MAINTENANCE.md).

---

## What's Inside

```
PolicyStack/
├── data/
│   ├── schemes/           # 15 flagship scheme metadata (CSV)
│   ├── budgets/           # 4-year budget allocation and spending data
│   └── indicators/        # Scheme performance indicators with baselines
├── scripts/
│   ├── analysis/          # Budget analysis and scheme scorecard scripts
│   └── scrapers/          # Templates for parsing budget PDFs and dashboards
├── docs/
│   └── methodology.md     # Data collection methodology and standards
└── requirements.txt       # Python dependencies
```

## Data Coverage

### 15 Flagship Schemes

| Sector | Schemes |
|--------|---------|
| Health | Ayushman Bharat (PM-JAY), POSHAN Abhiyaan, National Health Mission |
| WASH | Swachh Bharat Mission, Jal Jeevan Mission |
| Education | Samagra Shiksha, PM POSHAN (Mid-Day Meal), Skill India |
| Gender | Beti Bachao Beti Padhao, DAY-NRLM |
| Livelihoods | MGNREGA, PM-KISAN, PMAY-Gramin, PMAY-Urban |
| Climate | National Clean Air Programme |

### Budget Data (2020-2024)

4 years of budget data for each scheme:
- **Allocated** -- Budget Estimate from Union Budget
- **Revised** -- Revised Estimate (mid-year adjustment)
- **Spent** -- Actual expenditure
- **Utilization rate** -- Spent / Allocated (%)

### Performance Indicators

Baseline vs. latest values for key outcome indicators per scheme, with direction (higher/lower is better) and data source.

## Analysis Scripts

### Budget Analysis
```bash
python scripts/analysis/budget_analysis.py
```
Outputs:
- Sector-wise spending summary
- Top schemes ranked by allocation
- Budget trend charts (per scheme)
- Utilization heatmap across all schemes and years

### Scheme Performance Scorecard
```bash
python scripts/analysis/scheme_performance.py
```
Outputs:
- Indicator progress (baseline to latest, improving/worsening)
- Composite scorecard combining budget utilization and outcome indicators

### Scraper Templates
- `budget_pdf_parser.py` -- Template for extracting tables from Union Budget PDFs
- `scheme_dashboard_scraper.py` -- Patterns for fetching data from government dashboard APIs

## Getting Started

```bash
pip install -r requirements.txt
python scripts/analysis/budget_analysis.py
python scripts/analysis/scheme_performance.py
```

## Data Sources

| Source | URL | Data |
|--------|-----|------|
| Union Budget | indiabudget.gov.in | Budget allocations |
| MGNREGA MIS | nrega.nic.in | Employment days, wages |
| JJM Dashboard | ejalshakti.gov.in | Tap connections |
| PM-KISAN | pmkisan.gov.in | Beneficiaries |
| NHA Dashboard | pmjay.gov.in | Hospital admissions |
| NFHS-5 | rchiips.org/nfhs | Health/nutrition outcomes |
| UDISE+ | udiseplus.gov.in | Education indicators |

See [docs/methodology.md](docs/methodology.md) for full methodology and data standards.

## How It Connects

PolicyStack is a domain-specific stack in the [OpenStacks](https://openstacks.dev) ecosystem:

| Stack | Role |
|-------|------|
| [RootStack](https://github.com/Varnasr/RootStack) | Database with scheme data (PostgreSQL) |
| [BridgeStack](https://github.com/Varnasr/BridgeStack) | API serving scheme and budget data |
| [EquityStack](https://github.com/Varnasr/EquityStack) | Python analysis workflows |
| **PolicyStack** (this repo) | Source data, scrapers, and policy analysis |

## Contributing

Areas where contributions are welcome:
- Adding state-level budget disaggregation
- New scheme datasets
- Scraper scripts for government portals
- Data journalism and analysis notebooks

See [contributing guidelines](https://github.com/Varnasr/.github/blob/main/CONTRIBUTING.md) or open an issue.

## License

MIT -- free to use, modify, and share. See [LICENSE](LICENSE).

---

**Created by [Varna Sri Raman](https://github.com/Varnasr)** -- Development Economist & Social Researcher
