import typer
from rich.console import Console

from stockpile.config import init_config, load_config, DEFAULT_CONFIG_PATH

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def init() -> None:
    """Create a default configuration file."""
    path = init_config()
    console.print(f"Config file created at: [green]{path}[/green]")


@app.command()
def show() -> None:
    """Show current configuration."""
    config = load_config()
    console.print(f"[bold]Config path:[/bold] {DEFAULT_CONFIG_PATH}")
    console.print(f"[bold]Storage:[/bold] {config.storage_backend} ({config.storage_path})")
    console.print(f"[bold]Default market:[/bold] {config.default_market}")
    console.print(f"[bold]Output format:[/bold] {config.default_output_format}")
    console.print("[bold]API keys:[/bold]")
    for name in ("jquants", "fmp", "finnhub", "gnews", "fred"):
        value = getattr(config.api_keys, name)
        status = "[green]set[/green]" if value else "[dim]not set[/dim]"
        console.print(f"  {name}: {status}")
