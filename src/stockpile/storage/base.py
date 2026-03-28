from datetime import date
from typing import Protocol

from stockpile.models import OHLCV, Article, MacroDataPoint


class StorageBackend(Protocol):
    def save_prices(self, prices: list[OHLCV], source: str) -> None: ...

    def get_prices(self, symbol: str, start: date, end: date, source: str | None = None) -> list[OHLCV]: ...

    def save_financials(self, symbol: str, statement: str, period_type: str, data: dict, source: str) -> None: ...

    def get_financials(
        self, symbol: str, statement: str, period_type: str, source: str | None = None
    ) -> dict | None: ...

    def save_articles(self, articles: list[Article]) -> None: ...

    def save_macro(self, data: list[MacroDataPoint], source: str) -> None: ...

    def get_macro(
        self, indicator_id: str, start: date | None, end: date | None, source: str | None = None
    ) -> list[MacroDataPoint]: ...
