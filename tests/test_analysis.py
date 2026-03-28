from datetime import date

from stockpile.analysis import FinancialMetrics, _growth, _pct, calculate_metrics
from stockpile.models import BalanceSheet, IncomeStatement


class TestPct:
    def test_normal(self):
        assert _pct(50, 200) == 25.0

    def test_none_numerator(self):
        assert _pct(None, 200) is None

    def test_none_denominator(self):
        assert _pct(50, None) is None

    def test_zero_denominator(self):
        assert _pct(50, 0) is None

    def test_negative_values(self):
        assert _pct(-50, 200) == -25.0


class TestGrowth:
    def test_normal(self):
        assert _growth(110, 100) == 10.0

    def test_none_current(self):
        assert _growth(None, 100) is None

    def test_none_previous(self):
        assert _growth(110, None) is None

    def test_zero_previous(self):
        assert _growth(110, 0) is None

    def test_negative_previous(self):
        # Uses abs(previous)
        assert _growth(110, -100) == 210.0

    def test_decline(self):
        assert _growth(90, 100) == -10.0


class TestFinancialMetricsToDict:
    def test_filters_none(self):
        m = FinancialMetrics(
            symbol="AAPL",
            market="us",
            period_end="2024-09-30",
            period_type="annual",
            currency="USD",
            revenue=100000.0,
            net_income=None,
        )
        d = m.to_dict()
        assert "revenue" in d
        assert "net_income" not in d


class TestCalculateMetrics:
    def test_full_data(self, sample_income_statements, sample_balance_sheets, sample_cash_flows):
        results = calculate_metrics("AAPL", "us", sample_income_statements, sample_balance_sheets, sample_cash_flows)
        assert len(results) == 2
        m = results[0]
        assert m.symbol == "AAPL"
        assert m.currency == "USD"
        assert m.revenue == 391035000000
        assert m.operating_margin is not None
        assert m.net_margin is not None
        assert m.roe is not None
        assert m.revenue_growth is not None

    def test_jp_market_currency(self, sample_income_statements, sample_balance_sheets, sample_cash_flows):
        results = calculate_metrics("7203", "jp", sample_income_statements, sample_balance_sheets, sample_cash_flows)
        assert results[0].currency == "JPY"

    def test_missing_balance_sheet(self, sample_income_statements, sample_cash_flows):
        results = calculate_metrics("AAPL", "us", sample_income_statements, [], sample_cash_flows)
        m = results[0]
        assert m.roe is None
        assert m.roa is None
        assert m.equity_ratio is None
        assert m.de_ratio is None
        assert m.total_assets is None

    def test_missing_cashflow(self, sample_income_statements, sample_balance_sheets):
        results = calculate_metrics("AAPL", "us", sample_income_statements, sample_balance_sheets, [])
        m = results[0]
        assert m.free_cash_flow is None
        assert m.operating_margin is not None  # still calculated from income

    def test_single_period_no_growth(self):
        income = [IncomeStatement(symbol="AAPL", period_end=date(2024, 9, 30), period_type="annual", revenue=100000)]
        results = calculate_metrics("AAPL", "us", income, [], [])
        assert len(results) == 1
        assert results[0].revenue_growth is None

    def test_skip_none_revenue(self):
        income = [
            IncomeStatement(symbol="AAPL", period_end=date(2024, 9, 30), period_type="annual", revenue=None),
            IncomeStatement(symbol="AAPL", period_end=date(2023, 9, 30), period_type="annual", revenue=100000),
        ]
        results = calculate_metrics("AAPL", "us", income, [], [])
        assert len(results) == 1
        assert results[0].revenue == 100000

    def test_de_ratio_with_zero_equity(self):
        income = [IncomeStatement(symbol="X", period_end=date(2024, 9, 30), period_type="annual", revenue=100)]
        balance = [
            BalanceSheet(
                symbol="X",
                period_end=date(2024, 9, 30),
                period_type="annual",
                total_assets=200,
                equity=0,
                total_debt=100,
            )
        ]
        results = calculate_metrics("X", "us", income, balance, [])
        assert results[0].de_ratio is None

    def test_empty_income(self):
        results = calculate_metrics("AAPL", "us", [], [], [])
        assert results == []

    def test_growth_calculation(self):
        income = [
            IncomeStatement(
                symbol="X",
                period_end=date(2024, 9, 30),
                period_type="annual",
                revenue=110,
                operating_income=55,
                net_income=33,
                eps=2.2,
            ),
            IncomeStatement(
                symbol="X",
                period_end=date(2023, 9, 30),
                period_type="annual",
                revenue=100,
                operating_income=50,
                net_income=30,
                eps=2.0,
            ),
        ]
        results = calculate_metrics("X", "us", income, [], [])
        assert results[0].revenue_growth == 10.0
        assert results[0].operating_income_growth == 10.0
        assert results[0].net_income_growth == 10.0
        assert results[0].eps_growth == 10.0
        # Second period has no prior, so no growth
        assert results[1].revenue_growth is None
