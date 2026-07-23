import sqlite3
from datetime import datetime


class SQLitePipeline:
    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        o._crawler = crawler
        return o

    def open_spider(self):
        spider = self._crawler.spider
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()
        spider_file = spider.__class__.__module__.split(".")[-1]
        self.table_name = f"spider_{spider_file}"

    def close_spider(self):
        self.conn.close()

    def _ensure_table(self, fields):
        """Create table on first item if not exists."""
        column_defs = ["insert_time TEXT"] + [f"{f} TEXT" for f in fields]
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join(column_defs)})"
        )
        self.conn.commit()

    def _sync_columns(self, fields):
        """Add new columns that appear in later items."""
        self.cursor.execute(f"PRAGMA table_info({self.table_name})")
        existing = {row[1] for row in self.cursor.fetchall()}
        for f in fields:
            if f not in existing:
                self.cursor.execute(
                    f"ALTER TABLE {self.table_name} ADD COLUMN {f} TEXT"
                )
        self.conn.commit()

    def process_item(self, item):
        fields = list(item.fields.keys())
        self._ensure_table(fields)
        self._sync_columns(fields)

        values = [datetime.now().isoformat()]
        values += [
            datetime.now().isoformat() if f == "timestamp" and not item.get(f) else item.get(f)
            for f in fields
        ]
        placeholders = ", ".join(["?"] * (len(fields) + 1))
        self.cursor.execute(
            f"INSERT INTO {self.table_name} (insert_time, {', '.join(fields)}) VALUES ({placeholders})",
            values,
        )
        self.conn.commit()
        return item
