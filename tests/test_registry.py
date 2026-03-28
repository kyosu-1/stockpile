import pytest

from stockpile.config import Config
from stockpile.registry import ProviderRegistry
from stockpile.providers.yfinance_provider import YFinanceProvider


class TestProviderRegistry:
    def test_get_price_provider(self):
        registry = ProviderRegistry(Config())
        provider = registry.get_price_provider("us")
        assert isinstance(provider, YFinanceProvider)

    def test_get_fundamentals_provider(self):
        registry = ProviderRegistry(Config())
        provider = registry.get_fundamentals_provider("jp")
        assert isinstance(provider, YFinanceProvider)

    def test_get_news_provider_raises(self):
        registry = ProviderRegistry(Config())
        with pytest.raises(NotImplementedError):
            registry.get_news_provider()

    def test_get_macro_provider_raises(self):
        registry = ProviderRegistry(Config())
        with pytest.raises(NotImplementedError):
            registry.get_macro_provider()
