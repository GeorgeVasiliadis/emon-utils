"""Module intened to be run as an integrated app entry"""

import time
from datetime import datetime

from . import CONFIG_FILE
from . import SCHEMA_FILE

from .DBIO import DBIO
from .EmonIO import EmonIO

class Reporter:
    """Class used to implement the fetch-update-send cycle, as long as other
    important integration utilities.
    """

    def __init__(self, cooldown, *, log_to_screen=False):
        self.cooldown = cooldown
        self.log_to_screen = log_to_screen
        self.emonio = EmonIO(CONFIG_FILE, schema_file=SCHEMA_FILE)
        self.dbio = DBIO(CONFIG_FILE)
        self.current_document_id = None
        self.current_date = None

    def _create_new_document(self, date: str) -> str:
        """Create a new document containing the specified date and return the
        id of the created document.
        If something goes wrong, an empty string will be returned.

        date -- A string represantation of the document to be created.
        """
        document_id = self.dbio.create_document(initial_data={"date": date})
        return document_id

    def _handle_date_change(self):
        """If the date has changed since the last check, this means that either a
        new document must be created (usual case) or another document must be
        appended and not recreated (rare case, occurs in development).

        This function keeps
            - self.current_document_id
            - self.current_date
        up to date according to the current date.
        """

        temp = datetime.now()
        date = temp.strftime("%Y-%m-%d")

        if date != self.current_date:
            if self.log_to_screen:
                print("Changed date")
            document_id = self.dbio.get_document_id_for_date(date)
            if not document_id:
                document_id =  self._create_new_document(date)

            self.current_document_id = document_id
            self.current_date = date

    def _loop_cycle(self):
        """This function implements the fundamental fetch-update-send loop.
        As a *side effect*, it checks whether the date has changed and updates
        the document_id as needed.
        """

        self._handle_date_change()
        data = self.emonio.fetch_data()
        status = self.dbio.append_energy_data(data, document=self.current_document_id)

        if self.log_to_screen:
            print(self.current_document_id)
            print(self.current_date)
            print(data)
            print(f"Uploaded: {status}")

    def run(self):
        """Infinite execution of fetch-update-send cycle.
        Additionally, this method controls the cooldown system.

        If the fetch-update-send cycle takes less than a specified amount of
        time, this function will sleep as long as it is needed to prevent
        sending invalid (duplicate) measurements to database.
        """

        while True:
            t_1 = time.time()
            self._loop_cycle()
            t_2 = time.time()

            delta = t_2 - t_1

            if delta < self.cooldown:
                time.sleep(self.cooldown - delta)

reporter = Reporter(5, log_to_screen=True)
reporter.run()
