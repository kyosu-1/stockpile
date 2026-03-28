from datetime import date, datetime

import yfinance as yf

from stockpile.models import (
    BalanceSheet,
    CashFlow,
    IncomeStatement,
    OHLCV,
    Quote,
)


class YFinanceProvider:
    def __init__(self, market: str = "us") -> None:
        self._market = market

    def _resolve_symbol(self, symbol: str) -> str:
        if self._market == "jp" and not symbol.endswith(".T"):
            return f"{symbol}.T"
        return symbol

    def get_current_price(self, symbol: str) -> Quote:
        ticker = yf.Ticker(self._resolve_symbol(symbol))
        info = ticker.fast_info
        price = info.last_price
        prev_close = info.previous_close
        change = price - prev_close
        change_pct = (change / prev_close) * 100 if prev_close else 0.0
        return Quote(
            symbol=symbol,
            price=round(price, 4),
            change=round(change, 4),
            change_pct=round(change_pct, 2),
            timestamp=datetime.now(),
        )

    def get_historical_prices(self, symbol: str, start: date, end: date) -> list[OHLCV]:
        ticker = yf.Ticker(self._resolve_symbol(symbol))
        df = ticker.history(start=start.isoformat(), end=end.isoformat())
        if df.empty:
            return []

        results = []
        for idx, row in df.iterrows():
            results.append(
                OHLCV(
                    symbol=symbol,
                    date=idx.date(),
                    open=round(row["Open"], 4),
                    high=round(row["High"], 4),
                    low=round(row["Low"], 4),
                    close=round(row["Close"], 4),
                    volume=int(row["Volume"]),
                )
            )
        return results

    def get_income_statement(self, symbol: str, period: str = "annual") -> list[IncomeStatement]:
        ticker = yf.Ticker(self._resolve_symbol(symbol))
        df = ticker.income_stmt if period == "annual" else ticker.quarterly_income_stmt
        if df is None or df.empty:
            return []

        results = []
        for col in df.columns:
            results.append(
                IncomeStatement(
                    symbol=symbol,
                    period_end=col.date(),
                    period_type=period,
                    revenue=_safe_float(df, "Total Revenue", col),
                    operating_income=_safe_float(df, "Operating Income", col),
                    net_income=_safe_float(df, "Net Income", col),
                    ebitda=_safe_float(df, "EBITDA", col),
                    eps=_safe_float(df, "Basic EPS", col),
                )
            )
        return results

    def get_balance_sheet(self, symbol: str, period: str = "annual") -> list[BalanceSheet]:
        ticker = yf.Ticker(self._resolve_symbol(symbol))
        df = ticker.balance_sheet if period == "annual" else ticker.quarterly_balance_sheet
        if df is None or df.empty:
            return []

        results = []
        for col in df.columns:
            results.append(
                BalanceSheet(
                    symbol=symbol,
                    period_end=col.date(),
                    period_type=period,
                    total_assets=_safe_float(df, "Total Assets", col),
                    total_liabilities=_safe_float(df, "Total Liabilities Net Minority Interest", col),
                    equity=_safe_float(df, "Stockholders Equity", col),
                    cash=_safe_float(df, "Cash And Cash Equivalents", col),
                    total_debt=_safe_float(df, "Total Debt", col),
                )
            )
        return results

    def get_cash_flow(self, symbol: str, period: str = "annual") -> list[CashFlow]:
        ticker = yf.Ticker(self._resolve_symbol(symbol))
        df = ticker.cashflow if period == "annual" else ticker.quarterly_cashflow
        if df is None or df.empty:
            return []

        results = []
        for col in df.columns:
            results.append(
                CashFlow(
                    symbol=symbol,
                    period_end=col.date(),
                    period_type=period,
                    operating_cf=_safe_float(df, "Operating Cash Flow", col),
                    investing_cf=_safe_float(df, "Investing Cash Flow", col),
                    financing_cf=_safe_float(df, "Financing Cash Flow", col),
                    free_cash_flow=_safe_float(df, "Free Cash Flow", col),
                )
            )
        return results


def _safe_float(df, row_label: str, col) -> float | None:
    try:
        val = df.loc[row_label, col]
        if val is None or (hasattr(val, "__float__") and str(val) == "nan"):
            return None
        return round(float(val), 2)
    except (KeyError, ValueError, TypeError):
        return None
