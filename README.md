# Stockpile

Stock investment information gathering CLI tool for US and Japanese markets.

## Features

- **Stock Prices** - Historical and current price data (OHLCV) for US and Japanese stocks
- **Financial Statements** - Income statement, balance sheet, cash flow
- **News** - Company-related news articles
- **Macro Economic Indicators** - GDP, CPI, interest rates, etc. via FRED API
- **Multiple Output Formats** - Table, JSON, CSV

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
git clone https://github.com/kyosu-1/stockpile.git
cd stockpile
uv sync
```

## Usage

### Stock Prices

```bash
# Historical prices (defaults to last 30 days)
stockpile price get AAPL
stockpile price get AAPL --start 2025-01-01 --end 2025-03-01

# Japanese stocks
stockpile price get 7203 --market jp

# Current price
stockpile price current AAPL

# Output as JSON or CSV
stockpile price get AAPL --format json
stockpile price get AAPL --format csv
```

### Financial Statements

```bash
# Income statement
stockpile fundamentals income AAPL
stockpile fundamentals income AAPL --period quarterly

# Balance sheet
stockpile fundamentals balance AAPL

# Cash flow
stockpile fundamentals cashflow AAPL

# Japanese stocks
stockpile fundamentals income 7203 --market jp
```

### News

```bash
stockpile news get AAPL
stockpile news get AAPL --limit 5
stockpile news get 7203 --market jp
```

### Macro Economic Indicators

Requires a free [FRED API key](https://fred.stlouisfed.org/docs/api/api_key.html).

```bash
# List popular indicators
stockpile macro list

# Search for indicators
stockpile macro list --search "japan gdp"

# Fetch indicator data
stockpile macro get GDP
stockpile macro get FEDFUNDS --start 2024-01-01
```

### Configuration

```bash
# Create config file (~/.config/stockpile/config.toml)
stockpile config init

# Show current config
stockpile config show
```

## Configuration

Config file is stored at `~/.config/stockpile/config.toml`:

```toml
[storage]
backend = "sqlite"

[defaults]
market = "us"
output_format = "table"

[api_keys]
fred = "your-fred-api-key"
finnhub = ""
fmp = ""
```

## Data Sources

| Data Type | US | Japan |
|---|---|---|
| Stock Prices | yfinance | yfinance (`.T` suffix) |
| Financial Statements | yfinance | yfinance |
| News | yfinance | yfinance |
| Macro Indicators | FRED | FRED (Japan series) |

## Development

```bash
# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest

# Lint
uv run ruff check .
```

## License

MIT
