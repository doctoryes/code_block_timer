
from timeit import default_timer

class CodeBlockTimer(object):
    def __init__(self, block_desc, verbose=False):
        self.block_desc = block_desc
        self.verbose = verbose
        self.timer = default_timer

    def __enter__(self):
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        end = self.timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs * 1000  # millisecs
        if self.verbose:
            print '{}: elapsed time: {} ms'.format(self.block_desc, self.elapsed)

