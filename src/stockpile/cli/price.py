from datetime import date, timedelta

import typer
from rich.console import Console

from stockpile.cli.formatters import output
from stockpile.providers.yfinance_provider import YFinanceProvider

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def get(
    symbol: str = typer.Argument(help="Stock ticker symbol (e.g., AAPL, 7203)"),
    start: str = typer.Option(None, help="Start date (YYYY-MM-DD)"),
    end: str = typer.Option(None, help="End date (YYYY-MM-DD)"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get historical stock prices."""
    end_date = date.fromisoformat(end) if end else date.today()
    start_date = date.fromisoformat(start) if start else end_date - timedelta(days=30)

    provider = YFinanceProvider(market=market)
    with console.status(f"Fetching prices for {symbol}..."):
        prices = provider.get_historical_prices(symbol, start_date, end_date)

    output(prices, fmt=fmt, title=f"{symbol} Price History")


@app.command()
def current(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    market: str = typer.Option("us", help="Market: us or jp"),
) -> None:
    """Get current stock price."""
    provider = YFinanceProvider(market=market)
    with console.status(f"Fetching current price for {symbol}..."):
        quote = provider.get_current_price(symbol)

    color = "green" if quote.change >= 0 else "red"
    console.print(
        f"[bold]{quote.symbol}[/bold]  ${quote.price:.2f}  [{color}]{quote.change:+.2f} ({quote.change_pct:+.2f}%)[/{color}]"
    )
