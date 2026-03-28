from datetime import date, datetime

from stockpile.models import (
    OHLCV,
    Article,
    BalanceSheet,
    CashFlow,
    IncomeStatement,
    MacroDataPoint,
    Quote,
)


class TestOHLCV:
    def test_to_dict(self):
        ohlcv = OHLCV(
            symbol="AAPL", date=date(2025, 1, 2), open=150.0, high=155.0, low=149.0, close=153.0, volume=1000000
        )
        d = ohlcv.to_dict()
        assert d["date"] == "2025-01-02"
        assert d["symbol"] == "AAPL"
        assert d["close"] == 153.0
        assert isinstance(d["date"], str)


class TestQuote:
    def test_to_dict(self):
        ts = datetime(2025, 3, 15, 10, 30, 0)
        quote = Quote(symbol="AAPL", price=150.0, change=2.0, change_pct=1.35, timestamp=ts)
        d = quote.to_dict()
        assert d["timestamp"] == "2025-03-15T10:30:00"
        assert d["price"] == 150.0


class TestIncomeStatement:
    def test_to_dict(self):
        stmt = IncomeStatement(symbol="AAPL", period_end=date(2024, 9, 30), period_type="annual", revenue=100000.0)
        d = stmt.to_dict()
        assert d["period_end"] == "2024-09-30"
        assert d["revenue"] == 100000.0
        assert d["net_income"] is None

    def test_optional_fields_default_none(self):
        stmt = IncomeStatement(symbol="AAPL", period_end=date(2024, 9, 30), period_type="annual")
        assert stmt.revenue is None
        assert stmt.operating_income is None
        assert stmt.net_income is None
        assert stmt.ebitda is None
        assert stmt.eps is None


class TestBalanceSheet:
    def test_to_dict(self):
        bs = BalanceSheet(
            symbol="AAPL", period_end=date(2024, 9, 30), period_type="annual", total_assets=300000.0, equity=50000.0
        )
        d = bs.to_dict()
        assert d["period_end"] == "2024-09-30"
        assert d["total_assets"] == 300000.0
        assert d["total_debt"] is None


class TestCashFlow:
    def test_to_dict(self):
        cf = CashFlow(symbol="AAPL", period_end=date(2024, 9, 30), period_type="annual", free_cash_flow=80000.0)
        d = cf.to_dict()
        assert d["period_end"] == "2024-09-30"
        assert d["free_cash_flow"] == 80000.0
        assert d["operating_cf"] is None


class TestArticle:
    def test_to_dict_with_published_at(self):
        article = Article(
            title="Test", url="https://example.com", source="Reuters", published_at=datetime(2025, 1, 15, 12, 0)
        )
        d = article.to_dict()
        assert d["published_at"] == "2025-01-15T12:00:00"

    def test_to_dict_without_published_at(self):
        article = Article(title="Test", url="https://example.com", source="Reuters", published_at=None)
        d = article.to_dict()
        assert d["published_at"] is None

    def test_optional_fields(self):
        article = Article(title="Test", url="https://example.com", source="Reuters")
        assert article.published_at is None
        assert article.summary is None
        assert article.symbols is None


class TestMacroDataPoint:
    def test_to_dict(self):
        point = MacroDataPoint(indicator_id="GDP", date=date(2024, 10, 1), value=29719.5, unit="Billions")
        d = point.to_dict()
        assert d["date"] == "2024-10-01"
        assert d["value"] == 29719.5

    def test_default_unit(self):
        point = MacroDataPoint(indicator_id="GDP", date=date(2024, 10, 1), value=100.0)
        assert point.unit == ""
