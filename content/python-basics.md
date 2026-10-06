## [Main title](../README.md)
### [Interview questions](full.md)

# Python Basics for Data Engineers

**Notebook:** [`notebooks/topics/python-basics.ipynb`](../notebooks/topics/python-basics.ipynb) - runnable version of this topic with self-checking exercises.

This notebook teaches the Python language basics that data engineering interviews assume. It is intentionally plain and practical: each topic explains the idea in simple terms, then gives a small runnable example.

How to use it:

+ Run one code cell at a time.
+ Change a value and run the cell again.
+ Read the printed output before moving on.
+ Treat every example as a small building block for pipeline code.

This is the Python language itself, not pipeline architecture or puzzle solving. For example, before you tune Spark or design a CDC pipeline, you still need to be comfortable with variables, collections, functions, classes, exceptions, files, dates, and tests.

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

Think of a variable as a sticky label on a value. The value has the type, not the variable name. That means the same name can point to an integer now and a string later.

This is called **dynamic typing**. It makes Python flexible, but it also means you should choose clear names and use type hints for code that other people will maintain.

Python code is built from **expressions** and **statements**.

+ An expression produces a value: `2 + 3`, `"hi".upper()`, `len([1, 2])`.
+ A statement performs an action: assignment, `if`, `for`, `def`, `class`, `import`.

In a notebook, you can run tiny expressions first and inspect what Python gives back:

```python
print(2 + 3)
print("orders".upper())
print(len(["raw", "bronze", "silver"]))
```

Simple rules:

+ `type(x)` tells you the exact runtime type.
+ `isinstance(x, T)` checks whether `x` behaves like type `T` or a subclass of it.
+ `==` compares values.
+ `is` compares whether two names point to the exact same object.
+ Type hints such as `rate: float` help tools and readers; Python does not enforce them automatically.

```python
count = 3            # int
count = "three"      # rebinding to another type is legal
rate: float = 0.75   # annotation only: no runtime check

for value in (count, rate, [1, 2], None):
    print(f"{value!r:>8} -> {type(value).__name__}")
```

What to notice:

+ `count = 3` does not create a permanent integer variable.
+ It binds the name `count` to the integer object `3`.
+ `count = "three"` reuses the same name for a different object.
+ This is legal Python, but it can make code harder to read if overused.

Run this smaller cell to see the difference between equality and identity:

```python
a = [1, 2]
b = [1, 2]
c = a

print("a == b:", a == b)   # same contents
print("a is b:", a is b)   # different list objects
print("a is c:", a is c)   # same list object
```

For interview answers, say it this way: use `==` for value comparison and `is` for identity checks such as `x is None`.

```python
value = None

print(value is None)
print(value == None)  # works, but `is None` is the normal style
```

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do numbers and strings work in Python?

Python has a few number types you will use constantly:

+ `int` for whole numbers. Python integers can grow very large.
+ `float` for approximate decimal values. Floats are fast but not exact for money.
+ `Decimal` for exact decimal math, often used for financial values.

Strings are immutable text values. Immutable means you do not change a string in place; operations such as `.replace()` return a new string.

Start with the arithmetic operators. These are the ones you will see in simple transforms, metrics, and tests:

| Operator | Meaning | Example |
|---|---|---|
| `+` | add | `2 + 3` |
| `-` | subtract | `10 - 4` |
| `*` | multiply | `6 * 7` |
| `/` | true division | `7 / 2` gives `3.5` |
| `//` | floor division | `7 // 2` gives `3` |
| `%` | remainder | `7 % 2` gives `1` |
| `**` | power | `2 ** 10` |

Start with numbers:

```python
from decimal import Decimal

print(7 / 2, 7 // 2, 2**10, divmod(7, 2))
print(0.1 + 0.2, Decimal("0.1") + Decimal("0.2"))
```

What to notice:

+ `/` always returns a float.
+ `//` returns the quotient without the fractional part.
+ `divmod(a, b)` returns both quotient and remainder.
+ `0.1 + 0.2` is not exactly `0.3` with floats because many decimal fractions cannot be represented exactly in binary.

Use integer cents or `Decimal` for money:

```python
price_cents = 1999
quantity = 3
total_cents = price_cents * quantity

print(total_cents)
print(f"${total_cents / 100:.2f}")
```

Convert strings from files or APIs before doing math:

```python
raw_amount = "10.50"
amount = Decimal(raw_amount)

print(amount * Decimal("2"))
```

Now look at common string operations. Slicing uses `[start:stop:step]`, and f-strings are the normal way to format values:

```python
order_id = "ORD-2026-000123"
region, year, seq = order_id.split("-")

print(f"{region=} {seq:0>8} {int(seq):,} {0.4217:.2%}")
print(order_id[:3], order_id[-6:], order_id[::-1], "a,b,c".replace(",", "|"))
```

Strings are sequences, so indexing and slicing work left to right:

```python
text = "python"

print(text[0])     # first character
print(text[-1])    # last character
print(text[1:4])   # positions 1, 2, 3
print(text[:2])    # first two characters
print(text[2:])    # from position 2 to the end
```

Common string methods return new strings:

```python
raw = "  ORD-001,paid  "
clean = raw.strip().lower()

print(raw)
print(clean)
print(clean.startswith("ord"))
print(clean.split(","))
```

`bytes` is for raw binary payloads. Decode bytes into text before treating them like strings:

```python
payload = "café".encode("utf-8")
text = payload.decode("utf-8")

print(payload)
print(text)
```

Always pass `encoding="utf-8"` when crossing the text/binary boundary; mixing the two raises `TypeError` instead of silently producing mojibake.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What are the core collections: lists, tuples, sets, and dicts?

Collections hold multiple values. In data engineering, you use them for rows, schemas, counters, lookup tables, configuration, and small in-memory transformations.

The four core containers are:

| Type | Simple meaning | Common use |
|---|---|---|
| `list` | ordered and changeable | rows, columns, batches |
| `tuple` | ordered and usually not changed | fixed pairs such as `(id, amount)` |
| `set` | unique values | membership checks and duplicate removal |
| `dict` | key-value lookup | records, configs, mappings |

Start with the plain built-ins:

```python
columns = ["order_id", "amount", "amount"]
unique_columns = set(columns)
row = ("A1", 10.5)
record = {"order_id": "A1", "amount": 10.5}

print(columns)
print(unique_columns)
print(row[0])
print(record["amount"])
```

Lists are good when order matters and you expect to add, remove, or reorder values:

```python
stages = ["raw", "bronze"]
stages.append("silver")
stages[0] = "landing"

print(stages)
print(stages[-1])
```

Tuples are good for fixed shapes. They are often returned from functions or database libraries:

```python
order = ("A1", 10.5)
order_id, amount = order

print(order_id)
print(amount)
```

Sets are good for uniqueness and membership checks:

```python
seen_ids = {"A1", "A2"}

print("A1" in seen_ids)
print("A3" in seen_ids)
print({"A1", "A2"} | {"A2", "A3"})  # union
```

Dictionaries are good for named fields and lookups:

```python
order = {"order_id": "A1", "amount": 10.5}

print(order["order_id"])
print(order.get("status", "unknown"))
```

`Counter` and `defaultdict` are helpful when you would otherwise write a lot of "if this key is missing, create it" code:

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

This mistake is common:

```python
numbers = [3, 1, 2]
result = numbers.sort()

print("numbers:", numbers)
print("result:", result)
```

`numbers.sort()` changes the list in place and returns `None`. If you want a new sorted list, use `sorted(numbers)`.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do comprehensions work in Python?

A comprehension is a compact loop that creates a new collection. Use it when the logic is simple enough to read in one line.

Read a comprehension from left to right:

```text
[expression for item in iterable if condition]
```

The `for` part says where values come from. The optional `if` part filters values. The expression at the front says what to put in the result.

This normal loop:

```python
rows = [{"id": 1, "amount": 10}, {"id": 2, "amount": 0}, {"id": 3, "amount": 25}]

paid_amounts = []
for row in rows:
    if row["amount"] > 0:
        paid_amounts.append(row["amount"])

print(paid_amounts)
```

can be written as this list comprehension:

```python
paid_amounts = [row["amount"] for row in rows if row["amount"] > 0]
print(paid_amounts)
```

Comprehensions can build lists, sets, dicts, and lazy generator expressions:

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

Keep comprehensions boring. If you need several steps, side effects, or nested conditions, use a normal `for` loop.

Here is a good rule of thumb:

+ one transformation and one filter: comprehension is fine,
+ several temporary variables: normal loop,
+ logging, API calls, mutation, or exception handling: normal loop.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What is the difference between mutability, references, copy, and deepcopy?

Assignment does not copy an object. It gives the same object another name.

This matters most with mutable objects such as lists and dicts. If two names point to the same mutable object, changing through one name is visible through the other name.

First, see aliasing:

```python
original = ["raw", "bronze"]
alias = original

alias.append("silver")
print(original)
```

That output surprises beginners because `alias` and `original` are two names for the same list.

Use `id()` only for learning and debugging. It shows the identity of the object during the current Python process:

```python
original = ["raw", "bronze"]
alias = original
copy_of_original = list(original)

print(id(original) == id(alias))
print(id(original) == id(copy_of_original))
```

Now compare shallow copy and deep copy:

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

A **shallow copy** copies the outer dict or list only. Nested objects are still shared. A **deep copy** recursively copies nested objects too. Use deep copy only when you really need independent nested state; it can be expensive for large objects.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How does control flow work in Python?

Control flow decides what code runs and how many times it runs.

The basics are:

+ `if` / `elif` / `else` for choices.
+ `for` for looping over an iterable.
+ `while` for looping until a condition changes.
+ `break` to leave a loop.
+ `continue` to skip to the next iteration.
+ `match` for clearer multi-case branching in Python 3.10+.

Python also uses **truthiness**. Empty containers, `0`, `""`, `None`, and `False` are treated as false in conditions.

Start with `if`. It is just a question that returns `True` or `False`:

```python
amount = 125

if amount > 100:
    print("large order")
else:
    print("small order")
```

`for` loops are for walking through an iterable:

```python
for stage in ["raw", "bronze", "silver"]:
    print("run", stage)
```

`while` loops are for "keep going until this changes" situations:

```python
attempt = 1

while attempt <= 3:
    print("attempt", attempt)
    attempt += 1
```

```python
values = [10, 0, None, ""]

for value in values:
    if value:
        print("truthy:", value)
    else:
        print("falsy:", repr(value))
```

Here is a realistic retry classification example:

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

The `for ... else` form is uncommon but useful in interviews: the `else` block runs only when the loop did **not** hit `break`.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do functions, arguments, scope, and closures work?

A function is a named block of reusable work. A good function has a small job, clear parameter names, and a predictable return value.

The simplest function has inputs, a body, and a return value:

```python
def dollars(cents: int) -> float:
    return cents / 100

print(dollars(1250))
```

If a function has no `return`, Python returns `None` automatically:

```python
def log_message(message: str) -> None:
    print("LOG:", message)

result = log_message("started")
print(result)
```

The function signature is the interface:

+ normal parameters receive required values,
+ default parameters provide fallback values,
+ `*args` collects extra positional arguments,
+ `**kwargs` collects extra keyword arguments,
+ keyword-only parameters after `*` make the caller name important options.

```python
def load(*path_parts: str, mode: str = "batch", **options: object) -> dict:
    return {"path": "/".join(path_parts), "mode": mode, "options": options}

print(load("s3://bucket", "orders", mode="stream", compression="zstd"))
```

One important warning: default values are created once, when the function is defined. That is why mutable defaults like `[]` are dangerous.

Here is the bad pattern:

```python
def remember_bad(value: str, bucket: list[str] = []) -> list[str]:
    bucket.append(value)
    return bucket

print(remember_bad("a"))
print(remember_bad("b"))  # "a" is still there because the same list is reused
```

Use `None` as the default and create the list inside the function:

```python
def remember_good(value: str, bucket: list[str] | None = None) -> list[str]:
    bucket = [] if bucket is None else bucket
    bucket.append(value)
    return bucket

print(remember_good("a"))
print(remember_good("b"))
```

Closures are functions that remember names from the surrounding function:

```python
def make_counter(start: int = 0):
    count = start

    def increment(step: int = 1) -> int:
        nonlocal count          # rebind, not shadow, the enclosing name
        count += step
        return count

    return increment

counter = make_counter(10)
print(counter(), counter(5), counter(), sorted((3, 1, 2)))
```

Name lookup follows **LEGB**: Local, Enclosing, Global, Built-in. You usually do not need to memorize the acronym if you remember this: Python first checks the current function, then outer functions, then module globals, then built-ins.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do modules, packages, and the main guard work?

A module is one `.py` file. A package is a folder of modules. Imports let you reuse code instead of copying functions between files.

You have already used modules in this notebook:

```python
import math

print(math.sqrt(16))
```

`import math` gives you the module object. Then you access names inside it with dot notation, such as `math.sqrt`.

You can also import one name from a module:

```python
from decimal import Decimal

print(Decimal("0.1") + Decimal("0.2"))
```

In normal project code you might have this layout:

```text
jobs/
  __init__.py
  parsers.py
  run.py
```

The next cell creates that tiny package in a temporary folder so the example really runs in a notebook:

```python
import sys
import tempfile
import textwrap
from pathlib import Path

project = Path(tempfile.mkdtemp())
jobs = project / "jobs"
jobs.mkdir()
(jobs / "__init__.py").write_text("", encoding="utf-8")

(jobs / "parsers.py").write_text(
    textwrap.dedent(
        """
        from dataclasses import dataclass

        @dataclass(frozen=True)
        class Order:
            order_id: str
            amount: float

        def parse(raw: dict) -> Order:
            return Order(order_id=raw["id"], amount=float(raw["amount"]))
        """
    ),
    encoding="utf-8",
)

sys.path.insert(0, str(project))
print(project)
```

Now import the module and use it:

```python
from jobs.parsers import Order, parse

def main() -> int:
    order: Order = parse({"id": "A1", "amount": "10.5"})
    print(f"parsed {order.order_id} for {order.amount:.2f}")
    return 0

main()
```

The `if __name__ == "__main__":` guard is used in real `.py` files. It means "run this part only when the file is executed directly, not when another file imports it."

```python
example_name = "__main__"
if example_name == "__main__":
    print("This is where a script would call main().")
```

Prefer absolute imports (`from jobs.parsers import parse`) inside packages, keep `__init__.py` free of heavy work, and avoid mutating `sys.path` from library code. The notebook used `sys.path.insert` only to make the temporary demo package importable.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do classes, objects, and methods work?

A class is a blueprint for objects. An object is one concrete instance of that class.

Use a class when data and behavior naturally belong together. For example, an API extractor has a URL, a page size, and a method that fetches a page.

Before classes, you might pass dictionaries around:

```python
extractor = {"url": "https://api.example.com/orders", "page_size": 100}
print(extractor["url"])
```

That works for small scripts. A class becomes useful when the object also has behavior:

+ validate settings,
+ fetch a page,
+ close a connection,
+ format itself for logs,
+ expose alternative constructors.

Key ideas:

+ `__init__` initializes each new object.
+ `self` means "this object".
+ Instance attributes belong to one object.
+ Class attributes are shared by all objects unless shadowed.
+ Instance methods receive `self`.
+ Class methods receive `cls` and are often alternative constructors.
+ Static methods receive neither `self` nor `cls`.

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
print(extractor.fetch(1))
print(extractor.kind)
print(extractor.is_partition_column("dt=2026-10-04"))
```

`self` is only the conventional first parameter; Python never passes the receiver implicitly. Assigning `self.kind` would create an instance attribute that shadows the class attribute for that object alone.

Create two objects to see that instance attributes are separate:

```python
small = Extractor("https://api.example.com/small", page_size=10)
large = Extractor("https://api.example.com/large", page_size=1000)

print(small.fetch(1))
print(large.fetch(1))
```

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do inheritance, super, polymorphism, and MRO work?

Inheritance lets one class reuse and specialize another class. Use it for a true **is-a** relationship: a `ParquetSink` is a kind of `Sink`.

Polymorphism means you can call the same method on different object types and each object chooses its own behavior. In the example below, every sink has `.write(...)`, but each sink writes differently.

Do not use inheritance just to share a few helper functions. In data engineering code, composition is often simpler:

```python
class RetryPolicy:
    def __init__(self, attempts: int) -> None:
        self.attempts = attempts

class Loader:
    def __init__(self, retry_policy: RetryPolicy) -> None:
        self.retry_policy = retry_policy

loader = Loader(RetryPolicy(attempts=3))
print(loader.retry_policy.attempts)
```

This says a `Loader` **has a** retry policy. That is composition.

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

`super()` means "call the next implementation in the method resolution order". MRO is the order Python searches classes for attributes and methods.

Prefer composition when the relationship is "has-a": a `Loader` holding an `S3Client` is easier to test than `Loader(S3Client)`. Use `Protocol` or abstract base classes for the contract.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What are the most important dunder methods?

Dunder methods have names such as `__len__` and `__repr__`. Python calls them behind the scenes when you use normal syntax.

The word "dunder" just means "double underscore". So `__len__` is pronounced "dunder len".

You do not need to memorize every dunder method. Learn the ones that explain Python syntax. When you write `len(batch)`, Python looks for `batch.__len__()`. When you write `for row in batch`, Python looks for something iterable, usually `batch.__iter__()`.

Examples:

+ `print(obj)` uses `__str__`.
+ `repr(obj)` uses `__repr__`.
+ `len(obj)` uses `__len__`.
+ `for item in obj` uses `__iter__`.
+ `obj == other` uses `__eq__`.

You do not call most dunder methods directly. You implement them so your object works naturally with Python syntax.

Before writing a class, ask: "Do I want this object to behave like a collection, a value, a function, or a context manager?" The answer tells you which dunder method you might need.

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

What to notice:

+ `print(batch)` used `__str__`.
+ `repr(batch)` used `__repr__`.
+ `len(batch)` used `__len__`.
+ `list(batch)` used `__iter__`.
+ `batch == Batch(...)` used `__eq__`.

`__getitem__` powers indexing and slicing, `__call__` makes an instance callable, and `__enter__`/`__exit__` make it a context manager for the `with` statement.

Use dunder methods sparingly. They are powerful because they make objects feel native, but surprising dunder behavior makes code hard to debug.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do properties and encapsulation work?

Python does not have strict private fields like some languages. Instead, it uses naming conventions:

+ `name` is normal public data.
+ `_name` means "internal; please do not use from outside this class".
+ `__name` triggers name mangling and is rarely needed.

Use `@property` when an attribute needs validation or calculated output. The caller writes `snapshot.rows`, but your class can still run code behind the scenes.

Think of `@property` as a controlled door. The outside code uses simple attribute syntax, but the class decides what happens when someone reads or writes that value.

Without a property, this class cannot stop invalid data:

```python
class PlainSnapshot:
    def __init__(self, rows: int) -> None:
        self.rows = rows

plain = PlainSnapshot(-100)
print(plain.rows)  # Python allowed the invalid value
```

With a property, the class can reject bad values at the moment they are assigned:

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

Try the validation path:

```python
try:
    Snapshot(-1)
except ValueError as exc:
    print("validation worked:", exc)
```

What to notice:

+ `snapshot.rows` looks like a simple attribute read.
+ `self.rows = rows` inside `__init__` calls the setter.
+ `size_mb` has no setter, so it is read-only.
+ The validation lives in one place instead of being copied around the codebase.

Start with plain attributes. Add a property only when validation, lazy computation, or a refactoring shim requires it.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do dataclasses, NamedTuple, and enums work?

These tools help you model small structured values without writing a lot of class boilerplate.

+ `@dataclass` is usually best for readable business objects.
+ `NamedTuple` is useful for small immutable records that unpack like tuples.
+ `Enum` is useful when only a small fixed set of values is allowed.

The problem they solve is simple: dictionaries are flexible, but too flexible. A typo like `row["amunt"]` fails only when that line runs. A small typed object gives your code a clearer shape.

Start with an enum. It prevents "magic strings" from spreading through your code:

```python
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import NamedTuple

class Stage(StrEnum):
    EXTRACT, LOAD = auto(), auto()      # value is the lower-case member name
```

```python
stage = Stage.EXTRACT

if stage is Stage.EXTRACT:
    print("read source data")

print(stage.value)
```

Now use a dataclass for a small domain object:

```python
@dataclass(frozen=True, slots=True)
class S3Location:
    bucket: str
    key: str
    region: str = "us-east-1"

    @property
    def uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"

print(S3Location("lake", "raw.json").uri)
```

What `@dataclass` generated for you:

+ an `__init__` method,
+ a useful `__repr__`,
+ equality comparison,
+ field storage.

`frozen=True` means "do not allow changes after creation":

```python
location = S3Location("lake", "raw.json")

try:
    location.bucket = "other"
except Exception as exc:
    print(type(exc).__name__, exc)
```

Use a `NamedTuple` when you want something tuple-like with names:

```python
class Row(NamedTuple):
    order_id: str
    amount: float

print(Stage.LOAD.value)
print(Row("A1", 10.5) == Row("A1", 10.5), Row("A1", 10.5).amount)
```

Choose a dataclass when the object has behavior or validation, and a `NamedTuple` when it is a small immutable record that benefits from `order_id, amount = row`.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do exceptions and context managers work?

Exceptions are Python's way to stop the normal path and say "something went wrong."

Beginners sometimes try to avoid errors completely. A better habit is to expect errors at boundaries:

+ parsing user input,
+ reading files,
+ calling APIs,
+ connecting to databases,
+ converting strings to numbers,
+ looking up missing dictionary keys.

Use this shape:

+ `try`: code that might fail.
+ `except`: recovery or translation.
+ `else`: code that runs only when there was no exception.
+ `finally`: cleanup that always runs.

Start with a small example:

```python
try:
    amount = float("10.5")
except ValueError:
    amount = 0.0
else:
    print("parsed:", amount)
finally:
    print("cleanup runs either way")
```

Here is the same idea with bad input:

```python
raw_amount = "not-a-number"

try:
    amount = float(raw_amount)
except ValueError as exc:
    print("could not parse amount:", exc)
    amount = 0.0

print(amount)
```

A context manager is the object behind `with`. It guarantees setup and cleanup. Files, database sessions, temporary tables, and locks are common context-manager use cases.

The everyday example is opening a file:

```python
from pathlib import Path

path = Path("/tmp/context-demo.txt")

with path.open("w", encoding="utf-8") as handle:
    handle.write("hello")

print(path.read_text(encoding="utf-8"))
```

The `with` block makes sure the file is closed even if an error happens inside the block.

You can build your own context manager when the pattern is "do setup, run user code, always clean up":

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

In data pipelines, prefer errors that say what failed and what input caused it. "invalid literal for int()" is less useful than "invalid batch_size='abc' in pipeline config".

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do iterators and generators work in Python?

An **iterable** is something you can loop over. A list is iterable. A file handle is iterable. A generator is iterable.

A **generator** produces values lazily, one at a time. It uses `yield` instead of `return`.

The simple mental model:

+ `return` gives one final result and stops the function.
+ `yield` gives one value now and pauses the function until the next value is requested.

Generators are useful when the data might be large because you do not need to load everything into memory.

This is why data engineers care about generators. A CSV file might have 10 rows in a test and 100 million rows in production. A list tries to hold all rows at once. A generator lets you process one row at a time.

Compare eager and lazy thinking:

+ A list builds all values now.
+ A generator produces one value at a time when asked.

```python
eager = [number * 2 for number in range(5)]
lazy = (number * 2 for number in range(5))

print(eager)
print(lazy)
print(next(lazy))
print(next(lazy))
```

What to notice:

+ `eager` prints as a real list because all values were built immediately.
+ `lazy` prints as a generator object because values are waiting to be produced.
+ `next(lazy)` asks for one value.
+ Once a generator gives a value, it moves forward; it does not rewind.

```python
def numbers():
    yield 1
    yield 2
    yield 3

stream = numbers()
print(next(stream))
print(next(stream))
print(list(stream))
```

Here is a more data-engineering-shaped example:

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

The final `list(stream)` is empty because the generator was already consumed. This is a common bug: if you need to read data twice, materialize it into a list; if you need low memory usage, keep it as a generator and process it once.

Writing the protocol by hand — `__iter__` returning `self` and `__next__` raising `StopIteration` — is the interview answer for what a generator is under the hood.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do decorators work in Python?

A decorator is a function that takes another function and returns a replacement function.

This:

```text
@decorator
def fn():
    ...
```

means:

```text
fn = decorator(fn)
```

Decorators are used for retries, logging, timing, caching, authentication, and validation.

Start with a very small decorator:

```python
import functools

def announce(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print("calling", fn.__name__)
        return fn(*args, **kwargs)
    return wrapper

@announce
def add(a: int, b: int) -> int:
    return a + b

print(add(2, 3))
```

What happened:

+ `announce` received the original `add` function.
+ It created `wrapper`, which prints before calling `add`.
+ It returned `wrapper`.
+ The name `add` now points to `wrapper`, not directly to the original function.

Now a retry decorator:

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

Read the retry decorator from the inside out:

+ `fetch()` is the business function.
+ `@retry(attempts=3)` builds a decorator with a setting.
+ `decorate(fn)` receives `fetch`.
+ `wrapper(*args, **kwargs)` runs instead of `fetch`.
+ The wrapper calls `fetch`, catches transient errors, and tries again.

Always wrap with `functools.wraps` to preserve the function name and docstring. That keeps logs, traces, and tests readable. Add jitter and a cap to real retry backoff, and retry only transient errors.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What functional tools does Python provide?

Python has small built-in helpers that make common loop patterns shorter.

The most useful ones in day-to-day data code are:

+ `enumerate(items)` when you need position and value.
+ `zip(a, b)` when you want to pair two iterables.
+ `any(...)` when at least one value must be true.
+ `all(...)` when every value must be true.
+ `sorted(items, key=...)` when you need ordered output.

`map`, `filter`, and `reduce` exist, but list comprehensions and generator expressions are often easier to read.

You can learn these tools by translating them back into loops.

`enumerate` gives you an index and a value:

```python
columns = ["order_id", "amount", "status"]

for position, column in enumerate(columns, start=1):
    print(position, column)
```

`zip` pairs values from two iterables:

```python
names = ["order_id", "amount"]
values = ["A1", 10.5]

print(dict(zip(names, values)))
```

`any` and `all` stop as soon as the answer is known:

```python
amounts = [10, 0, 25]

print(any(amount == 0 for amount in amounts))
print(all(amount >= 0 for amount in amounts))
```

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

Type hints explain what kind of values your code expects and returns. They help humans, IDEs, and tools such as `mypy` or `pyright`.

Important: normal Python does not enforce type hints at runtime. This function still runs unless you use a checker:

```python
def add(a: int, b: int) -> int:
    return a + b

print(add(1, 2))
print(add("a", "b"))  # Python allows this because strings support +
```

So why use type hints? Because they make mistakes easier to catch before production. They are documentation that tools can read.

For example, this signature tells the reader three things:

```python
def total_amount(records: list[dict[str, float]]) -> float:
    return sum(record["amount"] for record in records)

print(total_amount([{"amount": 10.5}, {"amount": 2.0}]))
```

It says:

+ `records` should be a list.
+ each item should be a dictionary with string keys and float values.
+ the function returns a float.

Use type hints on public functions, data structures, and boundaries where JSON, CSV, APIs, or database rows enter your code.

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

Run static type checkers from a terminal or CI job, not usually from a notebook:

```text
uv run mypy --strict src/
uv run pyright src/
```

`Protocol` gives structural typing ("anything with a `write` method") so test doubles need not inherit from production classes, and `TypedDict` types dictionary payloads at JSON boundaries.

Use `TypedDict` when you still want dictionaries but want tools to understand the expected keys. Use a dataclass when you want an object with behavior, validation, or methods.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do datetime and time zones work in Python?

Dates and times are one of the easiest ways to create subtle pipeline bugs.

The simple rule is: store and compare timestamps in UTC. Convert to a local timezone only for display or business-calendar logic.

Python has two broad kinds of `datetime`:

+ **naive**: no timezone attached.
+ **aware**: timezone attached through `tzinfo`.

Use aware datetimes for production pipeline code.

The bug usually appears during scheduling, partitioning, or daylight-saving changes. For example, "today" depends on timezone. Midnight in UTC is still the previous day in some local zones.

Use `date` when you mean a calendar day. Use `datetime` when you mean a precise timestamp.

```python
from datetime import date, datetime, timezone

business_day = date(2026, 10, 4)
event_time = datetime(2026, 10, 4, 12, 30, tzinfo=timezone.utc)

print(business_day)
print(event_time)
```

```python
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

utc = datetime(2026, 10, 4, 12, 0, tzinfo=timezone.utc)
new_york = utc.astimezone(ZoneInfo("America/New_York"))

print(utc.isoformat(), new_york.isoformat(), new_york.utcoffset())
print(utc.date(), utc + timedelta(days=1), int(utc.timestamp()))
print(date(2026, 10, 4).strftime("%Y/%m/%d"), (date(2026, 10, 5) - date(2026, 10, 4)).days)
```

What to notice:

+ `utc` and `new_york` represent the same instant.
+ They display different clock times.
+ `timestamp()` is seconds since the Unix epoch.
+ `date` arithmetic gives whole days.

Avoid `datetime.utcnow()` and naive `datetime.now()`: they return values that silently mean "whatever the server thinks". Use `datetime.now(timezone.utc)` and keep durations as `timedelta` until the boundary.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do file I/O, pathlib, JSON, and CSV work?

File code is much easier with `pathlib.Path`. It lets you work with paths as objects instead of manually joining strings.

Common rules:

+ Use `encoding="utf-8"` for text files.
+ Use `newline=""` with the `csv` module.
+ CSV reads values as strings, so convert types yourself.
+ JSON stores one object; newline-delimited JSON stores one object per line and is easier to stream.

The most important habit is to separate three steps:

+ choose a path,
+ read or write text with an encoding,
+ parse the text into Python objects.

This example writes two files under `/tmp`, reads them back, and prints the type difference between JSON and CSV:

Start with a tiny text file:

```python
from pathlib import Path

path = Path("/tmp/python_basics_note.txt")
path.write_text("hello\n", encoding="utf-8")

print(path.exists())
print(path.read_text(encoding="utf-8"))
```

JSON is good for nested records and APIs:

```python
import json

record = {"order_id": "A1", "amount": 10.5, "items": ["book", "pen"]}
payload = json.dumps(record)
back = json.loads(payload)

print(payload)
print(back["items"][0])
```

Newline-delimited JSON is common in logs and data lakes because each line is a complete record:

```python
records = [{"id": 1}, {"id": 2}]
path = Path("/tmp/orders.ndjson")

with path.open("w", encoding="utf-8") as handle:
    for record in records:
        handle.write(json.dumps(record) + "\n")

print(path.read_text(encoding="utf-8"))
```

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

Concurrency means doing overlapping work. Parallelism means truly running work at the same time on multiple CPU cores.

In CPython, the **GIL** lets only one thread execute Python bytecode at a time. That sounds scary, but threads are still useful when the program mostly waits on IO such as network calls, S3 reads, database calls, or API responses.

Use this rough guide:

| Workload | Usual tool |
|---|---|
| Waiting on network or files | threads |
| Heavy CPU work | processes |
| Huge number of network calls | asyncio |

The example below simulates network waiting with sleep:

If your code spends most of its time waiting, concurrency can help. If your code spends most of its time calculating, use processes or a distributed engine such as Spark.

Here is the simple test: if the program is waiting on something outside Python, threads may help. If Python is doing math in a tight loop, threads usually will not help because of the GIL.

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
print(await main())          # notebooks already run an event loop
```

Use `ProcessPoolExecutor` for CPU-bound work (function and data must be picklable), and `asyncio.to_thread` to move unavoidable blocking calls off an event loop. In a normal `.py` script you would call `asyncio.run(main())`; in notebooks, use `await main()` because the kernel already has an event loop.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## How do virtual environments, pip, uv, pyproject, and pytest work?

Use one virtual environment per project. It keeps dependencies for one project from breaking another project.

In simple terms:

+ `venv` creates an isolated Python environment.
+ `pip` installs packages.
+ `uv` is a fast tool for creating environments, installing packages, and using lockfiles.
+ `pyproject.toml` describes the project and dependencies.
+ `pytest` runs tests.

Why this matters: data projects often depend on libraries with native code, cloud SDKs, Spark versions, and CLI tools. If every project installs packages into the same global Python, one project can break another by upgrading a shared package.

These are terminal commands, shown as reference:

```text
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q

uv venv && uv sync --frozen
uv run pytest -q
```

Example `pyproject.toml`:

```toml
[project]
name = "orders-pipeline"
requires-python = ">=3.11"
dependencies = ["httpx>=0.27", "pydantic>=2.7"]

[project.optional-dependencies]
dev = ["pytest>=8", "mypy>=1.11", "ruff>=0.5"]
```

This test example is runnable inside the notebook because it uses plain assertions:

```python
def normalize(value: str) -> str:
    return value.strip().lower()

for raw, expected in [("Us", "us"), ("EU", "eu")]:
    assert normalize(raw) == expected

try:
    if not normalize(""):
        raise ValueError("empty column name")
except ValueError as exc:
    print("caught expected error:", exc)

print("checks passed")
```

In a real project, `pytest` discovers functions whose names start with `test_`. Each test should check one behavior. A failing assertion should tell you exactly what changed.

Pin exact versions in CI (`uv sync --frozen`), keep dev tools in an extra so production images stay small, and make `python -m pytest` the entry point.

[Table of Contents](#Python-Basics-for-Data-Engineers)

## What are the most common Python pitfalls?

These five dominate code review: mutable defaults, late-binding closures, float equality, string building in loops, and shadowing builtins. Each has a one-line fix.

Do not try to memorize every pitfall at once. Learn the symptom and the fix.

| Pitfall | Symptom | Fix |
|---|---|---|
| mutable default | values leak between calls | use `None` then create inside |
| late-binding closure | lambdas all see the last loop value | bind with `i=i` |
| float equality | decimal math surprises you | use `Decimal` or `math.isclose` |
| string building in loops | slow large string creation | collect pieces and `"".join(...)` |
| shadowing builtins | `list` or `sum` stops working | use names like `values`, `total` |

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

Read the output carefully:

+ `add_bad("b")` still remembers `"a"` because the default list was reused.
+ the first lambda list returns `[2, 2, 2]` because all lambdas look at the final value of `i`.
+ `0.1 + 0.2 == 0.3` is false, but `math.isclose(...)` handles approximate float comparison.
+ `"".join(parts)` is the efficient way to build one large string from many pieces.

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
