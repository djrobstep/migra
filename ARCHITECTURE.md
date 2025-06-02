# Architecture

`migra` heavily depends on `schemainspect`, so please read the [Schema Inspect Architecture](https://github.com/PhilipWee/schemainspect/blob/master/README.md) first before continuing

## Overview

Essentially, what migra does is:
1. Run `schemainspect` on DB A
2. Run `schemainspect` on DB B
3. Find the differences between B and A
4. From `schemainspect`, get the necessary `create`, `drop` and `alter` statements, to get from B to A, recreating any dependencies as well

## Main class

The main class in this repo is `migra.py` and the function `add_all_changes` does most of the heavy lifting

The order of `add_all_changes` also affects the order of SQL statements generated


## Other important information

`differences` in `util.py` does alot of work to check what has been changed between DB A and DB B

`changes.py` is also an important file that creates the dependency graph in order to update dependencies in the right order