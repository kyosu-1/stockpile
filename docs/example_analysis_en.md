# Stockpile Usage Example: Financial Data Analysis

This document demonstrates practical workflows for fetching and analyzing financial data using the Stockpile CLI.

---

## Analysis 1: US Big Tech Comparison (AAPL / MSFT / GOOGL)

### Data Collection

```bash
# Income statements
stockpile fundamentals income AAPL --format json > aapl_income.json
stockpile fundamentals income MSFT --format json > msft_income.json
stockpile fundamentals income GOOGL --format json > googl_income.json

# Balance sheets
stockpile fundamentals balance AAPL --format json > aapl_balance.json
stockpile fundamentals balance MSFT --format json > msft_balance.json
stockpile fundamentals balance GOOGL --format json > googl_balance.json
```

### Profitability Comparison (Latest Annual)

| Metric | AAPL (FY2025/9) | MSFT (FY2025/6) | GOOGL (FY2025/12) |
|---|---|---|---|
| Revenue | $416.2B | $281.7B | $402.8B |
| Operating Income | $133.1B | $128.5B | $129.0B |
| Net Income | $112.0B | $101.8B | $132.2B |
| **Operating Margin** | **32.0%** | **45.6%** | **32.0%** |
| **Net Margin** | **26.9%** | **36.1%** | **32.8%** |
| EPS | $7.49 | $13.70 | $10.91 |

**Key Takeaways:**
- MSFT has the smallest revenue but the highest operating margin at 45.6%, driven by high-margin cloud (Azure) and software licensing
- GOOGL surpassed AAPL in net income ($132.2B), reflecting growth in non-advertising revenue
- AAPL leads in revenue but hardware mix results in lower margins vs MSFT

### Revenue Growth (YoY)

| Ticker | FY2022→2023 | FY2023→2024 | FY2024→2025 |
|---|---|---|---|
| AAPL | -2.8% | +2.0% | +6.4% |
| MSFT | +6.9% | +15.7% | +14.9% |
| GOOGL | +8.7% | +13.9% | +15.1% |

**Key Takeaways:**
- AAPL experienced a revenue decline in FY2022→2023, followed by gradual recovery
- MSFT and GOOGL maintain consistent double-digit growth, fueled by AI investments

### Financial Health

| Metric | AAPL | MSFT | GOOGL |
|---|---|---|---|
| Total Assets | $359.2B | $619.0B | $595.3B |
| Equity | $73.7B | $343.5B | $415.3B |
| Total Debt | $98.7B | $60.6B | $59.3B |
| **Equity Ratio** | **20.5%** | **55.5%** | **69.8%** |
| **D/E Ratio** | **1.34** | **0.18** | **0.14** |
| **ROE** | **151.9%** | **29.6%** | **31.8%** |

**Key Takeaways:**
- AAPL's low equity ratio (20.5%) is intentional — aggressive buybacks compress equity, inflating ROE to 151.9% through leverage
- GOOGL is the most conservative with a D/E ratio of 0.14, essentially debt-free
- MSFT's asset growth reflects the Activision Blizzard acquisition, but equity ratio remains healthy

---

## Analysis 2: Japanese Automaker Comparison (Toyota 7203 / Honda 7267)

### Data Collection

```bash
stockpile fundamentals income 7203 --market jp --format json
stockpile fundamentals income 7267 --market jp --format json
stockpile fundamentals balance 7203 --market jp --format json
stockpile fundamentals balance 7267 --market jp --format json
```

### Profitability Comparison (FY2025/3)

| Metric | Toyota (7203) | Honda (7267) |
|---|---|---|
| Revenue | ¥48.0T | ¥21.7T |
| Operating Income | ¥4.80T | ¥1.21T |
| Net Income | ¥4.77T | ¥0.84T |
| **Operating Margin** | **10.0%** | **5.6%** |
| **Net Margin** | **9.9%** | **3.9%** |
| EPS | ¥359.56 | ¥178.93 |

### Revenue Growth (YoY)

| Ticker | FY2022→2023 | FY2023→2024 | FY2024→2025 |
|---|---|---|---|
| Toyota | +18.4% | +21.4% | +6.5% |
| Honda | +16.2% | +20.8% | +6.2% |

### Financial Health

| Metric | Toyota (7203) | Honda (7267) |
|---|---|---|
| Total Assets | ¥93.6T | ¥30.8T |
| Equity | ¥35.9T | ¥12.3T |
| Total Debt | ¥38.8T | ¥4.4T |
| **Equity Ratio** | **38.4%** | **40.0%** |
| **D/E Ratio** | **1.08** | **0.36** |
| **ROE** | **13.3%** | **6.8%** |

**Key Takeaways:**
- Toyota doubles Honda in both revenue and profit, with a significantly higher operating margin (10.0% vs 5.6%)
- Toyota's high D/E ratio (1.08) includes its financial services segment (auto loans); the manufacturing core is less leveraged
- Honda maintains a more conservative balance sheet with D/E of 0.36

---

## Analysis 3: Cross-Market Comparison (US vs Japan)

### 1-Year Stock Returns (2024/4/1 → 2025/3/27)

| Ticker | Open | Close | Return |
|---|---|---|---|
| AAPL | $169.65 | $222.88 | **+31.4%** |
| MSFT | $417.54 | $387.61 | **-7.2%** |
| GOOGL | $149.45 | $161.68 | **+8.2%** |
| Toyota (7203) | ¥3,623 | ¥2,736 | **-24.5%** |
| Honda (7267) | ¥1,783 | ¥1,392 | **-21.9%** |

**Key Takeaways:**
- AAPL stood out with +31.4%, driven by iPhone demand recovery and AI feature integration
- MSFT posted -7.2% despite strong fundamentals, reflecting market concerns about AI investment returns
- Both Japanese automakers fell over 20%, impacted by yen appreciation and China market slowdown

### Operating Margin: US Tech vs Japanese Auto

| | US Tech (avg) | Japan Auto (avg) |
|---|---|---|
| Operating Margin | **36.5%** | **7.8%** |
| Net Margin | **31.9%** | **6.9%** |

The structural margin gap between software/platform businesses and manufacturing is clearly visible.

---

## Workflow Patterns

### Pattern 1: Quick Terminal Check

```bash
# View income statement directly
stockpile fundamentals income AAPL

# Check current price
stockpile price current AAPL
```

### Pattern 2: Export for Spreadsheet Analysis

```bash
# Export to CSV for Google Sheets / Excel
stockpile fundamentals balance AAPL --format csv > data/aapl_balance.csv
stockpile price get AAPL --start 2024-01-01 --format csv > data/aapl_prices.csv
```

### Pattern 3: Pipeline Processing

```bash
# Calculate stock returns via pipe to Python
stockpile price get AAPL --start 2024-04-01 --end 2025-03-28 --format json | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
first, last = data[0], data[-1]
ret = (last['close'] - first['open']) / first['open'] * 100
print(f'{first[\"date\"]} -> {last[\"date\"]}: {ret:+.1f}%')
"
```

### Pattern 4: Batch Multi-Ticker Analysis

```bash
# Loop through multiple tickers
for symbol in AAPL MSFT GOOGL AMZN META; do
  echo "=== $symbol ==="
  stockpile fundamentals income $symbol
  echo
done
```

### Pattern 5: Automated Daily Report

```bash
#!/bin/bash
# Add to crontab: 0 9 * * * /path/to/report.sh
echo "=== Daily Report $(date +%Y-%m-%d) ==="
for sym in AAPL MSFT GOOGL; do
  stockpile price current $sym
done
echo "--- Japan ---"
for sym in 7203 7267; do
  stockpile price current $sym --market jp
done
```

---

## Financial Metrics Reference

Key investment metrics that can be calculated from Stockpile data:

| Metric | Formula | Data Source |
|---|---|---|
| Operating Margin | operating_income / revenue | `fundamentals income` |
| Net Margin | net_income / revenue | `fundamentals income` |
| ROE | net_income / equity | `fundamentals income` + `balance` |
| ROA | net_income / total_assets | `fundamentals income` + `balance` |
| Equity Ratio | equity / total_assets | `fundamentals balance` |
| D/E Ratio | total_debt / equity | `fundamentals balance` |
| Revenue Growth | (current - prior) / prior | `fundamentals income` (multi-period) |
| Stock Return | (end_close - start_open) / start_open | `price get` |
