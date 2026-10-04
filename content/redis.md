## [Main title](../README.md)
### [Interview questions](full.md)

# Redis for Data Engineers

**Notebook:** [`notebooks/topics/redis.ipynb`](../notebooks/topics/redis.ipynb) - runnable version of this topic with self-checking exercises.

Redis (REmote DIctionary Server) is a single-process, in-memory key/value server that stores values as typed data structures and speaks RESP. Commands execute one at a time on the main thread, so each command is atomic and a Lua script is atomic as a whole.

The keyspace holds strings, hashes, lists, sets, sorted sets, streams, bitmaps, and HyperLogLogs; every key can carry a TTL; durability comes from RDB snapshots and the append-only file; replication and Redis Cluster provide availability and horizontal scale. A data engineer meets it as a cache in front of a warehouse, a dedupe and rate-limit layer at the API edge, a session store, a leaderboard, and a small event queue.

+ [What is Redis?](#What-is-Redis)
+ [What core data structures does Redis provide?](#What-core-data-structures-does-Redis-provide)
+ [How do you use bitmaps and HyperLogLog in Redis?](#How-do-you-use-bitmaps-and-HyperLogLog-in-Redis)
+ [How do Redis TTL and expiration work?](#How-do-Redis-TTL-and-expiration-work)
+ [How does Redis persistence work with RDB and AOF?](#How-does-Redis-persistence-work-with-RDB-and-AOF)
+ [How do eviction policies and maxmemory work?](#How-do-eviction-policies-and-maxmemory-work)
+ [How does Redis replication work?](#How-does-Redis-replication-work)
+ [What is Redis Sentinel and when do you need it?](#What-is-Redis-Sentinel-and-when-do-you-need-it)
+ [How does Redis Cluster shard data?](#How-does-Redis-Cluster-shard-data)
+ [How do pipelining and transactions with MULTI work?](#How-do-pipelining-and-transactions-with-MULTI-work)
+ [How do you use Lua scripting in Redis?](#How-do-you-use-Lua-scripting-in-Redis)
+ [What is the difference between pub/sub and Streams?](#What-is-the-difference-between-pubsub-and-Streams)
+ [How do consumer groups and pending entries work in Redis Streams?](#How-do-consumer-groups-and-pending-entries-work-in-Redis-Streams)
+ [What caching patterns work with Redis?](#What-caching-patterns-work-with-Redis)
+ [How do you prevent a cache stampede?](#How-do-you-prevent-a-cache-stampede)
+ [How do you implement a distributed lock in Redis?](#How-do-you-implement-a-distributed-lock-in-Redis)
+ [How do you build a rate limiter with Redis?](#How-do-you-build-a-rate-limiter-with-Redis)
+ [How do you use Redis for idempotency and deduplication?](#How-do-you-use-Redis-for-idempotency-and-deduplication)
+ [How do you build a leaderboard or trending list with Redis?](#How-do-you-build-a-leaderboard-or-trending-list-with-Redis)
+ [How do you use Redis as a session store?](#How-do-you-use-Redis-as-a-session-store)
+ [Redis Streams vs Kafka for a lightweight queue?](#Redis-Streams-vs-Kafka-for-a-lightweight-queue)
+ [Redis vs Memcached vs Kafka?](#Redis-vs-Memcached-vs-Kafka)
+ [How do you size Redis memory and handle hot keys?](#How-do-you-size-Redis-memory-and-handle-hot-keys)
+ [How do you monitor and operate Redis in production?](#How-do-you-monitor-and-operate-Redis-in-production)
+ [Real world use cases for Redis](#Real-world-use-cases-for-Redis)

## What is Redis?

Redis is an in-memory key/value server whose values are data structures, not just blobs. Execution is single-threaded, so `INCR`, `LPUSH`, and a Lua script are atomic without a lock, and the operational model is a keyspace replicated to read replicas and sharded across a cluster.

```bash
redis-cli SET product:1001 '{"sku":"A1","price":249.00}' EX 3600
redis-cli GET product:1001
redis-cli TTL product:1001
redis-cli INFO memory | head -5
```

What an interviewer wants named: strings, hashes, lists, sets, sorted sets, streams, bitmaps, and HyperLogLogs; per-key TTL; RDB and AOF persistence; replication; Redis Cluster with 16384 hash slots; pub/sub; transactions; and Lua scripting.

[Table of Contents](#Redis-for-Data-Engineers)

## What core data structures does Redis provide?

Each type maps to a real access pattern, and picking the wrong one is the most common design mistake. A hash is right for an object you update field by field; a string is right for a value you always read and write whole.

```text
SET page:home:views 0              # string counter
INCR page:home:views
HSET user:42 name Ada plan pro     # hash: independent fields
HINCRBY user:42 logins 1
LPUSH feed:user:42 post:9001       # list: bounded feed
LTRIM feed:user:42 0 499
SADD article:9001:seen user:7      # set: membership and dedupe
SISMEMBER article:9001:seen user:7
ZADD leaderboard 1500 user:7       # sorted set: ranking by score
ZINCRBY leaderboard 25 user:7
XADD events:orders '*' order_id 1001 amount 249.00
```

Small collections use compact encodings (`listpack`, `intset`) that become hash tables and skiplists past a threshold. A sorted set is a hash table plus a skiplist, so `ZADD` is O(log n) and a range read is O(log n + m).

[Table of Contents](#Redis-for-Data-Engineers)

## How do you use bitmaps and HyperLogLog in Redis?

Bitmaps are strings addressed by bit offset and answer cheap boolean questions about integer ids: daily active users, feature flags, or which of a million users clicked. HyperLogLog counts distinct elements in a fixed 12 KB per key with about 0.81% standard error, far cheaper than a set holding every id.

```bash
redis-cli SETBIT dau:2026-10-04 42 1
redis-cli BITCOUNT dau:2026-10-04
redis-cli BITOP AND retained:d1d2 dau:2026-10-03 dau:2026-10-04
redis-cli PFADD uv:page:home user:42 user:77 user:42
redis-cli PFCOUNT uv:page:home
redis-cli PFMERGE uv:site uv:page:home uv:page:search
```

The trade-off is exactness: `BITCOUNT` is exact, `PFCOUNT` is an estimate and cannot be read back element by element. Neither supports deleting one element, so use daily keys that expire rather than mutating one long-lived bitmap.

[Table of Contents](#Redis-for-Data-Engineers)

## How do Redis TTL and expiration work?

`EXPIRE`, `PEXPIRE`, and `SET ... EX` set a TTL; `TTL` reads it; `PERSIST` removes it. Expiration belongs to the key, so a plain `SET` clears the TTL - a classic bug when refreshing a cached value.

```text
SET session:abc '{"uid":42}' EX 1800
EXPIRE session:abc 1800
TTL session:abc                 # -1 no expiry, -2 key missing
SET cache:report:q3 'new' KEEPTTL
GETEX cache:report:q3 EX 600
```

Redis expires keys lazily on access and actively by sampling keys with a TTL in the background, so memory can exceed the live set briefly. A replica does not expire keys on its own; it waits for the primary's `DEL` and only hides logically expired keys from reads, so the memory is not reclaimed until that `DEL` arrives. Always jitter TTLs so a fleet of keys does not expire in the same second.

[Table of Contents](#Redis-for-Data-Engineers)

## How does Redis persistence work with RDB and AOF?

RDB writes a compact snapshot on a schedule by forking a child, so the write itself does not block the main thread but the fork and copy-on-write pages cost memory. AOF logs every write, and `appendfsync` decides durability: `everysec` loses at most about a second and is the normal choice, `always` fsyncs each command and is slow, `no` lets the OS decide.

```text
save 900 1
save 300 10
appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes
auto-aof-rewrite-percentage 100

INFO persistence
BGREWRITEAOF
```

Most teams keep both, using a hybrid AOF with an RDB preamble so restart is fast and at most a second of writes is lost. A pure cache can disable persistence and accept a cold start. A restart test - load, restart, compare the keyspace - is the only proof of a durability setting.

[Table of Contents](#Redis-for-Data-Engineers)

## How do eviction policies and maxmemory work?

`maxmemory` bounds the dataset and `maxmemory-policy` decides what happens at the bound. `noeviction` errors on writes that would exceed it, which is right for a store of record and wrong for a cache. Policies are `volatile-*` (only keys with a TTL) or `allkeys-*` (any key), with `lru`, `lfu`, `random`, and for volatile also `ttl`.

```text
maxmemory 12gb
maxmemory-policy allkeys-lfu
maxmemory-samples 10

INFO memory
```

Use `allkeys-lru` or `allkeys-lfu` for a shared cache and `volatile-*` only when keys without a TTL must never be evicted. LRU is sampled rather than exact, and LFU counters decay so yesterday's hot key loses to today's. Watch `evicted_keys` against `keyspace_misses`: rising misses with a healthy backend mean the cache is too small or the TTLs too short.

[Table of Contents](#Redis-for-Data-Engineers)

## How does Redis replication work?

A replica connects with `replicaof host port`, does a full synchronization once, then streams writes. Replication is asynchronous. After a short break it attempts a partial resynchronization from the replication backlog; if the break exceeded the backlog it does a full sync, which forks and ships the whole dataset.

```text
# replica redis.conf
replicaof redis-primary.internal 6379
replica-read-only yes
repl-backlog-size 64mb

INFO replication
WAIT 1 100
```

Read replicas scale reads but can serve stale data, so a pipeline reading a value it just wrote should read the primary or use `WAIT numreplicas timeout`. `WAIT` confirms replica acknowledgement, not disk durability on the primary.

[Table of Contents](#Redis-for-Data-Engineers)

## What is Redis Sentinel and when do you need it?

Sentinel is a set of processes that monitor a primary and its replicas, agree on failure with a quorum, and promote a replica. Clients ask Sentinel for the current primary instead of hard-coding an address, so failover is transparent to a correct client.

```text
sentinel monitor mymaster redis-primary.internal 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000

redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster
```

Choose Sentinel for one primary with replicas when the dataset fits on a node and you want high availability without sharding. Its limits are real: the failover window is seconds to tens of seconds, and a write acknowledged by the old primary but not yet replicated can be lost.

[Table of Contents](#Redis-for-Data-Engineers)

## How does Redis Cluster shard data?

Redis Cluster partitions the keyspace into 16384 hash slots, where the slot is `CRC16(key) mod 16384`. Each primary owns a set of slots with replicas for failover, and cluster-aware clients follow `MOVED` and `ASK` responses.

```bash
redis-cli --cluster create redis-1:6379 redis-2:6379 redis-3:6379 \
  redis-4:6379 redis-5:6379 redis-6:6379 --cluster-replicas 1

redis-cli --cluster check redis-1:6379
```

Multi-key commands such as `MGET`, `SINTERSTORE`, and multi-key Lua scripts require all keys in one slot. A hash tag forces that by hashing only the part in braces - `{user:42}:profile` and `{user:42}:sessions` share a slot - at the cost of concentrating related keys on one node.

[Table of Contents](#Redis-for-Data-Engineers)

## How do pipelining and transactions with MULTI work?

Pipelining sends many commands without waiting for each reply, turning 100 round trips into one; it is not atomic. `MULTI`/`EXEC` queues commands and runs them atomically, and `WATCH` adds optimistic concurrency.

```python
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)

with r.pipeline(transaction=False) as pipe:      # batched, not atomic
    for i in range(1000):
        pipe.hset(f"user:{i}", mapping={"plan": "pro"})
    pipe.execute()

with r.pipeline(transaction=True) as pipe:        # atomic, watched
    pipe.watch("balance:A")
    if int(pipe.get("balance:A") or 0) >= 100:
        pipe.multi()
        pipe.decrby("balance:A", 100)
        pipe.incrby("balance:B", 100)
        pipe.execute()
```

Redis transactions have no rollback: if one command fails at runtime the rest still run, so they are a batch of correct commands rather than an ACID unit. `WATCH` aborts `EXEC` if a watched key changed, which is the standard atomic read-modify-write.

[Table of Contents](#Redis-for-Data-Engineers)

## How do you use Lua scripting in Redis?

A script runs on the server and blocks other commands, making it the tool for an atomic multi-step operation that returns a computed result. `EVALSHA` sends the script's SHA1 so the body travels once, and keys must be passed through `KEYS` so a cluster can route the call.

```python
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)

RELEASE = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
  return redis.call('DEL', KEYS[1])
end
return 0
"""
sha = r.script_load(RELEASE)
r.set("lock:job:42", "token-a", nx=True, px=30000)
released = r.evalsha(sha, 1, "lock:job:42", "token-a")
```

Never loop over an unbounded keyspace inside a script, because it stops the world. Prefer `FUNCTION` (Redis 7) when the code should be persisted and versioned with the dataset.

[Table of Contents](#Redis-for-Data-Engineers)

## What is the difference between pub/sub and Streams?

Pub/sub is fire-and-forget: only clients subscribed at that instant receive a message, with no storage, acknowledgement, or replay. Streams are an append-only log with ids, persistence, consumer groups, and acknowledgements.

```bash
redis-cli SUBSCRIBE orders.created
redis-cli PUBLISH orders.created '{"order_id":1001}'

redis-cli XADD orders.created '*' order_id 1001 amount 249.00
redis-cli XRANGE orders.created - +
redis-cli XINFO STREAM orders.created
```

Use pub/sub for ephemeral notifications where losing a message during a deploy is acceptable - cache invalidation hints, a dashboard tick, chat fan-out. Use Streams when a consumer must process every message, retry failures, and resume after a restart.

[Table of Contents](#Redis-for-Data-Engineers)

## How do consumer groups and pending entries work in Redis Streams?

`XADD` appends an entry with a monotonic id. A consumer group tracks a last-delivered id and a pending entries list (PEL) of delivered-but-unacknowledged entries. `XREADGROUP` delivers to a named consumer, `XACK` clears the PEL, and `XAUTOCLAIM` reclaims entries whose consumer died.

```python
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)
STREAM, GROUP = "events:orders", "lake-writer"
try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except redis.exceptions.ResponseError as exc:  # BUSYGROUP: the group already exists
    if "BUSYGROUP" not in str(exc):
        raise

entries = r.xreadgroup(GROUP, "w1", {STREAM: ">"}, count=100, block=5000)
for _stream, records in entries or []:
    for entry_id, fields in records:
        write_to_lake(entry_id, fields)
        r.xack(STREAM, GROUP, entry_id)

claimed = r.xautoclaim(STREAM, GROUP, "w1", min_idle_time=60_000, count=100)
print(r.xpending(STREAM, GROUP))
```

`XADD MAXLEN ~ 1000000` caps memory because Streams are not infinite. A growing PEL means consumers are failing or slow; `XPENDING` plus `XAUTOCLAIM` is the recovery path. Ordering is global to a stream, so scale-out means many streams rather than partitions.

[Table of Contents](#Redis-for-Data-Engineers)

## What caching patterns work with Redis?

Cache-aside (lazy loading) is the default: read Redis, and on a miss read the source of truth, cache the value with a TTL, and return it. Write-through updates the cache in the write path; write-behind queues writes and flushes asynchronously; negative caching stores "not found" briefly so a missing key cannot hammer the database.

```python
import json
import random
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)


def get_product(sku: str, db) -> dict | None:
    key = f"product:{sku}"
    cached = r.get(key)
    if cached == "__miss__":
        return None
    if cached is not None:
        return json.loads(cached)
    row = db.fetch_one("SELECT sku, name, price FROM products WHERE sku = %s", (sku,))
    if row is None:
        r.set(key, "__miss__", ex=60)             # negative cache
        return None
    r.set(key, json.dumps(row), ex=3600 + random.randint(0, 300))  # jitter
    return row
```

The hard part is invalidation, not the read path. Delete the key on write rather than overwriting it, because concurrent writes can leave the older value cached. Accept a short stale window bounded by the TTL, and version keys (`product:v3:{sku}`) when the cached shape changes.

[Table of Contents](#Redis-for-Data-Engineers)

## How do you prevent a cache stampede?

A stampede happens when a popular key expires and thousands of requests miss at once, then all hit the database together. Three fixes: a mutex so only one worker rebuilds, early recomputation so a hot key refreshes before expiry, and stale-while-revalidate so readers get the old value while one caller refreshes.

```python
import json
import time
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)


def get_report(key: str, compute):
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    if not r.set(f"{key}:lock", "1", nx=True, px=10_000):
        time.sleep(0.05)                          # someone else is rebuilding
        cached = r.get(key)
        if cached:
            return json.loads(cached)
    fresh = compute()
    r.set(key, json.dumps(fresh), ex=300)
    r.delete(f"{key}:lock")
    return fresh
```

The cheapest fix is often to not let a hot key expire on a schedule: refresh it in a background job before the TTL, or keep a logical expiration inside the value so the cache can serve stale data deliberately. For static reference data, no TTL plus explicit invalidation removes the problem.

[Table of Contents](#Redis-for-Data-Engineers)

## How do you implement a distributed lock in Redis?

The basic lock is `SET key token NX PX ttl`: atomic acquisition with a unique owner token and a finite lease so a crashed holder cannot block forever. Release must compare the token and delete atomically, or one worker can delete another worker's lock after a pause.

```python
import uuid
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)
RELEASE = """
if redis.call('GET', KEYS[1]) == ARGV[1] then return redis.call('DEL', KEYS[1]) end
return 0
"""


def acquire(name: str, ttl_ms: int = 30_000) -> str | None:
    token = str(uuid.uuid4())
    return token if r.set(f"lock:{name}", token, nx=True, px=ttl_ms) else None


def release(name: str, token: str) -> bool:
    return bool(r.eval(RELEASE, 1, f"lock:{name}", token))
```

A lock is not fencing. If the holder pauses past the TTL, the lock expires, another worker acquires it, and the first still writes. For correctness against that, the storage layer must reject writes with an older fencing token. Use a Redis lock to avoid duplicated work, and a database constraint or conditional write for correctness.

[Table of Contents](#Redis-for-Data-Engineers)

## How do you build a rate limiter with Redis?

The simplest limiter is fixed-window `INCR` plus `EXPIRE`, which allows a burst at the window boundary. A sliding-window log uses a sorted set of timestamps; a token bucket refills continuously and is friendliest to real traffic.

```python
import time
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)

BUCKET = """
local tokens = tonumber(redis.call('HGET', KEYS[1], 'tokens') or ARGV[1])
local ts = tonumber(redis.call('HGET', KEYS[1], 'ts') or ARGV[3])
local now = tonumber(ARGV[3])
tokens = math.min(tonumber(ARGV[1]), tokens + (now - ts) * tonumber(ARGV[2]))
local ok = 0
if tokens >= 1 then tokens = tokens - 1; ok = 1 end
redis.call('HSET', KEYS[1], 'tokens', tokens, 'ts', now)
redis.call('PEXPIRE', KEYS[1], 60000)
return ok
"""
SHA = r.script_load(BUCKET)


def allow(api_key: str, rate: float = 50, capacity: int = 100) -> bool:
    return bool(r.evalsha(SHA, 1, f"rl:{api_key}", capacity, rate, time.time()))
```

At an API gateway the identity is the API key and the counters live in Redis so every node shares one view. Return `X-RateLimit-Remaining` and `Retry-After`, and fail open if Redis is unreachable unless the endpoint is abusive by nature.

[Table of Contents](#Redis-for-Data-Engineers)

## How do you use Redis for idempotency and deduplication?

A producer that retries can deliver an event twice. `SET key 1 NX EX` succeeds for exactly one caller and turns the second delivery into a no-op that can return the stored result instead of reprocessing.

```python
import json
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)


def process_once(request_id: str, payload: dict, handle) -> dict:
    key = f"idem:{request_id}"
    if not r.set(key, json.dumps({"status": "in_progress"}), nx=True, ex=86_400):
        previous = r.get(key)
        if previous and json.loads(previous).get("status") == "done":
            return json.loads(previous)["result"]
        return {"status": "duplicate_in_progress", "request_id": request_id}
    result = handle(payload)
    r.set(key, json.dumps({"status": "done", "result": result}), ex=86_400)
    return result
```

For stream-level dedupe, a Bloom filter (`BF.ADD`/`BF.EXISTS`) answers "have I seen this id" in constant memory with a tunable false-positive rate; a false positive drops a rare duplicate, and a false negative is impossible. Keep the window longer than the maximum producer retry window and no longer.

[Table of Contents](#Redis-for-Data-Engineers)

## How do you build a leaderboard or trending list with Redis?

A sorted set is a leaderboard by construction: the member is the player and the score is the rank. `ZINCRBY` updates in O(log n), `ZREVRANGE` reads the top N, and `ZREVRANK` returns a member's position.

```python
import time
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)


def award(user: str, points: int) -> None:
    pipe = r.pipeline(transaction=False)
    pipe.zincrby("lb:all-time", points, user)
    pipe.zincrby(f"lb:daily:{time.strftime('%Y-%m-%d')}", points, user)
    pipe.expire(f"lb:daily:{time.strftime('%Y-%m-%d')}", 3 * 86400)
    pipe.execute()


def trending(days: int = 7) -> list[tuple[str, float]]:
    keys = [f"lb:daily:{time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * i))}"
            for i in range(days)]
    weights = dict(zip(keys, [1.0 / (i + 1) for i in range(days)]))
    r.zunionstore("trending:weekly", weights, aggregate="SUM")
    r.expire("trending:weekly", 3600)
    return r.zrevrange("trending:weekly", 0, 9, withscores=True)
```

Use daily or hourly sorted sets plus a weighted union for "trending this week" rather than one unbounded set, and always set a TTL. A big sorted set is fine; one that lives forever is a memory leak. At cluster scale a leaderboard is a single slot, so shard it by an id prefix or size the node for it.

[Table of Contents](#Redis-for-Data-Engineers)

## How do you use Redis as a session store?

Sessions are small key/value objects with a TTL, which is exactly what Redis is good at, and centralizing them lets any application node serve any request. Store the session as a hash when fields update independently, or as one serialized value when it is always read whole.

```python
import secrets
import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)
SESSION_TTL = 3600


def create_session(user_id: str) -> str:
    sid = secrets.token_urlsafe(32)
    r.hset(f"sess:{sid}", mapping={"user_id": user_id})
    r.expire(f"sess:{sid}", SESSION_TTL)
    return sid


def destroy(sid: str) -> None:
    r.delete(f"sess:{sid}")                        # immediate logout
```

The cookie should carry an opaque token and be `HttpOnly`, `Secure`, and `SameSite`. A `FLUSHALL` on a shared cache logs every user out, so sessions deserve their own instance or a clearly separated database. If sessions must survive a restart, enable persistence and a replica.

[Table of Contents](#Redis-for-Data-Engineers)

## Redis Streams vs Kafka for a lightweight queue?

Streams and Kafka overlap but operate at different scales. The decision is about durability, throughput, and whether Kafka is already operated by the team.

| Aspect | Redis Streams | Apache Kafka |
|---|---|---|
| Storage | in memory, trimmed by MAXLEN | on disk, retention by time or size |
| Throughput | tens of thousands/s | millions/s with batching |
| Ordering | total within one stream | within a partition |
| Replay | any retained id | any retained offset |
| Delivery | at-least-once with ack and reclaim | at-least-once, exactly-once with transactions |
| Durability | AOF everysec loses up to ~1s | replicated log with configurable acks |
| Ops | one more Redis | brokers, controllers, rebalancing |

```text
XADD jobs:thumbnails MAXLEN ~ 100000 '*' image s3://acme/img/1.jpg
# after too many deliveries, move to a dead-letter stream instead of retrying forever
XADD jobs:thumbnails:dead '*' image s3://acme/img/1.jpg reason too_many_retries
```

Choose Streams when the queue is a side channel - a few thousand events per second, short retention, a Redis you already run. Choose Kafka when the log is the system of record, retention is weeks, replay from the beginning matters, or throughput exceeds one Redis node's memory.

[Table of Contents](#Redis-for-Data-Engineers)

## Redis vs Memcached vs Kafka?

These are not substitutes; the answer is to place each in its layer.

```text
Memcached : multithreaded simple key/value cache. Strings only, no persistence,
            no replication, no data structures. Scales by client-side hashing.
Redis     : data-structure server. Rich types, Lua, Streams, pub/sub, replication,
            Cluster, optional persistence. More use cases, slightly more CPU per op.
Kafka     : durable, partitioned, replicated log for events. Not a cache; retention
            and replay are the point.
```

Memcached wins on pure multi-core throughput for tiny string values and is simpler to operate; Redis wins as soon as you need counters, sets, sorted sets, locks, TTL semantics, persistence, or Streams. Redis versus Kafka: Kafka is the durable event backbone, Redis is the low-latency serving layer in front of it, and Redis Streams is only for internal short-lived work queues.

[Table of Contents](#Redis-for-Data-Engineers)

## How do you size Redis memory and handle hot keys?

Every key costs the value plus per-key overhead, and the usable ratio of `used_memory` to raw payload is often 1.5x to 2x. Start from the number of keys, average value and key size, and the TTL distribution.

```bash
redis-cli --bigkeys
redis-cli MEMORY USAGE product:1001 SAMPLES 5
redis-cli INFO memory | grep -E 'used_memory_human|mem_fragmentation_ratio'
redis-cli --scan --pattern 'product:*' --count 100 | head
```

Hot keys are the second constraint: one key - a celebrity user, a global counter, a flash-sale SKU - can saturate a core because execution is single-threaded. Read replicas help reads; write-hot keys need a different shape. Shard a counter into N keys and sum on read, split an object into per-shard fields, or add client-side caching.

```python
import random

import redis

r = redis.Redis(host="redis.internal", port=6379, decode_responses=True)


def hit(counter: str, shards: int = 16) -> int:
    # Pick a shard per write so concurrent callers actually spread the load:
    # hashing the counter alone would pin every write to one shard. Summing all
    # shards on read still yields the true total.
    return r.incr(f"counter:{counter}:{random.randrange(shards)}")


def total(counter: str, shards: int = 16) -> int:
    values = r.mget([f"counter:{counter}:{s}" for s in range(shards)])
    return sum(int(v) for v in values if v)
```

[Table of Contents](#Redis-for-Data-Engineers)

## How do you monitor and operate Redis in production?

Memory, evictions, hit rate, latency, replication, and persistence health answer almost every incident question, and `INFO` plus the slow log cover most of it.

```bash
redis-cli INFO memory        # used_memory, maxmemory, fragmentation
redis-cli INFO stats         # hits, misses, evicted_keys, expired_keys
redis-cli INFO replication   # role, replicas, link status, offset lag
redis-cli INFO persistence   # rdb_last_bgsave_status, aof_last_write_status
redis-cli SLOWLOG GET 10
redis-cli LATENCY DOCTOR
redis-cli --latency-history
# scrape the same counters with redis_exporter on :9121 for Prometheus
```

Alert on a falling hit ratio, continuously rising evictions, fragmentation far from 1.0, replication lag, a failed background save, and clients near the file-descriptor limit. Never run `KEYS *`, `FLUSHALL`, or `MONITOR` in production; they block or overload the single thread.

[Table of Contents](#Redis-for-Data-Engineers)

## Real world use cases for Redis

### 1. Read-through cache for a pricing API

Business context: a retail API serves 40,000 reads/s at peak against a Postgres primary that absorbs about 3,000. Design: cache-aside with jittered TTL, negative caching, and invalidation on price change.

```python
import json
import random
import redis

r = redis.Redis(host="redis-cache.internal", port=6379, decode_responses=True)


def price_for(sku: str, db) -> dict | None:
    cached = r.get(f"price:{sku}")
    if cached is not None:
        return None if cached == "__miss__" else json.loads(cached)
    row = db.fetch_one("SELECT sku, price FROM prices WHERE sku = %s", (sku,))
    if row is None:
        r.set(f"price:{sku}", "__miss__", ex=30)
        return None
    r.set(f"price:{sku}", json.dumps(row), ex=300 + random.randint(0, 60))
    return row
```

Why Redis: the hot set fits in a few GB, negative caching bounds the miss path, and invalidation is one `DEL` instead of a source-of-truth rewrite.

### 2. API gateway rate limiting and idempotency

Business context: a public ingestion API accepts 500M events/day from 12,000 keys and clients retry aggressively. Design: a Lua token bucket per key plus `SET idem:<id> NX EX` as the first write step.

```python
import time
import redis

r = redis.Redis(host="redis-gateway.internal", port=6379, decode_responses=True)
SHA = r.script_load(TOKEN_BUCKET)   # same script as the rate limiter section


def admit(api_key: str, event_id: str) -> str:
    if not r.evalsha(SHA, 1, f"rl:{api_key}", 100, 50, time.time()):
        return "rate_limited"
    if not r.set(f"idem:{event_id}", "1", nx=True, ex=86400):
        return "duplicate"
    return "accepted"
```

Why Redis: both checks are sub-millisecond and shared across every gateway pod, and the idempotency key expires on its own.

### 3. Real-time leaderboard

Business context: 20M daily players need an all-time board, a daily board that resets, and 100,000 score updates/s. Design: sorted sets, one all-time key and one per day with a TTL, and a weekly trending union.

```python
import time
import redis

r = redis.Redis(host="redis-leaderboard.internal", port=6379, decode_responses=True)


def page(user_id: str) -> dict:
    today = time.strftime("%Y-%m-%d")
    return {
        "rank": r.zrevrank("lb:all-time", user_id),
        "top": r.zrevrange("lb:all-time", 0, 9, withscores=True),
        "today": r.zrevrange(f"lb:daily:{today}", 0, 9, withscores=True),
    }
```

Why Redis: `ZINCRBY` and `ZREVRANGE` are O(log n), so a 20M-member board answers a top-10 page in microseconds, and per-day TTLs bound growth.

### 4. Session store for a stateless fleet

Business context: 300 pods behind a load balancer with no session affinity need sessions that survive restarts and a logout that takes effect everywhere. Design: session hashes with sliding TTLs in a dedicated Redis with AOF and a replica.

```python
import secrets
import redis

r = redis.Redis(host="redis-sessions.internal", port=6379, decode_responses=True)


def login(user_id: str) -> str:
    sid = secrets.token_urlsafe(32)
    r.hset(f"sess:{sid}", mapping={"user_id": user_id})
    r.expire(f"sess:{sid}", 3600)
    return sid


def logout(sid: str) -> None:
    r.delete(f"sess:{sid}")
```

Why Redis: any pod validates any session in one round trip, TTL enforces expiry without a cleanup job, and `DEL` is immediate across the fleet.

### 5. Lightweight stream ingestion into a lakehouse

Business context: 2,000 IoT gateways emit about 30,000 readings/s; a service batches them into Parquet in S3 every minute, and retention only needs to be minutes. Design: a trimmed Stream with a consumer group and `XAUTOCLAIM` for recovery.

```python
import redis

r = redis.Redis(host="redis-streams.internal", port=6379, decode_responses=True)
STREAM, GROUP, CONSUMER = "telemetry:readings", "s3-writers", "writer-1"
try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except redis.exceptions.ResponseError as exc:  # BUSYGROUP: the group already exists
    if "BUSYGROUP" not in str(exc):
        raise


def drain(batch: int = 500) -> int:
    entries = r.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=batch, block=2000)
    for _stream, records in entries or []:
        write_parquet_to_s3([fields for _id, fields in records])
        r.xack(STREAM, GROUP, *[entry_id for entry_id, _ in records])
    return sum(len(records) for _stream, records in entries or [])
```

Why Redis: one `XADD` per reading with `MAXLEN ~` keeps memory flat, consumer groups give at-least-once delivery, and the lakehouse still receives Parquet.

[Table of Contents](#Redis-for-Data-Engineers)
