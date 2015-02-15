Python module which times Python code blocks.

Features
--------
* Nesting of timers - higher level timers continue to tick during lower-level timers starting/stopping.
* Timing storage in a SQLite DB.
* Can be used as a decorator -or- a context manager.

Usage
-----
As a context manager:
```python
from code_block_timer import CodeBlockTimer

for __ in xrange(2):
    with CodeBlockTimer("all blocks"):
        performSetUp()

        with CodeBlockTimer("block1"):
            perform_lengthy_task()

        with CodeBlockTimer("block2"):
            perform_another_lengthy_task()

```
In the SQLite DB, you'll now see six rows, similar to these:
```
1|1|all blocks:block1|4003.94415855408|2015-02-15 18:30:32
2|1|all blocks:block2|5003.18717956543|2015-02-15 18:30:37
3|1|all blocks|11016.9990062714|2015-02-15 18:30:37
4|2|all blocks:block1|4003.73291969299|2015-02-15 18:30:43
5|2|all blocks:block2|5003.61299514771|2015-02-15 18:30:48
6|2|all blocks|11017.0860290527|2015-02-15 18:30:48
```
---
As a decorator:
```python
from code_block_timer import CodeBlockTimer

@CodeBlockTimer('method2')
def perform_another_lengthy_task():
    # Do several things.
    pass

@CodeBlockTimer('method1')
def perform_lengthy_task():
    # Do several things.
    perform_another_lengthy_task()

for __ in xrange(2):
    perform_lengthy_task()

```
In the SQLite DB, you'll now see four rows, similar to these:
```
1|1|method1:method2|2000.66590309143|2015-02-15 18:38:40
2|1|method1|3005.31411170959|2015-02-15 18:38:40
3|2|method1:method2|2001.1157989502|2015-02-15 18:38:43
4|2|method1|3003.61204147339|2015-02-15 18:38:43
```
