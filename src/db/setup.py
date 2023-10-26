import os
from . import SqliteDB

if __name__ == "__main__":
    db = SqliteDB()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f"{current_dir}/schema.sql") as f:
        db.connection.executescript(f.read())
    with open(f"{current_dir}/schema_test.sql") as f:
        db.connection.executescript(f.read())
        db.connection.close()