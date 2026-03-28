from unittest.mock import patch

from stockpile.analysis import FinancialMetrics
from stockpile.cli.app import app
from stockpile.cli.metrics import _format_value


def _make_metrics(symbol="AAPL", **kwargs):
    defaults = dict(
        market="us",
        period_end="2024-09-30",
        period_type="annual",
        currency="USD",
        revenue=391e9,
        operating_income=118e9,
        net_income=93e9,
        operating_margin=30.3,
        net_margin=23.9,
        roe=164.6,
        roa=25.7,
        equity_ratio=15.6,
    )
    defaults.update(kwargs)
    return FinancialMetrics(symbol=symbol, **defaults)


class TestFormatValue:
    def test_none(self):
        assert _format_value("revenue", None) == "-"

    def test_trillion(self):
        assert "T" in _format_value("revenue", 1.5e12)

    def test_billion(self):
        assert "B" in _format_value("revenue", 1.5e9)

    def test_million(self):
        assert "M" in _format_value("revenue", 150e6)

    def test_percentage_margin(self):
        result = _format_value("operating_margin", 30.3)
        assert "30.3%" in result

    def test_percentage_growth(self):
        result = _format_value("revenue_growth", 10.5)
        assert "+10.5%" in result

    def test_de_ratio(self):
        assert _format_value("de_ratio", 1.5) == "1.50"

    def test_eps(self):
        assert _format_value("eps", 6.08) == "6.08"


class TestGetMetrics:
    @patch("stockpile.cli.metrics._fetch_metrics")
    def test_get_command_json(self, mock_fetch, cli_runner):
        mock_fetch.return_value = [_make_metrics()]
        result = cli_runner.invoke(app, ["metrics", "get", "AAPL", "--format", "json"])
        assert result.exit_code == 0

    @patch("stockpile.cli.metrics._fetch_metrics")
    def test_get_command_table(self, mock_fetch, cli_runner):
        mock_fetch.return_value = [_make_metrics()]
        result = cli_runner.invoke(app, ["metrics", "get", "AAPL"])
        assert result.exit_code == 0

    @patch("stockpile.cli.metrics._fetch_metrics")
    def test_get_no_data(self, mock_fetch, cli_runner):
        mock_fetch.return_value = []
        result = cli_runner.invoke(app, ["metrics", "get", "AAPL"])
        assert result.exit_code == 0
        assert "No data" in result.output


class TestCompare:
    @patch("stockpile.cli.metrics._fetch_metrics")
    def test_compare_command(self, mock_fetch, cli_runner):
        mock_fetch.side_effect = [
            [_make_metrics(symbol="AAPL")],
            [_make_metrics(symbol="MSFT")],
        ]
        result = cli_runner.invoke(app, ["metrics", "compare", "AAPL", "MSFT"])
        assert result.exit_code == 0

    @patch("stockpile.cli.metrics._fetch_metrics")
    def test_compare_no_data(self, mock_fetch, cli_runner):
        mock_fetch.return_value = []
        result = cli_runner.invoke(app, ["metrics", "compare", "AAPL", "MSFT"])
        assert result.exit_code == 0
