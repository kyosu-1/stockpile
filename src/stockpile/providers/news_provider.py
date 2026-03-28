from datetime import datetime

import yfinance as yf

from stockpile.models import Article


class YFinanceNewsProvider:
    """News provider using yfinance (no API key required)."""

    def __init__(self, market: str = "us") -> None:
        self._market = market

    def _resolve_symbol(self, symbol: str) -> str:
        if self._market == "jp" and not symbol.endswith(".T"):
            return f"{symbol}.T"
        return symbol

    def get_news(self, symbol: str, limit: int = 10) -> list[Article]:
        ticker = yf.Ticker(self._resolve_symbol(symbol))
        news_items = ticker.news
        if not news_items:
            return []

        articles = []
        for item in news_items[:limit]:
            content = item.get("content", {})
            published = content.get("pubDate")
            published_at = None
            if published:
                try:
                    published_at = datetime.fromisoformat(published.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    pass

            articles.append(
                Article(
                    title=content.get("title", item.get("title", "No title")),
                    url=content.get("canonicalUrl", {}).get("url", item.get("link", "")),
                    source=content.get("provider", {}).get("displayName", "Yahoo Finance"),
                    published_at=published_at,
                    summary=content.get("summary"),
                    symbols=[symbol],
                )
            )
        return articles
