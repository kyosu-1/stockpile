---
name: stock-analysis-report
description: Use when the user asks to analyze a specific stock (US or JP) and produce a written report — gathers price history, fundamentals, and news via the stockpile CLI, synthesizes them, and saves a markdown report under docs/reports/.
---

# Stock Analysis Report

## Overview

Generate a single-stock analysis report by combining quantitative data (price, financials) with qualitative signals (news), and persist the result to `docs/reports/`. The report must be reproducible: every figure cited must come from a `stockpile` command shown in the report.

**Core principle:** Data → Synthesis → Persisted artifact. Never write numbers from memory; always run the CLI.

## When to Use

- User asks "analyze {symbol}", "{銘柄} を分析して", "{銘柄} のレポート作って" etc.
- User wants a report on the disk (not just a chat summary).

When NOT to use:
- Multi-stock screening / comparison → use `metrics compare` directly.
- Quick price check → just call `stockpile price current`.

## Workflow

1. **Resolve target**
   - US ticker (letters): `--market us`
   - 4-digit JP code: `--market jp`
   - Confirm with user if ambiguous.

2. **Fetch data in parallel** (single message, multiple Bash calls):
   ```bash
   uv run stockpile price get {SYM} --start {1Y_AGO} --end {TODAY} --market {MKT}
   uv run stockpile price current {SYM} --market {MKT}
   uv run stockpile fundamentals income {SYM} --market {MKT}
   uv run stockpile fundamentals balance {SYM} --market {MKT}
   uv run stockpile fundamentals cashflow {SYM} --market {MKT}
   uv run stockpile news get {SYM} --limit 10 --market {MKT}
   uv run stockpile metrics get {SYM} --market {MKT}   # if available
   ```
   If a command errors, note it in the report rather than silently dropping the section.

3. **Synthesize** — extract:
   - 1Y price range, current price & %, notable spikes/drops with dates
   - Revenue / op-income / net-income / EBITDA / EPS for last 3-4 FYs (with YoY)
   - Total assets / liabilities / equity / cash / debt — flag big YoY changes
   - Operating CF / Investing CF / Financing CF / FCF — comment on cash generation
   - Top 5-7 news items — group by theme (業績 / 製品 / 市場 / アナリスト評価)

4. **Write the report** to:
   ```
   docs/reports/{YYYY}/{MM}/{market}_{symbol_lower}_analysis.md
   ```
   Use the structure in **Report Template** below. Create the year/month directory if missing.

5. **Report path back to the user** so they can open it.

## Report Template

```markdown
# {会社名} ({SYMBOL}) 分析レポート

- **日付:** {YYYY-MM-DD}
- **市場:** {US/JP}
- **手法:** [財務指標定義](../../../methodology/financial_metrics.md)

---

## データ取得

```bash
{実行した stockpile コマンドを全て列挙}
```

---

## 株価動向（直近1年）
- 現在価格 / 1年レンジ / 主要イベント日

## 業績推移（年次）
| FY | 売上 | YoY | 営業損益 | 純損益 | EBITDA | EPS |

## 財務状態
- B/S 主要項目と前年比の変化
- 有利子負債とレバレッジ評価

## キャッシュフロー
- 営業CF / 投資CF / 財務CF / FCF の推移と評価

## 主要ニュース（直近）
- 箇条書き、テーマ別グループ化

## 投資観点まとめ
- **強み:** ...
- **懸念:** ...
- **次のチェックポイント:** 決算日, 注目KPI, マクロ要因

> Disclaimer: 本レポートは公開データの整理であり、投資助言ではありません。
```

## Quick Reference

| 用途 | コマンド |
|---|---|
| US 株 1年価格 | `uv run stockpile price get AAPL --start 2025-04-19 --end 2026-04-19` |
| JP 株財務 | `uv run stockpile fundamentals income 7203 --market jp` |
| ニュース | `uv run stockpile news get NET --limit 10` |
| メトリクス | `uv run stockpile metrics get NET` |

日付は **必ず会話冒頭に提供される `Today's date`** を基準に算出する（推測しない）。

## Common Mistakes

- **数値を記憶から書く** → 必ず CLI 出力に基づく。出力が truncated でも実コマンド結果から判断。
- **ファイル名のばらつき** → 命名は `{market}_{symbol_lower}_analysis.md` で固定。
- **レポート保存を忘れて会話だけで終わらせる** → 最後に必ず Write で保存し、パスを返す。
- **ニュースを Yahoo Finance 以外と書く** → 出典は yfinance 経由の Yahoo Finance（個別記事の `source` 列はその配信元）。
- **断定的な「買い」「売り」表現** → シナリオ別に提示し、Disclaimer を入れる。
