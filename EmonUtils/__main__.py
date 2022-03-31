import time

from . import CONFIG_FILE
from . import SCHEMA_FILE

from .DBIO import dbio
from .EmonIO import emonio


emon = emonio.EmonIO(CONFIG_FILE, schema_file=SCHEMA_FILE)
db = dbio.DBIO(CONFIG_FILE)

while True:
    data = emon.fetch_data()
    db.update_document(data)
    print("Sending", data)
    time.sleep(5)
