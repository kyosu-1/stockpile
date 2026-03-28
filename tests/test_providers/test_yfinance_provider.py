from datetime import date
from unittest.mock import MagicMock, patch

import pandas as pd

from stockpile.providers.yfinance_provider import YFinanceProvider, _safe_float


class TestResolveSymbol:
    def test_us_market_passthrough(self):
        provider = YFinanceProvider(market="us")
        assert provider._resolve_symbol("AAPL") == "AAPL"

    def test_jp_market_appends_suffix(self):
        provider = YFinanceProvider(market="jp")
        assert provider._resolve_symbol("7203") == "7203.T"

    def test_jp_market_no_double_suffix(self):
        provider = YFinanceProvider(market="jp")
        assert provider._resolve_symbol("7203.T") == "7203.T"


class TestGetCurrentPrice:
    @patch("stockpile.providers.yfinance_provider.yf.Ticker")
    def test_returns_quote(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        mock_ticker.fast_info.last_price = 150.0
        mock_ticker.fast_info.previous_close = 148.0
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceProvider(market="us")
        quote = provider.get_current_price("AAPL")

        assert quote.symbol == "AAPL"
        assert quote.price == 150.0
        assert quote.change == 2.0
        mock_ticker_cls.assert_called_once_with("AAPL")


class TestGetHistoricalPrices:
    @patch("stockpile.providers.yfinance_provider.yf.Ticker")
    def test_returns_ohlcv_list(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        df = pd.DataFrame(
            {"Open": [150.0], "High": [155.0], "Low": [149.0], "Close": [153.0], "Volume": [1000000]},
            index=pd.DatetimeIndex([pd.Timestamp("2025-01-02")]),
        )
        mock_ticker.history.return_value = df
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceProvider(market="us")
        result = provider.get_historical_prices("AAPL", date(2025, 1, 1), date(2025, 1, 31))

        assert len(result) == 1
        assert result[0].symbol == "AAPL"
        assert result[0].date == date(2025, 1, 2)
        assert result[0].close == 153.0

    @patch("stockpile.providers.yfinance_provider.yf.Ticker")
    def test_empty_dataframe(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = pd.DataFrame()
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceProvider(market="us")
        result = provider.get_historical_prices("AAPL", date(2025, 1, 1), date(2025, 1, 31))
        assert result == []


class TestGetIncomeStatement:
    @patch("stockpile.providers.yfinance_provider.yf.Ticker")
    def test_annual(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        df = pd.DataFrame(
            {
                "Total Revenue": [391035e6],
                "Operating Income": [118658e6],
                "Net Income": [93736e6],
                "EBITDA": [131781e6],
                "Basic EPS": [6.08],
            },
            index=[pd.Timestamp("2024-09-30")],
        ).T
        mock_ticker.income_stmt = df
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceProvider(market="us")
        result = provider.get_income_statement("AAPL", "annual")
        assert len(result) == 1
        assert result[0].revenue == round(391035e6, 2)
        assert result[0].period_type == "annual"

    @patch("stockpile.providers.yfinance_provider.yf.Ticker")
    def test_quarterly(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        df = pd.DataFrame(
            {"Total Revenue": [100e6]},
            index=[pd.Timestamp("2024-06-30")],
        ).T
        mock_ticker.quarterly_income_stmt = df
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceProvider(market="us")
        result = provider.get_income_statement("AAPL", "quarterly")
        assert len(result) == 1
        assert result[0].period_type == "quarterly"

    @patch("stockpile.providers.yfinance_provider.yf.Ticker")
    def test_empty(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        mock_ticker.income_stmt = pd.DataFrame()
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceProvider(market="us")
        assert provider.get_income_statement("AAPL") == []

    @patch("stockpile.providers.yfinance_provider.yf.Ticker")
    def test_none_dataframe(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        mock_ticker.income_stmt = None
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceProvider(market="us")
        assert provider.get_income_statement("AAPL") == []


class TestGetBalanceSheet:
    @patch("stockpile.providers.yfinance_provider.yf.Ticker")
    def test_returns_data(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        df = pd.DataFrame(
            {"Total Assets": [300e9], "Stockholders Equity": [50e9]},
            index=[pd.Timestamp("2024-09-30")],
        ).T
        mock_ticker.balance_sheet = df
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceProvider(market="us")
        result = provider.get_balance_sheet("AAPL")
        assert len(result) == 1
        assert result[0].total_assets == round(300e9, 2)


class TestGetCashFlow:
    @patch("stockpile.providers.yfinance_provider.yf.Ticker")
    def test_returns_data(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        df = pd.DataFrame(
            {"Operating Cash Flow": [118e9], "Free Cash Flow": [108e9]},
            index=[pd.Timestamp("2024-09-30")],
        ).T
        mock_ticker.cashflow = df
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceProvider(market="us")
        result = provider.get_cash_flow("AAPL")
        assert len(result) == 1
        assert result[0].free_cash_flow == round(108e9, 2)


class TestSafeFloat:
    def test_normal_value(self):
        df = pd.DataFrame({"col": [42.5]}, index=["row"])
        assert _safe_float(df, "row", "col") == 42.5

    def test_missing_row(self):
        df = pd.DataFrame({"col": [42.5]}, index=["row"])
        assert _safe_float(df, "nonexistent", "col") is None

    def test_nan_value(self):
        df = pd.DataFrame({"col": [float("nan")]}, index=["row"])
        assert _safe_float(df, "row", "col") is None
