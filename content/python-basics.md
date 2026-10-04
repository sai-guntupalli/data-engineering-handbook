## [Main title](../README.md)
### [Interview questions](full.md)

# Python Basics for Data Engineers

**Notebook:** [`notebooks/topics/python-basics.ipynb`](../notebooks/topics/python-basics.ipynb) - runnable version of this topic with self-checking exercises.

The language fundamentals data engineering interviews assume: typing, collections, functions and scope, classes and methods, protocols, exceptions, generators, decorators, typing, time, file I/O, concurrency, and packaging. This is the Python language itself, not pipeline architecture or coding puzzles.

+ [How do values, variables, and dynamic typing work in Python?](#How-do-values-variables-and-dynamic-typing-work-in-Python)
+ [How do numbers and strings work in Python?](#How-do-numbers-and-strings-work-in-Python)
+ [What are the core collections: lists, tuples, sets, and dicts?](#What-are-the-core-collections-lists-tuples-sets-and-dicts)
+ [How do comprehensions work in Python?](#How-do-comprehensions-work-in-Python)
+ [What is the difference between mutability, references, copy, and deepcopy?](#What-is-the-difference-between-mutability-references-copy-and-deepcopy)
+ [How does control flow work in Python?](#How-does-control-flow-work-in-Python)
+ [How do functions, arguments, scope, and closures work?](#How-do-functions-arguments-scope-and-closures-work)
+ [How do modules, packages, and the main guard work?](#How-do-modules-packages-and-the-main-guard-work)
+ [How do classes, objects, and methods work?](#How-do-classes-objects-and-methods-work)
+ [How do inheritance, super, polymorphism, and MRO work?](#How-do-inheritance-super-polymorphism-and-MRO-work)
+ [What are the most important dunder methods?](#What-are-the-most-important-dunder-methods)
+ [How do properties and encapsulation work?](#How-do-properties-and-encapsulation-work)
+ [How do dataclasses, NamedTuple, and enums work?](#How-do-dataclasses-NamedTuple-and-enums-work)
+ [How do exceptions and context managers work?](#How-do-exceptions-and-context-managers-work)
+ [How do iterators and generators work in Python?](#How-do-iterators-and-generators-work-in-Python)
+ [How do decorators work in Python?](#How-do-decorators-work-in-Python)
+ [What functional tools does Python provide?](#What-functional-tools-does-Python-provide)
+ [How do type hints and mypy work?](#How-do-type-hints-and-mypy-work)
+ [How do datetime and time zones work in Python?](#How-do-datetime-and-time-zones-work-in-Python)
+ [How do file I/O, pathlib, JSON, and CSV work?](#How-do-file-IO-pathlib-JSON-and-CSV-work)
+ [How do the GIL, threads, processes, and asyncio compare?](#How-do-the-GIL-threads-processes-and-asyncio-compare)
+ [How do virtual environments, pip, uv, pyproject, and pytest work?](#How-do-virtual-environments-pip-uv-pyproject-and-pytest-work)
+ [What are the most common Python pitfalls?](#What-are-the-most-common-Python-pitfalls)
+ [Real world use cases for Python basics in data engineering](#Real-world-use-cases-for-Python-basics-in-data-engineering)

## How do values, variables, and dynamic typing work in Python?

A variable is a **name bound to an object**: the object carries the type, names can be rebound at any time, and annotations are read by tools rather than enforced at runtime. `type()` gives the exact class, `isinstance()` also accepts subclasses, and `is` compares identity while `==` compares value.

```python
count = 3            # int
count = "three"      # rebinding to another type is legal
rate: float = 0.75   # annotation only: no runtime check

for value in (count, rate, [1, 2], None):
    print(f"{value!r:>8} -> {type(value).__name__}")
```

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do numbers and strings work in Python?

`int` is arbitrary precision and `float` is IEEE-754 binary, so `0.1 + 0.2 != 0.3`; exact money belongs in `Decimal` or integer cents. Strings are immutable Unicode sequences: slicing is `[start:stop:step]`, f-strings are the default formatting tool, and `bytes` is the type for raw payloads.

```python
from decimal import Decimal

print(7 / 2, 7 // 2, 2**10, divmod(7, 2))
print(0.1 + 0.2, Decimal("0.1") + Decimal("0.2"))

order_id = "ORD-2026-000123"
region, year, seq = order_id.split("-")
print(f"{region=} {seq:0>8} {int(seq):,} {0.4217:.2%}")
print(order_id[:3], order_id[-6:], order_id[::-1], "a,b,c".replace(",", "|"))
```

Always pass `encoding="utf-8"` when crossing the text/binary boundary; mixing the two raises `TypeError` instead of silently producing mojibake.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What are the core collections: lists, tuples, sets, and dicts?

The built-ins are **list** (ordered, mutable), **tuple** (ordered, immutable, hashable), **set** (unique, O(1) membership), and **dict** (key-value, insertion-ordered since 3.7). `Counter` and `defaultdict` remove most manual "if key not present" branching.

```python
from collections import Counter, defaultdict

rows = [("us", 12), ("eu", 7), ("us", 5)]
by_region: dict[str, list[int]] = defaultdict(list)
for name, amount in rows:
    by_region[name].append(amount)

print(dict(by_region), Counter(name for name, _ in rows).most_common(1))
print({"id", "ts"} & {"id", "to"}, {"id", "ts"} - {"id", "to"})
print({**{"id": 1}, "amount": 2}, "amount" in {"amount": 2})
```

Methods that mutate in place (`append`, `sort`, `update`) return `None`, so `sorted(x)` gives a new list while `x.sort()` returns nothing. Sets cannot hold lists or dicts because those are unhashable.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do comprehensions work in Python?

A comprehension builds a list, set, dict, or generator from an iterable in one expression. It replaces an append loop for simple mappings and filters; nesting beyond two clauses, or hiding side effects inside it, is where reviewers object. A generator expression is lazy, which makes `sum(...)` and `any(...)` streaming-friendly.

```python
rows = [{"id": 1, "amount": 10}, {"id": 2, "amount": 0}, {"id": 3, "amount": 25}]

ids = [row["id"] for row in rows]
paid = [row["amount"] for row in rows if row["amount"] > 0]
lookup = {row["id"]: row["amount"] for row in rows}
unique = {row["amount"] for row in rows}
flat = [item for batch in [[1, 2], [3]] for item in batch]   # order matters
total = sum(row["amount"] for row in rows)

print(ids, paid, lookup, sorted(unique), flat, total)
```

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What is the difference between mutability, references, copy, and deepcopy?

Assignment never copies: `b = a` binds a second name to the same object, so mutable objects change through either name. `copy.copy` duplicates only the outer container, while `copy.deepcopy` recursively duplicates everything reachable. Functions receive references too: mutating an argument is visible to the caller, rebinding it is not.

```python
import copy

config = {"source": "s3", "options": {"retries": 3}}
alias, shallow = config, copy.copy(config)
deep = copy.deepcopy(config)

alias["source"] = "gcs"
shallow["options"]["retries"] = 99       # nested dict is still shared
print(config["source"], config["options"]["retries"], deep["options"]["retries"])

def mutate(items: list[int]) -> None:
    items.append(0)                      # visible; rebinding would not be

data = [1, 2]
mutate(data)
print(data)
```

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How does control flow work in Python?

Control flow is `if`/`elif`/`else`, `for` over any iterable, `while`, and a loop `else` that runs only when the loop was not left by `break`. Truthiness is explicit — empty containers, `0`, `""`, `None`, and `False` are falsy — and `match` (3.10+) adds structural pattern matching with guards.

```python
def classify(status: str, attempts: int) -> str:
    match status:
        case "retry" if attempts < 3:
            return "backoff"
        case "retry":
            return "dead-letter"
        case _:
            return "unknown"

for part in ["2026-10-01", "2026-10-02"]:
    if part == "2026-10-02":
        print("found", part)
        break
else:
    print("missing")

attempt = completed = 0
while completed < 3:
    attempt += 1
    if attempt % 2 == 0:
        continue
    completed += 1
print(classify("retry", 1), classify("retry", 5), attempt, completed)
```

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do functions, arguments, scope, and closures work?

A signature is an interface: positional parameters, defaults, `*args` for extra positionals, `**kwargs` for extra keywords, and keyword-only parameters placed after `*`. Defaults are evaluated **once, at definition time**, which is why mutable defaults are a classic bug. Name resolution follows **LEGB** (Local, Enclosing, Global, Built-in); rebinding an enclosing name needs `nonlocal`, and a closure captures the names it reads.

```python
def load(*path_parts: str, mode: str = "batch", **options: object) -> dict:
    return {"path": "/".join(path_parts), "mode": mode, "options": options}

def make_counter(start: int = 0):
    count = start
    def increment(step: int = 1) -> int:
        nonlocal count          # rebind, not shadow, the enclosing name
        count += step
        return count
    return increment

counter = make_counter(10)
print(load("s3://b", "part", mode="stream", compression="zstd"))
print(counter(), counter(5), counter(), sorted((3, 1, 2)))
```

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do modules, packages, and the main guard work?

A module is a `.py` file; a package is a directory with an `__init__.py` (or a namespace package) grouping modules. `import x` binds the module, `from x import y` binds an attribute, and imports execute top-level code once per process, cached in `sys.modules`. The main guard keeps that code out of test imports.

```python
# file: jobs/parsers.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Order:
    order_id: str
    amount: float

def parse(raw: dict) -> Order:
    return Order(order_id=raw["id"], amount=float(raw["amount"]))
```

```python
# file: jobs/run.py
from parsers import Order, parse      # sibling module, or an installed package

def main() -> int:
    order: Order = parse({"id": "A1", "amount": "10.5"})
    print(f"parsed {order.order_id} for {order.amount:.2f}")
    return 0

if __name__ == "__main__":            # true when run directly, false when imported
    raise SystemExit(main())
```

Prefer absolute imports (`from jobs.parsers import parse`) inside packages, keep `__init__.py` free of heavy work, and never mutate `sys.path` from library code.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do classes, objects, and methods work?

A class is a factory for objects and a namespace for shared behavior. `__init__` receives the new instance as `self` and assigns instance attributes; class attributes live on the class and are shared. An **instance method** takes `self`, a **classmethod** takes `cls` and is the idiomatic alternative constructor, and a **staticmethod** takes neither.

```python
class Extractor:
    kind = "http"                     # class attribute: shared by all instances
    def __init__(self, url: str, page_size: int = 100) -> None:
        self.url = url                # instance attributes: one per object
        self.page_size = page_size
    def fetch(self, page: int) -> dict:            # instance method
        return {"page": page, "url": self.url, "size": self.page_size}
    @classmethod
    def from_env(cls, url: str) -> "Extractor":    # alternative constructor
        return cls(url, page_size=50)
    @staticmethod
    def is_partition_column(column: str) -> bool:  # no implicit argument
        return column.startswith("dt")

extractor = Extractor.from_env("https://api.example.com/orders")
print(extractor.fetch(1), extractor.kind, extractor.is_partition_column("dt=2026-10-04"))
```

`self` is only the conventional first parameter; Python never passes the receiver implicitly. Assigning `self.kind` would create an instance attribute that shadows the class attribute for that object alone.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do inheritance, super, polymorphism, and MRO work?

Inheritance expresses **is-a** and lets subclasses override methods; polymorphism means the same call gets each type's behavior. `super()` delegates to the next class in the **method resolution order (MRO)**, computed by C3 linearization: the subclass, then bases left to right, then shared ancestors, ending at `object`.

```python
class Sink:
    def __init__(self, path: str) -> None:
        self.path = path
    def write(self, rows: list[dict]) -> int:
        raise NotImplementedError
    def __repr__(self) -> str:
        return f"{type(self).__name__}(path={self.path!r})"

class ParquetSink(Sink):
    def __init__(self, path: str, compression: str = "zstd") -> None:
        super().__init__(path)              # cooperative base initialisation
        self.compression = compression
    def write(self, rows: list[dict]) -> int:
        return len(rows) * 2                # pretend each row is two bytes

class NullSink(Sink):
    def write(self, rows: list[dict]) -> int:
        return 0

for sink in (ParquetSink("s3://lake/orders"), NullSink("s3://lake/dev")):
    print(repr(sink), "->", sink.write([{}, {}]))
print([cls.__name__ for cls in ParquetSink.__mro__])
```

Prefer composition when the relationship is "has-a": a `Loader` holding an `S3Client` is easier to test than `Loader(S3Client)`. Use `Protocol` or abstract base classes for the contract.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What are the most important dunder methods?

Dunder methods let objects participate in Python syntax: `print()`, `len()`, `==`, `hash()`, `for`, indexing, calls, and `with` all dispatch to them. `__repr__` is for debugging, `__str__` is for people, and implementing `__eq__` without `__hash__` makes instances unhashable.

```python
class Batch:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows
    def __repr__(self) -> str:
        return f"Batch(rows={len(self._rows)})"
    def __str__(self) -> str:
        return f"batch of {len(self._rows)} rows"
    def __len__(self) -> int:
        return len(self._rows)
    def __iter__(self):
        return iter(self._rows)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return NotImplemented
        return self._rows == other._rows
    def __hash__(self) -> int:
        return hash(tuple(sorted(row["id"] for row in self._rows)))

batch = Batch([{"id": 1}, {"id": 2}])
print(batch, repr(batch), len(batch), batch == Batch([{"id": 1}, {"id": 2}]))
print(len({batch, Batch([{"id": 3}])}), list(batch) == batch._rows)
```

`__getitem__` powers indexing and slicing, `__call__` makes an instance callable, and `__enter__`/`__exit__` make it a context manager for the `with` statement.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do properties and encapsulation work?

Python has no enforced access control: `_name` means "internal by convention" and `__name` triggers name mangling. The real tool is `@property`, which makes a method call look like attribute access so writes can be validated and derived values computed lazily.

```python
class Snapshot:
    def __init__(self, rows: int) -> None:
        self._rows = 0
        self.rows = rows              # goes through the setter
    @property
    def rows(self) -> int:
        return self._rows
    @rows.setter
    def rows(self, value: int) -> None:
        if value < 0:
            raise ValueError("rows cannot be negative")
        self._rows = value
    @property
    def size_mb(self) -> float:       # computed, read-only
        return round(self._rows * 512 / 1_000_000, 3)

snapshot = Snapshot(2048)
print(snapshot.rows, snapshot.size_mb)
```

Start with plain attributes and add a property only when validation, lazy computation, or a refactoring shim requires it.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do dataclasses, NamedTuple, and enums work?

`@dataclass` generates `__init__`, `__repr__`, and `__eq__` from annotated fields; `frozen=True` makes instances immutable and hashable, while `field(default_factory=...)` is the correct mutable default. `NamedTuple` is the lighter tuple-based record that unpacks, and an `Enum` is a closed set of named constants with identity semantics.

```python
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import NamedTuple

class Stage(StrEnum):
    EXTRACT, LOAD = auto(), auto()      # value is the lower-case member name

@dataclass(frozen=True, slots=True)
class S3Location:
    bucket: str
    key: str
    region: str = "us-east-1"
    @property
    def uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"

class Row(NamedTuple):
    order_id: str
    amount: float

print(S3Location("lake", "raw.json").uri, Stage.LOAD.value)
print(Row("A1", 10.5) == Row("A1", 10.5), Row("A1", 10.5).amount)
```

Choose a dataclass when the object has behavior or validation, and a `NamedTuple` when it is a small immutable record that benefits from `order_id, amount = row`.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do exceptions and context managers work?

`try`/`except`/`else`/`finally` separates the happy path, recovery, and cleanup: `else` runs when the `try` suite leaves without an exception *and* without `return`/`break`/`continue`, and `finally` always runs. A context manager guarantees the same teardown: the class form implements `__enter__`/`__exit__`, and `@contextlib.contextmanager` derives it from a generator.

```python
from contextlib import contextmanager

class PipelineError(Exception):
    """Base class: callers can catch every pipeline failure at once."""

class TransientError(PipelineError):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status

@contextmanager
def staging_table(connection, name: str):
    connection.execute(f"CREATE TEMP TABLE {name}")
    try:
        yield name
    finally:
        connection.execute(f"DROP TABLE {name}")   # runs even on failure

try:
    raise TransientError(503, "service unavailable")
except PipelineError as exc:
    print("caught:", exc.status, exc)
```

Never use a bare `except:` — it also catches `KeyboardInterrupt` and `SystemExit`; catch `Exception` only at a top-level boundary that logs and fails the task. When translating errors, keep the original with `raise ConfigError("bad config") from exc`.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do iterators and generators work in Python?

An **iterable** produces an **iterator**; an iterator implements `__next__` and raises `StopIteration` when exhausted. A generator function contains `yield` and returns a lazy iterator automatically. Laziness lets a pipeline process a file larger than memory, and a generator is single-use.

```python
from collections.abc import Iterator

def parse_lines(lines: list[str]) -> Iterator[dict]:
    for line in lines:
        if not line.strip():
            continue
        key, _, value = line.partition("=")
        yield {"key": key.strip(), "value": int(value)}

def with_run_id(rows: Iterator[dict], run_id: str) -> Iterator[dict]:
    yield {"key": "_run_id", "value": run_id}
    yield from rows                       # delegate and stay lazy

stream = with_run_id(parse_lines(["a=1", "", "b=2"]), "run-7")
print(next(stream), list(stream), list(stream))   # the last call is exhausted
```

Writing the protocol by hand — `__iter__` returning `self` and `__next__` raising `StopIteration` — is the interview answer for what a generator is under the hood.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do decorators work in Python?

A decorator takes a function and returns a replacement, so `@retry` is `fetch = retry(fetch)`. Always wrap with `functools.wraps` to preserve the name, docstring, and signature, which keeps logs, tracing, and test discovery readable. `functools.lru_cache` is the standard memoization decorator for pure lookups.

```python
import functools

def retry(attempts: int = 3, exceptions: tuple[type[Exception], ...] = (TimeoutError,)):
    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    if attempt == attempts:
                        raise
                    print(f"attempt {attempt} failed ({exc}); retrying")
        return wrapper
    return decorate

@functools.lru_cache(maxsize=128)
def region_for(code: str) -> str:
    return {"us": "americas", "de": "emea"}[code]

state = {"calls": 0}

@retry(attempts=3)
def fetch() -> str:
    state["calls"] += 1
    if state["calls"] < 3:
        raise TimeoutError("deadline exceeded")
    return "payload"

print(fetch(), state["calls"], fetch.__name__)
print(region_for("us"), region_for("us"), region_for.cache_info().hits)
```

Stacked decorators apply bottom-up, so a timer placed above `@retry` measures the whole operation while the reverse times each attempt separately. Add jitter and a cap to real backoff, and retry only transient errors.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What functional tools does Python provide?

`map`, `filter`, `any`, `all`, `zip`, `enumerate`, `sorted(key=...)`, and `functools.reduce` turn explicit loops into intent-revealing expressions. In data code, `sorted` with a tuple key and short-circuiting `any`/`all` checks are far more common than `reduce`.

```python
from functools import reduce
from operator import add

rows = [{"region": "us", "amount": 10}, {"region": "eu", "amount": 5}]
amounts = list(map(lambda row: row["amount"], rows))
big = list(filter(lambda row: row["amount"] > 5, rows))

print(amounts, [row["region"] for row in big], reduce(add, amounts, 0))
print(any(row["amount"] > 9 for row in rows), all(row["amount"] > 0 for row in rows))
print(list(zip("abc", amounts)), list(enumerate(["a", "b"], start=1)))
print(sorted(rows, key=lambda row: (-row["amount"], row["region"]))[0])
```

`sorted` is stable and returns a new list while `list.sort()` mutates in place. A key function may return a tuple for multi-field ordering, and negating a numeric field is the standard descending sort.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do type hints and mypy work?

Type hints are runtime-neutral annotations read by `mypy` or `pyright`, by IDEs for completion, and by frameworks such as pydantic for validation. Annotate public signatures and data structures, use `X | None` instead of `Optional[X]`, builtin generics like `list[int]`, and `collections.abc` types for parameters you only read or iterate.

```python
from collections.abc import Iterable, Iterator, Sequence
from typing import Protocol, TypedDict

class Record(TypedDict):
    order_id: str
    amount: float

class Writer(Protocol):
    def write(self, records: Sequence[Record]) -> int: ...

def totals(records: Iterable[Record]) -> Iterator[tuple[str, float]]:
    for record in records:
        yield record["order_id"], record["amount"]

print(list(totals([{"order_id": "A1", "amount": 10.5}])))
```

```bash
uv run mypy --strict src/
uv run pyright src/
```

`Protocol` gives structural typing ("anything with a `write` method") so test doubles need not inherit from production classes, and `TypedDict` types dictionary payloads at JSON boundaries.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do datetime and time zones work in Python?

`datetime` values are **naive** (no timezone) or **aware** (has `tzinfo`), and mixing them raises `TypeError` on comparison. Store and compare in UTC, convert to a local zone only for display or business calendars, and use `zoneinfo` rather than fixed offsets because it applies daylight-saving rules.

```python
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

utc = datetime(2026, 10, 4, 12, 0, tzinfo=timezone.utc)
new_york = utc.astimezone(ZoneInfo("America/New_York"))

print(utc.isoformat(), new_york.isoformat(), new_york.utcoffset())
print(utc.date(), utc + timedelta(days=1), int(utc.timestamp()))
print(date(2026, 10, 4).strftime("%Y/%m/%d"), (date(2026, 10, 5) - date(2026, 10, 4)).days)
```

Avoid `datetime.utcnow()` and naive `datetime.now()`: they return values that silently mean "whatever the server thinks". Use `datetime.now(timezone.utc)` and keep durations as `timedelta` until the boundary.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do file I/O, pathlib, JSON, and CSV work?

`pathlib.Path` replaces string path juggling: `/` joins, `.open()` reads, `.glob()` discovers, `.unlink()` removes. Use `encoding="utf-8"` for text, `newline=""` with the `csv` module so quoting is handled correctly, and newline-delimited JSON for streaming because each line parses independently.

```python
import csv
import json
from pathlib import Path

root = Path("/tmp/pybasics")
root.mkdir(exist_ok=True)
records = [{"order_id": "A1", "amount": 10.5}, {"order_id": "A2", "amount": 7.0}]

with (root / "orders.ndjson").open("w", encoding="utf-8") as handle:
    for record in records:
        handle.write(json.dumps(record) + "\n")
loaded = [json.loads(line) for line in (root / "orders.ndjson").read_text(encoding="utf-8").splitlines()]

with (root / "orders.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["order_id", "amount"])
    writer.writeheader()
    writer.writerows(loaded)
with (root / "orders.csv").open(newline="", encoding="utf-8") as handle:
    back = list(csv.DictReader(handle))

print(len(back), back[0]["amount"], type(back[0]["amount"]).__name__, loaded[0]["amount"])
```

Two details worth stating: `csv` returns every field as `str`, so conversion is explicit, and `json.dumps` needs `default=str` or a custom encoder for `Decimal` and `datetime`.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do the GIL, threads, processes, and asyncio compare?

CPython's **GIL** lets only one thread execute bytecode at a time, so threads provide concurrency, not parallelism, for CPU-bound code. The split: **threads** for blocking IO, **processes** for CPU-bound work, **asyncio** for very high-concurrency network IO in one thread. Follow the bottleneck, and measure whether the code waits or computes.

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def fetch(url: str) -> str:
    time.sleep(0.01)          # pretend network IO: releases the GIL while waiting
    return url.upper()

async def afetch(url: str) -> str:
    await asyncio.sleep(0.01)
    return url.upper()

async def main() -> list[str]:
    return await asyncio.gather(*(afetch(url) for url in ["a", "b"]))

with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(fetch, ["a", "b"])))
print(asyncio.run(main()))
```

Use `ProcessPoolExecutor` for CPU-bound work (function and data must be picklable), and `asyncio.to_thread` to move unavoidable blocking calls off an event loop. Never mix blocking IO into async code.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do virtual environments, pip, uv, pyproject, and pytest work?

Use one virtual environment per project so the interpreter and dependencies are reproducible and isolated from the system Python. `pyproject.toml` is the single source of metadata, a lockfile pins the full transitive graph, and `uv` is a fast drop-in for `pip` that also manages interpreters and the lock.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q

uv venv && uv sync --frozen
uv run pytest -q
```

```text
[project]
name = "orders-pipeline"
requires-python = ">=3.11"
dependencies = ["httpx>=0.27", "pydantic>=2.7"]

[project.optional-dependencies]
dev = ["pytest>=8", "mypy>=1.11", "ruff>=0.5"]
```

```python
# tests/test_transform.py
import pytest

def normalize(value: str) -> str:
    return value.strip().lower()

@pytest.mark.parametrize("raw,expected", [("Us", "us"), ("EU", "eu")])
def test_normalize(raw: str, expected: str) -> None:
    assert normalize(raw) == expected

def test_rejects_empty() -> None:
    with pytest.raises(ValueError):
        if not normalize(""):
            raise ValueError("empty column name")
```

Pin exact versions in CI (`uv sync --frozen`), keep dev tools in an extra so production images stay small, and make `python -m pytest` the entry point.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What are the most common Python pitfalls?

These five dominate code review: mutable defaults, late-binding closures, float equality, string building in loops, and shadowing builtins. Each has a one-line fix.

```python
import math

def add_bad(item: str, bucket: list[str] = []) -> list[str]:   # created once
    bucket.append(item)
    return bucket

def add_good(item: str, bucket: list[str] | None = None) -> list[str]:
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket

funcs = [lambda: i for i in range(3)]        # late binding: all see i = 2
fixed = [lambda i=i: i for i in range(3)]    # bind the current value
parts = [str(i) for i in range(20000)]

print(add_bad("a"), add_bad("b"), add_good("a"), add_good("b"))
print([fn() for fn in funcs], [fn() for fn in fixed])
print(0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9))
print(len("".join(parts)), "".join(parts).endswith("19999"))
```

Also avoid mutating a list while iterating it, using `is` for value comparison instead of `==` (except with `None`), bare `except:`, shadowing builtins such as `sum` or `list`, and `dict.get` masking a missing key that should fail fast — `d["k"]` raising `KeyError` is often the better signal.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## Real world use cases for Python basics in data engineering

### 1. A reusable API client class with retries and a context manager

A class that owns the session, retries transient failures with capped backoff, and closes cleanly in `__exit__` keeps failure behavior identical across every endpoint.

```python
import random
import time

class ApiClient:
    def __init__(self, base_url: str, token: str, attempts: int = 3) -> None:
        self.base_url, self.token, self.attempts = base_url.rstrip("/"), token, attempts
        self.session: object | None = None
    def __enter__(self) -> "ApiClient":
        self.session = object()                 # stand-in for httpx.Client()
        return self
    def __exit__(self, exc_type, exc, tb) -> bool:
        self.session = None                     # close the real session here
        return False
    def get(self, path: str) -> dict:
        for attempt in range(1, self.attempts + 1):
            try:
                if attempt < 2:                 # stand-in for a 503 response
                    raise TimeoutError("503")
                return {"path": path, "attempt": attempt}
            except TimeoutError:
                if attempt == self.attempts:
                    raise
                time.sleep(min(8.0, 0.5 * 2 ** attempt) * (0.5 + random.random()))
        raise RuntimeError("unreachable")

with ApiClient("https://api.example.com", "token") as client:
    print(client.get("/orders/2026-10-04"))
```

**Why it matters:** retries, backoff, and cleanup live in one place, so extractor code stays a single readable call.

### 2. A validated config dataclass

Configuration belongs in typed objects, not scattered `os.environ` lookups. A frozen dataclass with `from_env` and an explicit `validate` fails at startup instead of mid-run.

```python
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class PipelineConfig:
    source_bucket: str
    target_table: str
    batch_size: int = 50_000
    def validate(self) -> None:
        if self.batch_size <= 0:
            raise ValueError(f"batch_size must be positive, got {self.batch_size}")
    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> "PipelineConfig":
        values = os.environ if env is None else env
        return cls(values["SOURCE_BUCKET"], values["TARGET_TABLE"],
                   int(values.get("BATCH_SIZE", "50000")))

config = PipelineConfig.from_env({"SOURCE_BUCKET": "lake-raw", "TARGET_TABLE": "analytics.orders"})
config.validate()
print(config, config.batch_size > 0)
```

**Why it matters:** config errors surface at deploy time rather than hours into a load, and the dataclass doubles as a test fixture.

### 3. A generator-based streaming reader

A finance export does not fit in memory. A chain of generators reads, filters, and batches it with peak memory proportional to the batch, and every stage is testable on a small list.

```python
import json
from collections.abc import Iterable, Iterator

def read_ndjson(lines: Iterable[str]) -> Iterator[dict]:
    for line in lines:
        row = json.loads(line) if line.strip() else None
        if row and row["amount"] >= 0:
            yield row

def batched(rows: Iterator[dict], size: int) -> Iterator[list[dict]]:
    batch: list[dict] = []
    for row in rows:
        batch.append(row)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch

lines = ['{"order_id": "A1", "amount": 10.5}', "", '{"order_id": "A2", "amount": -1}']
pipeline = batched(read_ndjson(lines), size=2)
print([sum(row["amount"] for row in batch) for batch in pipeline])
```

**Why it matters:** one machine with flat memory often beats provisioning a cluster, and generator boundaries keep each stage unit-testable.

### 4. A retry decorator with exponential backoff

Cross-cutting concerns belong in decorators so the transform function stays pure, and a decorator applies one retry policy uniformly to every wrapped function.

```python
import functools
import time

def retry(attempts: int = 3, base_delay: float = 0.5):
    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except TimeoutError:
                    if attempt == attempts:
                        raise
                    time.sleep(base_delay * 2 ** (attempt - 1))
        return wrapper
    return decorate

state = {"calls": 0}

@retry(attempts=3)
def load_partition(name: str) -> str:
    state["calls"] += 1
    if state["calls"] < 3:
        raise TimeoutError(name)
    return f"loaded:{name}"

print(load_partition("dt=2026-10-04"), "calls=", state["calls"])
```

**Why it matters:** observability and resilience are added without touching business logic and apply uniformly to every wrapped function.

### 5. A context manager for staging tables

A warehouse load needs a temp table created before the work and dropped even when the merge fails. A context manager guarantees cleanup and centralizes the transaction boundary.

```python
from contextlib import contextmanager

class FakeWarehouse:
    def __init__(self) -> None:
        self.log: list[str] = []
    def execute(self, sql: str) -> None:
        self.log.append(sql)

@contextmanager
def staging_table(warehouse: FakeWarehouse, name: str, source: str):
    warehouse.execute(f"CREATE TEMP TABLE {name} AS SELECT * FROM {source} WHERE 1=0")
    try:
        yield name
        warehouse.execute(f"MERGE INTO analytics.orders USING {name} ON orders.id = {name}.id")
    finally:
        warehouse.execute(f"DROP TABLE IF EXISTS {name}")

warehouse = FakeWarehouse()
with staging_table(warehouse, "stg_orders", "raw.orders") as staging:
    warehouse.execute(f"INSERT INTO {staging} SELECT * FROM raw.orders WHERE dt = '2026-10-04'")
print(len(warehouse.log), warehouse.log[-1])
```

**Why it matters:** the temp table always disappears, the merge runs exactly once per successful block, and a failure leaves the session in a known state for the retry.

[Table of Contents](#Python-Basics-for-Data-Engineers)
