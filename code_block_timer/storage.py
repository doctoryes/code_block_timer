
import sqlite3

# Assumes that the DB exists and the schema in schema.sql exists in it.

class TimingDataStorage(object):

    DB_NAME = 'block_times.db'

    def __init__(self):
        # Verify that the sqlite DB and schema exists.
        self.conn = sqlite3.connect(self.DB_NAME)

    def run_id(self, desc):
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
        cur.execute('insert into block_times (run_id, block_desc, elapsed) values (?, ?, ?)', (run_id, desc, elapsed))
        self.conn.commit()

