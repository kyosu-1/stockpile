from dataclasses import dataclass, asdict
from datetime import date, datetime


@dataclass
class OHLCV:
    symbol: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

    def to_dict(self) -> dict:
        d = asdict(self)
        d["date"] = self.date.isoformat()
        return d


@dataclass
class Quote:
    symbol: str
    price: float
    change: float
    change_pct: float
    timestamp: datetime

    def to_dict(self) -> dict:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


@dataclass
class IncomeStatement:
    symbol: str
    period_end: date
    period_type: str  # "annual" or "quarterly"
    revenue: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    ebitda: float | None = None
    eps: float | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["period_end"] = self.period_end.isoformat()
        return d


@dataclass
class BalanceSheet:
    symbol: str
    period_end: date
    period_type: str
    total_assets: float | None = None
    total_liabilities: float | None = None
    equity: float | None = None
    cash: float | None = None
    total_debt: float | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["period_end"] = self.period_end.isoformat()
        return d


@dataclass
class CashFlow:
    symbol: str
    period_end: date
    period_type: str
    operating_cf: float | None = None
    investing_cf: float | None = None
    financing_cf: float | None = None
    free_cash_flow: float | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["period_end"] = self.period_end.isoformat()
        return d


@dataclass
class Article:
    title: str
    url: str
    source: str
    published_at: datetime | None = None
    summary: str | None = None
    symbols: list[str] | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        if self.published_at:
            d["published_at"] = self.published_at.isoformat()
        return d


@dataclass
class MacroDataPoint:
    indicator_id: str
    date: date
    value: float
    unit: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["date"] = self.date.isoformat()
        return d
