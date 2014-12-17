
import sqlite3
import os

# Assumes that the DB exists and the schema in schema.sql exists in it.


class TimingDataStorage(object):

    SCHEMA_NAME = "code_block_timer/code_block_timer/schema.sql"
    DEFAULT_DB_NAME = 'block_times.db'

    def __init__(self, **kwargs):
        # Verify that the sqlite DB and schema exists.
        db_name = self.DEFAULT_DB_NAME
        if 'db_name' in kwargs:
            db_name = kwargs['db_name']
        if not os.path.exists(db_name):
            self._createDB(db_name)
        self.conn = sqlite3.connect(db_name)

    def _createDB(self, db_name):
        # Create the sqlite DB file.
        with open(db_name, "w") as f:
            conn = sqlite3.connect(db_name)
            with open(self.SCHEMA_NAME, "r") as schema_file:
                schema = schema_file.read()
                cur = conn.cursor()
                conn.executescript(schema)
                conn.commit()

    def run_id(self, desc=""):
        """
        Creates a new run ID and returns it.
        A single run ID can be used for multiple store()s for times in the same test.
        """
        cur = self.conn.cursor()
        cur.execute('insert into test_run (run_desc) values (?)', (desc,))
        self.conn.commit()
        cur.execute('select max(id) from test_run')
        return cur.fetchone()[0]

    def store(self, run_id, desc, elapsed):
        """
        Store the description and elapsed time in the DB, under the passed-in run_id.
        """
        cur = self.conn.cursor()
        cur.execute(
            'insert into block_times (run_id, block_desc, elapsed)'
            'values (?, ?, ?)', (run_id, desc, elapsed)
        )
        self.conn.commit()
