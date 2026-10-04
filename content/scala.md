## [Main title](../README.md)
### [Interview questions](full.md)

# Scala Basics for Data Engineers

**Notebook:** [`notebooks/topics/scala.ipynb`](../notebooks/topics/scala.ipynb) - runnable version of this topic with self-checking exercises.

+ [What is Scala and why do data engineers learn it?](#What-is-Scala-and-why-do-data-engineers-learn-it)
+ [How do vals and vars differ, and why does immutability matter?](#How-do-vals-and-vars-differ-and-why-does-immutability-matter)
+ [What are Scala basic types and how does type inference work?](#What-are-Scala-basic-types-and-how-does-type-inference-work)
+ [How does string interpolation work in Scala?](#How-does-string-interpolation-work-in-Scala)
+ [How does control flow work in Scala with if/else and match?](#How-does-control-flow-work-in-Scala-with-ifelse-and-match)
+ [How do you define functions and methods in Scala?](#How-do-you-define-functions-and-methods-in-Scala)
+ [What are higher-order functions and function values?](#What-are-higher-order-functions-and-function-values)
+ [What is currying and partial application?](#What-is-currying-and-partial-application)
+ [How do case classes and pattern matching work?](#How-do-case-classes-and-pattern-matching-work)
+ [What are sealed traits and extractors?](#What-are-sealed-traits-and-extractors)
+ [How do traits, mixins, and abstract classes work?](#How-do-traits-mixins-and-abstract-classes-work)
+ [What are objects and companion objects with apply and unapply?](#What-are-objects-and-companion-objects-with-apply-and-unapply)
+ [How do Scala collections and core combinators work?](#How-do-Scala-collections-and-core-combinators-work)
+ [How do for-comprehensions desugar in Scala?](#How-do-for-comprehensions-desugar-in-Scala)
+ [How do you use Option, Either, and Try instead of null?](#How-do-you-use-Option-Either-and-Try-instead-of-null)
+ [What are implicits, givens, and extension methods?](#What-are-implicits-givens-and-extension-methods)
+ [How do generics and type bounds work in Scala?](#How-do-generics-and-type-bounds-work-in-Scala)
+ [What are lazy val and by-name parameters?](#What-are-lazy-val-and-by-name-parameters)
+ [How do Futures and basic concurrency work in Scala?](#How-do-Futures-and-basic-concurrency-work-in-Scala)
+ [How does Java interoperability work in Scala?](#How-does-Java-interoperability-work-in-Scala)
+ [How do you structure an sbt project with dependencies and tests?](#How-do-you-structure-an-sbt-project-with-dependencies-and-tests)
+ [What Scala idioms matter for Spark?](#What-Scala-idioms-matter-for-Spark)
+ [What are common Scala pitfalls in data engineering?](#What-are-common-Scala-pitfalls-in-data-engineering)
+ [Real world use cases for Scala in data engineering](#Real-world-use-cases-for-Scala-in-data-engineering)

## What is Scala and why do data engineers learn it?

Scala is a statically typed JVM language that blends object-oriented and functional programming. Spark is written in Scala, the official Kafka clients are Java, and Flink exposes a JVM DataStream API, so Scala sits naturally next to all three.

```text
Kafka (Java clients) -> Spark/Flink JVM job -> lakehouse tables -> BI / ML
```

Data engineers learn Scala because:

+ Spark's API and internals are Scala-first, so source code and error messages are easier to read
+ Typed `Dataset[T]` code catches schema mistakes at compile time instead of at runtime
+ JVM-native logic avoids Python UDF serialization overhead for CPU-bound transforms
+ One library can be shared by Spark jobs, Flink jobs, and microservices

Real-world example: a team keeps revenue logic in one Scala library, and both a Spark batch job and a Flink streaming job call the same `OrderTransforms` object, so batch and streaming cannot silently diverge.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do vals and vars differ, and why does immutability matter?

`val` binds a name once; `var` can be reassigned. Default to `val` and use `var` only for tight local accumulation. `val` makes the reference immutable, not the object, so a `val` can still point at a mutable collection.

```scala
val rawPath = "s3://acme-raw/orders/"   // immutable binding
var attempt = 0                          // reassignable

attempt += 1
// rawPath = "s3://other/"               // compile error: reassignment to val

final case class JobConfig(rawPath: String, maxRetries: Int)
val config = JobConfig(rawPath, maxRetries = 3)
```

This matters in Spark and Flink because closures are serialized and shipped to executors or task managers. A captured mutable variable is copied, so updates on executors are invisible on the driver. Immutable values remove that failure mode and are safe to share across threads and Futures.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## What are Scala basic types and how does type inference work?

Scala has the JVM primitives (`Int`, `Long`, `Double`, `Boolean`, `Char`) plus `String`, `BigInt`, and `BigDecimal`. Everything is an object at the API level, with `Any` at the top, `AnyVal`/`AnyRef` below it, and `Nothing` at the bottom. The compiler infers types, so annotate when widening or when you want a stable contract.

```scala
val rows = 1_000_000L             // Long
val ratio = 0.42                  // Double
val ids = Vector(1L, 2L, 3L)      // Vector[Long]
val widened: Long = rows + 1      // explicit widening
val total: BigDecimal = BigDecimal("19.99") * 3
```

Two habits help in interviews:

+ Annotate public return types and dataset schemas; inference is for locals
+ `Nothing` is a subtype of everything, which is why `if (x) 1 else throw new RuntimeException` still infers `Int`

For money prefer `BigDecimal` over `Double`: Spark maps `decimal(p, s)` to `BigDecimal`, and floating-point rounding in revenue numbers is a classic production incident.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How does string interpolation work in Scala?

Three built-in interpolators: `s` substitutes values, `f` formats them, and `raw` disables escape processing. Interpolation accepts expressions in braces, so paths and log lines read cleanly.

```scala
val table = "silver.orders"
val rows = 4200L
val ratio = 0.127
val dt = "2026-10-04"

s"loaded $rows rows into $table"
f"$rows%,d rows, ${ratio * 100}%.1f%% null"   // %% is a literal percent
raw"C:\data\orders"                            // backslashes kept literally
s"s3://acme-curated/fact_order/dt=$dt/"
```

`f` type-checks the format specifier at compile time. `s` calls `toString`, so an `Option` prints as `Some(...)`; use `.getOrElse("")` before interpolating it into a message.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How does control flow work in Scala with if/else and match?

`if`/`else` is an expression that returns a value, so it can initialize a `val`. `match` is the general branch construct and replaces long `if`/`else if` chains and `switch`, including guards such as `case Order(_, _, amount, "PAID") if amount > 100`.

```scala
val amount = BigDecimal("1500.00")
val tier = if (amount > 1000) "high" else "standard"

sealed trait OrderEvent
final case class Created(orderId: Long) extends OrderEvent
final case class Updated(orderId: Long, amount: BigDecimal) extends OrderEvent
final case class Deleted(orderId: Long) extends OrderEvent

def describe(event: OrderEvent): String = event match {
  case Created(id)         => s"insert $id"
  case Updated(id, amount) => s"upsert $id for $amount"
  case Deleted(id)         => s"delete $id"
}
```

Because `OrderEvent` is `sealed`, the compiler warns if a case is missing. That exhaustiveness check is the main reason to model events as sealed hierarchies instead of strings.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do you define functions and methods in Scala?

`def` defines a method and can also define a local function inside another `def`. Scala supports default arguments, named arguments, and varargs written `Int*`.

```scala
def normalize(name: String, trim: Boolean = true, lower: Boolean = true): String = {
  var out = name
  if (trim) out = out.trim
  if (lower) out = out.toLowerCase
  out
}

normalize("  Alice ")
normalize("  Alice ", lower = false)         // named argument: only lower is overridden
def sumAll(values: Int*): Int = values.sum   // varargs

def parseAmount(raw: String): Option[BigDecimal] = {
  def clean(s: String): String = s.replace("$", "").replace(",", "").trim  // local function
  if (raw == null || raw.trim.isEmpty) None
  else scala.util.Try(BigDecimal(clean(raw))).toOption
}
```

A method returning `Unit` is written `def commit(): Unit = ...`. The older procedure syntax (`def commit() { ... }`) was deprecated in Scala 2.13 and removed in Scala 3, so an interviewer may check whether you still write it.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## What are higher-order functions and function values?

Functions are values. `A => B` is a type, and a method that takes or returns a function is higher-order. This is the basis of `map`, `filter`, `fold`, and Spark's typed transformations.

```scala
val double: Int => Int = _ * 2
val amounts = List(10, 20, 30)

amounts.map(double)
amounts.filter(_ > 15)
amounts.foldLeft(0)(_ + _)

def applyTwice[A](f: A => A)(x: A): A = f(f(x))
applyTwice(double)(5)     // 20

val pipeline: String => Option[String] = s => Option(s).map(_.trim.toLowerCase).filter(_.nonEmpty)
List(" Alice ", "", null).flatMap(pipeline)   // List("alice")

val add: (Int, Int) => Int = _ + _
val addTen: Int => Int = add(10, _)
addTen(7)                 // 17
```

In Spark, `_.amount` compiles to bytecode instead of a pickled Python lambda, which removes a serialization boundary between the driver and the executors.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## What is currying and partial application?

Currying splits a multi-argument function into a chain of single-argument functions, written as multiple parameter lists. The left lists become reusable configuration and the right list stays the changing data.

```scala
def add(a: Int)(b: Int): Int = a + b
val addTen = add(10)(_)           // Scala 2.13 placeholder; in Scala 3 write add(10)
addTen(5)                         // 15

import org.apache.spark.sql.SparkSession

def withSpark[A](appName: String)(body: SparkSession => A): A = {   // resource first, body second
  val spark = SparkSession.builder().appName(appName).getOrCreate()
  try body(spark) finally spark.stop()
}

val rowCount = withSpark("orders") { spark =>
  spark.read.parquet("s3://acme-curated/fact_order/").count()
}
```

Currying is not the same as default arguments: defaults fill in values at the call site, while currying returns a reusable function value after the first list is applied.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do case classes and pattern matching work?

A `case class` gets compiler-generated `equals`, `hashCode`, `toString`, `copy`, and companion `apply`/`unapply`, which makes it the standard immutable record type for domain models and Spark encoders.

```scala
final case class Order(orderId: Long, customerId: Long, amount: BigDecimal, status: String)

val order = Order(1L, 42L, BigDecimal("19.99"), "PAID")
val cancelled = order.copy(status = "CANCELLED")

def classify(order: Order): String = order match {
  case Order(_, _, amount, "PAID") if amount > 100 => "high-value paid"
  case Order(_, _, _, "CANCELLED")                 => "cancelled"
  case Order(id, _, _, _)                          => s"other:$id"
}
```

`copy` keeps record updates explicit, which matches Spark's immutable Dataset model. Field order and types must match the source: reading CSV straight into a case class with a `BigDecimal` field fails if the underlying column is a string, so read as a `DataFrame`, cast, then call `.as[Order]`.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## What are sealed traits and extractors?

A `sealed trait` restricts implementations to the same file, so the compiler can prove that a `match` covers every case. That is exactly what you want for event types and job states.

```scala
sealed trait OrderEvent
final case class Created(orderId: Long, customerId: Long) extends OrderEvent
final case class Updated(orderId: Long, amount: BigDecimal) extends OrderEvent
final case class Deleted(orderId: Long) extends OrderEvent
case object RolledBack extends OrderEvent

def dedupKey(event: OrderEvent): String = event match {
  case Created(id, _) => s"$id:create"
  case Updated(id, _) => s"$id:update"
  case Deleted(id)    => s"$id:delete"
  case RolledBack     => "rollback"
}

object EvenNumber {   // custom extractor: any object with unapply works in a pattern
  def unapply(n: Int): Option[Int] = if (n % 2 == 0) Some(n) else None
}
```

Real-world example: an ingestion job matches `OrderEvent` to route records to insert, merge, or delete paths, and adding a new event type makes the compiler report a non-exhaustive match at every routing site (an error under fatal warnings).

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do traits, mixins, and abstract classes work?

Traits define interfaces plus optional concrete behavior and are mixed in with `with`. A class can extend one class but mix in many traits, which is how data code composes concerns like logging, metrics, and clocks.

```scala
trait Clock { def now(): Long }
trait Logging { def log(message: String): Unit = println(s"[${getClass.getSimpleName}] $message") }
abstract class BaseJob(val name: String) { def run(): Unit }

final class OrdersJob(override val name: String) extends BaseJob(name) with Logging with Clock {
  def run(): Unit = log(s"running $name at ${now()}")
  def now(): Long = System.currentTimeMillis()
}

// stackable behavior is added the same way: trait Retrying extends BaseJob { abstract override def run(): Unit = ... }
val job: BaseJob = new OrdersJob("orders-nightly")
```

An abstract class is the better choice when you need constructor parameters or Java interoperability; traits are better for stackable behavior. Traits are linearized left to right, so the rightmost mixin wins for conflicting concrete methods, which is why `abstract override` is needed to wrap `super.run()`.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## What are objects and companion objects with apply and unapply?

An `object` is a singleton. An object with the same name as a class or case class in the same file is that class's companion, and it can see the class's private members. Companions are the idiomatic home for factories, constants, and `unapply`.

```scala
final case class Partition(dt: String, region: String)

object Partition {
  val DefaultRegion: String = "us"
  def forDate(dt: String): Partition = Partition(dt, DefaultRegion)
  def fromPath(path: String): Option[Partition] =
    if (path.contains("dt=")) Some(Partition(path.split("dt=")(1).take(10), DefaultRegion))
    else None
}

val p = Partition("2026-10-04", "eu")               // companion apply
val parsed = Partition.fromPath("s3://acme/fact_order/dt=2026-10-04/")
```

`apply` is syntax sugar for calling the object (`obj(args)` means `obj.apply(args)`), and `unapply` is what pattern matching calls to take a value apart. Defining both on a companion gives a plain class case-class-like ergonomics.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do Scala collections and core combinators work?

`List` is a linked list with cheap head/tail, `Vector` is the indexed immutable sequence, `Seq` is the general sequence abstraction, and `Map`/`Set` are the associative and unique collections. In Scala 2.13 the default `Seq` is `scala.collection.immutable.Seq`.

```scala
val statuses: List[String] = List("PAID", "PENDING", "PAID")
val regions: Set[String] = Set("us", "eu", "us")

final case class Order(orderId: Long, customerId: Long, amount: BigDecimal, status: String)
val orders = List(
  Order(1L, 10L, BigDecimal("50.00"), "PAID"),
  Order(2L, 10L, BigDecimal("25.00"), "PENDING"),
  Order(3L, 11L, BigDecimal("80.00"), "PAID")
)

orders.map(_.amount)                                    // transform each element
orders.filter(_.status == "PAID")                       // keep matching elements
orders.flatMap(o => List(o.orderId, o.customerId))      // map, then flatten
orders.groupBy(_.customerId)                            // Map[Long, List[Order]]
orders.sortBy(o => (-o.amount.toDouble, o.orderId))     // multi-key sort
orders.partition(_.status == "PAID")                    // (matching, rest)
orders.collect { case o if o.amount > 40 => o.orderId } // partial function
orders.foldLeft(BigDecimal(0))((sum, o) => sum + o.amount)
orders.map(_.amount).reduceOption(_ + _)
orders.distinctBy(_.customerId)                         // one row per customer
```

`fold`/`foldLeft` carries an initial accumulator and can change the result type; `reduce` seeds from the first element and fails on empty input, which is why `reduceOption` exists. Use `.view.mapValues(...)` to transform a `Map` lazily instead of rebuilding it eagerly.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do for-comprehensions desugar in Scala?

A `for` expression is syntax sugar: generators become `flatMap`, the final `yield` becomes `map`, filters become `withFilter`, and a `for` without `yield` becomes `foreach`.

```scala
val pairs = for {
  a <- List(1, 2, 3)
  b <- List(10, 20) if a < 3
} yield (a, b)

// desugars to
List(1, 2, 3).flatMap { a =>
  List(10, 20).withFilter(_ => a < 3).map(b => (a, b))
}
```

Because the desugaring only needs those methods, the same syntax sequences `Option`, `Either`, and `Future`:

```scala
def lookupCustomer(id: Long): Option[String] = if (id == 10L) Some("alice") else None

val region = for { c <- lookupCustomer(10L); suffix <- Option(":us") } yield s"$c$suffix"
```

Repository-style lookups return `Option`, so a chain of enrichment steps reads top to bottom and short-circuits on the first missing value instead of nesting `if` blocks or throwing.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do you use Option, Either, and Try instead of null?

Scala encodes failure in the type system. `Option[A]` means "a value or nothing", `Either[L, R]` carries a typed error on the left, and `Try[A]` captures a thrown exception.

```scala
import scala.util.{Failure, Success, Try}

def parseAmount(raw: String): Option[BigDecimal] =
  Option(raw).map(_.trim).filter(_.nonEmpty).flatMap(s => Try(BigDecimal(s)).toOption)

def lookupRegion(customerId: Long): Either[String, String] =
  if (customerId > 0) Right("us") else Left(s"invalid customer id: $customerId")

lookupRegion(-1).fold(err => s"error: $err", region => s"region: $region")

val attempt: Try[Int] = Try("not-a-number".toInt)
attempt match {
  case Success(value) => s"parsed $value"
  case Failure(err)   => s"failed: ${err.getMessage}"
}
```

Why this matters at data boundaries:

+ Java APIs, JDBC, and environment variables return `null`; wrap them immediately with `Option(...)`
+ Spark `Dataset[T]` rows can still contain `null` in a case class field, so validate with a filter before writing a governed table

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## What are implicits, givens, and extension methods?

Implicits are Scala 2's mechanism for automatically passing values and applying conversions. Scala 3 renamed the concept to `given`/`using` and added `extension` methods. Both add behavior to types you do not own, most commonly Spark's `Dataset`.

Scala 2.13 form, which is what Spark 3.x and Spark 4.x modules compile against:

```scala
import org.apache.spark.sql.Dataset

implicit class DatasetOps[T](private val ds: Dataset[T]) extends AnyVal {
  def logCount(): Dataset[T] = {
    println(s"rows=${ds.count()}")
    ds
  }
}

val result = ordersDs.logCount()
```

Scala 3 form of the same idea, plus an implicit type class instance:

```scala
// Scala 3 only: Spark core artifacts are published for Scala 2.12/2.13, not for Scala 3
extension (ds: Dataset[Order])
  def logCount(): Dataset[Order] = { println(s"rows=${ds.count()}"); ds }

given Ordering[Order] = Ordering.by((o: Order) => o.amount)
```

Be honest about versions: `implicit` is the safe answer for Spark work today, while `given`/`extension` need a Scala 3 toolchain. Keep implicits narrow and local, because broad implicit conversions slow compilation and make type errors hard to read.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do generics and type bounds work in Scala?

Generic methods and classes use type parameters in square brackets, like Java generics but with declaration-site variance and richer bounds.

```scala
trait Source[+A] { def read(): A }          // covariant: produces A
trait Sink[-A]   { def write(a: A): Unit }  // contravariant: consumes A

val strings: Source[String] = new Source[String] { def read(): String = "x" }
val anys: Source[Any] = strings             // allowed because Source is covariant

def first[A](xs: List[A]): Option[A] = xs.headOption
def maxOf[A: Ordering](xs: List[A]): A = xs.max             // context bound
```

Bounds that show up most in data code:

+ `<: A` upper bound requires a subtype, for example `Serializable` before shipping data across the network
+ `: Ordering` context bound supplies an implicit `Ordering[A]` so `sortBy` and `max` work
+ `: ClassTag` context bound supplies runtime class information, needed for arrays or encoders in generic code

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## What are lazy val and by-name parameters?

A `lazy val` is initialized on first access and memoized. A by-name parameter (`=> T`) defers evaluation until the method body uses it, and re-evaluates on each use unless you cache it.

```scala
lazy val spark = SparkSession.builder().appName("orders").getOrCreate()

def logDebug(message: => String): Unit =
  if (sys.env.get("DEBUG").contains("1")) println(message)   // not evaluated when debug is off

logDebug(s"expensive=${spark.read.parquet("s3://acme/orders/").count()}")

def twice[A](value: => A): (A, A) = (value, value)   // evaluates value twice
```

By-name parameters power assertions, retries, and cheap logging. In Spark jobs, `lazy val` for the `SparkSession` and for shared schemas avoids creating sessions during unit tests that never touch Spark. `lazy val` is thread-safe by default, so concurrent first access blocks until initialization completes.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do Futures and basic concurrency work in Scala?

`Future[T]` is a value that will be available later. Computation starts when the `Future` is created, runs on an `ExecutionContext`, and is composed with `map`, `flatMap`, and `Future.sequence`.

```scala
import scala.concurrent.{Await, ExecutionContext, Future}
import scala.concurrent.duration._

implicit val ec: ExecutionContext = ExecutionContext.global

def fetchPartitionCount(dt: String): Future[Long] = Future {
  Thread.sleep(50)          // stands in for a blocking call or a Spark job submission
  dt.hashCode.toLong & 0xffffL
}

val futures: Seq[Future[Long]] = (1 to 8).map(i => fetchPartitionCount(f"2026-10-$i%02d"))
val total: Future[Long] = Future.sequence(futures).map(_.sum)
total.foreach(rows => println(s"total rows=$rows"))
Await.result(total, 1.minute)
```

Rules that matter in data pipelines:

+ Do not use the global execution context for blocking work such as JDBC or file IO; size a dedicated pool, and bound fan-out because hundreds of concurrent Spark job submissions from one driver is worse than batching

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How does Java interoperability work in Scala?

Scala runs on the JVM, calls Java directly, and extends Java classes. The friction is mostly collection conversions and `null`, which is why `scala.jdk.CollectionConverters` exists.

```scala
import java.time.Instant
import java.util.{List => JList, Properties}
import scala.jdk.CollectionConverters._

val now: Instant = Instant.now()
val props = new Properties()
props.put("bootstrap.servers", "broker1:9092")

val javaList: JList[String] = List("orders", "payments").asJava
val backAgain: List[String] = javaList.asScala.toList
val bucket: Option[String] = Option(System.getenv("BUCKET"))   // wrap nullable Java result
```

Interop points interviewers check:

+ `scala.jdk.CollectionConverters._` is current in 2.13 and 3; the older `JavaConverters` is deprecated
+ Java methods that can return `null` should be wrapped with `Option(...)` at the call site
+ Scala annotations such as `@BeanProperty` and `@throws` expose Java-visible members when Java must consume the class
+ Java builders and setters stay as they are, which is why Kafka configuration uses `props.put(...)` rather than Scala collections

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## How do you structure an sbt project with dependencies and tests?

sbt is the standard Scala build tool. A job project has a small, predictable layout, and the build file is itself Scala code.

```text
my-job/
  build.sbt
  src/main/scala/com/acme/OrdersJob.scala
  src/test/scala/com/acme/OrdersJobSpec.scala
```

```scala
// build.sbt
ThisBuild / scalaVersion := "2.13.14"

val sparkVersion = "3.5.1"

lazy val root = (project in file("."))
  .settings(
    name := "orders-job",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-sql" % sparkVersion % Provided,
      "org.scalameta"    %% "munit" % "1.0.0" % Test
    ),
    Test / fork := true
  )
```

`%%` appends the Scala binary version (resolving `spark-sql_2.13`), and Spark dependencies are `Provided` because the cluster already ships them. `Test / fork := true` gives tests their own JVM so Spark and sbt classloaders do not conflict. Tests use MUnit below; ScalaTest works the same way with `AnyFunSuite` and `assert`.

```scala
// src/test/scala/com/acme/OrdersJobSpec.scala
import munit.FunSuite

final class OrdersJobSpec extends FunSuite {
  test("parseAmount strips currency symbols") {
    assertEquals(OrdersJob.parseAmount("$1,250.00"), Some(BigDecimal("1250.00")))
  }
}
```

Build and test with `sbt compile`, `sbt test`, `sbt "runMain com.acme.OrdersJob --dt 2026-10-04"`, or `sbt publishLocal` to share the transforms library with other jobs.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## What Scala idioms matter for Spark?

Spark's Scala API exposes typed `Dataset[T]`, `Encoders`, strongly typed aggregations, and direct access to internals. The main design decision is typed versus untyped.

```scala
import org.apache.spark.sql.{Dataset, SparkSession}
import org.apache.spark.sql.functions.{broadcast, col, udf}

final case class RawOrder(orderId: Long, customerId: Long, amount: BigDecimal, status: String)

val spark = SparkSession.builder().appName("orders").getOrCreate()
import spark.implicits._

val raw: Dataset[RawOrder] = spark.read
  .option("header", "true")
  .csv("s3://acme-raw/orders/")               // CSV columns arrive as strings
  .withColumn("orderId", col("orderId").cast("long"))
  .withColumn("customerId", col("customerId").cast("long"))
  .withColumn("amount", col("amount").cast("decimal(10,2)"))
  .as[RawOrder]

val paid: Dataset[RawOrder] = raw.filter(o => o.status == "PAID" && o.amount > 0)

val normalizeStatus = udf((s: String) => Option(s).map(_.trim.toUpperCase).getOrElse("UNKNOWN"))
val withStatus = paid.toDF().withColumn("status_norm", normalizeStatus(col("status")))
val enriched = withStatus.join(broadcast(spark.table("main.gold.dim_customer")), Seq("customerId"), "left")
```

Typed versus untyped:

+ `Dataset[T]` with case classes gives compile-time field checks and `Encoder[T]` derivation via `import spark.implicits._`
+ `DataFrame` (`Dataset[Row]`) with `Column` handles runtime-only schemas, is usually better optimized because Catalyst sees the whole expression tree, and suits wide or dynamic data

When Scala beats PySpark: CPU-heavy row-wise logic, logic shared as a JVM library with Kafka or Flink, and teams that want schema errors at build time. PySpark still wins on notebook iteration, the Python ML ecosystem, hiring friction, and built-in transformations where the JVM difference is small. Use a UDF only when no built-in function exists, and broadcast the small side of a join.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## What are common Scala pitfalls in data engineering?

+ `null` leaks from Java and from Spark rows. Wrap with `Option(...)` at the boundary, and remember that a `null` inside a `Dataset[T]` field does not throw until you call a method on it
+ `==` versus `equals`: `==` calls `equals` and is null-safe, so `a == b` is usually right. It is structural for case classes but reference-based for `Array`, where `sameElements` is what you want; `eq` is reference identity
+ Mutable collections captured in closures are copied to executors, so mutations are lost. Keep transformations pure and return values
+ Implicit conversions hide real errors and slow compilation; Scala 3 requires `import scala.language.implicitConversions` to use them, which is a hint to avoid them
+ Read stack traces bottom-up. Start from the deepest `Caused by` and the first frame in your own package; Spark wraps failures in `SparkException`, so the useful line is usually several causes down
+ Version mismatch is a real production failure: Spark 3.x artifacts exist for Scala 2.12 and 2.13, while Spark 4.x dropped 2.12 and publishes 2.13 only; adding a Scala 3 or mismatched 2.13 library to a 2.12 cluster gives `NoSuchMethodError` at runtime
+ Scala 2 versus Scala 3: `implicit`/`implicit class` versus `given`/`using`/`extension`; `_` versus `?` for wildcard types; procedure syntax and symbol literals removed; in 2.13 `Seq` defaults to `scala.collection.immutable.Seq`

A defensive pattern for the `null` pitfall:

```scala
def validate(o: RawOrder): Either[String, RawOrder] = {
  if (o.status == null || o.status.trim.isEmpty) Left(s"missing status for order ${o.orderId}")
  else if (o.amount == null || o.amount <= 0)    Left(s"bad amount for order ${o.orderId}")
  else Right(o.copy(status = o.status.trim.toUpperCase))
}
```

Route `Left` values to a quarantine table and continue, rather than throwing and failing the whole partition.

[Table of Contents](#Scala-Basics-for-Data-Engineers)

## Real world use cases for Scala in data engineering

### 1. Typed Spark Dataset pipeline

Case classes plus `Dataset[T]` make the transform contract explicit, and `partitionBy` keeps output rewritable per day.

```scala
import org.apache.spark.sql.{Dataset, SparkSession}

final case class RawOrder(orderId: Long, customerId: Long, amount: BigDecimal, status: String, ts: String)
final case class FactOrder(orderId: Long, customerId: Long, amount: BigDecimal, status: String, dt: String)

object TypedOrdersJob {
  def transform(raw: Dataset[RawOrder]): Dataset[FactOrder] = {
    import raw.sparkSession.implicits._
    raw.filter(o => o.status != null && o.amount > 0)
      .map(o => FactOrder(o.orderId, o.customerId, o.amount, o.status.trim.toUpperCase, o.ts.take(10)))
  }

  def run(spark: SparkSession): Unit = {
    import spark.implicits._
    import org.apache.spark.sql.functions.col
    val raw = spark.read.option("header", "true").csv("s3://acme-raw/orders/")
      .withColumn("orderId", col("orderId").cast("long"))
      .withColumn("customerId", col("customerId").cast("long"))
      .withColumn("amount", col("amount").cast("decimal(10,2)"))
      .as[RawOrder]
    transform(raw).write.mode("overwrite").partitionBy("dt").parquet("s3://acme-curated/fact_order/")
  }
}
```

Why Scala: a renamed or retyped case class field fails the build instead of the midnight run, and `transform` is unit-testable on a local `SparkSession` with a small `Seq` input.

### 2. Kafka consumer that lands raw events

The official Kafka client is Java, so Scala consumes it directly and pattern matches on the decoded payload for routing.

```scala
import java.time.Duration
import java.util.{Collections, Properties}
import org.apache.kafka.clients.consumer.{ConsumerConfig, KafkaConsumer}
import org.apache.kafka.common.serialization.StringDeserializer
import scala.jdk.CollectionConverters._

object OrdersConsumer {
  def main(args: Array[String]): Unit = {
    val props = new Properties()
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092")
    props.put(ConsumerConfig.GROUP_ID_CONFIG, "orders-loader")
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, classOf[StringDeserializer].getName)
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, classOf[StringDeserializer].getName)
    props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false")

    val consumer = new KafkaConsumer[String, String](props)
    consumer.subscribe(Collections.singletonList("orders"))
    try {
      while (true) {
        val records = consumer.poll(Duration.ofMillis(500))
        records.asScala.foreach(r => println(s"partition=${r.partition()} offset=${r.offset()}"))
        if (!records.isEmpty) consumer.commitSync()   // commit only after the batch is durable
      }
    } finally consumer.close()
  }
}
```

Why Scala: disabling auto-commit and committing after the batch is durable gives at-least-once delivery with a controlled checkpoint, and the consumer can ship in the same JVM artifact as the transformation library.

### 3. Flink job sketch

Flink exposes a JVM DataStream API with a Scala layer, so a Scala service can own a streaming job end to end.

```scala
import org.apache.flink.api.common.eventtime.WatermarkStrategy
import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.connector.kafka.source.KafkaSource
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer
import org.apache.flink.streaming.api.scala._

object OrdersFlinkJob {
  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.enableCheckpointing(60000)

    val source = KafkaSource.builder[String]()
      .setBootstrapServers("broker1:9092")
      .setTopics("orders")
      .setGroupId("orders-flink")
      .setStartingOffsets(OffsetsInitializer.earliest())
      .setValueOnlyDeserializer(new SimpleStringSchema())
      .build()

    env.fromSource(source, WatermarkStrategy.noWatermarks(), "orders")
      .map(json => (json.take(1), BigDecimal(json.length)))   // parse: (customerId, amount)
      .filter { case (_, amount) => amount > 1000 }
      .keyBy(_._1)
      .sum(1)
      .print()

    env.execute("orders-flink")
  }
}
```

Why Scala: the job is a normal JVM deployment with the same build, logging, and tests as the rest of the platform. Version caveat: Flink's Scala DataStream API has been deprecated and removed in recent releases, so prefer the Java API for new projects.

### 4. Shared transformation library for batch and streaming

One library keeps batch and streaming definitions from drifting apart.

```scala
// src/main/scala/com/acme/transforms/OrderTransforms.scala
package com.acme.transforms

import org.apache.spark.sql.Dataset

final case class Order(orderId: Long, customerId: Long, amount: BigDecimal, status: String)

object OrderTransforms {
  def paidOnly(ds: Dataset[Order]): Dataset[Order] =
    ds.filter(o => o.status == "PAID" && o.amount > 0)

  def revenueByStatus(ds: Dataset[Order]): Dataset[(String, BigDecimal)] = {
    import ds.sparkSession.implicits._
    ds.groupByKey(_.status).mapValues(_.amount).reduceGroups(_ + _)
  }
}
```

Published with `sbt publishLocal` or to the company artifact repository, then pulled into the batch job and the streaming job as one versioned dependency, so a revenue-rule change is reviewed and released once.

### 5. Streaming ETL with Futures and bounded batching

A micro-batch streaming ETL step consumes a checkpointed stream, and catch-up or replay work is driven with `Future` batching so the driver stays in control of write parallelism.

```scala
import scala.concurrent.{Await, Future}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._

object StreamingEtlRunner {
  def runPartition(dt: String): Future[Long] = Future {
    // submit one Spark job or API call for a single day and return its row count
    dt.hashCode.toLong & 0xffffL
  }

  def main(args: Array[String]): Unit = {
    val dates = (1 to 10).map(i => f"2026-09-$i%02d")
    dates.grouped(4).foreach { batch =>
      val rows = Await.result(Future.sequence(batch.map(runPartition)), 30.minutes).sum
      println(s"batch ${batch.head}..${batch.last}: $rows rows")
    }
  }
}
```

Why Scala: bounded batches stop a driver from submitting thousands of concurrent jobs while draining a backlog, completion is tracked per batch so a failed group can be retried, and the row counts feed data-quality checkpoints.

[Table of Contents](#Scala-Basics-for-Data-Engineers)
