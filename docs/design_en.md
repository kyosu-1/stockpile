# Stockpile Design Document

## 1. Overview

Stockpile is a Python CLI tool that gathers stock investment information from free data sources, covering both US and Japanese markets.

### Purpose

- Provide a unified interface for accessing multiple free financial data sources
- Collect stock prices, financial statements, news, and macro economic indicators in a single tool
- Cache data locally in SQLite for offline access and re-analysis

### Target Users

Individual investors and data analysts who are comfortable with terminal-based workflows and prefer programmatic data access.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────┐
│                     CLI Layer                    │
│  (Typer + Rich)                                  │
│  price / fundamentals / news / macro / config    │
└──────────────┬──────────────────┬────────────────┘
               │                  │
       ┌───────▼───────┐  ┌──────▼───────┐
       │   Providers    │  │  Formatters  │
       │  (Protocol)    │  │  table/json  │
       │                │  │  /csv        │
       │  yfinance      │  └──────────────┘
       │  FRED          │
       │  (future:      │
       │   J-Quants,    │
       │   EDINET,      │
       │   e-Stat,      │
       │   FMP,         │
       │   Finnhub)     │
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │    Storage      │
       │   (SQLite)      │
       └────────────────┘
```

### Design Principles

- **Provider Pattern**: Each data source implements a Protocol-based class. Adding a new source requires only adding a single class
- **Minimal dependencies**: Uses dataclass instead of Pydantic. pandas exists only as a transitive dependency of yfinance and is not exposed to the application layer
- **Synchronous I/O**: No async. Synchronous HTTP via requests is sufficient for a CLI tool

---

## 3. Data Sources

### 3.1 Currently Implemented

| Source | Data Types | API Key | Markets | Notes |
|---|---|---|---|---|
| **yfinance** | Prices, financials, news | Not required | US + JP | Unofficial Yahoo Finance wrapper. JP stocks via `.T` suffix |
| **FRED** | Macro economic indicators | **Required** (free) | US + some JP | 800,000+ economic time series. GDP, CPI, rates, etc. |

### 3.2 Planned

| Source | Data Types | API Key | Markets | Notes |
|---|---|---|---|---|
| **J-Quants** | Prices, financials | Required (free) | JP (official) | Official JPX data for TSE-listed stocks |
| **EDINET** | Financial statements | Not required | JP (official) | FSA disclosure system. XBRL data from annual/quarterly reports |
| **e-Stat** | Macro indicators | Required (free) | JP | Japanese government statistics. GDP, CPI, labor data |
| **Financial Modeling Prep** | Financial statements | Required (free: 250/day) | US | Well-structured US company financials |
| **Finnhub** | News, prices | Required (free: 60/min) | US | Real-time WebSocket support, sentiment analysis |
| **GNews** | News | Required (free: 100/day) | Global | Supports Japanese language news sources |

### 3.3 Provider Selection Logic

The Registry selects providers based on market and data type:

| Data Type | US Default | JP Default | Fallback |
|---|---|---|---|
| Prices | yfinance | J-Quants -> yfinance | yfinance |
| Financials | FMP -> yfinance | EDINET -> yfinance | yfinance |
| News | Finnhub -> yfinance | GNews -> yfinance | yfinance |
| Macro | FRED | e-Stat / FRED | FRED |

When an API key is not configured, the system falls back to yfinance (except for macro indicators).

---

## 4. Data Models

All models are defined as Python `dataclass` types. Each includes a `to_dict()` method that converts date/datetime fields to ISO 8601 strings for serialization.

### Price Data

```
OHLCV
├── symbol: str          # Ticker symbol
├── date: date           # Trading date
├── open: float          # Opening price
├── high: float          # High price
├── low: float           # Low price
├── close: float         # Closing price
└── volume: int          # Trading volume

Quote
├── symbol: str
├── price: float         # Current price
├── change: float        # Change from previous close
├── change_pct: float    # Change percentage
└── timestamp: datetime
```

### Financial Statements

```
IncomeStatement            BalanceSheet               CashFlow
├── symbol                 ├── symbol                 ├── symbol
├── period_end             ├── period_end             ├── period_end
├── period_type            ├── period_type            ├── period_type
├── revenue                ├── total_assets           ├── operating_cf
├── operating_income       ├── total_liabilities      ├── investing_cf
├── net_income             ├── equity                 ├── financing_cf
├── ebitda                 ├── cash                   └── free_cash_flow
└── eps                    └── total_debt
```

All financial fields are `float | None`. Fields unavailable from a specific data source are set to `None`.

### News & Macro

```
Article                    MacroDataPoint
├── title: str             ├── indicator_id: str
├── url: str               ├── date: date
├── source: str            ├── value: float
├── published_at: datetime └── unit: str
├── summary: str | None
└── symbols: list[str] | None
```

---

## 5. Storage

### SQLite Schema

```sql
-- Stock prices (stored per provider, updated daily)
ohlcv (symbol, date, open, high, low, close, volume, source, fetched_at)
  PK: (symbol, date, source)

-- Financial statements (stored as JSON blobs to handle schema differences across providers)
financials (symbol, period_end, statement, period_type, data, source, fetched_at)
  PK: (symbol, period_end, statement, period_type, source)
  statement: "income" | "balance" | "cashflow"

-- News articles (unique constraint on URL)
articles (id, title, url, source, published_at, summary, symbols, fetched_at)
  PK: id (AUTO INCREMENT)
  UNIQUE: url

-- Macro economic indicators
macro (indicator_id, date, value, unit, source, fetched_at)
  PK: (indicator_id, date, source)
```

### Design Decisions

- **JSON blob for financials**: EDINET (JP GAAP/IFRS) and FMP (US GAAP) have different field sets. Normalizing into a rigid schema would be fragile. Common fields are extracted into dataclasses for display; raw data is preserved as JSON
- **source column**: Distinguishes data from different providers for the same ticker
- **fetched_at**: Used for cache freshness management
- **Upsert strategy**: Prices and macro use `INSERT OR REPLACE`; news uses `INSERT OR IGNORE` to prevent URL duplicates

---

## 6. CLI Design

### Command Structure

```bash
# Prices
stockpile price get <SYMBOL> [--start DATE] [--end DATE] [--market us|jp] [--format table|json|csv]
stockpile price current <SYMBOL> [--market us|jp]

# Financial Statements
stockpile fundamentals income <SYMBOL> [--period annual|quarterly] [--market us|jp] [--format ...]
stockpile fundamentals balance <SYMBOL> [--period annual|quarterly] [--market us|jp] [--format ...]
stockpile fundamentals cashflow <SYMBOL> [--period annual|quarterly] [--market us|jp] [--format ...]

# News
stockpile news get <SYMBOL> [--limit N] [--market us|jp] [--format ...]

# Macro Economic Indicators
stockpile macro get <INDICATOR_ID> [--start DATE] [--end DATE] [--source fred|estat] [--format ...]
stockpile macro list [--source fred|estat] [--search QUERY]

# Configuration
stockpile config init
stockpile config show
```

### Output Formats

| Format | Use Case |
|---|---|
| `table` (default) | Terminal viewing. Colored output via Rich |
| `json` | Programmatic consumption, pipeline integration |
| `csv` | Spreadsheet export |

---

## 7. Configuration

Config file: `~/.config/stockpile/config.toml`

```toml
[storage]
backend = "sqlite"
path = "~/.local/share/stockpile/data"

[defaults]
market = "us"           # Default market
output_format = "table" # Default output format

[api_keys]
jquants = ""   # J-Quants (JP official stock data)
fmp = ""       # Financial Modeling Prep (US financials)
finnhub = ""   # Finnhub (news, prices)
gnews = ""     # GNews (news)
fred = ""      # FRED (macro indicators)
```

### API Key Sources

| Service | Registration URL | Free Tier |
|---|---|---|
| FRED | https://fred.stlouisfed.org/docs/api/api_key.html | 120 req/min |
| J-Quants | https://jpx-jquants.com/ | 12 req/min |
| FMP | https://financialmodelingprep.com/ | 250 req/day |
| Finnhub | https://finnhub.io/ | 60 req/min |
| GNews | https://gnews.io/ | 100 req/day |

---

## 8. Technology Stack

| Component | Choice | Rationale |
|---|---|---|
| Language | Python 3.13+ | Rich ecosystem for data libraries, yfinance availability |
| Package manager | uv | Fast, lockfile support |
| CLI framework | Typer | Type-hint driven, auto-generated help |
| Terminal output | Rich | Tables, colors, spinners |
| HTTP client | requests | Simple synchronous HTTP, sufficient for CLI |
| Data models | dataclass | No Pydantic, minimal dependencies |
| Storage | SQLite (stdlib) | Zero additional dependencies, single-file database |

---

## 9. Project Structure

```
stockpile/
├── docs/
│   ├── design.md              # Design document (Japanese)
│   └── design_en.md           # Design document (English)
├── src/stockpile/
│   ├── __init__.py
│   ├── config.py              # Configuration loading
│   ├── models.py              # Data models (dataclass)
│   ├── registry.py            # Provider selection
│   ├── cli/
│   │   ├── app.py             # Entry point
│   │   ├── price.py           # Price commands
│   │   ├── fundamentals.py    # Financial statement commands
│   │   ├── news.py            # News commands
│   │   ├── macro.py           # Macro indicator commands
│   │   ├── config_cmd.py      # Config commands
│   │   └── formatters.py      # Output formatting
│   ├── providers/
│   │   ├── base.py            # Protocol definitions
│   │   ├── yfinance_provider.py  # yfinance (prices, financials, news)
│   │   ├── fred_provider.py      # FRED (macro economics)
│   │   └── news_provider.py      # yfinance news
│   └── storage/
│       ├── base.py            # Storage Protocol
│       └── sqlite.py          # SQLite implementation
├── tests/
├── pyproject.toml
├── config.example.toml
└── README.md
```

---

## 10. Future Roadmap

### Phase 6: Japan-Specific Providers
- J-Quants provider (official TSE stock data)
- EDINET provider (XBRL financial statement parsing)
- e-Stat provider (Japanese government macro statistics)

### Phase 7: Feature Enhancements
- `price compare` command (multi-ticker comparison)
- `fundamentals summary` command (key metrics overview)
- Automatic SQLite caching on data fetch
- Rate limiting and retry logic
- Watchlist functionality

### Phase 8: Quality Improvements
- Test suite (HTTP mocking via responses library)
- CI/CD (GitHub Actions: lint + test)
- Improved error messages and user guidance
