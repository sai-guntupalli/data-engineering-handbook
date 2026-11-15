import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from nbtools import build, run

PATH = "notebooks/topics/ingestion/ingestion-02-apis.ipynb"
SPEC = """%% md
# Ingestion 2: APIs, pagination and retries

SaaS tools and partner systems expose data through HTTP APIs that page their results, limit your request rate and
fail now and then. This lesson writes an API extractor with `httpx` and checks it against a fake API: comparing
offset and cursor pagination while data changes, retrying with backoff, pulling incrementally with an overlap
window, and validating records before they land.

The API is served by `httpx.MockTransport`, which hands each request to a Python function instead of the network.
The client code is exactly what you would point at a real base URL.
%% code
# Setup: install notebook dependencies in Colab.
!pip install -q httpx
%% md
## Setup and sample data

The next cell defines the fake API's data, seven orders, and a `client` helper that builds an `httpx.Client` around
any handler function. Each section adds the endpoint behavior it needs.
%% code
import random

import httpx

orders = [{"id": i, "cents": 100 * i, "updated_at": f"2026-02-01T09:{i:02d}:00Z"} for i in range(1, 8)]


def client(handler):
    return httpx.Client(base_url="https://api.example.com", transport=httpx.MockTransport(handler))


print(len(orders), "orders; newest:", orders[-1])
%% md
## Offset pagination shifts under you

Many APIs page with `offset` and `limit`, newest first. If a record is inserted while you page, every later record
shifts by one position: the next page repeats a record you already have, and a deletion makes you skip one instead.
**Cursor pagination** (the API returns an opaque `next` token tied to the last record) is stable under inserts.

**Where it matters**

Busy sources change during a long extract. Prefer an API's cursor or `since` parameters when it offers them, and always
deduplicate by ID when it does not.

**Watch out for**

Do not build your own cursor from a page number or a count; and stop if the API ever returns a cursor you have seen
before, or a bug on either side turns the extract into an infinite loop.
%% code
requests = []


def paged_api(request):
    requests.append(request)
    if len(requests) == 2:  # a new order arrives just before the second page is requested
        orders.append({"id": 8, "cents": 800, "updated_at": "2026-02-01T09:08:00Z"})
    newest_first = sorted(orders, key=lambda o: o["id"], reverse=True)
    if "offset" in request.url.params:
        offset, limit = int(request.url.params["offset"]), int(request.url.params["limit"])
        return httpx.Response(200, json={"data": newest_first[offset : offset + limit]})
    after = int(request.url.params.get("after", 10**9))
    page = [o for o in newest_first if o["id"] < after][:3]
    return httpx.Response(200, json={"data": page, "next": page[-1]["id"] if len(page) == 3 else None})


with client(paged_api) as api:
    seen, offset = [], 0
    while page := api.get("/orders", params={"offset": offset, "limit": 3}).json()["data"]:
        seen += [o["id"] for o in page]
        offset += 3
print("offset pages:", seen)

orders.pop()  # remove order 8, then replay the same arrival with cursor paging
requests.clear()
with client(paged_api) as api:
    seen, after = [], None
    while True:
        body = api.get("/orders", params={"after": after} if after else {}).json()
        seen += [o["id"] for o in body["data"]]
        if body["next"] is None:
            break
        after = body["next"]
print("cursor pages:", seen)
%% md
**What to notice:** Order 8 arrived after the first page. Every older order shifted down one position, so the offset
extract read order 5 twice. The cursor extract asked for orders older than the last one it had, so nothing shifted
and each order arrived exactly once. Both missed order 8, which is newer than where they started; the next run
picks it up.
%% md
## Retries with backoff

APIs fail transiently: `429 Too Many Requests` (often with a `Retry-After` header) and `5xx` errors usually succeed
on a later attempt, while `4xx` errors such as `400` or `401` will not. A robust client retries only the first kind,
waits longer after each failure (**exponential backoff**), adds randomness (**jitter**) so many clients do not retry in
lockstep, honours `Retry-After`, and gives up after a fixed budget.

**Where it matters**

Rate limits are normal operation for API extracts, not an error. Without backoff, a pipeline either hammers the API
into longer bans or fails on the first hiccup.

**Watch out for**

Retry only requests that are safe to repeat. A `GET` is; a `POST` that creates something may already have succeeded
before the error. The sleep function is passed in below so the lesson can record the waits instead of sleeping.
%% code
def get_with_retries(api, path, sleep, attempts=5, base=0.5):
    for attempt in range(attempts):
        response = api.get(path)
        if response.status_code < 400:
            return response.json()
        if response.status_code != 429 and response.status_code < 500:
            response.raise_for_status()  # a client error: retrying cannot fix it
        retry_after = response.headers.get("Retry-After")
        delay = float(retry_after) if retry_after else base * 2**attempt * random.uniform(0.5, 1.5)
        sleep(delay)
    raise RuntimeError(f"gave up on {path} after {attempts} attempts")


responses = iter([httpx.Response(503), httpx.Response(429, headers={"Retry-After": "2"}), httpx.Response(503),
                  httpx.Response(200, json={"ok": True})])
waits = []
random.seed(7)
with client(lambda request: next(responses)) as api:
    print("result:", get_with_retries(api, "/orders", sleep=waits.append))
print("waits:", [round(w, 2) for w in waits])

with client(lambda request: httpx.Response(400, json={"error": "bad parameter"})) as api:
    try:
        get_with_retries(api, "/orders", sleep=waits.append)
    except httpx.HTTPStatusError as error:
        print("not retried:", error.response.status_code)
%% md
**What to notice:** The client succeeded on the fourth attempt. The two `503` waits come from the backoff formula,
growing and jittered, while the `429` wait is exactly the 2 seconds the server asked for. The `400` failed at once
with no retry, because sending the same bad request again cannot help.
%% md
## Incremental pulls with an overlap window

APIs that accept `updated_since` let each run ask only for records changed after the last run's high-water mark. Clocks
and replication lag mean a record can appear with a timestamp slightly older than the mark, so ask from a little
**before** it (an overlap window) and deduplicate by ID, keeping the newest version.

**Where it matters**

This is the same pattern as the incremental database extract in Ingestion 1, applied to APIs: it keeps each run small
without losing late records.

**Watch out for**

Save the new high-water mark only after the records are stored, and compute it from the records you received, not from
the clock: the API's clock and yours can disagree.
%% code
from datetime import datetime, timedelta


def since_api(request):
    since = request.url.params["updated_since"]
    return httpx.Response(200, json={"data": [o for o in orders if o["updated_at"] > since]})


landed = {o["id"]: o for o in orders[:5]}  # yesterday's run stored orders 1-5
watermark = max(o["updated_at"] for o in landed.values())
orders[1] = {**orders[1], "cents": 250, "updated_at": "2026-02-01T09:04:30Z"}  # late: older than the watermark

overlap = (datetime.fromisoformat(watermark.replace("Z", "+00:00")) - timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
with client(since_api) as api:
    for record in api.get("/orders", params={"updated_since": overlap}).json()["data"]:
        current = landed.get(record["id"])
        if current is None or record["updated_at"] >= current["updated_at"]:
            landed[record["id"]] = record
print("asked from", overlap, "instead of", watermark)
print("order 2 now:", landed[2]["cents"], "| ids:", sorted(landed))
%% md
**What to notice:** Order 2 changed with a timestamp of 09:04:30, older than the 09:05 watermark, so a plain
`updated_since=watermark` would have missed it. Asking from two minutes earlier picked it up (now 250 cents), and the
overlap's repeated records replaced themselves by ID.
%% md
## Validate before landing

An API response is untrusted input. Check each record's required fields and types before it reaches a table, and
send records that fail to a **quarantine** with the reason, instead of failing the whole run or silently loading bad
values.

**Where it matters**

Partners change formats without warning: an amount sent as `"12.00"` instead of `1200`, a missing ID. Quarantining
keeps the good records flowing and leaves an exact list to send back.

**Watch out for**

Alert on the quarantine's size. A quarantine nobody reads is just a slower way to lose data, and a sudden spike usually
means the API changed, not that the data got worse.
%% code
payload = orders[:3] + [{"id": 9, "cents": "12.00", "updated_at": "2026-02-01T10:00:00Z"}, {"cents": 500}]


def problems(record):
    found = []
    if not isinstance(record.get("id"), int):
        found.append("id missing or not an integer")
    if not isinstance(record.get("cents"), int):
        found.append(f"cents is {type(record.get('cents')).__name__}, expected int")
    return found


good = [r for r in payload if not problems(r)]
quarantine = [(r, problems(r)) for r in payload if problems(r)]
print("to load:", [r["id"] for r in good])
for record, reasons in quarantine:
    print("quarantined:", record, reasons)
%% md
**What to notice:** Three records passed. Order 9 was quarantined because its amount arrived as text, and the last
record because it has no ID; each carries the reason, so the problem can be reported back precisely.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Exhaust the retry budget

**Difficulty:** Easy · about 5 min

Point `get_with_retries` at an API that always returns `503` and show the error and the number of waits.
%% code
# Try your solution here.
%% solution
waits = []
with client(lambda request: httpx.Response(503)) as api:
    try:
        get_with_retries(api, "/orders", sleep=waits.append, attempts=3)
    except RuntimeError as error:
        print(error, "| waits:", len(waits))
%% md
### Exercise 2: The next watermark

**Difficulty:** Easy · about 5 min

Compute the high-water mark to save after the incremental pull, from the records in `landed`.
%% code
# Try your solution here.
%% solution
print(max(record["updated_at"] for record in landed.values()))
%% md
### Exercise 3: A new validation rule

**Difficulty:** Medium · about 10 min

Extend `problems` so negative amounts are quarantined too, and run it on a record with `cents=-50`.
%% code
# Try your solution here.
%% solution
def problems_v2(record):
    found = problems(record)
    if isinstance(record.get("cents"), int) and record["cents"] < 0:
        found.append("cents is negative")
    return found


print(problems_v2({"id": 10, "cents": -50}), problems_v2({"id": 11, "cents": 50}))
%% md
## Key takeaways

- Offset pagination repeats or skips records when data changes mid-extract; prefer cursor or `since` parameters, and
  deduplicate by ID either way.
- Retry `429` and `5xx` with exponential backoff, jitter, `Retry-After` and a budget; never retry `4xx` client errors
  or unsafe requests.
- Pull incrementally from slightly before the last high-water mark and keep the newest version of each ID.
- Validate every record and quarantine failures with a reason, then alert on the quarantine.
%% md
**Next:** [Ingestion 3: Object storage and manifests](ingestion-03-object-storage.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
