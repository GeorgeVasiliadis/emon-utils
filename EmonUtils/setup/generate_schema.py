import json

from ..EmonIO import emonio

def generate_schema(CONFIG_FILE, SCHEMA_FILE):
    emon = emonio.EmonIO(CONFIG_FILE)
    list_ = emon._get_feed_list()

    print("Listing available feeds:\n")

    map_ = {}

    for position_id, feed in enumerate(list_):
        name = feed["name"]
        print(f"#{feed['id']} {name}: {feed['value']}")
        ans = input(f"Rename {name} to: ")
        if ans:
            name = ans
        map_[position_id] = name
        print("---")

    with open(SCHEMA_FILE, "w", encoding="utf8") as f_out:
        json.dump(map_, f_out)

    print(f"File was generated successfully at: {SCHEMA_FILE}!")
