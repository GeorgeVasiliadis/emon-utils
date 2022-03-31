import json

from ..DBIO import dbio
from ..EmonIO import emonio

def generate_schema(CONFIG_FILE, SCHEMA_FILE):
    emon = emonio.EmonIO(CONFIG_FILE)
    list = emon._get_feed_list()

    print("Listing available feeds:\n")

    map = {}

    for position_id, feed in enumerate(list):
        name = feed["name"]
        print(f"#{feed['id']} {name}: {feed['value']}")
        ans = input(f"Rename {name} to: ")
        if ans: name = ans
        map[position_id] = name
        print("---")

    with open(SCHEMA_FILE, "w") as f_out:
        json.dump(map, f_out)

    print(f"File was generated successfully at: {SCHEMA_FILE}!")
