import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def get(
    indicator_id: str = typer.Argument(help="Indicator ID (e.g., GDP, CPIAUCSL)"),
    start: str = typer.Option(None, help="Start date (YYYY-MM-DD)"),
    end: str = typer.Option(None, help="End date (YYYY-MM-DD)"),
    source: str = typer.Option("fred", help="Data source: fred or estat"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get macro economic indicator data."""
    typer.echo(f"[TODO] Fetching {indicator_id} from {source}")


@app.command("list")
def list_indicators(
    source: str = typer.Option("fred", help="Data source: fred or estat"),
    search: str = typer.Option(None, help="Search query"),
) -> None:
    """List available macro indicators."""
    typer.echo(f"[TODO] Listing indicators from {source}")
