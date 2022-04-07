import configparser
import json
import time

import requests

class EmonIO:
    """EmonPi handler class used to fetch data using REST API."""

    def __init__(self, config_file: str, *, schema_file: str=""):

        # Load configuration file
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(config_file)
        self.config_file = config_file
        self.endpoint = cfg["Emon"]["endpoint"]
        self.credentials = cfg["Emon"]["bearer_credentials"]
        self.headers =  {"Authorization":f"Bearer {self.credentials}"}

        if schema_file:
            with open(schema_file, "r", encoding="utf8") as f_in:
                self.schema = json.load(f_in)

    def _test(self):
        """Checks if connection with given credentials can be established.
        Returns False if request status returns something other than OK.
        """

        try:
            res = requests.get(f"{self.endpoint}/feed/list.json", data={"id":1}, headers=self.headers)
        except Exception as e:
            print(e)
            return False

        return res.ok

    def _get_feed_list(self) -> dict:
        """Fetches the feed list from server.
        Returns the feed list in json format. If something goes wrong, an empty
        dictionary is being returned.
        """

        url = f"{self.endpoint}/feed/list.json"

        res = requests.get(url, headers=self.headers)

        feed_list = {}

        if res.ok:
            feed_list = res.json()

        return feed_list

    def fetch_data(self) -> dict:
        """Fetches only the specified data from server adding an accurate fetch-
        timestamp.
        Returns the json-like object containing the desired data in the specified
        schema. If something goes wrong, an empty dictionary is being returned.
        """

        feeds = self._get_feed_list()

        # Filter data according to provided schema
        data = {name:feeds[int(id)]["value"] for id, name in self.schema.items()}

        # Add a timestamp
        data["timestamp"] = time.time()

        return data

if __name__ == "__main__":
    CONFIG_FILE = "../data/dev.cfg"
    SCHEMA_FILE = "../data/schema.json"
    emonio = EmonIO(CONFIG_FILE, schema_file=SCHEMA_FILE)

    if emonio._test():
        print("General testing: ok")
    else:
        print("General testing: ko")

    data = emonio.fetch_data()

    if data:
        print(data)
    else:
        print("Something went wrong while fetching data")
