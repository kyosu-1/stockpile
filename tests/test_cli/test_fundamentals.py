from datetime import date
from unittest.mock import MagicMock, patch

from stockpile.cli.app import app
from stockpile.models import IncomeStatement


class TestFundamentals:
    @patch("stockpile.cli.fundamentals.YFinanceProvider")
    def test_income_command(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_income_statement.return_value = [
            IncomeStatement(symbol="AAPL", period_end=date(2024, 9, 30), period_type="annual", revenue=391e9),
        ]
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["fundamentals", "income", "AAPL", "--format", "json"])
        assert result.exit_code == 0
        mock_provider.get_income_statement.assert_called_once_with("AAPL", "annual")

    @patch("stockpile.cli.fundamentals.YFinanceProvider")
    def test_balance_command(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_balance_sheet.return_value = []
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["fundamentals", "balance", "AAPL"])
        assert result.exit_code == 0

    @patch("stockpile.cli.fundamentals.YFinanceProvider")
    def test_cashflow_command(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_cash_flow.return_value = []
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["fundamentals", "cashflow", "AAPL"])
        assert result.exit_code == 0

    @patch("stockpile.cli.fundamentals.YFinanceProvider")
    def test_quarterly_period(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_income_statement.return_value = []
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["fundamentals", "income", "AAPL", "--period", "quarterly"])
        assert result.exit_code == 0
        mock_provider.get_income_statement.assert_called_once_with("AAPL", "quarterly")
