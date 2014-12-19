Python module which times Python code blocks.

Features
--------
* Nesting of timers - higher level timers continue to tick during lower-level timers starting/stopping.
* Timing storage in a SQLite DB.

Usage
-----
```
from code_block_timer import CodeBlockTimer

for i in xrange(0, 2):
    with CodeBlockTimer("all blocks"):
        performSetUp()

        with CodeBlockTimer("block1"):
            perform_lengthy_task()

        with CodeBlockTimer("block2"):
            perform_another_lengthy_task()

```
In the SQLite DB, you'll now see six rows, similar to these:
```
1|1|all blocks:block1|201.16|2014-10-12 12:26:01
2|1|all blocks:block2|516.492|2014-10-12 12:26:01
3|1|all blocks|916.54|2014-10-12 12:26:01
4|2|all blocks:block1|199.16|2014-10-12 12:26:04
5|2|all blocks:block2|505.142|2014-10-12 12:26:04
6|2|all blocks|903.212|2014-10-12 12:26:04
```

