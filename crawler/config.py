import os

CELERY_BROKER = os.environ.get("CELERY_BROKER",
                               "sqla+sqlite:////app/celery.db")
CELERY_BACKEND = os.environ.get("CELERY_BACKEND",
                                "db+sqlite:////app/celery_results.db")
SCREENSHOT_DB_CONN_STR = os.environ.get("SCREENSHOT_DB_CONN_STR",
                                        "sqlite+pysqlite:////app/screenshot.db")

DATA_DIR = os.environ.get("DATA_DIR", "/app/data")