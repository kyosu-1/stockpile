import csv
import io
import json
from dataclasses import asdict
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


def format_table(data: list[dict[str, Any]], title: str = "") -> None:
    if not data:
        console.print("[dim]No data found.[/dim]")
        return

    table = Table(title=title, show_lines=False)
    for key in data[0]:
        table.add_column(key, style="cyan" if key in ("symbol", "indicator_id") else "")

    for row in data:
        table.add_row(*[str(v) if v is not None else "-" for v in row.values()])

    console.print(table)


def format_json(data: list[dict[str, Any]]) -> None:
    console.print_json(json.dumps(data, ensure_ascii=False, default=str))


def format_csv(data: list[dict[str, Any]]) -> None:
    if not data:
        return
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    console.print(output.getvalue())


def output(data: list, fmt: str = "table", title: str = "") -> None:
    if not data:
        console.print("[dim]No data found.[/dim]")
        return

    dicts = [item.to_dict() if hasattr(item, "to_dict") else asdict(item) for item in data]

    match fmt:
        case "json":
            format_json(dicts)
        case "csv":
            format_csv(dicts)
        case _:
            format_table(dicts, title=title)
