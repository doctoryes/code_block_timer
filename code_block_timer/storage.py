# Copyright 2014 John Eskew

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sqlite3
from path import path


MODULE_DIR = path(__file__).dirname()


class TimingDataStorage(object):

    SCHEMA_NAME = 'schema.sql'
    SCHEMA_PATH = MODULE_DIR / self.SCHEMA_NAME
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
            with open(self.SCHEMA_PATH, "r") as schema_file:
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
