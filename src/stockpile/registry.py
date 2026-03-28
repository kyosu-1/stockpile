from stockpile.config import Config


class ProviderRegistry:
    """Maps (market, data_type) to concrete provider instances."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._providers: dict[tuple[str, str], object] = {}

    def get_price_provider(self, market: str = "us"):
        from stockpile.providers.yfinance_provider import YFinanceProvider

        return YFinanceProvider(market=market)

    def get_fundamentals_provider(self, market: str = "us"):
        from stockpile.providers.yfinance_provider import YFinanceProvider

        return YFinanceProvider(market=market)

    def get_news_provider(self, market: str = "us"):
        raise NotImplementedError("News provider not yet implemented")

    def get_macro_provider(self, source: str = "fred"):
        raise NotImplementedError("Macro provider not yet implemented")
