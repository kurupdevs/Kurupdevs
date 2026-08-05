"""KurupDevs - Database (SQLite/MongoDB)"""
import json
import re
import sqlite3
import threading
from utils import config


class SqliteDatabase:
    def __init__(self, file):
        self._conn = sqlite3.connect(file, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()

    @staticmethod
    def _parse_row(row):
        if row["type"] == "bool":
            return row["val"] == "1"
        if row["type"] == "int":
            return int(row["val"])
        if row["type"] == "str":
            return row["val"]
        return json.loads(row["val"])

    def _execute(self, module, *args, **kwargs):
        if not re.match(r"^(core|custom)", module):
            raise ValueError(f"Invalid module: {module}")
        self._lock.acquire()
        try:
            return self._conn.cursor().execute(*args, **kwargs)
        except sqlite3.OperationalError as e:
            if str(e).startswith("no such table"):
                self._conn.cursor().execute(
                    f"CREATE TABLE IF NOT EXISTS '{module}' (var TEXT UNIQUE, val TEXT, type TEXT)"
                )
                self._conn.commit()
                return self._conn.cursor().execute(*args, **kwargs)
            raise
        finally:
            self._lock.release()

    def get(self, module, variable, default=None):
        cur = self._execute(module, f"SELECT * FROM '{module}' WHERE var=?", (variable,))
        row = cur.fetchone()
        return default if row is None else self._parse_row(row)

    def set(self, module, variable, value):
        if isinstance(value, bool):
            val, typ = ("1" if value else "0"), "bool"
        elif isinstance(value, (int,)):
            val, typ = str(value), "int"
        elif isinstance(value, str):
            val, typ = value, "str"
        else:
            val, typ = json.dumps(value), "json"
        self._execute(module,
            f"INSERT INTO '{module}' VALUES(?,?,?) ON CONFLICT(var) DO UPDATE SET val=?, type=? WHERE var=?",
            (variable, val, typ, val, typ, variable))
        self._conn.commit()
        return True

    def remove(self, module, variable):
        self._execute(module, f"DELETE FROM '{module}' WHERE var=?", (variable,))
        self._conn.commit()

    def get_collection(self, module):
        cur = self._execute(module, f"SELECT * FROM '{module}'")
        return {row["var"]: self._parse_row(row) for row in cur}

    def close(self):
        self._conn.commit()
        self._conn.close()


if config.db_type in ["mongo", "mongodb"]:
    import pymongo
    class MongoDatabase:
        def __init__(self, url, name):
            self._client = pymongo.MongoClient(url)
            self._db = self._client[name]
        def get(self, m, v, d=None):
            doc = self._db[m].find_one({"var": v})
            return d if doc is None else doc["val"]
        def set(self, m, v, val):
            self._db[m].replace_one({"var": v}, {"var": v, "val": val}, upsert=True)
        def remove(self, m, v):
            self._db[m].delete_one({"var": v})
        def get_collection(self, m):
            return {i["var"]: i["val"] for i in self._db[m].find()}
        def close(self):
            self._client.close()
    db = MongoDatabase(config.db_url, config.db_name)
else:
    db = SqliteDatabase(config.db_name)
