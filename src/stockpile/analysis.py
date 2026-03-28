"""Financial metrics calculation from raw provider data."""

from dataclasses import dataclass

from stockpile.models import BalanceSheet, CashFlow, IncomeStatement


@dataclass
class FinancialMetrics:
    symbol: str
    market: str
    period_end: str
    period_type: str
    currency: str
    # Scale
    revenue: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    ebitda: float | None = None
    total_assets: float | None = None
    equity: float | None = None
    total_debt: float | None = None
    cash: float | None = None
    free_cash_flow: float | None = None
    eps: float | None = None
    # Profitability
    operating_margin: float | None = None
    net_margin: float | None = None
    roe: float | None = None
    roa: float | None = None
    ebitda_margin: float | None = None
    # Leverage
    equity_ratio: float | None = None
    de_ratio: float | None = None
    # Growth (vs prior period)
    revenue_growth: float | None = None
    operating_income_growth: float | None = None
    net_income_growth: float | None = None
    eps_growth: float | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


def _pct(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator == 0:
        return None
    return round(numerator / denominator * 100, 2)


def _growth(current: float | None, previous: float | None) -> float | None:
    if current is None or previous is None or previous == 0:
        return None
    return round((current - previous) / abs(previous) * 100, 2)


def calculate_metrics(
    symbol: str,
    market: str,
    income: list[IncomeStatement],
    balance: list[BalanceSheet],
    cashflow: list[CashFlow],
) -> list[FinancialMetrics]:
    """Calculate financial metrics for each period.

    Assumes income/balance/cashflow are sorted newest-first (as returned by yfinance).
    """
    currency = "JPY" if market == "jp" else "USD"

    # Index balance sheets and cash flows by period_end for lookup
    balance_by_period = {b.period_end.isoformat(): b for b in balance}
    cf_by_period = {c.period_end.isoformat(): c for c in cashflow}

    results = []
    for i, inc in enumerate(income):
        if inc.revenue is None:
            continue

        period_key = inc.period_end.isoformat()
        bs = balance_by_period.get(period_key)
        cf = cf_by_period.get(period_key)

        # Prior period for growth calculation
        prior_inc = income[i + 1] if i + 1 < len(income) and income[i + 1].revenue is not None else None

        m = FinancialMetrics(
            symbol=symbol,
            market=market,
            period_end=period_key,
            period_type=inc.period_type,
            currency=currency,
            # Raw values
            revenue=inc.revenue,
            operating_income=inc.operating_income,
            net_income=inc.net_income,
            ebitda=inc.ebitda,
            eps=inc.eps,
            total_assets=bs.total_assets if bs else None,
            equity=bs.equity if bs else None,
            total_debt=bs.total_debt if bs else None,
            cash=bs.cash if bs else None,
            free_cash_flow=cf.free_cash_flow if cf else None,
            # Profitability
            operating_margin=_pct(inc.operating_income, inc.revenue),
            net_margin=_pct(inc.net_income, inc.revenue),
            ebitda_margin=_pct(inc.ebitda, inc.revenue),
            roe=_pct(inc.net_income, bs.equity) if bs else None,
            roa=_pct(inc.net_income, bs.total_assets) if bs else None,
            # Leverage
            equity_ratio=_pct(bs.equity, bs.total_assets) if bs else None,
            de_ratio=round(bs.total_debt / bs.equity, 2) if bs and bs.total_debt and bs.equity and bs.equity != 0 else None,
            # Growth
            revenue_growth=_growth(inc.revenue, prior_inc.revenue) if prior_inc else None,
            operating_income_growth=_growth(inc.operating_income, prior_inc.operating_income) if prior_inc else None,
            net_income_growth=_growth(inc.net_income, prior_inc.net_income) if prior_inc else None,
            eps_growth=_growth(inc.eps, prior_inc.eps) if prior_inc else None,
        )
        results.append(m)

    return results
