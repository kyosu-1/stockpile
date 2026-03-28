import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def income(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    period: str = typer.Option("annual", help="Period: annual or quarterly"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get income statement."""
    typer.echo(f"[TODO] Fetching income statement for {symbol}")


@app.command()
def balance(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    period: str = typer.Option("annual", help="Period: annual or quarterly"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get balance sheet."""
    typer.echo(f"[TODO] Fetching balance sheet for {symbol}")


@app.command()
def cashflow(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    period: str = typer.Option("annual", help="Period: annual or quarterly"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get cash flow statement."""
    typer.echo(f"[TODO] Fetching cash flow for {symbol}")
