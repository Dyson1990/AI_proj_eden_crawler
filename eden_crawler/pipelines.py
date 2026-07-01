import sqlite3
from datetime import datetime


class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect("ip_check.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ip_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                country TEXT,
                region TEXT,
                city TEXT,
                org TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute(
            "INSERT INTO ip_records (ip, country, region, city, org, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (item.get("ip"), item.get("country"), item.get("region"), item.get("city"), item.get("org"), datetime.now().isoformat()),
        )
        self.conn.commit()
        return item
