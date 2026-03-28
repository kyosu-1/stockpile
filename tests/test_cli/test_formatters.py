from stockpile.cli.formatters import format_csv, format_json, format_table, output
from stockpile.models import OHLCV
from datetime import date


class TestFormatTable:
    def test_empty_data(self, capsys):
        format_table([])
        # Rich output goes to its own console, so just verify no exception

    def test_with_data(self):
        data = [{"symbol": "AAPL", "price": 150.0}]
        # Should not raise
        format_table(data, title="Test")


class TestFormatJson:
    def test_outputs_json(self):
        data = [{"symbol": "AAPL", "price": 150.0}]
        # Should not raise
        format_json(data)


class TestFormatCsv:
    def test_empty_data(self):
        format_csv([])  # Should not raise

    def test_with_data(self):
        data = [{"symbol": "AAPL", "price": 150.0}]
        format_csv(data)  # Should not raise


class TestOutput:
    def test_empty_list(self):
        output([], fmt="table")  # Should not raise

    def test_with_objects(self):
        items = [OHLCV(symbol="AAPL", date=date(2025, 1, 2), open=150, high=155, low=149, close=153, volume=100)]
        output(items, fmt="json")  # Should not raise

    def test_csv_format(self):
        items = [OHLCV(symbol="AAPL", date=date(2025, 1, 2), open=150, high=155, low=149, close=153, volume=100)]
        output(items, fmt="csv")  # Should not raise
