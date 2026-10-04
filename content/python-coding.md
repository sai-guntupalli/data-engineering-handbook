## [Main title](../README.md)
### [Interview questions](full.md)

# Python Coding Problems for Data Engineers

**Notebook:** [`notebooks/topics/python-coding.ipynb`](../notebooks/topics/python-coding.ipynb) - runnable version of this topic with self-checking exercises.

+ [Problem 1 deduplicate records while preserving order](#Problem-1-deduplicate-records-while-preserving-order)
+ [Problem 2 count frequencies and group by without pandas](#Problem-2-count-frequencies-and-group-by-without-pandas)
+ [Problem 3 sort records with multi field key functions](#Problem-3-sort-records-with-multi-field-key-functions)
+ [Problem 4 rank items with heapq top K and top N per group](#Problem-4-rank-items-with-heapq-top-K-and-top-N-per-group)
+ [Problem 5 sliding window over an event stream](#Problem-5-sliding-window-over-an-event-stream)
+ [Problem 6 two pointers and prefix sums over sorted data](#Problem-6-two-pointers-and-prefix-sums-over-sorted-data)
+ [Problem 7 merge overlapping intervals](#Problem-7-merge-overlapping-intervals)
+ [Problem 8 binary search a sorted partition list](#Problem-8-binary-search-a-sorted-partition-list)
+ [Problem 9 stream a large file with generators](#Problem-9-stream-a-large-file-with-generators)
+ [Problem 10 parse CSV JSON and NDJSON line by line](#Problem-10-parse-CSV-JSON-and-NDJSON-line-by-line)
+ [Problem 11 flatten nested JSON into tabular rows](#Problem-11-flatten-nested-JSON-into-tabular-rows)
+ [Problem 12 hash join two datasets in memory](#Problem-12-hash-join-two-datasets-in-memory)
+ [Problem 13 detect schema drift between batches](#Problem-13-detect-schema-drift-between-batches)
+ [Problem 14 deduplicate late arriving records by key and timestamp](#Problem-14-deduplicate-late-arriving-records-by-key-and-timestamp)
+ [Problem 15 sessionize clickstream events](#Problem-15-sessionize-clickstream-events)
+ [Problem 16 compute percentiles and rolling windows](#Problem-16-compute-percentiles-and-rolling-windows)
+ [Problem 17 implement an LRU cache](#Problem-17-implement-an-LRU-cache)
+ [Problem 18 parse datetimes and normalize time zones](#Problem-18-parse-datetimes-and-normalize-time-zones)
+ [Problem 19 retry with exponential backoff and context managers](#Problem-19-retry-with-exponential-backoff-and-context-managers)
+ [When should you use pandas instead of Python loops](#When-should-you-use-pandas-instead-of-Python-loops)
+ [How do you port a pandas solution to a PySpark equivalent](#How-do-you-port-a-pandas-solution-to-a-PySpark-equivalent)
+ [Real world use cases for Python coding in data engineering](#Real-world-use-cases-for-Python-coding-in-data-engineering)

## Problem 1 deduplicate records while preserving order
Statement: yield the first occurrence of each dedupe key in input order. `set(records)` fails because it loses order and needs hashable rows.

```text
input:  [{"id":"a","v":1}, {"id":"b","v":2}, {"id":"a","v":3}]
output: [{"id":"a","v":1}, {"id":"b","v":2}]
```

```python
from collections.abc import Iterable, Iterator
from typing import Any


def dedupe_first(records: Iterable[dict[str, Any]], key: str = "id") -> Iterator[dict[str, Any]]:
    seen: set[Any] = set()
    for record in records:
        value = record.get(key)
        if value is None or value in seen:
            continue
        seen.add(value)
        yield record
```

Complexity: O(n) time, O(k) memory for k distinct keys. Edge cases: unhashable keys (cast to a tuple first); a null or missing key is dropped by the `value is None` guard, so decide explicitly whether nulls should collapse or survive; an unbounded key space where a Bloom filter or a sort-merge dedupe beats a set.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 2 count frequencies and group by without pandas
Statement: implement `COUNT`, `COUNT(DISTINCT ...)`, `SUM`, and `AVG` grouped by a dimension — the in-memory shape of a warehouse aggregation.

```text
input:  [("us", 10.0), ("eu", 5.0), ("us", 30.0), ("eu", 5.0)]
output: {"us": {"rows": 2, "distinct": 2, "total": 40.0, "avg": 20.0}, ...}
```

```python
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from typing import Any


def aggregate(rows: Iterable[Sequence[Any]]) -> dict[Any, dict[str, Any]]:
    groups: dict[Any, dict[str, Any]] = defaultdict(lambda: {"rows": 0, "seen": set(), "total": 0.0})
    for key, value in rows:
        bucket = groups[key]
        bucket["rows"] += 1
        if value is not None:
            bucket["seen"].add(value)
            bucket["total"] += value
    return {
        key: {"rows": b["rows"], "distinct": len(b["seen"]), "total": b["total"], "avg": b["total"] / b["rows"]}
        for key, b in groups.items()
    }


def frequency(items: Iterable[Any]) -> dict[Any, int]:
    return dict(Counter(items))
```

Complexity: O(n) time; memory is O(groups + distinct values) and the distinct sets dominate. Edge cases: empty input returns `{}`; nulls count as rows but not values (SQL `SUM` semantics); aggregate money as integer cents or `Decimal` to avoid float drift; mixed key types compare equal in Python (`1 == True`), so normalize on ingest.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 3 sort records with multi field key functions
Statement: sort by several fields with mixed direction and nulls last, reproducing `ORDER BY status ASC, amount DESC, id ASC`.

```text
input:  [{"status":"a","amount":3,"id":3}, {"status":"a","amount":1,"id":1},
         {"status":"b","amount":2,"id":2}, {"status":"a","amount":1,"id":4}]
output: [{"status":"a","amount":3,"id":3}, {"status":"a","amount":1,"id":1},
         {"status":"a","amount":1,"id":4}, {"status":"b","amount":2,"id":2}]
```

```python
from typing import Any


def sort_orders(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # ORDER BY status ASC, amount DESC, id ASC.
    return sorted(rows, key=lambda row: (row["status"], -row["amount"], row["id"]))


def sort_nulls_last(rows: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    # A tuple key cannot compare None with numbers; key on a flag first.
    return sorted(rows, key=lambda row: (row[field] is None, row[field]))
```

Complexity: O(n log n) comparisons plus O(n) memory for `sorted`. Edge cases: `None` in a tuple key raises `TypeError` unless a null flag leads it; negating a value fails for strings and `Decimal("NaN")`; naive and aware datetimes cannot be compared; `cmp_to_key` runs Python per comparison and is several times slower than a key function.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 4 rank items with heapq top K and top N per group
Statement: return the K most frequent keys from a large stream. A full sort is O(n log n); a bounded heap is O(n log k) and stores only k elements. The same per-group bounded heap returns the top N rows for each group in one pass.

```text
input:  ["a","b","a","c","a","b","d"], k = 2
output: [("a", 3), ("b", 2)]
```

```python
import heapq
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Any


def top_k(keys: Iterable[Any], k: int) -> list[tuple[Any, int]]:
    return Counter(keys).most_common(k)


def top_k_bounded(keys: Iterable[Any], k: int) -> list[tuple[Any, int]]:
    heap: list[tuple[int, Any]] = []
    for key, count in Counter(keys).items():
        if len(heap) < k:
            heapq.heappush(heap, (count, key))
        elif count > heap[0][0]:
            heapq.heapreplace(heap, (count, key))
    return sorted(((key, count) for count, key in heap), key=lambda item: -item[1])


def top_n_per_group(rows: Iterable[dict[str, Any]], group: str, metric: str, n: int) -> dict[Any, list[dict[str, Any]]]:
    heaps: dict[Any, list[tuple[float, int, dict[str, Any]]]] = defaultdict(list)
    for index, row in enumerate(rows):
        heapq.heappush(heaps[row[group]], (row[metric], index, row))
        if len(heaps[row[group]]) > n:
            heapq.heappop(heaps[row[group]])
    return {key: [row for _value, _index, row in sorted(heap, key=lambda item: -item[0])] for key, heap in heaps.items()}
```

Complexity: `most_common(k)` is O(n log k); the explicit heap is O(n + d log k) for d distinct keys, and `top_n_per_group` is O(n log n) over n rows with O(g x n) memory for g groups. Edge cases: k larger than the distinct count returns all keys; ties need a deterministic secondary sort; one heavy hitter means the counter dominates memory, so a Count-Min Sketch is the scalable answer; unhashable keys must be normalized first.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 5 sliding window over an event stream
Statement: emit the count of events in the trailing window ending at each event without rescanning history — the basis of smoothed metrics and rate limiting.

```text
input:  ts = [0, 1, 2, 10, 11], window = 3
output: [1, 2, 3, 1, 2]
```

```python
from collections import deque
from collections.abc import Iterable


def trailing_counts(timestamps: Iterable[int], window: int) -> list[int]:
    buffer: deque[int] = deque()
    out: list[int] = []
    for current in timestamps:
        buffer.append(current)
        while buffer and buffer[0] <= current - window:
            buffer.popleft()
        out.append(len(buffer))
    return out
```

Complexity: O(n) time because each element enters and leaves the deque once; O(w) memory for a window of w. Edge cases: unsorted input breaks the deque invariant, so sort first or state the assumption; events exactly on the boundary (choose inclusive or exclusive and document it); `window = 0`; timestamps that go backwards from clock skew should be dropped and counted.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 6 two pointers and prefix sums over sorted data
Statement: find two values in a sorted array summing to a target, then answer range-sum queries in O(1) with a prefix-sum array.

```text
input:  nums = [1, 3, 4, 6, 8, 11], target = 10
output: indices (2, 3)
input:  prefix over [2, 4, 6, 8], range [1, 3]
output: 10
```

```python
from itertools import accumulate


def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return left, right
        left, right = (left + 1, right) if total < target else (left, right - 1)
    return None


class RangeSums:
    def __init__(self, values: list[int]) -> None:
        self.prefix = [0, *accumulate(values)]

    def query(self, lo: int, hi: int) -> int:
        # sum(values[lo:hi]): inclusive of lo, exclusive of hi.
        return self.prefix[hi] - self.prefix[lo]
```

Complexity: two pointers is O(n) time and O(1) memory on sorted input; a prefix array builds in O(n) and answers in O(1). Edge cases: duplicates are handled because any valid pair is acceptable; negative values are fine for prefix sums but break a "sum >= target" sliding window; `lo == hi` yields 0; `bisect_left` gives the insertion point a range query needs.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 7 merge overlapping intervals
Statement: merge every overlapping or touching `[start, end)` interval — how a scheduler coalesces file-availability windows and how compaction groups small files.

```text
input:  [[1, 3], [2, 6], [8, 10], [15, 18]]
output: [[1, 6], [8, 10], [15, 18]]
input:  [[1, 4], [4, 5]]
output: [[1, 5]]
```

```python
from collections.abc import Iterable


def merge_intervals(intervals: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(intervals):
        if start > end:
            raise ValueError(f"invalid interval: {(start, end)}")
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged
```

Complexity: O(n log n) for the sort plus O(n) for the sweep and O(n) output memory; the input is not mutated because `sorted` copies. Edge cases: empty input returns `[]`; zero-length intervals; closed intervals need `start < merged[-1][1]` so touching endpoints stay separate; nested intervals are absorbed by `max`; huge coordinates make an interval list better than a bitmap.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 8 binary search a sorted partition list
Statement: a table is stored as sorted ISO-date partitions. Find the partition that can contain a key, or the first partition at or after a watermark, without listing every file.

```text
partitions = ["2026-01-01", "2026-02-01", "2026-03-01", "2026-04-01"]
first_at_or_after("2026-03-15") -> "2026-04-01"
partition_for_key("2026-03-15") -> "2026-03-01"
```

```python
from bisect import bisect_left, bisect_right


def first_at_or_after(partitions: list[str], target: str) -> str | None:
    index = bisect_left(partitions, target)
    return partitions[index] if index < len(partitions) else None


def partition_for_key(partitions: list[str], key: str) -> str | None:
    index = bisect_right(partitions, key) - 1
    return partitions[index] if index >= 0 else None
```

Complexity: O(log n) comparisons and O(1) extra memory; `bisect` is implemented in C and is several times faster than a hand-written loop. Edge cases: an empty list; duplicate partition keys (`bisect_left` gives the first, `bisect_right` the last); the predicate must be monotonic, so date partitions must be zero-padded ISO strings; be explicit about "contains" versus "next" at exact boundaries.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 9 stream a large file with generators
Statement: process a file far larger than RAM on one machine. Read it in bounded batches, transform each batch, and never hold the whole file; generators keep memory flat.

```text
file   : 20_000_000 lines of "user_id,amount"
target : total amount per user with flat memory
```

```python
import gzip
import itertools
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path


def read_lines(path: Path) -> Iterator[str]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            yield line.rstrip("\r\n")


def totals(path: Path) -> dict[str, float]:
    sums: dict[str, float] = defaultdict(float)
    for batch in itertools.batched(read_lines(path), 50_000):
        for line in batch:
            user_id, _, amount = line.partition(",")
            sums[user_id] += float(amount)
    return dict(sums)
```

Complexity: O(n) time, O(batch size + distinct keys) memory. Edge cases: a final line without a newline; CRLF endings; a malformed record should be dead-lettered rather than aborting the file; sniff the gzip magic bytes instead of trusting the suffix; to parallelize, give each worker a byte range and resync to the next newline.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 10 parse CSV JSON and NDJSON line by line
Statement: read the common landing formats without loading them fully: CSV with a header, NDJSON, and a JSON array that must be materialized.

```text
orders.csv   : order_id,amount -- then rows like 1,10.5
orders.ndjson: {"order_id": 1, "amount": 10.5} -- one object per line
orders.json  : [{"order_id": 1, "amount": 10.5}]
```

```python
import csv
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def read_csv(path: Path) -> Iterator[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        yield from csv.DictReader(handle)


def read_ndjson(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"bad NDJSON at line {number}") from exc
```

Complexity: O(n) time and O(1) memory for CSV and NDJSON; a JSON array is O(n) memory because the structure must exist. Edge cases: a UTF-8 BOM (`utf-8-sig`); embedded newlines inside quoted CSV fields, which `csv` handles; very long NDJSON lines; empty strings that break `float`; deeply nested JSON needs `ijson` or `jsonlines` for real streaming.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 11 flatten nested JSON into tabular rows
Statement: turn nested order documents into one row per line item with parent fields repeated, the in-memory equivalent of `UNNEST` or `LATERAL VIEW explode`.

```text
input:  {"order_id":1, "customer":{"country":"us"}, "items":[{"sku":"a","qty":2},{"sku":"b","qty":1}]}
output: [{"order_id":1,"country":"us","sku":"a","qty":2}, {"order_id":1,"country":"us","sku":"b","qty":1}]
```

```python
from collections.abc import Iterator
from typing import Any


def explode_order(order: dict[str, Any]) -> Iterator[dict[str, Any]]:
    base = {"order_id": order["order_id"], "country": order.get("customer", {}).get("country")}
    for item in order.get("items") or [{}]:
        yield {**base, "sku": item.get("sku"), "qty": item.get("qty")}


def flatten(payload: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in payload.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            out.update(flatten(value, path))
        elif isinstance(value, list):
            for index, element in enumerate(value):
                nested = flatten(element, f"{path}[{index}]") if isinstance(element, dict) else {f"{path}[{index}]": element}
                out.update(nested)
        else:
            out[path] = value
    return out
```

Complexity: O(nodes) time and O(depth) recursion. Edge cases: a missing `customer` key; an empty `items` array should emit the parent row once with nulls to match a left join; arrays of arrays; a literal key containing the flatten separator colliding with a nested path.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 12 hash join two datasets in memory
Statement: join a large fact stream to a small dimension without a database. Build a hash map on the smaller side and stream the larger side through it — the same shape as a broadcast join. Both sides are `(join_key, payload)` tuples, so the fact carries the key in the same position as the dimension.

```text
facts      : [("c1","o1"), ("c2","o2"), ("c9","o3")]
dimensions : [("c1","Alice"), ("c2","Bob")]
output     : [("c1","o1","Alice"), ("c2","o2","Bob")]
```

```python
from collections import defaultdict
from collections.abc import Iterable, Iterator
from typing import Any, TypeVar

K = TypeVar("K")
V = TypeVar("V")


def hash_join(facts: Iterable[tuple[K, V]], dimensions: Iterable[tuple[K, V]], how: str = "inner", null: Any = None) -> Iterator[tuple[K, V, Any]]:
    index: dict[K, list[V]] = defaultdict(list)
    for key, value in dimensions:
        index[key].append(value)
    for key, fact_value in facts:
        matches = index.get(key)
        if matches:
            for dim_value in matches:
                yield key, fact_value, dim_value
        elif how == "left":
            yield key, fact_value, null
```

Complexity: O(n + m) time and O(m) memory for the m-row build side; always build on the smaller side or the join materializes the large table. Edge cases: duplicate build-side keys multiply rows, which is correct SQL semantics; null keys never match in SQL; `1` versus `"1"` key types silently drop rows, so normalize on ingest; a single skewed key defeats the in-memory approach and needs a sort-merge or distributed shuffle.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 13 detect schema drift between batches
Statement: compare today's schema to yesterday's and classify each field as added, removed, or retyped. Silent type changes are the classic cause of a pipeline that "worked yesterday".

```text
baseline: {"id": "int", "amount": "float"}
current : {"id": "int", "amount": "str", "coupon": "str"}
drift   : {"added": ["coupon"], "removed": [], "retyped": ["amount"]}
```

```python
from collections.abc import Iterable, Mapping
from typing import Any


def infer_columns(rows: Iterable[Mapping[str, Any]]) -> dict[str, set[str]]:
    columns: dict[str, set[str]] = {}
    for row in rows:
        for key, value in row.items():
            if value is not None:
                columns.setdefault(key, set()).add(type(value).__name__)
    return columns


def type_of(types: set[str]) -> str:
    if not types:
        return "null"
    return next(iter(types)) if len(types) == 1 else "mixed(" + "|".join(sorted(types)) + ")"


def detect_drift(baseline: Mapping[str, set[str]], current: Mapping[str, set[str]]) -> dict[str, list[str]]:
    base, now = set(baseline), set(current)
    retyped = sorted(col for col in base & now if type_of(baseline[col]) != type_of(current[col]))
    return {"added": sorted(now - base), "removed": sorted(base - now), "retyped": retyped}
```

Complexity: O(rows x columns) to infer and O(columns) to diff; diffing declared Parquet or Avro metadata is O(columns) and much cheaper than sampling. Edge cases: all-null columns have no type; int-to-float widening is benign while string-to-number is breaking; column order changes are invisible to a set diff but break positional CSV reads; compare against the catalog schema, not just yesterday's file.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 14 deduplicate late arriving records by key and timestamp
Statement: a retry or backfill replays records out of order. Keep only the record with the latest `updated_at` per key, deterministically when timestamps tie.

```text
input:  [("u1","t1"), ("u2","t1"), ("u1","t3"), ("u1","t2")]
output: u1 -> the t3 record, u2 -> the t1 record
```

```python
from collections.abc import Iterable
from typing import Any


def latest_wins(records: Iterable[dict[str, Any]], key: str = "id", ts: str = "updated_at", tiebreak: str = "version") -> list[dict[str, Any]]:
    winners: dict[Any, dict[str, Any]] = {}
    for record in records:
        current = winners.get(record[key])
        if current is None or (record[ts], record.get(tiebreak, 0)) > (current[ts], current.get(tiebreak, 0)):
            winners[record[key]] = record
    return list(winners.values())
```

Complexity: O(n) time and O(k) memory for k distinct keys; a table-level `MERGE` or a sort-merge by key spills to disk instead. Edge cases: equal timestamps need a version or Kafka offset tiebreak; naive and aware datetimes cannot be compared, so normalize to UTC on read; tombstone rows (`op="delete"`) must win and be applied by the writer; producer clock skew makes the ingestion timestamp more trustworthy for lateness.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 15 sessionize clickstream events
Statement: group ordered user events into sessions, starting a new session after a gap of inactivity — the exercise behind every product-analytics model.

```text
input:  u1 at [10:00, 10:05, 10:40, 11:00], gap = 30m
output: [10:00-10:05], [10:40-11:00]
```

```python
from collections.abc import Iterable, Iterator
from datetime import datetime, timedelta
from typing import Any


def sessionize(events: Iterable[tuple[str, datetime, str]], gap: timedelta) -> Iterator[dict[str, Any]]:
    current: dict[str, Any] | None = None
    for user_id, when, event_id in events:
        if current is None or current["user_id"] != user_id or when - current["end"] >= gap:
            if current is not None:
                yield current
            current = {"user_id": user_id, "start": when, "end": when, "events": 1, "event_ids": [event_id]}
        else:
            current["end"] = when
            current["events"] += 1
            current["event_ids"].append(event_id)
    if current is not None:
        yield current
```

Complexity: O(n log n) if the input must be sorted per user, O(n) if the source already delivers ordered partitions, with O(1) state per active user. Edge cases: out-of-order events need a lateness buffer before emitting; one event forms a one-event session; define `>=` versus `>` at the boundary (the code treats exactly 30 minutes as inactive); users with no events are absent, so downstream joins must be left joins.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 16 compute percentiles and rolling windows
Statement: compute p50, p95, and p99 latency plus a rolling mean. Percentiles drive capacity and SLO decisions because the mean hides the tail.

```text
input:  latencies = [10.0, 12.0, 13.0, 15.0, 20.0, 100.0]
output: {"p50": 13.0, "p95": 100.0, "p99": 100.0}
input:  daily = [1, 2, 3, 4, 5], window = 3
output: [None, None, 2.0, 3.0, 4.0]
```

```python
import math
from collections import deque


def percentile_nearest_rank(values: list[float], pct: float) -> float:
    if not values:
        raise ValueError("empty sample")
    ordered = sorted(values)
    return ordered[max(1, math.ceil(pct / 100 * len(ordered))) - 1]


class RollingStats:
    def __init__(self, window: int) -> None:
        self.window = window
        self.values: deque[float] = deque()
        self.total = 0.0

    def push(self, value: float) -> None:
        self.values.append(value)
        self.total += value
        if len(self.values) > self.window:
            self.total -= self.values.popleft()

    def mean(self) -> float | None:
        return self.total / self.window if len(self.values) == self.window else None
```

Complexity: a full sort is O(n log n) with O(1) per percentile afterward; an exact streaming percentile is O(log n) per insert with an order-statistic tree, or O(1) with a t-digest. Edge cases: empty samples raise; with fewer than 100 points p99 is just the maximum, so p99 on low-traffic endpoints is noise; nearest-rank and linear interpolation differ, so document which the metric uses; percentiles are not additive across buckets.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 17 implement an LRU cache
Statement: implement a fixed-capacity least-recently-used cache — the eviction policy behind dimension caches and metadata caches in a pipeline.

```text
capacity 2: put("a",1) put("b",2) get("a") -> 1; put("c",3) evicts "b"
```

```python
from collections import OrderedDict
from collections.abc import Hashable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._data: OrderedDict[K, V] = OrderedDict()

    def get(self, key: K) -> V | None:
        if key not in self._data:
            return None
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: K, value: V) -> None:
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)
```

Complexity: O(1) amortized for `get` and `put` because `OrderedDict` is a hash map plus a doubly linked list. Edge cases: capacity zero silently stores nothing because every insert is evicted immediately, so validate capacity up front; returning `None` is ambiguous when `None` is a legal cached value, so use a sentinel; a manual implementation must update both the map and the list on every hit and eviction; `functools.lru_cache` is faster for pure functions but cannot key on a mutable object.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 18 parse datetimes and normalize time zones
Statement: parse mixed timestamp formats from producers and normalize them to UTC so partitioning, windows, and joins are correct.

```text
input:  ["2026-10-04T13:00:00Z", "2026-10-04T09:00:00-04:00", "2026-10-04 13:00:00"]
output: all three become the same UTC instant 2026-10-04T13:00:00+00:00
```

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def parse_iso(value: str) -> datetime:
    # Python 3.11+ accepts "Z"; replace defensively for wider input.
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def to_utc(value: datetime, assume_tz: str = "UTC") -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=ZoneInfo(assume_tz))
    return value.astimezone(timezone.utc)
```

Complexity: O(1) per timestamp, with `zoneinfo` caching zone lookups after the first load. Edge cases: DST makes local times ambiguous or nonexistent, so store UTC plus the original zone; naive timestamps silently become wrong under a permissive assumption; epoch seconds versus milliseconds differ by 1000x; `fromisoformat` rejects some real formats, so keep a fallback format list or `dateutil`.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Problem 19 retry with exponential backoff and context managers
Statement: wrap a flaky API call in capped exponential backoff with jitter, and wrap a pipeline run in a context manager that records success or failure.

```text
attempt 1 fails -> sleep uniform(0, 0.5)
attempt 2 fails -> sleep uniform(0, 1.0)
attempt 3 fails -> sleep uniform(0, 2.0), ...
```

```python
import random
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any, TypeVar

T = TypeVar("T")


class Retryable(Exception):
    pass


def retry_with_backoff(func: Callable[[], T], attempts: int = 5, base: float = 0.5, max_sleep: float = 30.0) -> T:
    for attempt in range(attempts):
        try:
            return func()
        except Retryable:
            if attempt == attempts - 1:
                raise
            # Full jitter spreads retries so a recovering service is not stampeded.
            time.sleep(random.uniform(0, min(max_sleep, base * 2**attempt)))
    raise RuntimeError("unreachable")


@contextmanager
def pipeline_run(name: str, logger: Any) -> Iterator[dict[str, Any]]:
    run: dict[str, Any] = {"name": name, "status": "running"}
    try:
        yield run
        run["status"] = "success"
    except Exception:
        run["status"] = "failed"
        raise
    finally:
        logger.info("run finish", extra={"run": name, "status": run["status"]})
```

Complexity: O(1) extra memory, with total sleep bounded by `attempts x max_sleep`. Edge cases: only retry idempotent operations or a retried write duplicates data; retry only transient errors such as timeouts, 429, and 503 and fail fast on 400 or 401; cap attempts so a bad deploy does not hang a scheduler slot; jitter is mandatory or synchronized clients create retry storms; the context manager must re-raise after recording so the orchestrator still fails.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## When should you use pandas instead of Python loops
Loops are simple but run per row in the interpreter; pandas runs vectorized operations in C over whole columns. Use pure Python for control flow and row-level logic, and pandas (or Polars and DuckDB) as soon as a transformation is column-wise or group-wise.

```python
from time import perf_counter

import pandas as pd


def margin_loop(frame: pd.DataFrame) -> list[float]:
    out: list[float] = []
    for row in frame.itertuples(index=False):
        out.append((row.revenue - row.cost) / row.revenue if row.revenue else 0.0)
    return out


def margin_vectorized(frame: pd.DataFrame) -> pd.Series:
    return ((frame["revenue"] - frame["cost"]) / frame["revenue"]).fillna(0.0)


def benchmark(rows: int = 200_000) -> dict[str, float]:
    frame = pd.DataFrame({"revenue": [100.0] * rows, "cost": [70.0] * rows})
    start = perf_counter()
    margin_loop(frame)
    loop_seconds = perf_counter() - start
    start = perf_counter()
    margin_vectorized(frame)
    return {"loop_seconds": loop_seconds, "vector_seconds": perf_counter() - start}
```

Stay in pandas when the data fits comfortably in memory (roughly a few gigabytes), the transformation is column arithmetic, `groupby`, `merge`, or a rolling window, and a cluster is not worth the serialization tax. Stay in pure Python when data is streamed, the per-record logic is branchy, or the work is orchestration and API calls. Move to Polars or DuckDB when pandas hits memory or speed limits, and to Spark only when data no longer fits one machine or the shuffle truly needs a cluster.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## How do you port a pandas solution to a PySpark equivalent
The port is mechanical once the grain is clear: `groupby` becomes `groupBy`, a pandas merge becomes a join, and any row-by-row `apply` must become column expressions or a window.

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("port").getOrCreate()
orders = spark.read.parquet("s3://acme/orders/")
customers = spark.read.parquet("s3://acme/customers/")

# pandas: orders.merge(customers, on="customer_id").groupby("country")["amount"].sum()
summary = (
    orders.join(customers, on="customer_id", how="left")
    .groupBy("country")
    .agg(F.count("*").alias("rows"), F.sum("amount").alias("revenue"))
)

# pandas: orders.sort_values("updated_at").drop_duplicates("order_id", keep="last")
window = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
deduped = orders.withColumn("_rank", F.row_number().over(window)).filter(F.col("_rank") == 1).drop("_rank")
```

Adaptation notes: keep data in the JVM and never call `toPandas()` on a large frame because it collects everything to the driver; replace `apply(axis=1)` with `F.when` or `F.expr` and use `pandas_udf` only when vectorized UDFs are unavoidable; partition and bucket join keys so the shuffle stays bounded; prefer built-in aggregates over Python UDFs, which serialize per row and disable Catalyst. Keep the pandas version as the correctness oracle in tests and compare both on a small sample.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)

## Real world use cases for Python coding in data engineering
### 1. Deduplicating an at-least-once event stream
A Kafka consumer delivers duplicates after rebalances. Before writing to the lake, the sink keeps the newest record per event id, using the Kafka offset as a deterministic tiebreak.

```python
def collapse_batch(batch: list[dict]) -> list[dict]:
    best: dict[str, dict] = {}
    for record in batch:
        rank = (record["updated_at"], record["offset"])
        current = best.get(record["event_id"])
        if current is None or rank > (current["updated_at"], current["offset"]):
            best[record["event_id"]] = record
    return list(best.values())
```

Why it matters: idempotent sinks are the difference between a duplicate incident and a rerun, and the offset tiebreak makes the result reproducible.

### 2. Streaming a 200 GB CSV on one machine
A nightly finance export does not fit in memory. The job streams rows through `csv.DictReader`, keeps running totals in a dict, and writes Parquet in 50,000-row batches.

Why it matters: one machine with flat memory often beats provisioning a cluster and paying the serialization tax.

### 3. Hash-joining facts to a reference table
An enrichment job loads a 50,000-row country and currency reference into a dict, then streams 40M fact rows through it, replacing one database round trip per row.

```python
reference = {code: name for code, name in load_countries()}
enriched = ({"country": reference.get(row["code"], "unknown"), **row} for row in facts())
```

Why it matters: one broadcast-side dict turns an O(n x m) lookup pattern into O(n), which is the same principle a Spark broadcast join uses.

### 4. Retry and dead-letter handling for partner APIs
Partner APIs rate-limit and time out. The extractor retries transient failures with exponential backoff and jitter, and writes exhausted pages to a quarantine prefix with the cursor that produced them.

Why it matters: storing the cursor, not just the error, lets the next run resume from the last good page instead of re-reading the day.

### 5. Sessionizing clickstream data before the warehouse load
A product-analytics pipeline turns raw click events into sessions in the transform step, so the BI layer reads pre-aggregated session tables instead of scanning billions of raw events per dashboard load.

```python
from datetime import timedelta

sessions = list(sessionize(ordered_events, gap=timedelta(minutes=30)))
session_rows = [{"user_id": s["user_id"], "start": s["start"], "end": s["end"], "events": s["events"]} for s in sessions]
```

Why it matters: pre-computing a stateful window function once is far cheaper than repeating it per query, and the logic stays testable in plain Python.

[Table of Contents](#Python-Coding-Problems-for-Data-Engineers)
