
from timeit import default_timer
from .storage import TimingDataStorage


class Globals(object):
    pass

_m = Globals()

# Current module-level nest stack.
# As CodeBlockTimer objects are __enter__ed, their descriptions are pushed
# onto this stack. The stack length indicates the current nesting level.
_m.nest_stack = []

# Current run_id.
# Set from data storage when stack size increases from 0.
# While nest stack is populated, remains at a constant value.
# Identifies all the times from the same run.
_m.run_id = None


class CodeBlockTimer(object):
    def __init__(self, block_desc, **kwargs):
        self.block_desc = block_desc
        self.verbose = False if 'verbose' not in kwargs else kwargs['verbose']
        self.timer = default_timer
        self.data_store = TimingDataStorage(**kwargs)

    def __enter__(self):
        global _m
        if len(_m.nest_stack) == 0:
            _m.run_id = self.data_store.run_id()
        _m.nest_stack.append(self.block_desc)
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        global _m

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
