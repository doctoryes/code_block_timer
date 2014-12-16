
from timeit import default_timer

from .storage import TimingDataStorage

class Globals(object):
    pass

__m = Globals()
__m.nest_level = 0


class CodeBlockTimer(object):
    def __init__(self, block_desc, verbose=False):
        self.block_desc = block_desc
        self.verbose = verbose
        self.timer = default_timer
        self.data_store = TimingDataStorage()
        self.run_id = None

    def __enter__(self):
        if __m.nest_level == 0:
            self.run_id = self.data_store.run_id()
        __m.nest_level += 1
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        end = self.timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs * 1000  # millisecs
        self.data_store.store(self.run_id, self.block_desc, self.elapsed)
        __m.nest_level -= 1
        if __m.nest_level == 0:
            self.run_id = None
        if self.verbose:
            print '{}: elapsed time: {} ms'.format(self.block_desc, self.elapsed)

