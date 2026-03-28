# Financial Metrics / 財務指標の定義

Stockpile の `metrics` コマンドが算出する指標の定義・計算式・解釈方法を記載する。

---

## 1. 収益性指標 (Profitability)

### 営業利益率 (Operating Margin)

| 項目 | 内容 |
|---|---|
| 計算式 | `operating_income / revenue × 100` |
| データソース | `stockpile fundamentals income` |
| 意味 | 本業でどれだけ効率的に利益を生んでいるか |
| 目安 | 10%以上で優良、20%以上で非常に高い、40%超は独占的ポジション |

### 純利益率 (Net Margin)

| 項目 | 内容 |
|---|---|
| 計算式 | `net_income / revenue × 100` |
| データソース | `stockpile fundamentals income` |
| 意味 | 税引後で株主に帰属する利益の割合 |
| 注意 | 特別損益や税制の影響を受けるため、営業利益率と併せて見る |

### EBITDA マージン (EBITDA Margin)

| 項目 | 内容 |
|---|---|
| 計算式 | `ebitda / revenue × 100` |
| データソース | `stockpile fundamentals income` |
| 意味 | 減価償却前の収益力。設備投資の大きい業種間の比較に有用 |

---

## 2. 資本効率指標 (Capital Efficiency)

### ROE (Return on Equity / 自己資本利益率)

| 項目 | 内容 |
|---|---|
| 計算式 | `net_income / equity × 100` |
| データソース | `stockpile fundamentals income` + `balance` |
| 意味 | 株主資本に対する利益率。投資家にとって最重要指標の一つ |
| 目安 | 8%以上で合格、15%以上で優良、30%超は要因分析が必要 |
| 注意 | 自社株買い等で自己資本が小さい場合、見かけ上高くなる (例: AAPL 151.9%) |

### ROA (Return on Assets / 総資産利益率)

| 項目 | 内容 |
|---|---|
| 計算式 | `net_income / total_assets × 100` |
| データソース | `stockpile fundamentals income` + `balance` |
| 意味 | 全資産に対する利益率。レバレッジの影響を排除した資本効率 |
| 目安 | 5%以上で優良、10%超で非常に効率的 |
| 用途 | ROE が高い企業が実力なのかレバレッジなのかを判別する |

### DuPont 分解 (参考)

```
ROE = 純利益率 × 総資産回転率 × 財務レバレッジ
    = (Net Income / Revenue) × (Revenue / Total Assets) × (Total Assets / Equity)
```

ROE が高い要因を分解して「利益率型」「回転率型」「レバレッジ型」を判別する。

---

## 3. 財務健全性指標 (Financial Health)

### 自己資本比率 (Equity Ratio)

| 項目 | 内容 |
|---|---|
| 計算式 | `equity / total_assets × 100` |
| データソース | `stockpile fundamentals balance` |
| 意味 | 総資産のうち自己資本の割合。高いほど財務的に安定 |
| 目安 | 40%以上で安定、60%以上で堅固、80%超は過剰資本の可能性も |
| 注意 | 金融・保険業は事業特性上低くなる（保険準備金等） |

### D/E レシオ (Debt to Equity Ratio)

| 項目 | 内容 |
|---|---|
| 計算式 | `total_debt / equity` |
| データソース | `stockpile fundamentals balance` |
| 意味 | 自己資本に対する有利子負債の倍率。低いほど安全 |
| 目安 | 0.5以下で健全、1.0以下で許容範囲、1.0超は要精査 |
| 注意 | 自動車・商社は金融事業を含むため構造的に高くなる |

---

## 4. 成長性指標 (Growth)

### 売上成長率 (Revenue Growth)

| 項目 | 内容 |
|---|---|
| 計算式 | `(current_revenue - prior_revenue) / abs(prior_revenue) × 100` |
| データソース | `stockpile fundamentals income` (複数期) |
| 意味 | 前年比の売上増加率 |
| 目安 | 5%以上で成長、10%以上で高成長、20%超で急成長 |

### 純利益成長率 (Net Income Growth)

| 項目 | 内容 |
|---|---|
| 計算式 | `(current_net_income - prior_net_income) / abs(prior_net_income) × 100` |
| データソース | `stockpile fundamentals income` (複数期) |
| 注意 | 前期が赤字の場合、成長率は参考にならない |

### EPS 成長率 (EPS Growth)

| 項目 | 内容 |
|---|---|
| 計算式 | `(current_eps - prior_eps) / abs(prior_eps) × 100` |
| 意味 | 1株当たり利益の成長率。自社株買いの効果も反映 |

---

## 5. 指標の取得コマンド

```bash
# 1銘柄の全指標を一括取得
stockpile metrics get AAPL
stockpile metrics get 6861 --market jp

# 複数銘柄の横並び比較
stockpile metrics compare AAPL MSFT GOOGL
stockpile metrics compare 6861 4519 8035 --market jp

# JSON で取得 (LLM / スクリプト向け)
stockpile metrics get AAPL --format json
stockpile metrics compare AAPL MSFT --format json
```

---

## 6. 業種別の注意点

| 業種 | 注意点 |
|---|---|
| **製造業** | D/E は設備投資水準に依存。EBITDA マージンで比較するのが適切 |
| **金融・保険** | 自己資本比率は事業特性上低い。営業利益が取れない場合がある |
| **商社** | 売上（取扱高）が巨額だが利益率は構造的に低い。ROE で評価 |
| **IT/SaaS** | 営業利益率が高い傾向。R&D 費用の資本化に注意 |
| **医薬品** | パイプラインの将来価値が財務に反映されない。成長率で補完 |
| **小売** | 薄利多売型。営業利益率 5-15% でも業界では優良 |
