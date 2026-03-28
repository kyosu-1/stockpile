from datetime import date

import requests

from stockpile.models import MacroDataPoint

FRED_BASE_URL = "https://api.stlouisfed.org/fred"


class FREDProvider:
    """FRED (Federal Reserve Economic Data) provider. Requires a free API key."""

    # Common indicators for quick reference
    POPULAR_INDICATORS = {
        "GDP": "GDP",
        "CPI": "CPIAUCSL",
        "UNRATE": "UNRATE",
        "FEDFUNDS": "FEDFUNDS",
        "T10Y2Y": "T10Y2Y",
        "DGS10": "DGS10",
        "JPNCPIALLMINMEI": "JPNCPIALLMINMEI",  # Japan CPI
        "JPNGDP": "JPNRGDPEXP",  # Japan Real GDP
    }

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError(
                "FRED API key is required. Get one free at https://fred.stlouisfed.org/docs/api/api_key.html\n"
                "Then set it in your config: stockpile config set api_keys.fred YOUR_KEY"
            )
        self._api_key = api_key

    def get_indicator(
        self,
        indicator_id: str,
        start: date | None = None,
        end: date | None = None,
    ) -> list[MacroDataPoint]:
        # Resolve common aliases
        series_id = self.POPULAR_INDICATORS.get(indicator_id.upper(), indicator_id)

        params: dict = {
            "series_id": series_id,
            "api_key": self._api_key,
            "file_type": "json",
        }
        if start:
            params["observation_start"] = start.isoformat()
        if end:
            params["observation_end"] = end.isoformat()

        resp = requests.get(f"{FRED_BASE_URL}/series/observations", params=params)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for obs in data.get("observations", []):
            value_str = obs.get("value", ".")
            if value_str == ".":
                continue
            results.append(
                MacroDataPoint(
                    indicator_id=series_id,
                    date=date.fromisoformat(obs["date"]),
                    value=float(value_str),
                    unit="",
                )
            )
        return results

    def search_indicators(self, query: str, limit: int = 20) -> list[dict]:
        params = {
            "search_text": query,
            "api_key": self._api_key,
            "file_type": "json",
            "limit": limit,
        }
        resp = requests.get(f"{FRED_BASE_URL}/series/search", params=params)
        resp.raise_for_status()
        data = resp.json()

        return [
            {
                "id": s["id"],
                "title": s["title"],
                "frequency": s.get("frequency_short", ""),
                "units": s.get("units_short", ""),
                "seasonal_adjustment": s.get("seasonal_adjustment_short", ""),
            }
            for s in data.get("seriess", [])
        ]
