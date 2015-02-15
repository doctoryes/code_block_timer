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

import functools
import threading
from timeit import default_timer

import storage


class Globals(threading.local):
    # Current module-level nest stack.
    # As CodeBlockTimer objects are __enter__ed, their descriptions are pushed
    # onto this stack. The stack length indicates the current nesting level.
    nest_stack = []

    # Current run_id.
    # Set from data storage when stack size increases from 0.
    # While nest stack is populated, remains at a constant value.
    # Identifies all the times from the same run.
    run_id = None


_m = Globals()


class CodeBlockTimer(object):
    def __init__(self, block_desc, **kwargs):
        self.block_desc = block_desc
        self.verbose = False if 'verbose' not in kwargs else kwargs['verbose']
        self.timer = default_timer
        self.data_store = storage.TimingDataStorage(**kwargs)

    def __enter__(self):
        if len(_m.nest_stack) == 0:
            _m.run_id = self.data_store.run_id()
        _m.nest_stack.append(self.block_desc)
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        # Compute elapsed times.
        end = self.timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs * 1000  # millisecs

        # Store the timings.
        nested_desc = ":".join(_m.nest_stack)
        self.data_store.store(_m.run_id, nested_desc, self.elapsed)

        # Pop the stack.
        _m.nest_stack.pop()
        if len(_m.nest_stack) == 0:
            _m.run_id = None
        if self.verbose:
            print '{}: elapsed time: {} ms'.format(
                self.block_desc, self.elapsed
            )


def code_block_timer(block_desc, **cbt_kwargs):
    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with CodeBlockTimer(block_desc, **cbt_kwargs):
                return func(*args, **kwargs)
        return inner
    return outer
