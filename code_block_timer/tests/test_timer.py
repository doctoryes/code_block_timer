
import mock
import os
import unittest
import random
import math
import sqlite3
from code_block_timer import CodeBlockTimer, code_block_timer, _m
import ddt


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

    @mock.patch('code_block_timer.storage.TimingDataStorage')
    def test_decorator(self, mock_class):

        store = mock.Mock()
        mock_class.return_value = store
        store.run_id.return_value = 45

        @code_block_timer('decorator_test', db_name=self.db_name)
        def wrapped_thing(*args, **kwargs):
            self.assertEquals(args, ('an_arg',))
            self.assertEquals(kwargs, {'a_dict': {}})
            kwargs['a_dict'].update(entered=True)

        test_dict = {}
        run_id = wrapped_thing('an_arg', a_dict=test_dict)
        mock_class.assert_called_once_with(db_name=self.db_name)
        self.assertTrue(test_dict['entered'])
        store.store.assert_called_with(45, 'decorator_test', mock.ANY)

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
        try:
            # Destroy the sqlite DB.
            os.remove(self.db_name)
        except:
            pass

if __name__ == '__main__':
    unittest.main()
