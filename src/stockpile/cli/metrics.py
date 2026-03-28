from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from stockpile.analysis import FinancialMetrics, calculate_metrics
from stockpile.cli.formatters import output
from stockpile.providers.yfinance_provider import YFinanceProvider

app = typer.Typer(no_args_is_help=True)
console = Console()


def _fetch_metrics(symbol: str, market: str, period: str) -> list[FinancialMetrics]:
    provider = YFinanceProvider(market=market)
    income = provider.get_income_statement(symbol, period)
    balance = provider.get_balance_sheet(symbol, period)
    cashflow = provider.get_cash_flow(symbol, period)
    return calculate_metrics(symbol, market, income, balance, cashflow)


# Display labels for human-readable table output
_DISPLAY_LABELS = {
    "revenue": "Revenue",
    "operating_income": "Operating Income",
    "net_income": "Net Income",
    "ebitda": "EBITDA",
    "eps": "EPS",
    "total_assets": "Total Assets",
    "equity": "Equity",
    "total_debt": "Total Debt",
    "cash": "Cash",
    "free_cash_flow": "Free Cash Flow",
    "operating_margin": "Operating Margin (%)",
    "net_margin": "Net Margin (%)",
    "ebitda_margin": "EBITDA Margin (%)",
    "roe": "ROE (%)",
    "roa": "ROA (%)",
    "equity_ratio": "Equity Ratio (%)",
    "de_ratio": "D/E Ratio",
    "revenue_growth": "Revenue Growth (%)",
    "operating_income_growth": "Op. Income Growth (%)",
    "net_income_growth": "Net Income Growth (%)",
    "eps_growth": "EPS Growth (%)",
}


def _format_value(key: str, value) -> str:
    if value is None:
        return "-"
    if key in ("de_ratio", "eps"):
        return f"{value:,.2f}"
    if key.endswith(("_margin", "_growth", "_ratio")) or key in ("roe", "roa", "equity_ratio"):
        return f"{value:+.1f}%" if "growth" in key else f"{value:.1f}%"
    if isinstance(value, float) and abs(value) >= 1_000_000:
        if abs(value) >= 1_000_000_000_000:
            return f"{value / 1_000_000_000_000:.2f}T"
        if abs(value) >= 1_000_000_000:
            return f"{value / 1_000_000_000:.1f}B"
        return f"{value / 1_000_000:.0f}M"
    return str(value)


@app.command("get")
def get_metrics(
    symbol: str = typer.Argument(help="Stock ticker symbol (e.g., AAPL, 7203)"),
    market: str = typer.Option("us", help="Market: us or jp"),
    period: str = typer.Option("annual", help="Period: annual or quarterly"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Calculate key financial metrics for a stock."""
    with console.status(f"Calculating metrics for {symbol}..."):
        metrics = _fetch_metrics(symbol, market, period)

    if not metrics:
        console.print("[dim]No data available.[/dim]")
        return

    if fmt != "table":
        output(metrics, fmt=fmt, title=f"{symbol} Metrics")
        return

    # Transpose: rows = metrics, columns = periods
    table = Table(title=f"{symbol} Financial Metrics ({metrics[0].currency})")
    table.add_column("Metric", style="bold")
    for m in metrics:
        table.add_column(m.period_end, justify="right")

    for key, label in _DISPLAY_LABELS.items():
        row = [label]
        for m in metrics:
            row.append(_format_value(key, getattr(m, key)))
        table.add_row(*row)

    console.print(table)


@app.command("compare")
def compare(
    symbols: Annotated[list[str], typer.Argument(help="Ticker symbols to compare (e.g., AAPL MSFT GOOGL)")],
    market: str = typer.Option("us", help="Market: us or jp"),
    period: str = typer.Option("annual", help="Period: annual or quarterly"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Compare financial metrics across multiple stocks (latest period)."""
    all_metrics: list[FinancialMetrics] = []

    with console.status(f"Fetching data for {', '.join(symbols)}..."):
        for sym in symbols:
            metrics = _fetch_metrics(sym, market, period)
            if metrics:
                all_metrics.append(metrics[0])  # Latest period only

    if not all_metrics:
        console.print("[dim]No data available.[/dim]")
        return

    if fmt != "table":
        output(all_metrics, fmt=fmt, title="Comparison")
        return

    # Table: rows = metrics, columns = symbols
    table = Table(title=f"Comparison ({all_metrics[0].currency}, latest period)")
    table.add_column("Metric", style="bold")
    for m in all_metrics:
        table.add_column(f"{m.symbol}\n{m.period_end}", justify="right")

    for key, label in _DISPLAY_LABELS.items():
        row = [label]
        for m in all_metrics:
            row.append(_format_value(key, getattr(m, key)))
        table.add_row(*row)

    console.print(table)
