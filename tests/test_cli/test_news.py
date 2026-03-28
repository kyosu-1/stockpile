from unittest.mock import MagicMock, patch

from stockpile.cli.app import app
from stockpile.models import Article


class TestNewsGet:
    @patch("stockpile.cli.news.YFinanceNewsProvider")
    def test_get_command(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_news.return_value = [
            Article(title="Test", url="https://example.com", source="Reuters"),
        ]
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["news", "get", "AAPL", "--format", "json"])
        assert result.exit_code == 0
        mock_provider.get_news.assert_called_once_with("AAPL", 10)

    @patch("stockpile.cli.news.YFinanceNewsProvider")
    def test_get_with_limit(self, mock_provider_cls, cli_runner):
        mock_provider = MagicMock()
        mock_provider.get_news.return_value = []
        mock_provider_cls.return_value = mock_provider

        result = cli_runner.invoke(app, ["news", "get", "AAPL", "--limit", "5"])
        assert result.exit_code == 0
        mock_provider.get_news.assert_called_once_with("AAPL", 5)
