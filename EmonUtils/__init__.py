import os

__version__ = "0.4"

from .EmonIO import EmonIO
from .DBIO import DBIO

PACKAGE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
CONFIG_FILE = os.path.join(DATA_DIR, "dev.cfg")
SCHEMA_FILE = os.path.join(DATA_DIR, "schema.json")

if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

if not os.path.isfile(CONFIG_FILE):
    from .setup import generate_config
    generate_config(CONFIG_FILE)

if not os.path.isfile(SCHEMA_FILE):
    from .setup import generate_schema
    generate_schema(CONFIG_FILE, SCHEMA_FILE)

if __name__ == "__main__":
    print(PACKAGE_DIR)
    print(DATA_DIR)
    print(CONFIG_FILE)
    print(SCHEMA_FILE)
