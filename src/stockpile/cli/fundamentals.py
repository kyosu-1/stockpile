import typer
from rich.console import Console

from stockpile.cli.formatters import output
from stockpile.providers.yfinance_provider import YFinanceProvider

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def income(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    period: str = typer.Option("annual", help="Period: annual or quarterly"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get income statement."""
    provider = YFinanceProvider(market=market)
    with console.status(f"Fetching income statement for {symbol}..."):
        data = provider.get_income_statement(symbol, period)
    output(data, fmt=fmt, title=f"{symbol} Income Statement ({period})")


@app.command()
def balance(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    period: str = typer.Option("annual", help="Period: annual or quarterly"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get balance sheet."""
    provider = YFinanceProvider(market=market)
    with console.status(f"Fetching balance sheet for {symbol}..."):
        data = provider.get_balance_sheet(symbol, period)
    output(data, fmt=fmt, title=f"{symbol} Balance Sheet ({period})")


@app.command()
def cashflow(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    period: str = typer.Option("annual", help="Period: annual or quarterly"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get cash flow statement."""
    provider = YFinanceProvider(market=market)
    with console.status(f"Fetching cash flow for {symbol}..."):
        data = provider.get_cash_flow(symbol, period)
    output(data, fmt=fmt, title=f"{symbol} Cash Flow ({period})")
