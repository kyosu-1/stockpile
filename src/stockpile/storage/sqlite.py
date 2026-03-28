import json
import sqlite3
from datetime import date, datetime
from pathlib import Path

from stockpile.models import OHLCV, Article, MacroDataPoint


class SQLiteStorage:
    def __init__(self, db_path: str | Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._db_path))
        self._conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self) -> None:
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS ohlcv (
                symbol      TEXT NOT NULL,
                date        TEXT NOT NULL,
                open        REAL,
                high        REAL,
                low         REAL,
                close       REAL,
                volume      INTEGER,
                source      TEXT NOT NULL,
                fetched_at  TEXT NOT NULL,
                PRIMARY KEY (symbol, date, source)
            );

            CREATE TABLE IF NOT EXISTS financials (
                symbol      TEXT NOT NULL,
                period_end  TEXT NOT NULL,
                statement   TEXT NOT NULL,
                period_type TEXT NOT NULL,
                data        TEXT NOT NULL,
                source      TEXT NOT NULL,
                fetched_at  TEXT NOT NULL,
                PRIMARY KEY (symbol, period_end, statement, period_type, source)
            );

            CREATE TABLE IF NOT EXISTS articles (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                title        TEXT NOT NULL,
                url          TEXT NOT NULL UNIQUE,
                source       TEXT,
                published_at TEXT,
                summary      TEXT,
                symbols      TEXT,
                fetched_at   TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS macro (
                indicator_id TEXT NOT NULL,
                date         TEXT NOT NULL,
                value        REAL,
                unit         TEXT,
                source       TEXT NOT NULL,
                fetched_at   TEXT NOT NULL,
                PRIMARY KEY (indicator_id, date, source)
            );
        """)

    def save_prices(self, prices: list[OHLCV], source: str) -> None:
        now = datetime.now().isoformat()
        self._conn.executemany(
            """INSERT OR REPLACE INTO ohlcv
               (symbol, date, open, high, low, close, volume, source, fetched_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (p.symbol, p.date.isoformat(), p.open, p.high, p.low, p.close, p.volume, source, now)
                for p in prices
            ],
        )
        self._conn.commit()

    def get_prices(
        self, symbol: str, start: date, end: date, source: str | None = None
    ) -> list[OHLCV]:
        query = "SELECT * FROM ohlcv WHERE symbol = ? AND date >= ? AND date <= ?"
        params: list = [symbol, start.isoformat(), end.isoformat()]
        if source:
            query += " AND source = ?"
            params.append(source)
        query += " ORDER BY date"

        rows = self._conn.execute(query, params).fetchall()
        return [
            OHLCV(
                symbol=row["symbol"],
                date=date.fromisoformat(row["date"]),
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                volume=row["volume"],
            )
            for row in rows
        ]

    def save_financials(
        self, symbol: str, statement: str, period_type: str, data: dict, source: str
    ) -> None:
        now = datetime.now().isoformat()
        for period_end, values in data.items():
            self._conn.execute(
                """INSERT OR REPLACE INTO financials
                   (symbol, period_end, statement, period_type, data, source, fetched_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (symbol, period_end, statement, period_type, json.dumps(values), source, now),
            )
        self._conn.commit()

    def get_financials(
        self, symbol: str, statement: str, period_type: str, source: str | None = None
    ) -> dict | None:
        query = "SELECT * FROM financials WHERE symbol = ? AND statement = ? AND period_type = ?"
        params: list = [symbol, statement, period_type]
        if source:
            query += " AND source = ?"
            params.append(source)
        query += " ORDER BY period_end DESC"

        rows = self._conn.execute(query, params).fetchall()
        if not rows:
            return None
        return {row["period_end"]: json.loads(row["data"]) for row in rows}

    def save_articles(self, articles: list[Article]) -> None:
        now = datetime.now().isoformat()
        for a in articles:
            self._conn.execute(
                """INSERT OR IGNORE INTO articles
                   (title, url, source, published_at, summary, symbols, fetched_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    a.title,
                    a.url,
                    a.source,
                    a.published_at.isoformat() if a.published_at else None,
                    a.summary,
                    ",".join(a.symbols) if a.symbols else None,
                    now,
                ),
            )
        self._conn.commit()

    def save_macro(self, data: list[MacroDataPoint], source: str) -> None:
        now = datetime.now().isoformat()
        self._conn.executemany(
            """INSERT OR REPLACE INTO macro
               (indicator_id, date, value, unit, source, fetched_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [(d.indicator_id, d.date.isoformat(), d.value, d.unit, source, now) for d in data],
        )
        self._conn.commit()

    def get_macro(
        self, indicator_id: str, start: date | None, end: date | None, source: str | None = None
    ) -> list[MacroDataPoint]:
        query = "SELECT * FROM macro WHERE indicator_id = ?"
        params: list = [indicator_id]
        if start:
            query += " AND date >= ?"
            params.append(start.isoformat())
        if end:
            query += " AND date <= ?"
            params.append(end.isoformat())
        if source:
            query += " AND source = ?"
            params.append(source)
        query += " ORDER BY date"

        rows = self._conn.execute(query, params).fetchall()
        return [
            MacroDataPoint(
                indicator_id=row["indicator_id"],
                date=date.fromisoformat(row["date"]),
                value=row["value"],
                unit=row["unit"] or "",
            )
            for row in rows
        ]

    def close(self) -> None:
        self._conn.close()
