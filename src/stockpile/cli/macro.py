import typer
from rich.console import Console
from rich.table import Table

from stockpile.cli.formatters import output
from stockpile.config import load_config
from stockpile.providers.fred_provider import FREDProvider

app = typer.Typer(no_args_is_help=True)
console = Console()


def _get_fred_provider() -> FREDProvider:
    config = load_config()
    return FREDProvider(api_key=config.api_keys.fred)


@app.command()
def get(
    indicator_id: str = typer.Argument(help="Indicator ID (e.g., GDP, CPIAUCSL, FEDFUNDS)"),
    start: str = typer.Option(None, help="Start date (YYYY-MM-DD)"),
    end: str = typer.Option(None, help="End date (YYYY-MM-DD)"),
    source: str = typer.Option("fred", help="Data source: fred or estat"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get macro economic indicator data."""
    from datetime import date as date_type

    start_date = date_type.fromisoformat(start) if start else None
    end_date = date_type.fromisoformat(end) if end else None

    if source == "fred":
        provider = _get_fred_provider()
        with console.status(f"Fetching {indicator_id} from FRED..."):
            data = provider.get_indicator(indicator_id, start_date, end_date)
        output(data, fmt=fmt, title=f"FRED: {indicator_id}")
    else:
        console.print(f"[yellow]Source '{source}' not yet implemented.[/yellow]")


@app.command("list")
def list_indicators(
    source: str = typer.Option("fred", help="Data source: fred or estat"),
    search: str = typer.Option(None, help="Search query"),
) -> None:
    """List or search available macro indicators."""
    if source == "fred":
        if not search:
            # Show popular indicators
            table = Table(title="Popular FRED Indicators")
            table.add_column("Alias", style="cyan")
            table.add_column("Series ID")
            for alias, sid in FREDProvider.POPULAR_INDICATORS.items():
                table.add_row(alias, sid)
            console.print(table)
            console.print("\n[dim]Use --search to find more indicators[/dim]")
            return

        provider = _get_fred_provider()
        with console.status(f"Searching FRED for '{search}'..."):
            results = provider.search_indicators(search)

        if not results:
            console.print("[dim]No indicators found.[/dim]")
            return

        table = Table(title=f"FRED Search: {search}")
        table.add_column("ID", style="cyan")
        table.add_column("Title")
        table.add_column("Freq")
        table.add_column("Units")
        for r in results:
            table.add_row(r["id"], r["title"], r["frequency"], r["units"])
        console.print(table)
    else:
        console.print(f"[yellow]Source '{source}' not yet implemented.[/yellow]")
