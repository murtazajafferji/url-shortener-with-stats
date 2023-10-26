import os
import sqlite3

_current_dir = os.path.dirname(os.path.realpath(__file__))


class SqliteDB(object):
    """
    Wraps SQLite database connection.

    Sample usage:

        db = SqliteDB()
        db.connection.execute(
            "INSERT INTO test (key, value) VALUES (?, ?), (?, ?)", ("foo", 1, "bar", 2)
        )
        db.connection.commit()

        rows = db.connection.execute("SELECT * FROM test").fetchall()
        for row in rows:
            print(" ".join(f"{column}={row[column]}" for column in row.keys()))
    """

    def __init__(self, database_file_path: str = f"{_current_dir}/db.sqlite"):
        """Initialize the sqlite database connection.

        Args:
            database_file_path (str): Path to file where database is stored. The file
                will be created if it does not exist.
        """
        # Initialize the database connection, using sqlite3.Row as the row_factory
        self._connection = sqlite3.connect(database_file_path)
        self._connection.row_factory = sqlite3.Row

    @property
    def connection(self) -> sqlite3.Connection:
        """Get the database connection object.

        Returns:
            sqlite3.Connection: The SQLite database connection
        """
        return self._connection
