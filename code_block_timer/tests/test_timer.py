
import os
import unittest
import random
import math
import sqlite3
import ddt
from code_block_timer import CodeBlockTimer, _m


@ddt.ddt
class TestCodeBlockTimer(unittest.TestCase):
    """
    Tests for CodeBlockTimer.
    """
    def setUp(self):
        super(TestCodeBlockTimer, self).setUp()
        self.db_name = "tmp_db_{}".format(random.randint(100000, 999999))

    def _verifyEvents(self, run_id, event_names):
        """
        Verify that the run identified by the run_id has the events identified by the event_names.
        """
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        for event in event_names:
            cur.execute("select count(*) from block_times where run_id=? and block_desc=?", (run_id, event))
            self.assertEquals(cur.fetchone()[0], 1)

    def test_stuff(self):
        iterations = ['iter0', 'iter1', 'iter2', 'iter3']
        with CodeBlockTimer("test", db_name=self.db_name) as timer:
            run_id = _m.run_id
            for i, iter_name in enumerate(iterations):
                with CodeBlockTimer(iter_name, db_name=self.db_name) as inner:
                    z = math.factorial(10)
        self._verifyEvents(run_id, ['test', ] + ["test:{}".format(x) for x in iterations])

    def test_exception_handled(self):
        msg = "exception_but_still_timed"
        try:
            with CodeBlockTimer(msg, db_name=self.db_name) as __:
                run_id = _m.run_id
                z = math.factorial(10)
                raise Exception
        except Exception:
            pass
        self._verifyEvents(run_id, [msg])

    def test_default_delimiter(self):
        with CodeBlockTimer("test", db_name=self.db_name) as timer:
            run_id = _m.run_id
            with CodeBlockTimer("delimiter", db_name=self.db_name) as inner:
                z = math.factorial(10)
        self._verifyEvents(run_id, ['test', 'test:delimiter'])

    @ddt.data(':::::', '%', '-', '/')
    def test_delimiters(self, delimiter):
        with CodeBlockTimer("test", delimiter=delimiter, db_name=self.db_name) as timer:
            run_id = _m.run_id
            with CodeBlockTimer("delimiter", delimiter=delimiter, db_name=self.db_name) as inner:
                z = math.factorial(10)
        self._verifyEvents(run_id, ['test', 'test{}delimiter'.format(delimiter)])

    def tearDown(self):
        # Destroy the sqlite DB.
        os.remove(self.db_name)

if __name__ == '__main__':
    unittest.main()
