from unittest.mock import MagicMock, patch

from stockpile.providers.news_provider import YFinanceNewsProvider


class TestResolveSymbol:
    def test_us_passthrough(self):
        provider = YFinanceNewsProvider(market="us")
        assert provider._resolve_symbol("AAPL") == "AAPL"

    def test_jp_appends_suffix(self):
        provider = YFinanceNewsProvider(market="jp")
        assert provider._resolve_symbol("7203") == "7203.T"


class TestGetNews:
    @patch("stockpile.providers.news_provider.yf.Ticker")
    def test_returns_articles(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        mock_ticker.news = [
            {
                "content": {
                    "title": "Apple News",
                    "canonicalUrl": {"url": "https://example.com/1"},
                    "provider": {"displayName": "Reuters"},
                    "pubDate": "2025-01-15T12:00:00Z",
                    "summary": "Summary text",
                },
            }
        ]
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceNewsProvider(market="us")
        articles = provider.get_news("AAPL", limit=10)
        assert len(articles) == 1
        assert articles[0].title == "Apple News"
        assert articles[0].source == "Reuters"
        assert articles[0].published_at is not None
        assert articles[0].symbols == ["AAPL"]

    @patch("stockpile.providers.news_provider.yf.Ticker")
    def test_respects_limit(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        mock_ticker.news = [
            {
                "content": {
                    "title": f"Article {i}",
                    "canonicalUrl": {"url": f"https://example.com/{i}"},
                    "provider": {"displayName": "Test"},
                }
            }
            for i in range(5)
        ]
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceNewsProvider(market="us")
        articles = provider.get_news("AAPL", limit=2)
        assert len(articles) == 2

    @patch("stockpile.providers.news_provider.yf.Ticker")
    def test_empty_news(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        mock_ticker.news = []
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceNewsProvider(market="us")
        assert provider.get_news("AAPL") == []

    @patch("stockpile.providers.news_provider.yf.Ticker")
    def test_none_news(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        mock_ticker.news = None
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceNewsProvider(market="us")
        assert provider.get_news("AAPL") == []

    @patch("stockpile.providers.news_provider.yf.Ticker")
    def test_missing_pub_date(self, mock_ticker_cls):
        mock_ticker = MagicMock()
        mock_ticker.news = [
            {
                "content": {
                    "title": "No date",
                    "canonicalUrl": {"url": "https://example.com/1"},
                    "provider": {"displayName": "Test"},
                }
            }
        ]
        mock_ticker_cls.return_value = mock_ticker

        provider = YFinanceNewsProvider(market="us")
        articles = provider.get_news("AAPL")
        assert articles[0].published_at is None
