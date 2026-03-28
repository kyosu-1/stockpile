from datetime import date

from stockpile.models import OHLCV, Article


class TestSQLiteStoragePrices:
    def test_save_and_get_roundtrip(self, storage, sample_ohlcv_list):
        storage.save_prices(sample_ohlcv_list, source="yfinance")
        result = storage.get_prices("AAPL", date(2025, 1, 1), date(2025, 1, 31))
        assert len(result) == 2
        assert result[0].symbol == "AAPL"
        assert result[0].date == date(2025, 1, 2)
        assert result[0].close == 153.0
        assert result[1].date == date(2025, 1, 3)

    def test_get_prices_date_range(self, storage, sample_ohlcv_list):
        storage.save_prices(sample_ohlcv_list, source="yfinance")
        result = storage.get_prices("AAPL", date(2025, 1, 3), date(2025, 1, 3))
        assert len(result) == 1
        assert result[0].date == date(2025, 1, 3)

    def test_get_prices_with_source_filter(self, storage):
        prices_a = [OHLCV(symbol="AAPL", date=date(2025, 1, 2), open=150, high=155, low=149, close=153, volume=100)]
        prices_b = [OHLCV(symbol="AAPL", date=date(2025, 1, 2), open=151, high=156, low=150, close=154, volume=200)]
        storage.save_prices(prices_a, source="yfinance")
        storage.save_prices(prices_b, source="fmp")
        result = storage.get_prices("AAPL", date(2025, 1, 1), date(2025, 1, 31), source="fmp")
        assert len(result) == 1
        assert result[0].close == 154

    def test_upsert_replaces(self, storage):
        p1 = [OHLCV(symbol="AAPL", date=date(2025, 1, 2), open=150, high=155, low=149, close=153, volume=100)]
        p2 = [OHLCV(symbol="AAPL", date=date(2025, 1, 2), open=150, high=155, low=149, close=160, volume=100)]
        storage.save_prices(p1, source="yfinance")
        storage.save_prices(p2, source="yfinance")
        result = storage.get_prices("AAPL", date(2025, 1, 1), date(2025, 1, 31))
        assert len(result) == 1
        assert result[0].close == 160

    def test_empty_result(self, storage):
        result = storage.get_prices("AAPL", date(2025, 1, 1), date(2025, 1, 31))
        assert result == []


class TestSQLiteStorageFinancials:
    def test_save_and_get_roundtrip(self, storage):
        data = {
            "2024-09-30": {"revenue": 391035000000, "net_income": 93736000000},
            "2023-09-30": {"revenue": 383285000000, "net_income": 96995000000},
        }
        storage.save_financials("AAPL", "income", "annual", data, "yfinance")
        result = storage.get_financials("AAPL", "income", "annual")
        assert result is not None
        assert "2024-09-30" in result
        assert result["2024-09-30"]["revenue"] == 391035000000

    def test_get_returns_none_when_empty(self, storage):
        result = storage.get_financials("AAPL", "income", "annual")
        assert result is None

    def test_source_filter(self, storage):
        data = {"2024-09-30": {"revenue": 100}}
        storage.save_financials("AAPL", "income", "annual", data, "yfinance")
        storage.save_financials("AAPL", "income", "annual", {"2024-09-30": {"revenue": 200}}, "fmp")
        result = storage.get_financials("AAPL", "income", "annual", source="fmp")
        assert result["2024-09-30"]["revenue"] == 200


class TestSQLiteStorageArticles:
    def test_save_and_dedup(self, storage, sample_articles):
        storage.save_articles(sample_articles)
        # Insert same articles again - should be ignored (URL unique constraint)
        storage.save_articles(sample_articles)
        rows = storage._conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        assert rows == 2

    def test_save_with_none_fields(self, storage):
        articles = [
            Article(
                title="Test", url="https://example.com/1", source="Test", published_at=None, summary=None, symbols=None
            )
        ]
        storage.save_articles(articles)
        rows = storage._conn.execute("SELECT * FROM articles").fetchall()
        assert len(rows) == 1
        assert rows[0]["published_at"] is None


class TestSQLiteStorageMacro:
    def test_save_and_get_roundtrip(self, storage, sample_macro_data):
        storage.save_macro(sample_macro_data, source="fred")
        result = storage.get_macro("GDP", start=None, end=None)
        assert len(result) == 2
        assert result[0].indicator_id == "GDP"
        assert result[0].value == 29349.0

    def test_date_range_filter(self, storage, sample_macro_data):
        storage.save_macro(sample_macro_data, source="fred")
        result = storage.get_macro("GDP", start=date(2024, 10, 1), end=None)
        assert len(result) == 1
        assert result[0].date == date(2024, 10, 1)

    def test_source_filter(self, storage, sample_macro_data):
        storage.save_macro(sample_macro_data, source="fred")
        result = storage.get_macro("GDP", start=None, end=None, source="estat")
        assert result == []

    def test_empty_result(self, storage):
        result = storage.get_macro("NONEXISTENT", start=None, end=None)
        assert result == []


class TestSQLiteStorageClose:
    def test_close(self, storage):
        storage.close()
        # Should not raise
