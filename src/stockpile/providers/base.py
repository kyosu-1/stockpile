from datetime import date
from typing import Protocol

from stockpile.models import (
    Article,
    BalanceSheet,
    CashFlow,
    IncomeStatement,
    MacroDataPoint,
    OHLCV,
    Quote,
)


class PriceProvider(Protocol):
    def get_current_price(self, symbol: str) -> Quote: ...

    def get_historical_prices(self, symbol: str, start: date, end: date) -> list[OHLCV]: ...


class FundamentalsProvider(Protocol):
    def get_income_statement(self, symbol: str, period: str = "annual") -> list[IncomeStatement]: ...

    def get_balance_sheet(self, symbol: str, period: str = "annual") -> list[BalanceSheet]: ...

    def get_cash_flow(self, symbol: str, period: str = "annual") -> list[CashFlow]: ...


class NewsProvider(Protocol):
    def get_news(self, symbol: str, limit: int = 10) -> list[Article]: ...


class MacroProvider(Protocol):
    def get_indicator(
        self,
        indicator_id: str,
        start: date | None = None,
        end: date | None = None,
    ) -> list[MacroDataPoint]: ...
