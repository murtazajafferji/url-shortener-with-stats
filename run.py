import importlib
import os

from src import app


if __name__ == "__main__":
    # Import and register routes with Flask application
    importlib.import_module(".routes", "src")

    app.run(
        os.environ.get("HOST", "localhost"),
        port=os.environ.get("PORT", 8080),
        debug=True,
    )
