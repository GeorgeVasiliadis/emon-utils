"""Database-related communication module"""

import configparser
import json
from typing import Any

import requests

class DBIO:
    """ChouchDB handler class used to exchange data using REST API."""

    def __init__(self, config_file: str):

        # Load configuration file
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(config_file)

        self.endpoint = cfg["DB"]["endpoint"]
        self.db = cfg["DB"]["db_name"]
        self.document = cfg["DB"]["document_name"]
        self.username = cfg["DB"]["username"]
        self.password = cfg["DB"]["password"]
        self.base_url = f"{self.endpoint}"

    def _test(self) -> bool:
        """Checks if connection with given credentials can be established.
        Returns False if request status returns something other than OK.
        """

        try:
            res = requests.get(self.base_url, auth=(self.username, self.password))
        except Exception as e:
            print(e)
            return False

        return res.ok

    def _fetch_document(self, *, document: str=None) -> dict:
        """Fetches the default document.
        Returns its content in json-format. If operation is unsuccessful, an
        empty dict is being returned.

        document -- The document to be fetched. It is usually ommitted as the
                    default document is being implied, but an arbitrary document
                    can be specified as well.

        Throws:
        AssertionError -- If no document can be found.
        """

        if not document:
            document = self.document

        assert document, "No document was supplied!"

        res = requests.get(f"{self.base_url}/{self.db}/{document}",
            auth=(self.username, self.password)
        )

        data = {}

        if res.ok:
            data = res.json()

        return data

    def _update_document(self, data: dict, *, document=None) -> bool:
        """Updates the default document with the given data. This is equivalent
        to overwriting the stored data. Use with caution!
        Returns True if the document was updated successfully.

        data -- The data that will be used to update the specified document.
                data should be json-serializable. If ommitted, an empty json
                object will be passed instead which will be equivalent to
                dropping the whole document.
        document -- The document to be updated. It is usually ommitted as the
                    default document is being implied, but an arbitrary document
                    can be specified as well.

        Throws:
        AssertionError -- If no document can be found.
        """

        if not document:
            document = self.document

        assert document, "No document was supplied!"

        if not data:
            data = {}

        res = requests.put(f"{self.base_url}/{self.db}/{document}",
            data=json.dumps(data),
            auth=(self.username, self.password)
        )

        return res.ok

    def create_document(self, name: str=None, *, initial_data: dict=None) -> str:
        """Creates a new document named `name`, intialized with `initial_data` json
        object.
        Returns the name of the document if creation was successful, and an empty
        string otherwise.

        name -- The name of the document to be created. If ommitted, a new UUID
        will be auto-generated and assigned.
        initial_data -- The initial data that will be contained in the created document.
        initial_data should be json-serializable. If ommitted, an empty json
        object will be passed instead.
        """

        # If no name is provided, generate a new UUID on the fly
        if not name:
            res = requests.get(f"{self.base_url}/_uuids")
            name = res.json()["uuids"][0]

        # Empty bodied requests cannot create new CouchDB Documents.
        # Make sure no empty data are sent.
        if not initial_data:
            initial_data = {}

        res = requests.put(f"{self.base_url}/{self.db}/{name}",
            auth=(self.username, self.password),
            data=json.dumps(initial_data)
        )

        if not res.ok:
            name = ""

        return name

    def append_energy_data(self, energy_data: Any, *, document=None) -> bool:
        """Accepts a measurement object and appends it to the energy_data list
        of specified document.
        """

        old_data = self._fetch_document(document=document)

        if "energy_data" not in old_data:
            old_data["energy_data"] = []

        old_data["energy_data"].append(energy_data)
        new_data = old_data

        return self._update_document(new_data, document=document)

    def get_document_id_for_date(self, date: str) -> str:
        """Returns the id of the document that matches the given date. If there
        is no such information available on the database, there are no
        appropriate views defined, or there is just no such matching date, an
        empty string will be returned.
        """

        res = requests.get(f"{self.base_url}/{self.db}/_design/api/_view/get_dates",
            auth=(self.username, self.password)
        )

        data = {}
        if res.ok:
            data = res.json()

        rows = []
        if "rows" in data:
            rows = data["rows"]

        document_id = ""
        for row in rows:
            if row["key"] == date:
                document_id = row["value"]
                break

        return document_id

# Test Section
if __name__ == "__main__":
    CONFIG_FILE = "../data/dev.cfg"
    dbio = DBIO(CONFIG_FILE)
    #
    # if dbio._test():
    #     print("General test: ok")
    # else:
    #     print("General test: ko")
    #
    # name = dbio.create_document(initial_data={"hello": "world"})
    # if name:
    #     ("A random document was created successfully")
    # else:
    #     print("Could not create the desired document")
    #
    # data = dbio._fetch_document(document=name)
    #
    # if data:
    #     print(data)
    # else:
    #     print("Could not fetch data")

    data = dbio.get_document_id_for_date("2022-04-06")
