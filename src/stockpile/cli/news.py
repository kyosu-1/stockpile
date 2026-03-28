import typer
from rich.console import Console

from stockpile.cli.formatters import output
from stockpile.providers.news_provider import YFinanceNewsProvider

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def get(
    symbol: str = typer.Argument(help="Stock ticker symbol"),
    limit: int = typer.Option(10, help="Number of articles to fetch"),
    market: str = typer.Option("us", help="Market: us or jp"),
    fmt: str = typer.Option("table", "--format", help="Output format: table, json, csv"),
) -> None:
    """Get news for a stock."""
    provider = YFinanceNewsProvider(market=market)
    with console.status(f"Fetching news for {symbol}..."):
        articles = provider.get_news(symbol, limit)
    output(articles, fmt=fmt, title=f"{symbol} News")
