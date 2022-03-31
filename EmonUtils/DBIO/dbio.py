"""Database-related communication module"""

import configparser
import json

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

    def create_document(self, name: str=None, *, data: dict=None) -> str:
        """Creates a new document named `name`, intialized with `data` json
        object.
        Returns the name of the document if creation was successful, and an empty
        string otherwise.

        name -- The name of the document to be created. If ommitted, a new UUID
                will be auto-generated and assigned.
        data -- The initial data that will be contained in the created document.
                data should be json-serializable. If ommitted, an empty json
                object will be passed instead.
        """

        # If no name is provided, generate a new UUID on the fly
        if not name:
            res = requests.get(f"{self.base_url}/_uuids")
            name = res.json()["uuids"][0]

        # Empty bodied requests cannot create new CouchDB Documents.
        # Make sure no empty data are sent.
        if not data:
            data = {}

        res = requests.put(f"{self.base_url}/{self.db}/{name}",
            auth=(self.username, self.password),
            data=json.dumps(data)
        )

        if not res.ok:
            name = ""

        return name

    def fetch_document(self, *, document: str=None) -> dict:
        """Fetches the default document.
        Returns its content in json-format. If operation is unsuccessful, an
        empty dict is being returned.

        document -- The document to be fetched. It is usually ommitted as the
                    default document is being implied, but an arbitrary document
                    can be specified as well.

        Throws:
        AssertionError -- If no document can be found.
        """

        if not document: document = self.document

        assert document, "No document was supplied!"

        res = requests.get(f"{self.base_url}/{self.db}/{document}",
            auth=(self.username, self.password)
        )

        data = {}

        if res.ok:
            data = res.json()

        return data

    def update_document(self, data: dict, *, document=None) -> bool:
        """Updates the default document with the given data.
        Returns True if the document was updated successfully.

        data -- The data that will be used to update the specified document.
                data should be json-serializable. If ommitted, an empty json
                object will be passed instead.
        document -- The document to be updated. It is usually ommitted as the
                    default document is being implied, but an arbitrary document
                    can be specified as well.

        Throws:
        AssertionError -- If no document can be found.
        """

        if not document:
            document = self.document

        assert document, "No document was supplied!"

        old_data = self.fetch_document()
        old_data["energy_data"].append(data)
        data = old_data

        res = requests.put(f"{self.base_url}/{self.db}/{document}",
            data=json.dumps(data),
            auth=(self.username, self.password)
        )

        return res.ok

# Test Section
if __name__ == "__main__":
    CONFIG_FILE = "../data/dev.cfg"
    dbio = DBIO(CONFIG_FILE)

    if dbio._test():
        print("General test: ok")
    else:
        print("General test: ko")

    name = dbio.create_document(data={"hello": "world"})
    if name:
        ("A random document was created successfully")
    else:
        print("Could not create the desired document")

    data = dbio.fetch_document(document=name)

    if data:
        print(data)
    else:
        print("Could not fetch data")
