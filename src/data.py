from abc import ABC, abstractmethod
from typing import Dict, Optional
from datetime import datetime

from src.db import SqliteDB

class DataStore(ABC):

    @abstractmethod
    def __init__(self, test: bool = False) -> None:
         raise NotImplementedError

    @abstractmethod
    def create_url(self, url_id: str, redirect_url: str, auth_token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_direct_url(self, src: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def has_redirect(self, src: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_url(self, src: str) -> bool:
        raise NotImplementedError

# TODO: Add Redis data store for caching

class SqliteDataStore(DataStore):
    # TODO: Look up Flask way to handle test data stores
    # TODO: Look up if I can 
    def __init__(self, testing: bool = False) -> None:
        self.url_table_name = f"{'test_' if testing else ''}urls"
        self.stats_table_name = f"{'test_' if testing else ''}stats"

    def create_url(self, url_id: str, redirect_url: str, auth_token: str) -> None:
        db = SqliteDB()
        db.connection.execute(
            f"INSERT INTO {self.url_table_name} (url_id, redirect_url, auth_token) VALUES (?, ?, ?)",(url_id, redirect_url, auth_token)
        )
        db.connection.commit()
        db.connection.close()

    def get_direct_url(self, url_id: str) -> str:
        db = SqliteDB()
        row = db.connection.execute(f'SELECT redirect_url FROM {self.url_table_name} WHERE url_id = ?',(url_id,)).fetchone()
        db.connection.close()
        return row[0]

    def has_redirect(self, url_id: str) -> bool:
        db = SqliteDB()
        row = db.connection.execute(f'SELECT 1 FROM {self.url_table_name} WHERE url_id = ?',(url_id,)).fetchone()
        db.connection.close()
        return row is not None

    def has_valid_auth_token(self, url_id: str, auth_token: str) -> bool:
        db = SqliteDB()
        row = db.connection.execute(f'SELECT 1 FROM {self.url_table_name} WHERE url_id = ? AND auth_token = ?',(url_id, auth_token)).fetchone()
        db.connection.close()
        return row is not None

    def delete_url(self, url_id: str) -> None:
        db = SqliteDB()
        db.connection.execute(f'SELECT 1 FROM {self.url_table_name} WHERE url_id = ?',(url_id,))
        db.connection.commit()
        db.connection.close()

    def visit_url_id(self, url_id: str, ip: str) -> None:
        db = SqliteDB()
        db.connection.execute(f'INSERT OR IGNORE INTO {self.stats_table_name} (url_id, ip) VALUES (?, ?)',(url_id,ip))
        db.connection.commit()
        db.connection.execute(f'UPDATE {self.stats_table_name} SET visits = visits + 1 WHERE url_id = ? AND ip = ?',(url_id,ip))
        db.connection.commit()
        db.connection.close()

    def visits_per_ip(self, url_id: str) -> dict:
        db = SqliteDB()
        rows = db.connection.execute(f'SELECT ip, visits FROM {self.stats_table_name} WHERE url_id = ? GROUP BY ip ORDER BY visits DESC',(url_id,)).fetchall()
        db.connection.commit()
        db.connection.close()
        return dict(rows)

    def get_expiration(self, url_id: str) -> dict:
        db = SqliteDB()
        row = db.connection.execute(f'SELECT expire_time FROM {self.url_table_name} WHERE url_id = ?',(url_id,)).fetchone()
        db.connection.commit()
        db.connection.close()
        return row[0] if row else None

    def set_expiration(self, url_id: str, expire_time: datetime) -> None:
        db = SqliteDB()
        db.connection.execute(f'UPDATE {self.url_table_name} SET expire_time = ? WHERE url_id = ?',(expire_time.strftime("%Y-%m-%d %H:%M:%S"), url_id,))
        db.connection.commit()
        db.connection.close()

    def delete_url_id(self, url_id: str) -> None:
        db = SqliteDB()
        db.connection.execute(f'DELETE FROM {self.url_table_name} WHERE url_id = ?',(url_id,))
        db.connection.commit()
        db.connection.execute(f'DELETE FROM {self.stats_table_name} WHERE url_id = ?',(url_id,))
        db.connection.commit()
        db.connection.close()

    def clear_data(self) -> bool:
        db = SqliteDB()
        db.connection.execute(f"DELETE FROM {self.url_table_name}")
        db.connection.commit()
        db.connection.execute(f"DELETE FROM {self.stats_table_name}")
        db.connection.commit()
        db.connection.close()
