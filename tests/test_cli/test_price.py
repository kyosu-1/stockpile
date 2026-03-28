from datetime import date, datetime
from unittest.mock import MagicMock, patch

from stockpile.cli.app import app
from stockpile.models import OHLCV, Quote


class TestPriceGet:
    @patch("stockpile.cli.price.YFinanceProvider")
    def test_get_command(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_historical_prices.return_value = [
            OHLCV(symbol="AAPL", date=date(2025, 1, 2), open=150, high=155, low=149, close=153, volume=100),
        ]
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["price", "get", "AAPL", "--format", "json"])
        assert result.exit_code == 0
        mock_provider.get_historical_prices.assert_called_once()

    @patch("stockpile.cli.price.YFinanceProvider")
    def test_get_with_dates(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_historical_prices.return_value = []
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["price", "get", "AAPL", "--start", "2025-01-01", "--end", "2025-01-31"])
        assert result.exit_code == 0
        mock_provider.get_historical_prices.assert_called_once_with("AAPL", date(2025, 1, 1), date(2025, 1, 31))

    @patch("stockpile.cli.price.YFinanceProvider")
    def test_get_jp_market(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_historical_prices.return_value = []
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["price", "get", "7203", "--market", "jp"])
        assert result.exit_code == 0
        mock_provider_cls.assert_called_once_with(market="jp")


class TestPriceCurrent:
    @patch("stockpile.cli.price.YFinanceProvider")
    def test_current_command(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_current_price.return_value = Quote(
            symbol="AAPL",
            price=150.0,
            change=2.0,
            change_pct=1.35,
            timestamp=datetime.now(),
        )
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["price", "current", "AAPL"])
        assert result.exit_code == 0
        assert "AAPL" in result.output
        assert "150.00" in result.output
