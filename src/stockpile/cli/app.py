import typer

from stockpile.cli.price import app as price_app
from stockpile.cli.fundamentals import app as fundamentals_app
from stockpile.cli.news import app as news_app
from stockpile.cli.macro import app as macro_app
from stockpile.cli.config_cmd import app as config_app
from stockpile.cli.metrics import app as metrics_app

app = typer.Typer(
    name="stockpile",
    help="Stock investment information gathering CLI for US and Japanese markets.",
    no_args_is_help=True,
)

app.add_typer(price_app, name="price", help="Stock price data")
app.add_typer(fundamentals_app, name="fundamentals", help="Financial statements")
app.add_typer(news_app, name="news", help="Company news")
app.add_typer(macro_app, name="macro", help="Macro economic indicators")
app.add_typer(config_app, name="config", help="Configuration management")
app.add_typer(metrics_app, name="metrics", help="Financial metrics and comparison")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
