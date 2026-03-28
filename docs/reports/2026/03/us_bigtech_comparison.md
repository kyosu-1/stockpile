# US Big Tech 財務分析: GAFAM + TSLA + NVDA

- **日付:** 2026-03-28
- **対象:** AAPL, MSFT, GOOGL, AMZN, META, TSLA, NVDA
- **手法:** [財務指標定義](../../methodology/financial_metrics.md) / [スクリーニング基準](../../methodology/screening_criteria.md)

---

## データ取得

```bash
stockpile metrics compare AAPL MSFT GOOGL --format json
stockpile metrics compare AMZN META --format json
stockpile metrics compare TSLA NVDA --format json
```

---

## 収益性

| 銘柄 | 営業利益率 | 純利益率 | EBITDA利益率 |
|---|---:|---:|---:|
| **NVDA** | **60.4%** | **55.6%** | **66.9%** |
| MSFT | 45.6% | 36.1% | 56.9% |
| META | 41.4% | 30.1% | 52.6% |
| AAPL | 32.0% | 26.9% | 34.8% |
| GOOGL | 32.0% | 32.8% | 44.9% |
| AMZN | 11.2% | 10.8% | 23.1% |
| TSLA | 5.1% | 4.0% | 12.4% |

NVDA が全指標で圧倒。TSLA は営業利益率 5.1% まで低下し、Tier 1 基準ギリギリ。

## 資本効率

| 銘柄 | ROE | ROA |
|---|---:|---:|
| AAPL | 151.9%※ | 31.2% |
| **NVDA** | **76.3%** | **58.1%** |
| GOOGL | 31.8% | 22.2% |
| MSFT | 29.6% | 16.4% |
| META | 27.8% | 16.5% |
| AMZN | 18.9% | 9.5% |
| TSLA | 4.6% | 2.8% |

※AAPL の ROE はレバレッジ効果 (自己資本比率 20.5%)。ROA で見ると NVDA (58.1%) が真の効率王。

## 財務健全性

| 銘柄 | 自己資本比率 | D/E |
|---|---:|---:|
| **NVDA** | **76.1%** | **0.07** |
| GOOGL | 69.8% | 0.14 |
| TSLA | 59.6% | 0.18 |
| META | 59.3% | 0.39 |
| MSFT | 55.5% | 0.18 |
| AMZN | 50.2% | 0.37 |
| AAPL | 20.5% | 1.34 |

## 成長性

| 銘柄 | 売上成長 | 純利益成長 |
|---|---:|---:|
| **NVDA** | **+65.5%** | **+64.8%** |
| META | +22.2% | -3.1% |
| GOOGL | +15.1% | +32.0% |
| MSFT | +14.9% | +15.5% |
| AMZN | +12.4% | +31.1% |
| AAPL | +6.4% | +19.5% |
| TSLA | -2.9% | -46.8% |

## 株価リターン (2024/4 → 2025/3)

| 銘柄 | リターン |
|---|---:|
| TSLA | +55.0% |
| AAPL | +31.4% |
| META | +24.1% |
| NVDA | +23.4% |
| AMZN | +11.4% |
| GOOGL | +8.2% |
| MSFT | -7.2% |

## 総合評価

| 銘柄 | 収益性 | 資本効率 | 財務 | 成長性 | 総合 |
|---|---|---|---|---|---|
| **NVDA** | S | S | S | S | **S** |
| **MSFT** | S | A | A | A | **S** |
| **GOOGL** | A | A | S | A | **A** |
| META | S | A | A | B | A |
| AAPL | A | A | C | B | A |
| AMZN | C | B | B | A | B |
| TSLA | C | C | A | C | C |

### 結論

- **NVDA が全 4 軸で S ランク。** 利益率 60%、ROA 58%、D/E 0.07、売上 +65%。現時点で最も優良
- **MSFT が GAFAM 内で最優良。** 利益率と安定成長のバランスが最も良い
- **TSLA は財務的には最下位。** 純利益 -47% で C 評価。株価 +55% は将来期待のみ
