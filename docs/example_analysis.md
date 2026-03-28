# Stockpile 活用例: 財務データ分析

このドキュメントでは、Stockpile CLI を使って実際に財務データを取得・分析するワークフローを示す。

---

## 分析 1: 米国テック大手 3社比較 (AAPL / MSFT / GOOGL)

### データ取得

```bash
# 損益計算書
stockpile fundamentals income AAPL --format json > aapl_income.json
stockpile fundamentals income MSFT --format json > msft_income.json
stockpile fundamentals income GOOGL --format json > googl_income.json

# 貸借対照表
stockpile fundamentals balance AAPL --format json > aapl_balance.json
stockpile fundamentals balance MSFT --format json > msft_balance.json
stockpile fundamentals balance GOOGL --format json > googl_balance.json
```

### 収益性比較 (直近通期)

| 指標 | AAPL (2025/9期) | MSFT (2025/6期) | GOOGL (2025/12期) |
|---|---|---|---|
| 売上高 | $416.2B | $281.7B | $402.8B |
| 営業利益 | $133.1B | $128.5B | $129.0B |
| 純利益 | $112.0B | $101.8B | $132.2B |
| **営業利益率** | **32.0%** | **45.6%** | **32.0%** |
| **純利益率** | **26.9%** | **36.1%** | **32.8%** |
| EPS | $7.49 | $13.70 | $10.91 |

**考察:**
- MSFT は売上規模では最小だが、営業利益率 45.6% と群を抜いて高い。クラウド (Azure) とソフトウェアライセンスの高マージンビジネスが寄与
- GOOGL は純利益で AAPL を上回った ($132.2B)。広告以外の収益源が成長
- AAPL は売上高が最大だが、ハードウェア比率が高く利益率では MSFT に劣る

### 売上成長率 (YoY)

| 銘柄 | FY2022→2023 | FY2023→2024 | FY2024→2025 |
|---|---|---|---|
| AAPL | -2.8% | +2.0% | +6.4% |
| MSFT | +6.9% | +15.7% | +14.9% |
| GOOGL | +8.7% | +13.9% | +15.1% |

**考察:**
- AAPL は FY2022→2023 で売上が減少した後、緩やかに回復
- MSFT と GOOGL は安定して 2桁成長。AI 関連投資が成長を牽引

### 財務健全性

| 指標 | AAPL | MSFT | GOOGL |
|---|---|---|---|
| 総資産 | $359.2B | $619.0B | $595.3B |
| 自己資本 | $73.7B | $343.5B | $415.3B |
| 有利子負債 | $98.7B | $60.6B | $59.3B |
| **自己資本比率** | **20.5%** | **55.5%** | **69.8%** |
| **D/E レシオ** | **1.34** | **0.18** | **0.14** |
| **ROE** | **151.9%** | **29.6%** | **31.8%** |

**考察:**
- AAPL の自己資本比率は 20.5% と低い。自社株買いを積極的に行い意図的に自己資本を圧縮しているため。ROE は 151.9% と異常に高いが、レバレッジ効果が大きい
- GOOGL は D/E レシオ 0.14 と最も保守的な財務。実質無借金に近い
- MSFT は Activision Blizzard 買収等で資産が急増しているが、自己資本比率は健全

---

## 分析 2: 日本自動車メーカー比較 (トヨタ 7203 / ホンダ 7267)

### データ取得

```bash
stockpile fundamentals income 7203 --market jp --format json
stockpile fundamentals income 7267 --market jp --format json
stockpile fundamentals balance 7203 --market jp --format json
stockpile fundamentals balance 7267 --market jp --format json
```

### 収益性比較 (直近通期: 2025年3月期)

| 指標 | トヨタ (7203) | ホンダ (7267) |
|---|---|---|
| 売上高 | ¥48.0兆 | ¥21.7兆 |
| 営業利益 | ¥4.80兆 | ¥1.21兆 |
| 純利益 | ¥4.77兆 | ¥0.84兆 |
| **営業利益率** | **10.0%** | **5.6%** |
| **純利益率** | **9.9%** | **3.9%** |
| EPS | ¥359.56 | ¥178.93 |

### 売上成長率 (YoY)

| 銘柄 | FY2022→2023 | FY2023→2024 | FY2024→2025 |
|---|---|---|---|
| トヨタ | +18.4% | +21.4% | +6.5% |
| ホンダ | +16.2% | +20.8% | +6.2% |

### 財務健全性

| 指標 | トヨタ (7203) | ホンダ (7267) |
|---|---|---|
| 総資産 | ¥93.6兆 | ¥30.8兆 |
| 自己資本 | ¥35.9兆 | ¥12.3兆 |
| 有利子負債 | ¥38.8兆 | ¥4.4兆 |
| **自己資本比率** | **38.4%** | **40.0%** |
| **D/E レシオ** | **1.08** | **0.36** |
| **ROE** | **13.3%** | **6.8%** |

**考察:**
- トヨタは売上・利益ともにホンダの約 2倍。営業利益率も 10.0% vs 5.6% とトヨタが優位
- ただしトヨタの D/E レシオ 1.08 は自動車ローン等の金融事業を含むため高く見える。製造業本体だけなら実質的にはもっと低い
- ホンダは D/E 0.36 と相対的に保守的な財務

---

## 分析 3: 日米クロスマーケット比較

### 1年間の株価リターン (2024/4/1 → 2025/3/27)

| 銘柄 | 始値 | 終値 | リターン |
|---|---|---|---|
| AAPL | $169.65 | $222.88 | **+31.4%** |
| MSFT | $417.54 | $387.61 | **-7.2%** |
| GOOGL | $149.45 | $161.68 | **+8.2%** |
| トヨタ (7203) | ¥3,623 | ¥2,736 | **-24.5%** |
| ホンダ (7267) | ¥1,783 | ¥1,392 | **-21.9%** |

**考察:**
- 米国テックでは AAPL が +31.4% と突出。iPhone 需要の回復と AI 機能搭載が材料
- MSFT は -7.2% と意外にもマイナス。AI 投資の収益化への不透明感が株価を圧迫
- 日本自動車 2 社はともに -20% 超の下落。円高進行と中国市場の減速が逆風

### 営業利益率の日米比較

| | 米国テック平均 | 日本自動車平均 |
|---|---|---|
| 営業利益率 | **36.5%** | **7.8%** |
| 純利益率 | **31.9%** | **6.9%** |

ソフトウェア/プラットフォームビジネスと製造業の構造的な利益率差が明確に表れている。

---

## 分析のワークフロー

### ステップ 1: データ取得

```bash
# ターミナルで直接確認
stockpile fundamentals income AAPL

# JSON で取得してファイルに保存
stockpile fundamentals income AAPL --format json > data/aapl_income.json

# CSV でスプレッドシートに流し込み
stockpile fundamentals balance AAPL --format csv > data/aapl_balance.csv
```

### ステップ 2: パイプラインで加工

```bash
# 株価リターンの計算 (json出力をPythonでパイプ処理)
stockpile price get AAPL --start 2024-04-01 --end 2025-03-28 --format json | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
first, last = data[0], data[-1]
ret = (last['close'] - first['open']) / first['open'] * 100
print(f'{first[\"date\"]} → {last[\"date\"]}: {ret:+.1f}%')
"
```

### ステップ 3: 複数銘柄を一括取得

```bash
# シェルスクリプトで複数銘柄をループ
for symbol in AAPL MSFT GOOGL AMZN META; do
  echo "=== $symbol ==="
  stockpile fundamentals income $symbol
  echo
done
```

### ステップ 4: 定期レポートの自動化

```bash
# crontab に登録して毎朝 9:00 に実行
# 0 9 * * * /path/to/report.sh

#!/bin/bash
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

## 指標の計算方法

Stockpile で取得した生データから、主要な投資指標を計算できる。

| 指標 | 計算式 | 使用データ |
|---|---|---|
| 営業利益率 | operating_income / revenue | `fundamentals income` |
| 純利益率 | net_income / revenue | `fundamentals income` |
| ROE | net_income / equity | `fundamentals income` + `balance` |
| ROA | net_income / total_assets | `fundamentals income` + `balance` |
| 自己資本比率 | equity / total_assets | `fundamentals balance` |
| D/E レシオ | total_debt / equity | `fundamentals balance` |
| 売上成長率 | (今期revenue - 前期revenue) / 前期revenue | `fundamentals income` (複数期) |
| 株価リターン | (終値 - 始値) / 始値 | `price get` |
