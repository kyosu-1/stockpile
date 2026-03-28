# Stockpile Design Document

## 1. Overview

Stockpile は、日本・米国の株式投資に必要な情報を無料のデータソースから収集する Python CLI ツールである。

### 目的

- 複数の無料データソースを統一的なインターフェースで扱う
- 株価・財務諸表・ニュース・マクロ経済指標を 1 つのツールで取得できる
- ローカルにデータをキャッシュし、オフラインでの再参照を可能にする

### 対象ユーザー

個人投資家・データ分析者。ターミナル操作に慣れており、プログラムによるデータ取得を好むユーザーを想定。

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

### 設計方針

- **Provider Pattern**: データソースごとに Protocol に準拠したクラスを実装。新しいデータソースの追加はクラスを 1 つ追加するだけで完了する
- **軽量な依存**: Pydantic を使わず dataclass で統一。pandas は yfinance の内部依存としてのみ存在し、アプリケーション層には露出しない
- **同期 I/O**: CLI ツールのため async は不使用。requests による同期 HTTP で十分

---

## 3. Data Sources

### 3.1 現在実装済み

| ソース | 種別 | API キー | 対象市場 | 備考 |
|---|---|---|---|---|
| **yfinance** | 株価・財務・ニュース | 不要 | US + JP | Yahoo Finance の非公式ラッパー。日本株は `.T` サフィックスで対応 |
| **FRED** | マクロ経済指標 | **必要** (無料) | US + 一部 JP | 80万以上の経済時系列。GDP, CPI, 金利等 |

### 3.2 今後追加予定

| ソース | 種別 | API キー | 対象市場 | 備考 |
|---|---|---|---|---|
| **J-Quants** | 株価・財務 | 必要 (無料) | JP (公式) | JPX 公式データ。TSE 上場銘柄の信頼性の高いデータ |
| **EDINET** | 財務諸表 | 不要 | JP (公式) | 金融庁の開示システム。有報・四半期報告の XBRL データ |
| **e-Stat** | マクロ経済指標 | 必要 (無料) | JP | 日本政府統計。GDP, CPI, 労働統計等 |
| **Financial Modeling Prep** | 財務諸表 | 必要 (無料枠 250回/日) | US | 整形済みの米国企業財務データ |
| **Finnhub** | ニュース・株価 | 必要 (無料枠 60回/分) | US | リアルタイム WebSocket 対応、センチメント分析 |
| **GNews** | ニュース | 必要 (無料枠 100回/日) | グローバル | 日本語ニュースにも対応 |

### 3.3 データソース選択ロジック

Registry がマーケットとデータ種別に基づいてプロバイダーを選択する:

| データ種別 | US デフォルト | JP デフォルト | フォールバック |
|---|---|---|---|
| 株価 | yfinance | J-Quants → yfinance | yfinance |
| 財務諸表 | FMP → yfinance | EDINET → yfinance | yfinance |
| ニュース | Finnhub → yfinance | GNews → yfinance | yfinance |
| マクロ | FRED | e-Stat / FRED | FRED |

API キーが設定されていない場合は yfinance にフォールバックする（マクロ以外）。

---

## 4. Data Models

すべて `dataclass` で定義。`to_dict()` メソッドで日付型を ISO 8601 文字列に変換し、シリアライズに対応。

### 株価

```
OHLCV
├── symbol: str          # ティッカーシンボル
├── date: date           # 取引日
├── open: float          # 始値
├── high: float          # 高値
├── low: float           # 安値
├── close: float         # 終値
└── volume: int          # 出来高

Quote
├── symbol: str
├── price: float         # 現在価格
├── change: float        # 前日比
├── change_pct: float    # 前日比 (%)
└── timestamp: datetime
```

### 財務諸表

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

各フィールドは `float | None` で、データソースによって取得できない項目は `None` となる。

### ニュース・マクロ

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

### SQLite スキーマ

```sql
-- 株価データ (プロバイダー別に保存、日次で更新)
ohlcv (symbol, date, open, high, low, close, volume, source, fetched_at)
  PK: (symbol, date, source)

-- 財務諸表 (JSON blob で保存、プロバイダー間のスキーマ差異を吸収)
financials (symbol, period_end, statement, period_type, data, source, fetched_at)
  PK: (symbol, period_end, statement, period_type, source)
  statement: "income" | "balance" | "cashflow"

-- ニュース記事 (URL でユニーク制約)
articles (id, title, url, source, published_at, summary, symbols, fetched_at)
  PK: id (AUTO INCREMENT)
  UNIQUE: url

-- マクロ経済指標
macro (indicator_id, date, value, unit, source, fetched_at)
  PK: (indicator_id, date, source)
```

### 設計判断

- **financials を JSON blob で保存**: EDINET (JP GAAP/IFRS) と FMP (US GAAP) ではフィールドが異なる。正規化すると脆弱になるため、共通フィールドは dataclass で抽出し、生データは JSON で保持
- **source カラム**: 同一銘柄を複数プロバイダーから取得した場合に区別可能
- **fetched_at**: キャッシュの鮮度管理に使用
- **UPSERT 戦略**: 株価・マクロは `INSERT OR REPLACE`、ニュースは `INSERT OR IGNORE` (URL 重複防止)

---

## 6. CLI Design

### コマンド体系

```bash
# 株価
stockpile price get <SYMBOL> [--start DATE] [--end DATE] [--market us|jp] [--format table|json|csv]
stockpile price current <SYMBOL> [--market us|jp]

# 財務諸表
stockpile fundamentals income <SYMBOL> [--period annual|quarterly] [--market us|jp] [--format ...]
stockpile fundamentals balance <SYMBOL> [--period annual|quarterly] [--market us|jp] [--format ...]
stockpile fundamentals cashflow <SYMBOL> [--period annual|quarterly] [--market us|jp] [--format ...]

# ニュース
stockpile news get <SYMBOL> [--limit N] [--market us|jp] [--format ...]

# マクロ経済指標
stockpile macro get <INDICATOR_ID> [--start DATE] [--end DATE] [--source fred|estat] [--format ...]
stockpile macro list [--source fred|estat] [--search QUERY]

# 設定
stockpile config init
stockpile config show
```

### 出力フォーマット

| フォーマット | 用途 |
|---|---|
| `table` (デフォルト) | ターミナルでの閲覧。Rich ライブラリによるカラー表示 |
| `json` | プログラムからの利用、パイプライン連携 |
| `csv` | スプレッドシートへのエクスポート |

---

## 7. Configuration

設定ファイル: `~/.config/stockpile/config.toml`

```toml
[storage]
backend = "sqlite"
path = "~/.local/share/stockpile/data"

[defaults]
market = "us"           # デフォルトの市場
output_format = "table" # デフォルトの出力形式

[api_keys]
jquants = ""   # J-Quants (JP 公式株価)
fmp = ""       # Financial Modeling Prep (US 財務)
finnhub = ""   # Finnhub (ニュース・株価)
gnews = ""     # GNews (ニュース)
fred = ""      # FRED (マクロ経済指標)
```

### API キーの取得先

| サービス | 取得URL | 無料枠 |
|---|---|---|
| FRED | https://fred.stlouisfed.org/docs/api/api_key.html | 120 req/min |
| J-Quants | https://jpx-jquants.com/ | 12 req/min |
| FMP | https://financialmodelingprep.com/ | 250 req/day |
| Finnhub | https://finnhub.io/ | 60 req/min |
| GNews | https://gnews.io/ | 100 req/day |

---

## 8. Technology Stack

| 項目 | 選定 | 理由 |
|---|---|---|
| 言語 | Python 3.13+ | データ分析ライブラリが豊富、yfinance 等の既存資産 |
| パッケージ管理 | uv | 高速、lockfile 対応 |
| CLI フレームワーク | Typer | 型ヒントベースで簡潔、自動ヘルプ生成 |
| ターミナル出力 | Rich | テーブル表示、カラー、スピナー |
| HTTP クライアント | requests | 同期 I/O で十分、シンプル |
| データモデル | dataclass | Pydantic 不使用で依存を最小化 |
| ストレージ | SQLite (stdlib) | 追加依存なし、単一ファイルで管理容易 |

---

## 9. Project Structure

```
stockpile/
├── docs/
│   └── design.md              # 本ドキュメント
├── src/stockpile/
│   ├── __init__.py
│   ├── config.py              # 設定読み込み・初期化
│   ├── models.py              # データモデル (dataclass)
│   ├── registry.py            # プロバイダー選択
│   ├── cli/
│   │   ├── app.py             # エントリポイント
│   │   ├── price.py           # 株価コマンド
│   │   ├── fundamentals.py    # 財務諸表コマンド
│   │   ├── news.py            # ニュースコマンド
│   │   ├── macro.py           # マクロ指標コマンド
│   │   ├── config_cmd.py      # 設定コマンド
│   │   └── formatters.py      # 出力整形
│   ├── providers/
│   │   ├── base.py            # Protocol 定義
│   │   ├── yfinance_provider.py  # yfinance (株価・財務・ニュース)
│   │   ├── fred_provider.py      # FRED (マクロ経済)
│   │   └── news_provider.py      # yfinance ニュース
│   └── storage/
│       ├── base.py            # Storage Protocol
│       └── sqlite.py          # SQLite 実装
├── tests/
├── pyproject.toml
├── config.example.toml
└── README.md
```

---

## 10. Future Roadmap

### Phase 6: 日本市場専用プロバイダー
- J-Quants プロバイダー (TSE 公式株価データ)
- EDINET プロバイダー (有報 XBRL パース)
- e-Stat プロバイダー (日本政府マクロ統計)

### Phase 7: 機能拡充
- `price compare` コマンド (複数銘柄比較)
- `fundamentals summary` コマンド (主要指標サマリー)
- SQLite キャッシュの CLI 組み込み (取得時に自動保存)
- レートリミット対応とリトライ
- ウォッチリスト機能

### Phase 8: 品質改善
- テストスイート整備 (responses によるモック HTTP テスト)
- CI/CD (GitHub Actions: lint + test)
- エラーメッセージの改善
