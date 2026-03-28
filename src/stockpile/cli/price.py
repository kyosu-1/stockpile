import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def get(
    symbol: str = typer.Argument(help="Stock ticker symbol (e.g., AAPL, 7203)"),
    start: str = typer.Option(None, help="Start date (YYYY-MM-DD)"),
    end: str = typer.Option(None, help="End date (YYYY-MM-DD)"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get historical stock prices."""
    typer.echo(f"[TODO] Fetching prices for {symbol} (market={market})")


@app.command()
def current(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    market: str = typer.Option("us", help="Market: us or jp"),
) -> None:
    """Get current stock price."""
    typer.echo(f"[TODO] Fetching current price for {symbol} (market={market})")
