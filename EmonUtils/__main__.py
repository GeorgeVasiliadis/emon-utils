import time

from . import CONFIG_FILE
from . import SCHEMA_FILE

from .DBIO import dbio
from .EmonIO import emonio

COOLDOWN = 5 # How many seconds should each fetch-update-send cycle last at least

emon = emonio.EmonIO(CONFIG_FILE, schema_file=SCHEMA_FILE)
db = dbio.DBIO(CONFIG_FILE)

while True:
    t1 = time.time()
    data = emon.fetch_data()
    db.update_document(data)
    t2 = time.time()

    print(data)

    delta = t2 - t1

    # Make sure that the next loop fetches data after a cooldown period
    # If the update process takes more than the cooldown period, there is no
    # reason to wait any longer
    if delta < COOLDOWN:
        time.sleep(COOLDOWN - delta)
