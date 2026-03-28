from datetime import date
from unittest.mock import MagicMock, patch

from stockpile.cli.app import app
from stockpile.models import MacroDataPoint


class TestMacroGet:
    @patch("stockpile.cli.macro._get_fred_provider")
    def test_get_command(self, mock_get_provider, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_indicator.return_value = [
            MacroDataPoint(indicator_id="GDP", date=date(2024, 7, 1), value=29349.0),
        ]
        mock_get_provider.return_value = mock_provider

        result = cli_runner.invoke(app, ["macro", "get", "GDP", "--format", "json"])
        assert result.exit_code == 0
        mock_provider.get_indicator.assert_called_once()

    def test_unsupported_source(self, cli_runner):
        result = cli_runner.invoke(app, ["macro", "get", "GDP", "--source", "estat"])
        assert result.exit_code == 0
        assert "not yet implemented" in result.output


class TestMacroList:
    def test_list_popular(self, cli_runner):
        result = cli_runner.invoke(app, ["macro", "list"])
        assert result.exit_code == 0
        assert "GDP" in result.output

    @patch("stockpile.cli.macro._get_fred_provider")
    def test_list_with_search(self, mock_get_provider, cli_runner):
        mock_provider = MagicMock()
        mock_provider.search_indicators.return_value = [
            {"id": "GDP", "title": "Gross Domestic Product", "frequency": "Q", "units": "Bil."},
        ]
        mock_get_provider.return_value = mock_provider

        result = cli_runner.invoke(app, ["macro", "list", "--search", "gdp"])
        assert result.exit_code == 0
        assert "GDP" in result.output
