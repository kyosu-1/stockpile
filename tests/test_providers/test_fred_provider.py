from datetime import date

import pytest
import responses

from stockpile.providers.fred_provider import FRED_BASE_URL, FREDProvider


class TestFREDProviderInit:
    def test_raises_on_empty_key(self):
        with pytest.raises(ValueError, match="FRED API key is required"):
            FREDProvider(api_key="")

    def test_valid_key(self):
        provider = FREDProvider(api_key="test-key")
        assert provider._api_key == "test-key"


class TestGetIndicator:
    @responses.activate
    def test_returns_data(self):
        responses.add(
            responses.GET,
            f"{FRED_BASE_URL}/series/observations",
            json={
                "observations": [
                    {"date": "2024-07-01", "value": "29349.0"},
                    {"date": "2024-10-01", "value": "29719.5"},
                ]
            },
        )
        provider = FREDProvider(api_key="test-key")
        result = provider.get_indicator("GDP")
        assert len(result) == 2
        assert result[0].indicator_id == "GDP"
        assert result[0].date == date(2024, 7, 1)
        assert result[0].value == 29349.0

    @responses.activate
    def test_alias_resolution(self):
        responses.add(
            responses.GET,
            f"{FRED_BASE_URL}/series/observations",
            json={"observations": [{"date": "2024-01-01", "value": "3.5"}]},
        )
        provider = FREDProvider(api_key="test-key")
        result = provider.get_indicator("CPI")
        # CPI should resolve to CPIAUCSL
        assert result[0].indicator_id == "CPIAUCSL"

    @responses.activate
    def test_skips_dot_values(self):
        responses.add(
            responses.GET,
            f"{FRED_BASE_URL}/series/observations",
            json={
                "observations": [
                    {"date": "2024-01-01", "value": "."},
                    {"date": "2024-02-01", "value": "100.5"},
                ]
            },
        )
        provider = FREDProvider(api_key="test-key")
        result = provider.get_indicator("FEDFUNDS")
        assert len(result) == 1
        assert result[0].value == 100.5

    @responses.activate
    def test_with_date_params(self):
        responses.add(
            responses.GET,
            f"{FRED_BASE_URL}/series/observations",
            json={"observations": []},
        )
        provider = FREDProvider(api_key="test-key")
        provider.get_indicator("GDP", start=date(2024, 1, 1), end=date(2024, 12, 31))
        assert "observation_start=2024-01-01" in responses.calls[0].request.url
        assert "observation_end=2024-12-31" in responses.calls[0].request.url

    @responses.activate
    def test_http_error(self):
        responses.add(
            responses.GET,
            f"{FRED_BASE_URL}/series/observations",
            status=500,
        )
        provider = FREDProvider(api_key="test-key")
        with pytest.raises(Exception):
            provider.get_indicator("GDP")


class TestSearchIndicators:
    @responses.activate
    def test_returns_results(self):
        responses.add(
            responses.GET,
            f"{FRED_BASE_URL}/series/search",
            json={
                "seriess": [
                    {
                        "id": "GDP",
                        "title": "Gross Domestic Product",
                        "frequency_short": "Q",
                        "units_short": "Bil. of $",
                        "seasonal_adjustment_short": "SAAR",
                    }
                ]
            },
        )
        provider = FREDProvider(api_key="test-key")
        result = provider.search_indicators("gdp")
        assert len(result) == 1
        assert result[0]["id"] == "GDP"
        assert result[0]["title"] == "Gross Domestic Product"
        assert result[0]["frequency"] == "Q"

    @responses.activate
    def test_empty_results(self):
        responses.add(
            responses.GET,
            f"{FRED_BASE_URL}/series/search",
            json={"seriess": []},
        )
        provider = FREDProvider(api_key="test-key")
        result = provider.search_indicators("nonexistent")
        assert result == []
