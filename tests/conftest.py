from datetime import date, datetime

import pytest

from stockpile.models import (
    OHLCV,
    Article,
    BalanceSheet,
    CashFlow,
    IncomeStatement,
    MacroDataPoint,
)
from stockpile.config import Config, ApiKeys


@pytest.fixture
def sample_ohlcv_list():
    return [
        OHLCV(symbol="AAPL", date=date(2025, 1, 2), open=150.0, high=155.0, low=149.0, close=153.0, volume=1000000),
        OHLCV(symbol="AAPL", date=date(2025, 1, 3), open=153.0, high=157.0, low=152.0, close=156.0, volume=1200000),
    ]


@pytest.fixture
def sample_income_statements():
    return [
        IncomeStatement(
            symbol="AAPL",
            period_end=date(2024, 9, 30),
            period_type="annual",
            revenue=391035000000,
            operating_income=118658000000,
            net_income=93736000000,
            ebitda=131781000000,
            eps=6.08,
        ),
        IncomeStatement(
            symbol="AAPL",
            period_end=date(2023, 9, 30),
            period_type="annual",
            revenue=383285000000,
            operating_income=114301000000,
            net_income=96995000000,
            ebitda=125820000000,
            eps=6.13,
        ),
    ]


@pytest.fixture
def sample_balance_sheets():
    return [
        BalanceSheet(
            symbol="AAPL",
            period_end=date(2024, 9, 30),
            period_type="annual",
            total_assets=364980000000,
            total_liabilities=308030000000,
            equity=56950000000,
            cash=29943000000,
            total_debt=96834000000,
        ),
        BalanceSheet(
            symbol="AAPL",
            period_end=date(2023, 9, 30),
            period_type="annual",
            total_assets=352583000000,
            total_liabilities=290437000000,
            equity=62146000000,
            cash=29965000000,
            total_debt=111088000000,
        ),
    ]


@pytest.fixture
def sample_cash_flows():
    return [
        CashFlow(
            symbol="AAPL",
            period_end=date(2024, 9, 30),
            period_type="annual",
            operating_cf=118254000000,
            investing_cf=-2935000000,
            financing_cf=-121983000000,
            free_cash_flow=108807000000,
        ),
        CashFlow(
            symbol="AAPL",
            period_end=date(2023, 9, 30),
            period_type="annual",
            operating_cf=110543000000,
            investing_cf=-7077000000,
            financing_cf=-108488000000,
            free_cash_flow=99584000000,
        ),
    ]


@pytest.fixture
def sample_articles():
    return [
        Article(
            title="Apple Reports Q4 Results",
            url="https://example.com/article1",
            source="Reuters",
            published_at=datetime(2025, 1, 30, 14, 0, 0),
            summary="Apple beat expectations",
            symbols=["AAPL"],
        ),
        Article(
            title="Tech Stocks Rise",
            url="https://example.com/article2",
            source="Bloomberg",
            published_at=None,
            summary=None,
            symbols=None,
        ),
    ]


@pytest.fixture
def sample_macro_data():
    return [
        MacroDataPoint(indicator_id="GDP", date=date(2024, 7, 1), value=29349.0, unit="Billions of Dollars"),
        MacroDataPoint(indicator_id="GDP", date=date(2024, 10, 1), value=29719.5, unit="Billions of Dollars"),
    ]


@pytest.fixture
def mock_config():
    return Config(
        storage_backend="sqlite",
        storage_path="/tmp/stockpile-test",
        default_market="us",
        default_output_format="table",
        api_keys=ApiKeys(fred="test-api-key"),
    )
