import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def get(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    limit: int = typer.Option(10, help="Number of articles to fetch"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get news for a stock."""
    typer.echo(f"[TODO] Fetching news for {symbol}")
