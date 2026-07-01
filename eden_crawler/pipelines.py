import importlib
import inspect
import sqlite3
from datetime import datetime

import scrapy


class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()
        spider_file = spider.__class__.__module__.split(".")[-1]
        self.table_name = f"spider_{spider_file}"

        # auto-detect Item class from spider module
        mod = importlib.import_module(spider.__class__.__module__)
        for _, obj in inspect.getmembers(mod, inspect.isclass):
            if issubclass(obj, scrapy.Item) and obj is not scrapy.Item:
                self._ensure_table(list(obj.fields.keys()))
                self._fields = list(obj.fields.keys())
                break

    def close_spider(self, spider):
        self.conn.close()

    def _ensure_table(self, fields):
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (self.table_name,),
        )
        if self.cursor.fetchone() is None:
            column_defs = ["insert_time TEXT"] + [f"{f} TEXT" for f in fields]
            self.cursor.execute(
                f"CREATE TABLE {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join(column_defs)})"
            )
        else:
            self.cursor.execute(f"PRAGMA table_info({self.table_name})")
            existing = [row[1] for row in self.cursor.fetchall()]
            existing_set = set(existing)
            wanted = set(fields) | {"insert_time"}

            for f in ["insert_time"] + fields:
                if f not in existing_set:
                    self.cursor.execute(
                        f"ALTER TABLE {self.table_name} ADD COLUMN {f} TEXT"
                    )

            for c in existing:
                if c not in ("id",) and c not in wanted:
                    self.cursor.execute(
                        f"ALTER TABLE {self.table_name} DROP COLUMN {c}"
                    )
        self.conn.commit()

    def process_item(self, item, spider):
        fields = self._fields
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
