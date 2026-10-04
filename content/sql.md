## [Main title](../README.md)
### [Interview questions](full.md)

# SQL

**Notebook:** [`notebooks/topics/sql.ipynb`](../notebooks/topics/sql.ipynb) - runnable version of this topic with self-checking exercises.

+ [Write sql query to get the second highest salary among all employees?](#Write-sql-query-to-get-the-second-highest-salary-among-all-employees)
+ [There are multiple ways to get the second highest salary among all employees.](#There-are-multiple-ways-to-get-the-second-highest-salary-among-all-employees)
+ [How can we retrieve alternate records from a table in oracle?](#How-can-we-retrieve-alternate-records-from-a-table-in-oracle)
+ [Write sql query to find max salary and department name from each department.](#Write-sql-query-to-find-max-salary-and-department-name-from-each-department)
+ [Write sql query to find records in table a that are not in table b without using not in operator.](#Write-sql-query-to-find-records-in-table-a-that-are-not-in-table-b-without-using-not-in-operator)
+ [What is the result of following query?](#What-is-the-result-of-following-query)
+ [Write sql query to find employees that have same name and email.](#Write-sql-query-to-find-employees-that-have-same-name-and-email)
+ [Write sql query to find max salary from each department.](#Write-sql-query-to-find-max-salary-from-each-department)
+ [Write sql query to get the nth highest salary among all employees.](#Write-sql-query-to-get-the-nth-highest-salary-among-all-employees)
+ [How can you find 10 employees with odd number as employee id?](#How-can-you-find-10-employees-with-odd-number-as-employee-id)
+ [Write sql query to get the names of employees whose date of birth is between 01/01/1990 to 31/12/2000.](#Write-sql-query-to-get-the-names-of-employees-whose-date-of-birth-is-between-01011990-to-31122000)
+ [Write sql query to get the quarter from date.](#Write-sql-query-to-get-the-quarter-from-date)
+ [Write query to find employees with duplicate email.](#Write-query-to-find-employees-with-duplicate-email)
+ [Write a query to find all employee whose name contains the word "rich", regardless of case.](#Write-a-query-to-find-all-employee-whose-name-contains-the-word-rich-regardless-of-case)
+ [Is it safe to use rowid to locate a record in oracle sql queries?](#Is-it-safe-to-use-rowid-to-locate-a-record-in-oracle-sql-queries)
+ [What is a pseudo-column?](#What-is-a-pseudo-column)
+ [What are the reasons for denormalizing the data?](#What-are-the-reasons-for-denormalizing-the-data)
+ [What is the feature in sql for writing if and else statements?](#What-is-the-feature-in-sql-for-writing-if-and-else-statements)
+ [What is the difference between delete and truncate in sql?](#What-is-the-difference-between-delete-and-truncate-in-sql)
+ [What is the difference between ddl and dml commands in sql?](#What-is-the-difference-between-ddl-and-dml-commands-in-sql)
+ [Why do we use escape characters in sql queries?](#Why-do-we-use-escape-characters-in-sql-queries)
+ [What is the difference between primary key and unique key in sql?](#What-is-the-difference-between-primary-key-and-unique-key-in-sql)
+ [What is the difference between inner join and outer join in sql?](#What-is-the-difference-between-inner-join-and-outer-join-in-sql)
+ [What is the difference between left outer join and right outer join?](#What-is-the-difference-between-left-outer-join-and-right-outer-join)
+ [What is the datatype of rowid?](#What-is-the-datatype-of-rowid)
+ [What is the difference between where clause and having clause?](#What-is-the-difference-between-where-clause-and-having-clause)
+ [How will you calculate the number of days between two dates in mysql?](#How-will-you-calculate-the-number-of-days-between-two-dates-in-mysql)
+ [What are the different types of triggers in mysql?](#What-are-the-different-types-of-triggers-in-mysql)
+ [What are the differences between heap table and temporary table in mysql?](#What-are-the-differences-between-heap-table-and-temporary-table-in-mysql)
+ [What is a heap table in mysql?](#What-is-a-heap-table-in-mysql)
+ [What is the difference between blob and text data type in mysql?](#What-is-the-difference-between-blob-and-text-data-type-in-mysql)
+ [What will happen when auto increme on an integer column reaches max value in mysql?](#What-will-happen-when-auto-increme-on-an-integer-column-reaches-max-value-in-mysql)
+ [What are the advantages of mysql as compared with oracle db?](#What-are-the-advantages-of-mysql-as-compared-with-oracle-db)
+ [What are the disadvantages of mysql?](#What-are-the-disadvantages-of-mysql)
+ [What is the difference between char and varchar datatype in mysql?](#What-is-the-difference-between-char-and-varchar-datatype-in-mysql)
+ [What is the use of i am a dummy flag in mysql?](#What-is-the-use-of-i-am-a-dummy-flag-in-mysql)
+ [How can we get current date and time in mysql?](#How-can-we-get-current-date-and-time-in-mysql)
+ [What is the difference between timestamp in unix and mysql?](#What-is-the-difference-between-timestamp-in-unix-and-mysql)
+ [How will you limit a mysql query to display only top 10 rows?](#How-will-you-limit-a-mysql-query-to-display-only-top-10-rows)
+ [What is automatic initialization and updating for timestamp in a mysql table?](#What-is-automatic-initialization-and-updating-for-timestamp-in-a-mysql-table)
+ [How can we get the list of all the indexes on a table?](#How-can-we-get-the-list-of-all-the-indexes-on-a-table)
+ [What is savepoint in mysql?](#What-is-savepoint-in-mysql)
+ [What is the difference between rollback to savepoint and release savepoint?](#What-is-the-difference-between-rollback-to-savepoint-and-release-savepoint)
+ [How will you search for a string in mysql column?](#How-will-you-search-for-a-string-in-mysql-column)
+ [How can we find the version of the mysql server and the name of the current database by select query?](#How-can-we-find-the-version-of-the-mysql-server-and-the-name-of-the-current-database-by-select-query)
+ [What is the use of ifnull operator in mysql?](#What-is-the-use-of-ifnull-operator-in-mysql)
+ [How will you check if a table exists in mysql?](#How-will-you-check-if-a-table-exists-in-mysql)
+ [How will you see the structure of a table in mysql?](#How-will-you-see-the-structure-of-a-table-in-mysql)
+ [What are the objects that can be created by create statement in mysql?](#What-are-the-objects-that-can-be-created-by-create-statement-in-mysql)
+ [How will you see the current user logged into mysql connection?](#How-will-you-see-the-current-user-logged-into-mysql-connection)
+ [What is the difference between batch and interactive modes of mysql?](#What-is-the-difference-between-batch-and-interactive-modes-of-mysql)
+ [How can we get a random number between 1 and 100 in mysql?](#How-can-we-get-a-random-number-between-1-and-100-in-mysql)
+ [What does sql in mysql stand for?](#What-does-sql-in-mysql-stand-for)
+ [What does a mysql database contain?](#What-does-a-mysql-database-contain)
+ [How can you interact with mysql?](#How-can-you-interact-with-mysql)
+ [What is mysql database queries?](#What-is-mysql-database-queries)
+ [What are some common mysql commands?](#What-are-some-common-mysql-commands)
+ [How do you create a database in mysql?](#How-do-you-create-a-database-in-mysql)
+ [How do you create a table using mysql?](#How-do-you-create-a-table-using-mysql)
+ [How do you insert data into mysql?](#How-do-you-insert-data-into-mysql)
+ [How do you upsert with MERGE in SQL?](#How-do-you-upsert-with-MERGE-in-SQL)
+ [How do you remove a column from a database?](#How-do-you-remove-a-column-from-a-database)
+ [How to create an index in mysql?](#How-to-create-an-index-in-mysql)
+ [How to delete data from a mysql table?](#How-to-delete-data-from-a-mysql-table)
+ [How do you view a database in mysql?](#How-do-you-view-a-database-in-mysql)
+ [What are the numeric data types in mysql?](#What-are-the-numeric-data-types-in-mysql)
+ [What are the string data types in mysql?](#What-are-the-string-data-types-in-mysql)
+ [What are the temporal data types in mysql?](#What-are-the-temporal-data-types-in-mysql)
+ [What is blob in mysql?](#What-is-blob-in-mysql)
+ [How to add users in mysql?](#How-to-add-users-in-mysql)
+ [What is mysql views?](#What-is-mysql-views)
+ [How do you create and execute views in mysql?](#How-do-you-create-and-execute-views-in-mysql)
+ [What is mysql triggers?](#What-is-mysql-triggers)
+ [How many triggers are possible in mysql?](#How-many-triggers-are-possible-in-mysql)
+ [What is the mysql server?](#What-is-the-mysql-server)
+ [What are the mysql clients and utilities?](#What-are-the-mysql-clients-and-utilities)
+ [Can you explain the logical architecture of mysql?](#Can-you-explain-the-logical-architecture-of-mysql)
+ [What is scaling in mysql?](#What-is-scaling-in-mysql)
+ [What is sharding in sql?](#What-is-sharding-in-sql)
+ [What are transaction storage engines in mysql?](#What-are-transaction-storage-engines-in-mysql)
+ [What is mysql?](#What-is-mysql)
+ [What are some advantages of using mysql?](#What-are-some-advantages-of-using-mysql)
+ [What do you mean by databases?](#What-do-you-mean-by-databases)
+ [Query to find second highest marks of a student?](#Query-to-find-second-highest-marks-of-a-student)
+ [Query to find duplicate rows in table?](#Query-to-find-duplicate-rows-in-table)
+ [What is the query to fetch first record from student table?](#What-is-the-query-to-fetch-first-record-from-student-table)
+ [What is the query to fetch last record from student table?](#What-is-the-query-to-fetch-last-record-from-student-table)
+ [What is query to display first 4 records from student table?](#What-is-query-to-display-first-4-records-from-student-table)
+ [What is query to display last 3 records from student table?](#What-is-query-to-display-last-3-records-from-student-table)
+ [What is query to display nth record from student table?](#What-is-query-to-display-nth-record-from-student-table)
+ [How to get 3 highest marks from student table?](#How-to-get-3-highest-marks-from-student-table)
+ [How to display odd rows in student table?](#How-to-display-odd-rows-in-student-table)
+ [How to display even rows in student table?](#How-to-display-even-rows-in-student-table)
+ [How can i create table with same structure of student table?](#How-can-i-create-table-with-same-structure-of-student-table)
+ [Select all records from student table whose name is a and b.](#Select-all-records-from-student-table-whose-name-is-a-and-b)
+ [What is ddl and dml and dcl?](#What-is-ddl-and-dml-and-dcl)
+ [How do you get the number of rows affected by query?](#How-do-you-get-the-number-of-rows-affected-by-query)
+ [If the value in the column is repeatable and how do you find out unique values?](#If-the-value-in-the-column-is-repeatable-and-how-do-you-find-out-unique-values)
+ [How do you return hundred books starting from 25th?](#How-do-you-return-hundred-books-starting-from-25th)
+ [You wrote search engine that should retrieve 10 results at a time but at the same time you do like to know how many rows there are total.](#You-wrote-search-engine-that-should-retrieve-10-results-at-a-time-but-at-the-same-time-you-do-like-to-know-how-many-rows-there-are-total)
+ [How would you write a query to select all teams that won either 2 and 4 and 6 or 8 games?](#How-would-you-write-a-query-to-select-all-teams-that-won-either-2-and-4-and-6-or-8-games)
+ [How would you select all users whose phone number is null?](#How-would-you-select-all-users-whose-phone-number-is-null)
+ [How do you find out which auto increment was assigned on the last insert?](#How-do-you-find-out-which-auto-increment-was-assigned-on-the-last-insert)
+ [On executing delete statement i keep getting the error about foreign key constraint failing so what do i do?](#On-executing-delete-statement-i-keep-getting-the-error-about-foreign-key-constraint-failing-so-what-do-i-do)
+ [When would you use order by in delete statement?](#When-would-you-use-order-by-in-delete-statement)
+ [How can you see all indexes defined for a table?](#How-can-you-see-all-indexes-defined-for-a-table)
+ [How would you delete column?](#How-would-you-delete-column)
+ [How would you change a table to innodb?](#How-would-you-change-a-table-to-innodb)
+ [How do you concatenate strings in mysql?](#How-do-you-concatenate-strings-in-mysql)
+ [How do you get a portion of string?](#How-do-you-get-a-portion-of-string)
+ [What is the difference between char length and length?](#What-is-the-difference-between-char-length-and-length)
+ [How do you convert string to utf-8?](#How-do-you-convert-string-to-utf-8)
+ [How do you get month from timestamp?](#How-do-you-get-month-from-timestamp)
+ [How do you offload the time and date handling to mysql?](#How-do-you-offload-the-time-and-date-handling-to-mysql)
+ [How do you add three minutes to a date?](#How-do-you-add-three-minutes-to-a-date)
+ [What is the difference between unix timestamps and mysql timestamps?](#What-is-the-difference-between-unix-timestamps-and-mysql-timestamps)
+ [How do you convert between unix timestamps and mysql timestamps?](#How-do-you-convert-between-unix-timestamps-and-mysql-timestamps)
+ [What are enums used for in mysql?](#What-are-enums-used-for-in-mysql)
+ [How are enums and sets represented internally?](#How-are-enums-and-sets-represented-internally)
+ [How do you start and stop mysql on windows?](#How-do-you-start-and-stop-mysql-on-windows)
+ [How do you start mysql on linux?](#How-do-you-start-mysql-on-linux)
+ [Explain the difference between mysql and mysql interfaces in php?](#Explain-the-difference-between-mysql-and-mysql-interfaces-in-php)
+ [What is the default port for mysql server?](#What-is-the-default-port-for-mysql-server)
+ [What does tee command do in mysql?](#What-does-tee-command-do-in-mysql)
+ [Can you save your connection settings to a conf file?](#Can-you-save-your-connection-settings-to-a-conf-file)
+ [How do you change a password for an existing user via mysqladmin?](#How-do-you-change-a-password-for-an-existing-user-via-mysqladmin)
+ [Use mysqldump to create a copy of the database?](#Use-mysqldump-to-create-a-copy-of-the-database)
+ [Have you ever used mysql administrator and mysql query browser?](#Have-you-ever-used-mysql-administrator-and-mysql-query-browser)
+ [What are some good ideas regarding user security in mysql?](#What-are-some-good-ideas-regarding-user-security-in-mysql)
+ [Explain the difference between myisam static and myisam dynamic?](#Explain-the-difference-between-myisam-static-and-myisam-dynamic)
+ [What does myisamchk do?](#What-does-myisamchk-do)
+ [Explain advantages of innodb over myisam?](#Explain-advantages-of-innodb-over-myisam)
+ [Explain advantages of myisam over innodb?](#Explain-advantages-of-myisam-over-innodb)
+ [What are heap tables in mysql?](#What-are-heap-tables-in-mysql)
+ [How do you control the max size of a heap table?](#How-do-you-control-the-max-size-of-a-heap-table)
+ [What are csv tables?](#What-are-csv-tables)
+ [Explain federated tables?](#Explain-federated-tables)
+ [What is serial data type in mysql?](#What-is-serial-data-type-in-mysql)
+ [What happens when the column is set to auto increment and you reach the maximum value for that table?](#What-happens-when-the-column-is-set-to-auto-increment-and-you-reach-the-maximum-value-for-that-table)
+ [Explain the difference between bool, tinyint and bit?](#Explain-the-difference-between-bool-tinyint-and-bit)
+ [Explain the difference between float, double and real?](#Explain-the-difference-between-float-double-and-real)
+ [What happens if a table has one column defined as timestamp?](#What-happens-if-a-table-has-one-column-defined-as-timestamp)
+ [But what if you really want to store the timestamp data, such as the publication date of the article?](#But-what-if-you-really-want-to-store-the-timestamp-data-such-as-the-publication-date-of-the-article)
+ [Explain data type timestamp default current_timestamp on update current_timestamp?](#Explain-data-type-timestamp-default-current_timestamp-on-update-current_timestamp)
+ [What does timestamp on update current_timestamp data type do?](#What-does-timestamp-on-update-current_timestamp-data-type-do)
+ [If I created a column with data type varchar(3) so what would I expect to see in mysql table?](#If-I-created-a-column-with-data-type-varchar3-so-what-would-I-expect-to-see-in-mysql-table)
+ [General information about mysql.](#General-information-about-mysql)
+ [Why use mysql?](#Why-use-mysql)
+ [How mysql optimizes distinct?](#How-mysql-optimizes-distinct)
+ [How mysql optimizes limit?](#How-mysql-optimizes-limit)
+ [Mysql speed of delete queries ?](#Mysql-speed-of-delete-queries)
+ [What is the difference between mysql_fetch_array and mysql_fetch_object?](#What-is-the-difference-between-mysql_fetch_array-and-mysql_fetch_object)
+ [What are the different table present in mysql?](#What-are-the-different-table-present-in-mysql)
+ [What is primary key?](#What-is-primary-key)
+ [What is foreign key?](#What-is-foreign-key)
+ [What is index?](#What-is-index)
+ [What is join?](#What-is-join)
+ [What is union?](#What-is-union)
+ [What is isam?](#What-is-isam)
+ [What is innodb?](#What-is-innodb)
+ [What is bdb berkeleydb?](#What-is-bdb-berkeleydb)
+ [What is csv?](#What-is-csv)
+ [What is transaction?](#What-is-transaction)
+ [What is commit?](#What-is-commit)
+ [What is rollback?](#What-is-rollback)
+ [How many groups of data types?](#How-many-groups-of-data-types)
+ [What is the differences between char and nchar?](#What-is-the-differences-between-char-and-nchar)
+ [How to escape special characters in sql statements?](#How-to-escape-special-characters-in-sql-statements)
+ [How to concatenate two character strings?](#How-to-concatenate-two-character-strings)
+ [How to enter characters as hex numbers?](#How-to-enter-characters-as-hex-numbers)
+ [How to enter boolean values in sql statements?](#How-to-enter-boolean-values-in-sql-statements)
+ [How to convert numeric values to character strings?](#How-to-convert-numeric-values-to-character-strings)
+ [How to use in conditions?](#How-to-use-in-conditions)
+ [How to use like conditions?](#How-to-use-like-conditions)
+ [How to present a past time in hours and minutes and seconds?](#How-to-present-a-past-time-in-hours-and-minutes-and-seconds)
+ [How to add a new column to an existing table in mysql?](#How-to-add-a-new-column-to-an-existing-table-in-mysql)
+ [How to delete an existing column in a table?](#How-to-delete-an-existing-column-in-a-table)
+ [How to rename an existing column in a table?](#How-to-rename-an-existing-column-in-a-table)
+ [How to rename an existing table in mysql?](#How-to-rename-an-existing-table-in-mysql)
+ [How to create a table index in mvsql?](#How-to-create-a-table-index-in-mvsql)
+ [How to get a list of indexes of an existing table?](#How-to-get-a-list-of-indexes-of-an-existing-table)
+ [How to drop an existing index in mysql?](#How-to-drop-an-existing-index-in-mysql)
+ [How to drop an existing view in mysql?](#How-to-drop-an-existing-view-in-mysql)
+ [How to create a new view in mysql?](#How-to-create-a-new-view-in-mysql)
+ [How to increment dates by 1111 mysql?](#How-to-increment-dates-by-1111-mysql)
+ [Explain what is a database?](#Explain-what-is-a-database)
+ [Explain what is dbms?](#Explain-what-is-dbms)
+ [Explain what is rdbms?](#Explain-what-is-rdbms)
+ [What are the popular database management systems in it industry?](#What-are-the-popular-database-management-systems-in-it-industry)
+ [Explain what is sql?](#Explain-what-is-sql)
+ [Explain what is table in a database?](#Explain-what-is-table-in-a-database)
+ [Explain what is a field in a database and record in a database?](#Explain-what-is-a-field-in-a-database-and-record-in-a-database)
+ [What is the use of nvl function?](#What-is-the-use-of-nvl-function)
+ [Explain what is a column in a table?](#Explain-what-is-a-column-in-a-table)
+ [What are the different types of sql commands?](#What-are-the-different-types-of-sql-commands)
+ [What are the different ddl commands in sql?](#What-are-the-different-ddl-commands-in-sql)
+ [What are the different dml commands in sql?](#What-are-the-different-dml-commands-in-sql)
+ [What are the different dcl commands in sql?](#What-are-the-different-dcl-commands-in-sql)
+ [What are the different tcl commands in sql?](#What-are-the-different-tcl-commands-in-sql)
+ [Explain what is an index?](#Explain-what-is-an-index)
+ [Explain what is a view?](#Explain-what-is-a-view)
+ [Explain what is a subquery ?](#Explain-what-is-a-subquery)
+ [How do you write a CTE and a recursive CTE in SQL?](#How-do-you-write-a-CTE-and-a-recursive-CTE-in-SQL)
+ [What is the difference between rename and alias?](#What-is-the-difference-between-rename-and-alias)
+ [What is a join?](#What-is-a-join)
+ [What are the different types of joins?](#What-are-the-different-types-of-joins)
+ [What are sql constraints?](#What-are-sql-constraints)
+ [What are the constraints available in sql?](#What-are-the-constraints-available-in-sql)
+ [What is a unique key and primary key and foreign key?](#What-is-a-unique-key-and-primary-key-and-foreign-key)
+ [What is the difference between unique and primary key constraints?](#What-is-the-difference-between-unique-and-primary-key-constraints)
+ [What is a null value?](#What-is-a-null-value)
+ [What is normalization?](#What-is-normalization)
+ [What is stored procedure?](#What-is-stored-procedure)
+ [What is a trigger?](#What-is-a-trigger)
+ [List out the acid properties and explain?](#List-out-the-acid-properties-and-explain)
+ [What is the difference between delete, truncate and drop command?](#What-is-the-difference-between-delete-truncate-and-drop-command)
+ [What is the difference between having and where clause?](#What-is-the-difference-between-having-and-where-clause)
+ [What are aggregate functions in sql?](#What-are-aggregate-functions-in-sql)
+ [What are string functions in sql?](#What-are-string-functions-in-sql)
+ [Explain the working of sql privileges?](#Explain-the-working-of-sql-privileges)
+ [How many types of privileges are available in sql?](#How-many-types-of-privileges-are-available-in-sql)
+ [What is sql injection?](#What-is-sql-injection)
+ [What is the difference between clustered and non-clustered indexes?](#What-is-the-difference-between-clustered-and-non-clustered-indexes)
+ [What is relationship and how many types of relationship are there?](#What-is-relationship-and-how-many-types-of-relationship-are-there)
+ [What is collation?](#What-is-collation)
+ [What is database white box testing and black box testing?](#What-is-database-white-box-testing-and-black-box-testing)
+ [What are the advantages of views?](#What-are-the-advantages-of-views)
+ [What is schema?](#What-is-schema)
+ [What is the difference between sql and mysql?](#What-is-the-difference-between-sql-and-mysql)
+ [What is sql sandbox in sql server?](#What-is-sql-sandbox-in-sql-server)
+ [What are the steps to take to improve performance of a poor performing query?](#What-are-the-steps-to-take-to-improve-performance-of-a-poor-performing-query)
+ [What is a deadlock and what is a live lock?](#What-is-a-deadlock-and-what-is-a-live-lock)
+ [What is blocking and how would you troubleshoot it?](#What-is-blocking-and-how-would-you-troubleshoot-it)
+ [Explain the different types of backups available in sql server.](#Explain-the-different-types-of-backups-available-in-sql-server)
+ [What is database isolation in sql server?](#What-is-database-isolation-in-sql-server)
+ [What is a schema in sql server 2005? explain how to create a new schema in a database?](#What-is-a-schema-in-sql-server-2005-explain-how-to-create-a-new-schema-in-a-database)
+ [Explain how to create a scrollable cursor with the scroll option.](#Explain-how-to-create-a-scrollable-cursor-with-the-scroll-option)
+ [Explain how to create a dynamic cursor with the dynamic option?](#Explain-how-to-create-a-dynamic-cursor-with-the-dynamic-option)
+ [What are database files and filegroups?](#What-are-database-files-and-filegroups)
+ [Describe in brief databases and sql server databases architecture.](#Describe-in-brief-databases-and-sql-server-databases-architecture)
+ [What are the steps to improve the performance of a query?](#What-are-the-steps-to-improve-the-performance-of-a-query)
+ [How do you read a query plan with EXPLAIN?](#How-do-you-read-a-query-plan-with-EXPLAIN)
+ [How would you use the sp_ functions to identify the blocking problems?](#How-would-you-use-the-sp_-functions-to-identify-the-blocking-problems)
+ [What are the different types of backups?](#What-are-the-different-types-of-backups)
+ [What are the different levels of isolation?](#What-are-the-different-levels-of-isolation)
+ [How can you start the sql server in the single user mode and the minimal configuration mode?](#How-can-you-start-the-sql-server-in-the-single-user-mode-and-the-minimal-configuration-mode)
+ [How can you know that statistics should be updated?](#How-can-you-know-that-statistics-should-be-updated)
+ [What is replication in sql server?](#What-is-replication-in-sql-server)
+ [Can we initiate a external com object from within sql?](#Can-we-initiate-a-external-com-object-from-within-sql)
+ [What is a schema? how is it useful in sql servers?](#What-is-a-schema-how-is-it-useful-in-sql-servers)
+ [What is write ahead log?](#What-is-write-ahead-log)
+ [What is the use of check points in the transaction logs?](#What-is-the-use-of-check-points-in-the-transaction-logs)
+ [What is a column with identity?](#What-is-a-column-with-identity)
+ [What are scrollable cursors? how are they created?](#What-are-scrollable-cursors-how-are-they-created)
+ [What is raid and how does it help storage of databases?](#What-is-raid-and-how-does-it-help-storage-of-databases)
+ [How can you identify the version number of the sql server installed?](#How-can-you-identify-the-version-number-of-the-sql-server-installed)
+ [What is the use of cascade constraints?](#What-is-the-use-of-cascade-constraints)
+ [What is the function of a odbc manager ?](#What-is-the-function-of-a-odbc-manager)
+ [What are the different types of indexes available in sql server?](#What-are-the-different-types-of-indexes-available-in-sql-server)
+ [What is the difference between clustered and non-clustered index?](#What-is-the-difference-between-clustered-and-non-clustered-index)
+ [What are the high-availability solutions in sql server?](#What-are-the-high-availability-solutions-in-sql-server)
+ [What is denormalization and when would you go for it?](#What-is-denormalization-and-when-would-you-go-for-it)
+ [How do you implement one-to-one, one-to-many and many-to-many relationships while designing tables?](#How-do-you-implement-one-to-one-one-to-many-and-many-to-many-relationships-while-designing-tables)
+ [What is the difference between a primary key and a unique key?](#What-is-the-difference-between-a-primary-key-and-a-unique-key)
+ [What are user defined datatypes and when you should go for them?](#What-are-user-defined-datatypes-and-when-you-should-go-for-them)
+ [What is bit datatype and what is the information that can be stored inside a bit column?](#What-is-bit-datatype-and-what-is-the-information-that-can-be-stored-inside-a-bit-column)
+ [Define candidate key and alternate key and composite key.](#Define-candidate-key-and-alternate-key-and-composite-key)
+ [What is a transaction and what are acid properties?](#What-is-a-transaction-and-what-are-acid-properties)
+ [Explain different isolation levels?](#Explain-different-isolation-levels)
+ [What type of index will get created after executing the above statement?](#What-type-of-index-will-get-created-after-executing-the-above-statement)
+ [Differences between active and active or active and passive cluster configurations?](#Differences-between-active-and-active-or-active-and-passive-cluster-configurations)
+ [What is lock escalation?](#What-is-lock-escalation)
+ [What is the difference between delete table and truncate table commands?](#What-is-the-difference-between-delete-table-and-truncate-table-commands)
+ [What are constraints?](#What-are-constraints)
+ [What is an index and what are the types of indexes and how many clustered indexes can be created on a table?](#What-is-an-index-and-what-are-the-types-of-indexes-and-how-many-clustered-indexes-can-be-created-on-a-table)
+ [How to restart sql server in single user mode and how to start sql server in minimal configuration mode?](#How-to-restart-sql-server-in-single-user-mode-and-how-to-start-sql-server-in-minimal-configuration-mode)
+ [What are statistics under what circumstances they go out of date and how do you update them?](#What-are-statistics-under-what-circumstances-they-go-out-of-date-and-how-do-you-update-them)
+ [If there is significant change in the key values in the index?](#If-there-is-significant-change-in-the-key-values-in-the-index)
+ [What is database replication and what are the different types of replication you can set up in sql server?](#What-is-database-replication-and-what-are-the-different-types-of-replication-you-can-set-up-in-sql-server)
+ [What are the components of physical database structure of oracle database?](#What-are-the-components-of-physical-database-structure-of-oracle-database)
+ [What are the components of logical database structure of oracle database?](#What-are-the-components-of-logical-database-structure-of-oracle-database)
+ [What is a tablespace?](#What-is-a-tablespace)
+ [What is system tablespace and when is it created?](#What-is-system-tablespace-and-when-is-it-created)
+ [Explain the relationship among database and tablespace and data file.](#Explain-the-relationship-among-database-and-tablespace-and-data-file)
+ [What is schema?](#What-is-schema)
+ [What are schema objects?](#What-are-schema-objects)
+ [Can objects of the same schema reside in different tablespaces?](#Can-objects-of-the-same-schema-reside-in-different-tablespaces)
+ [Can a tablespace hold objects from different schemes?](#Can-a-tablespace-hold-objects-from-different-schemes)
+ [What is oracle table?](#What-is-oracle-table)
+ [What is an oracle view?](#What-is-an-oracle-view)
+ [What is partial backup?](#What-is-partial-backup)
+ [What is mirrored on line redo log?](#What-is-mirrored-on-line-redo-log)
+ [What is full backup?](#What-is-full-backup)
+ [Can a view based on another view?](#Can-a-view-based-on-another-view)
+ [Can a tablespace hold objects from different schemes?](#Can-a-tablespace-hold-objects-from-different-schemes)
+ [Can objects of the same schema reside in different tablespaces?](#Can-objects-of-the-same-schema-reside-in-different-tablespaces)
+ [What is the use of control file?](#What-is-the-use-of-control-file)
+ [Do view contain data?](#Do-view-contain-data)
+ [What are the referential actions supported by foreign key integrity constraint?](#What-are-the-referential-actions-supported-by-foreign-key-integrity-constraint)
+ [What are the type of synonyms?](#What-are-the-type-of-synonyms)
+ [What is an index segment?](#What-is-an-index-segment)
+ [What are the different type of segments?](#What-are-the-different-type-of-segments)
+ [What are clusters?](#What-are-clusters)
+ [What is an integrity constrains?](#What-is-an-integrity-constrains)
+ [What is an index?](#What-is-an-index)
+ [What is an extent?](#What-is-an-extent)
+ [What is a view?](#What-is-a-view)
+ [What is table?](#What-is-table)
+ [Can a view based on another view?](#Can-a-view-based-on-another-view)
+ [What are the advantages of views?](#What-are-the-advantages-of-views)
+ [What is an oracle sequence?](#What-is-an-oracle-sequence)
+ [What is a synonym?](#What-is-a-synonym)
+ [What are the types of synonyms?](#What-are-the-types-of-synonyms)
+ [What is a private synonym?](#What-is-a-private-synonym)
+ [What is a public synonym?](#What-is-a-public-synonym)
+ [What are synonyms used for?](#What-are-synonyms-used-for)
+ [What is an oracle index?](#What-is-an-oracle-index)
+ [How are the index updates?](#How-are-the-index-updates)
+ [What is rollback segment?](#What-is-rollback-segment)
+ [What are the characteristics of data files?](#What-are-the-characteristics-of-data-files)
+ [How to define data block size?](#How-to-define-data-block-size)
+ [What does a control file contain?](#What-does-a-control-file-contain)
+ [What is difference between unique constraint and primary key constraint?](#What-is-difference-between-unique-constraint-and-primary-key-constraint)
+ [What is index cluster?](#What-is-index-cluster)
+ [When does a transaction end?](#When-does-a-transaction-end)
+ [How does one create a new database?](#How-does-one-create-a-new-database)
+ [What database block size should I use?](#What-database-block-size-should-I-use)
+ [What are the different approaches used by optimizer in choosing an execution plan?](#What-are-the-different-approaches-used-by-optimizer-in-choosing-an-execution-plan)
+ [What does rollback do?](#What-does-rollback-do)
+ [What is cost based approach to optimization?](#What-is-cost-based-approach-to-optimization)
+ [What does commit do?](#What-does-commit-do)
+ [Define transaction?](#Define-transaction)
+ [What is read only transaction?](#What-is-read-only-transaction)
+ [What is a deadlock?](#What-is-a-deadlock)
+ [What is a schema?](#What-is-a-schema)
+ [What is a cluster key?](#What-is-a-cluster-key)
+ [What is parallel server?](#What-is-parallel-server)
+ [What is cluster?](#What-is-cluster)
+ [What is an index and how it is implemented in oracle database?](#What-is-an-index-and-how-it-is-implemented-in-oracle-database)
+ [What is a database instance?](#What-is-a-database-instance)
+ [What is the use of analyze command?](#What-is-the-use-of-analyze-command)
+ [What is default tablespace?](#What-is-default-tablespace)
+ [What are the system resources that can be controlled through profile?](#What-are-the-system-resources-that-can-be-controlled-through-profile)
+ [What is tablespace quota?](#What-is-tablespace-quota)
+ [What are the different levels of auditing?](#What-are-the-different-levels-of-auditing)
+ [What is statement auditing?](#What-is-statement-auditing)
+ [What are the database administrators utilities available?](#What-are-the-database-administrators-utilities-available)
+ [How can you enable automatic archiving?](#How-can-you-enable-automatic-archiving)
+ [What are roles and how can we implement roles?](#What-are-roles-and-how-can-we-implement-roles)
+ [What are roles?](#What-are-roles)
+ [What are the uses of roles?](#What-are-the-uses-of-roles)
+ [What is privilege auditing?](#What-is-privilege-auditing)
+ [What is object auditing?](#What-is-object-auditing)
+ [What is auditing?](#What-is-auditing)
+ [Where are my tempfiles?](#Where-are-my-tempfiles)
+ [How do I find used or free space in a temporary tablespace?](#How-do-I-find-used-or-free-space-in-a-temporary-tablespace)
+ [What is a profile?](#What-is-a-profile)
+ [How will you enforce security using stored procedures?](#How-will-you-enforce-security-using-stored-procedures)
+ [How does one get the view definition of fixed views or tables?](#How-does-one-get-the-view-definition-of-fixed-views-or-tables)
+ [What are the dictionary tables used to monitor a database spaces?](#What-are-the-dictionary-tables-used-to-monitor-a-database-spaces)
+ [What is user account in oracle database?](#What-is-user-account-in-oracle-database)
+ [What is dynamic data replication?](#What-is-dynamic-data-replication)
+ [What is two phase commit?](#What-is-two-phase-commit)
+ [How can you enforce referential integrity in snapshots?](#How-can-you-enforce-referential-integrity-in-snapshots)
+ [What is a snapshot?](#What-is-a-snapshot)
+ [What is the mechanism provided by oracle for table replication?](#What-is-the-mechanism-provided-by-oracle-for-table-replication)
+ [What are the various type of snapshots?](#What-are-the-various-type-of-snapshots)
+ [Describe two phases of two phase commit?](#Describe-two-phases-of-two-phase-commit)
+ [What is snapshot log?](#What-is-snapshot-log)
+ [What are the benefits of distributed options in databases?](#What-are-the-benefits-of-distributed-options-in-databases)
+ [What are the options available to refresh snapshots?](#What-are-the-options-available-to-refresh-snapshots)
+ [What is a snapshot log?](#What-is-a-snapshot-log)
+ [What is distributed database?](#What-is-distributed-database)
+ [How can we reduce the network traffic?](#How-can-we-reduce-the-network-traffic)
+ [Differentiate simple and complex and snapshots?](#Differentiate-simple-and-complex-and-snapshots)
+ [What are the built-ins used for sending parameters to forms?](#What-are-the-built-ins-used-for-sending-parameters-to-forms)
+ [Can You Have More Than One Content Canvas View Attached With A Window?](#Can-You-Have-More-Than-One-Content-Canvas-View-Attached-With-A-Window)
+ [Is the after report trigger fired if the report execution fails?](#Is-the-after-report-trigger-fired-if-the-report-execution-fails)
+ [Does a before form trigger fire when the parameter form is suppressed?](#Does-a-before-form-trigger-fire-when-the-parameter-form-is-suppressed)
+ [What is sga?](#What-is-sga)
+ [What is a shared pool?](#What-is-a-shared-pool)
+ [What is mean by program global area?](#What-is-mean-by-program-global-area)
+ [What is a data segment?](#What-is-a-data-segment)
+ [What are the factors causing the reparsing of sql statements in sga?](#What-are-the-factors-causing-the-reparsing-of-sql-statements-in-sga)
+ [Does a view contain data?](#Does-a-view-contain-data)
+ [What is trigger associated with the timer?](#What-is-trigger-associated-with-the-timer)
+ [What are the triggers associated with image items?](#What-are-the-triggers-associated-with-image-items)
+ [What are the different windows events activated at runtimes?](#What-are-the-different-windows-events-activated-at-runtimes)
+ [When do you use data parameter type?](#When-do-you-use-data-parameter-type)
+ [What is difference between open_form and call_form?](#What-is-difference-between-open_form-and-call_form)
+ [What is new_form built in?](#What-is-new_form-built-in)
+ [What is the difference when flex mode is mode on and when it is off?](#What-is-the-difference-when-flex-mode-is-mode-on-and-when-it-is-off)
+ [What is the difference when confine mode is on and when it is off?](#What-is-the-difference-when-confine-mode-is-on-and-when-it-is-off)
+ [What are visual attributes?](#What-are-visual-attributes)
+ [What are the vbx controls?](#What-are-the-vbx-controls)
+ [What is the use of transactional triggers?](#What-is-the-use-of-transactional-triggers)
+ [How do you create a new session while open a new form?](#How-do-you-create-a-new-session-while-open-a-new-form)
+ [What are the ways to monitor the performance of the report?](#What-are-the-ways-to-monitor-the-performance-of-the-report)
+ [Explain about horizontal and vertical tool bar canvas views?](#Explain-about-horizontal-and-vertical-tool-bar-canvas-views)
+ [What is the purpose of the product order option in the column property sheet?](#What-is-the-purpose-of-the-product-order-option-in-the-column-property-sheet)
+ [What is the use of image_zoom built-in?](#What-is-the-use-of-image_zoom-built-in)
+ [What is a timer?](#What-is-a-timer)
+ [What are the two phases of block coordination?](#What-are-the-two-phases-of-block-coordination)
+ [What are most common types of complex master-detail relationships?](#What-are-most-common-types-of-complex-master-detail-relationships)
+ [What is a text list?](#What-is-a-text-list)
+ [What is term?](#What-is-term)
+ [What is use of term?](#What-is-use-of-term)
+ [What is pop list?](#What-is-pop-list)
+ [What is the maximum no. of chars the parameter can store?](#What-is-the-maximum-no-of-chars-the-parameter-can-store)
+ [What are the default extensions of the files created by library module?](#What-are-the-default-extensions-of-the-files-created-by-library-module)
+ [How do you display console on a window?](#How-do-you-display-console-on-a-window)
+ [What are the coordination properties in a master-detail relationship?](#What-are-the-coordination-properties-in-a-master-detail-relationship)
+ [What are the different parameter types?](#What-are-the-different-parameter-types)
+ [What are the types of calculated columns available?](#What-are-the-types-of-calculated-columns-available)
+ [Explain about stacked canvas views?](#Explain-about-stacked-canvas-views)
+ [What is the difference between show_editor and edit_textitem?](#What-is-the-difference-between-show_editor-and-edit_textitem)
+ [What are the different file extensions that are created by oracle reports?](#What-are-the-different-file-extensions-that-are-created-by-oracle-reports)
+ [What is the basic data structure that is required for creating an lov?](#What-is-the-basic-data-structure-that-is-required-for-creating-an-lov)
+ [What is the maximum allowed length of record group column?](#What-is-the-maximum-allowed-length-of-record-group-column)
+ [Which parameter can be used to set read level consistency across multiple queries?](#Which-parameter-can-be-used-to-set-read-level-consistency-across-multiple-queries)
+ [What are the different types of record groups?](#What-are-the-different-types-of-record-groups)
+ [From which designation is it preferred to send the output to the printed?](#From-which-designation-is-it-preferred-to-send-the-output-to-the-printed)
+ [What is difference between post database commit and post-form commit?](#What-is-difference-between-post-database-commit-and-post-form-commit)
+ [With which function of summary item is the compute at options required?](#With-which-function-of-summary-item-is-the-compute-at-options-required)
+ [What are parameters?](#What-are-parameters)
+ [What are the three types of user exits available?](#What-are-the-three-types-of-user-exits-available)
+ [How many windows in a form can have console?](#How-many-windows-in-a-form-can-have-console)
+ [Is it possible to modify an external query in a report which contains it?](#Is-it-possible-to-modify-an-external-query-in-a-report-which-contains-it)
+ [Does a grouping done for objects in the layout editor affect the grouping done in the data model editor?](#Does-a-grouping-done-for-objects-in-the-layout-editor-affect-the-grouping-done-in-the-data-model-editor)
+ [If a break order is set on a column would it affect columns which are under the column?](#If-a-break-order-is-set-on-a-column-would-it-affect-columns-which-are-under-the-column)
+ [Can you pass data parameters to forms?](#Can-you-pass-data-parameters-to-forms)
+ [Is it possible to link two groups inside a cross products after the cross products group has been created?](#Is-it-possible-to-link-two-groups-inside-a-cross-products-after-the-cross-products-group-has-been-created)
+ [What are the different modals of windows?](#What-are-the-different-modals-of-windows)
+ [What are modal windows?](#What-are-modal-windows)
+ [What is the advantage of the library?](#What-is-the-advantage-of-the-library)
+ [What is lexical reference? how can it be created?](#What-is-lexical-reference-how-can-it-be-created)
+ [What is system.coordination_operation?](#What-is-systemcoordination_operation)
+ [What is synchronize?](#What-is-synchronize)
+ [What use of command line parameter cmd file?](#What-use-of-command-line-parameter-cmd-file)
+ [What is a text_io package?](#What-is-a-text_io-package)
+ [What is forms_ddl?](#What-is-forms_ddl)
+ [What are the built-ins used for processing rows?](#What-are-the-built-ins-used-for-processing-rows)
+ [What are the built-ins used for getting cell values?](#What-are-the-built-ins-used-for-getting-cell-values)
+ [At least how many set of data must a data model have before a data model can be based on it?](#At-least-how-many-set-of-data-must-a-data-model-have-before-a-data-model-can-be-based-on-it)
+ [To execute row from being displayed that still use column in the row which property can be used?](#To-execute-row-from-being-displayed-that-still-use-column-in-the-row-which-property-can-be-used)
+ [What is the remove on exit property?](#What-is-the-remove-on-exit-property)
+ [What is a difference between pre-select and pre-query?](#What-is-a-difference-between-pre-select-and-pre-query)
+ [What are the built-ins used for finding object id function?](#What-are-the-built-ins-used-for-finding-object-id-function)
+ [Any attempt to navigate programmatically to disabled form in a call_form stack is allowed?](#Any-attempt-to-navigate-programmatically-to-disabled-form-in-a-call_form-stack-is-allowed)
+ [How can a break order be created on a column in an existing group? what are the various sub events a mouse double click event involves?](#How-can-a-break-order-be-created-on-a-column-in-an-existing-group-what-are-the-various-sub-events-a-mouse-double-click-event-involves)
+ [What is the use of placeholder column? what are the various sub events a mouse double click event involves?](#What-is-the-use-of-placeholder-column-what-are-the-various-sub-events-a-mouse-double-click-event-involves)
+ [What are the built-ins used for creating and deleting groups?](#What-are-the-built-ins-used-for-creating-and-deleting-groups)
+ [What are the different types of delete details we can establish in master-details?](#What-are-the-different-types-of-delete-details-we-can-establish-in-master-details)
+ [Where is the external query executed at the client or the server?](#Where-is-the-external-query-executed-at-the-client-or-the-server)
+ [Where is a procedure return in an external pl/sql library executed at the client or at the server?](#Where-is-a-procedure-return-in-an-external-plsql-library-executed-at-the-client-or-at-the-server)
+ [What is coordination event?](#What-is-coordination-event)
+ [What is the difference between ole server & ole container?](#What-is-the-difference-between-ole-server-ole-container)
+ [What is an object group?](#What-is-an-object-group)
+ [What is the difference between the conventional and direct path loader?](#What-is-the-difference-between-the-conventional-and-direct-path-loader)
+ [How does one load multi-line records?](#How-does-one-load-multi-line-records)
+ [Why is where clause faster than group filter or format trigger?](#Why-is-where-clause-faster-than-group-filter-or-format-trigger)
+ [Difference between substr and instr?](#Difference-between-substr-and-instr)
+ [What is rman?](#What-is-rman)
+ [What are two parts of procedure?](#What-are-two-parts-of-procedure)
+ [What are the datatypes available in plsql?](#What-are-the-datatypes-available-in-plsql)
+ [What is overloading of procedures?](#What-is-overloading-of-procedures)
+ [What is master detail relationship?](#What-is-master-detail-relationship)
+ [How many number of columns a record group can have?](#How-many-number-of-columns-a-record-group-can-have)
+ [How do window functions help in data engineering SQL?](#How-do-window-functions-help-in-data-engineering-SQL)
+ [How do you deduplicate data with SQL?](#How-do-you-deduplicate-data-with-SQL)
+ [How do you write incremental SQL models?](#How-do-you-write-incremental-SQL-models)
+ [How do you optimize analytical SQL queries?](#How-do-you-optimize-analytical-SQL-queries)
+ [Real world use cases for SQL](#Real-world-use-cases-for-SQL)

## Write sql query to get the second highest salary among all employees?
Given Employee Table with two columns
ID, Salary 10, 2000
11, 5000
12, 3000

The modern answer uses a window function, which also handles ties and works when salaries repeat.

```sql
select distinct salary
from (
  select salary,
         dense_rank() over (order by salary desc) as rnk
  from employee
) ranked
where rnk = 2;
```

Trade-off: `dense_rank` returns the second distinct salary value, so equal salaries do not consume a rank. `row_number` would return the second row even when it ties the first, and `rank` would skip ranks after a tie. State which definition of "second highest" you are using before writing the query.

[Table of Contents](#SQL)

## There are multiple ways to get the second highest salary among all employees.
Option 1: Use Subquery
SELECT MAX(Salary) FROM Employee WHERE Salary NOT IN (SELECT MAX(Salary) FROM Employee );
In this approach, we are getting the maximum salary in a subquery and then excluding this from the rest of the resultset.
Option 2: Use Not equals
select MAX(Salary) from Employee WHERE Salary <> (select MAX(Salary) from Employee )
This is same as option 1 but we are using <> instead of NOT IN.

[Table of Contents](#SQL)

## How can we retrieve alternate records from a table in oracle?
We can use rownum and MOD function to retrieve the alternate records from a table.
To get Even number records:
SELECT * FROM (SELECT rownum, ID, Name FROM Employee) WHERE MOD(rownum,2)=0
To get Odd number records: SELECT * FROM (SELECT rownum, ID, Name FROM Employee)
WHERE MOD(rownum,2)=1

[Table of Contents](#SQL)

## Write sql query to find max salary and department name from each department.
Given Employee table with three columns
ID, Salary, DeptID
10, 1000, 2
20, 5000, 3
30, 3000, 2

Department table with two columns: ID, DeptName
1, Marketing
2, IT
3, Finance

This is a trick question. There can be some department without any employee. So we have to ask interviewer if they expect the name of such Department also in result.
If yes then we have to join Department table with Employee table by using foreign key DeptID. We have to use LEFT OUTER JOIN to print all the departments.
Query would be like as follows:
SELECT d.DeptName, MAX(e.Salary) FROM Department d LEFT OUTER JOIN Employee e ON e.DeptId = d.ID GROUP BY DeptName

[Table of Contents](#SQL)

## Write sql query to find records in table a that are not in table b without using not in operator.
Consider two tables
Table_A

10
20
30

Table_B
15
30
45
We can use MINUS operator in this case for Oracle and EXCEPT for SQL Server.
Query will be as follows:
SELECT * FROM Table_A MINUS SELECT * FROM Table_B

The same "rows in A with no match in B" result is called an anti-join.

```sql
-- null-safe and usually the fastest
select a.*
from table_a a
where not exists (select 1 from table_b b where b.id = a.id);

-- left anti-join
select a.*
from table_a a
left join table_b b on b.id = a.id
where b.id is null;

-- set operators (deduplicate as a side effect)
select id from table_a
except
select id from table_b;          -- Oracle spells this minus
```

Trade-off: `not exists` and the left anti-join compile to the same plan on most engines, while `except`/`minus` also removes duplicate rows. Avoid `not in` whenever the subquery column can be null, because a single null makes the predicate unknown and the query returns no rows.

[Table of Contents](#SQL)

## What is the result of following query?
SELECT CASE WHEN null = null THEN "True" ELSE "False" END AS Result;
Answer: In SQL null can not be compared with itself. There fore null = null is not true. We can compare null with a non-null value to check whether a value is not null.
Therefore the result of above query is False.
The correct way to check for null is to use IS NULL clause.
Following query will give result True. SELECT CASE WHEN null IS NULL THEN "True" ELSE "False" END AS Result;

```sql
select case when null = null then 'True' else 'False' end as result;  -- False
select case when null is null then 'True' else 'False' end as result; -- True
select case when null <> null then 'True' else 'False' end as result; -- False
```

`null` is the absence of a value, so every comparison with it evaluates to `unknown`, and `where`/`case` treat `unknown` as not true. Use `is null`, `is not null`, `coalesce`, or `nullif` for null-safe logic, and remember that `not (null = null)` is also `unknown`.

[Table of Contents](#SQL)

## Write sql query to find employees that have same name and email.
Employee table:
ID NAME EMAIL
10 John jbaldwin
20 George gadams
30 John jsmith

This is a simple question with one trick. The trick here is to use Group by on two columns Name and Email.
Query would be as follows: SELECT name, email, COUNT(*) FROM Employee GROUP BY name, email HAVING COUNT(*) > 1

[Table of Contents](#SQL)

## Write sql query to find max salary from each department.
Given Employee table with three columns
ID, Salary, DeptID 10, 1000, 2
20, 5000, 3
30, 3000, 2

We can first use group by DeptID on Employee table and then get the Max salary from each Dept group.
SELECT DeptID, MAX(salary) FROM Employee GROUP BY DeptID

```sql
select dept_id, max(salary) as max_salary
from employee
group by dept_id;
```

To return the whole row of the top earner per department, rank instead of aggregating:

```sql
select dept_id, id, name, salary
from (
  select e.*,
         row_number() over (partition by dept_id order by salary desc) as rn
  from employee e
) t
where rn = 1;
```

Trade-off: `max()` gives one number per group and cannot return the employee name without a second join; the window version returns the full row and controls tie-breaking with `row_number` versus `rank`.

[Table of Contents](#SQL)

## Write sql query to get the nth highest salary among all employees.
Given Employee Table with two columns
ID, Salary 10, 2000
11, 5000
12, 3000

Option 1: Use Subquery We can use following sub query approach for this:
SELECT * FROM Employee emp1 WHERE (N-1) = ( SELECT COUNT(DISTINCT(emp2.salary)) FROM Employee emp2 WHERE emp2.salary > emp1.salary)
Option 2: Using Rownum in Oracle
SELECT * FROM (SELECT emp.*,row_number() OVER (ORDER BY salary DESC) rnum FROM Employee emp) WHERE rnum = n;

Ranking functions are the cleanest answer. `row_number` skips ties, `rank` leaves gaps, and `dense_rank` does not, which changes what the "nth highest" means when salaries tie.

```sql
-- nth distinct salary
select distinct salary
from (
  select salary, dense_rank() over (order by salary desc) as rnk
  from employee
) ranked
where rnk = :n;

-- nth row by salary
select salary
from (
  select salary, row_number() over (order by salary desc) as rn
  from employee
) ranked
where rn = :n;
```

Trade-off: `dense_rank` is the usual interview answer because duplicate salaries should not consume a rank. The correlated-subquery form `(select count(distinct salary) ...)` still works but rescans the table per row.

[Table of Contents](#SQL)

## How can you find 10 employees with odd number as employee id?
In Oracle we can use Top to limit the number of records. We can also use Rownum < 11 to get the only 10 or less number of records.To find the Odd number Employee ID, we can use % function.
Sample Query with TOP:
SELECT TOP 10 ID FROM Employee WHERE ID % 2 = 1;
Sample Query with ROWNUM:
SELECT ID FROM Employee WHERE ID % 2 = 1 AND ROWNUM < 11;

[Table of Contents](#SQL)

## Write sql query to get the names of employees whose date of birth is between 01/01/1990 to 31/12/2000.
This SQL query appears a bit tricky. We can use BETWEEN clause to get all the employees whose date of birth lies between two given dates.
Query will be as follows:
SELECT EmpName FROM Employees WHERE birth_date BETWEEN "01/01/1990" AND "31/12/2000"
Remember BETWEEN is always inclusive of both the dates.

[Table of Contents](#SQL)

## Write sql query to get the quarter from date.
Answer: We can use to_char function with "Q" option for quarter to get quarter from a date.
Use TO_CHAR with option "Q" for Quarter
SELECT TO_CHAR(TO_DATE("3/31/2016", "MM/DD/YYYY"), "Q") AS quarter FROM DUAL

```sql
-- Oracle
select to_char(date '2026-03-31', 'Q') as quarter from dual;

-- portable
select extract(quarter from date '2026-03-31') as quarter;        -- Postgres, Snowflake, BigQuery
select date_trunc('quarter', date '2026-03-31') as quarter_start; -- first day of the quarter
select quarter('2026-03-31') as quarter;                          -- MySQL
```

Trade-off: `extract` returns a number, which is easy to compare but awkward to label; `date_trunc('quarter', ...)` returns a date and is usually what a date-dimension join wants. Use single quotes for string and date literals — double quotes are identifiers in ANSI SQL and Oracle.

[Table of Contents](#SQL)

## Write query to find employees with duplicate email.
Employee table:
ID NAME EMAIL
10 John jsmith
20 George gadams
30 Jane jsmith
We can use Group by clause on the column in which we want to find duplicate values.
Query would be as follows:
SELECT name, COUNT(email) FROM Employee GROUP BY email HAVING ( COUNT(email) > 1 )

```sql
select email, count(*) as occurrences
from employees
group by email
having count(*) > 1
order by occurrences desc;
```

To keep the newest row and delete the rest:

```sql
delete from employees
where id in (
  select id from (
    select id,
           row_number() over (partition by email order by updated_at desc) as rn
    from employees
  ) ranked
  where rn > 1
);
```

Trade-off: the window-function delete is portable; MySQL refuses to delete from a table that a subquery also selects from unless you wrap it in a derived table (as above) or stage the ids in a temporary table.

[Table of Contents](#SQL)

## Write a query to find all employee whose name contains the word "rich", regardless of case.
E.g. Rich, RICH, rich.
We can use UPPER function for comparing the both sides with uppercase.
SELECT * FROM Employees WHERE UPPER(emp_name) like "%RICH%"

[Table of Contents](#SQL)

## Is it safe to use rowid to locate a record in oracle sql queries?
ROWID is the physical location of a row. We can do very fast lookup based on ROWID. In a transaction where we first search a few rows and then update them one by one, we can use ROWID. But ROWID of a record can change over time. If we rebuild a table a record can get a new ROWID. If a record is deleted, its ROWID can be given to another record. So it is not recommended to store and use ROWID in long term. It should be used in same transactions.

[Table of Contents](#SQL)

## What is a pseudo-column?
A Pseudocolumn is like a table column, but it is not stored in the same table. We can select from a Pseudocolumn, but we can not insert, update or delete on a Pseudocolumn. A Pseudocolumn is like a function with no arguments. Two most popular Pseudocolumns in Oracle are ROWID and ROWNUM. NEXTVAL and CURRVAL are also pseudo columns.

[Table of Contents](#SQL)

## What are the reasons for denormalizing the data?
We de-normalize data when we need better performance. Sometimes there are many joins in a query due to highly normalized data. In that case, for faster data retrieval it becomes essential to de-normalize data.

[Table of Contents](#SQL)

## What is the feature in sql for writing if and else statements?
In SQL, we can use CASE statements to write If/Else statements. We can also use DECODE function in Oracle SQL for writing simple If/Else logic.

```sql
select
  order_id,
  case
    when amount >= 1000 then 'high'
    when amount >= 100  then 'medium'
    else 'low'
  end as amount_band,
  case status when 'C' then 'completed'
              when 'X' then 'cancelled'
              else 'other' end as status_label
from orders;
```

Trade-off: searched `case` (with conditions) is portable and readable; Oracle's `decode` is shorter for equality-only logic but Oracle-specific. `case` works in `select`, `where`, `order by`, and inside aggregates, which is how you build pivot-style columns such as `sum(case when status = 'paid' then amount else 0 end)`.

[Table of Contents](#SQL)

## What is the difference between delete and truncate in sql?
Main differences between DELETE and TRUNCATE commands are:
DML vs. DDL: DELETE is a Data Manipulation Language (DML) command. TRUNCATE is a Data Definition Language (DDL) command.

Number of Rows: We can use DELETE command to remove one or more rows from a table. TRUNCATE command will remove all the rows from a table.
WHERE clause: DELETE command provides support for WHERE clause that can be used to filter the data that we want to delete. TRUNCATE command can only delete all the rows. There is no WHERE clause in TRUNCATE command.
Commit: After DELETE command we have to issue COMMIT or ROLLBACK command to confirm our changes. After TRUNCATE command there is no need to run COMMIT. Changes done by TRUNCATE command can not be rolled back.

```sql
delete from orders where order_date < date '2020-01-01';  -- row by row, logged, filterable
truncate table orders;                                    -- all rows, minimal logging
```

Trade-off: `delete` fires triggers, honors `where`, and can be rolled back; `truncate` is far faster on large tables but deletes everything, resets identity values in MySQL, and in SQL Server fails when a foreign key references the table.

[Table of Contents](#SQL)

## What is the difference between ddl and dml commands in sql?
Main differences between Data Definition Language (DDL) and Data Manipulation Language (DML) commands are:
+ DDL vs. DML: DDL statements are used for creating and defining the Database structure. DML statements are used for managing data within Database. Sample Statements: DDL statements are CREATE, ALTER, DROP, TRUNCATE, RENAME etc. DML statements are SELECT, INSERT, DELETE, UPDATE, MERGE, CALL etc.
+ Number of Rows: DDL statements work on whole table. CREATE will a create a new table. DROP will remove the whole table. TRUNCATE will delete all records in a table. DML statements can work on one or more rows. INSERT can insert one or more rows. DELETE can remove one or more rows.
+ WHERE clause: DDL statements do not have a WHERE clause to filter the data. Most of DML statements support filtering the data by WHERE clause.
+ Commit: Changes done by a DDL statement can not be rolled back. So there is no need to issue a COMMIT or ROLLBACK command after DDL statement. We need to run COMMIT or ROLLBACK to confirm our changed after running a DML statement.
+ Transaction: Since each DDL statement is permanent, we can not run multiple DDL statements in a group like Transaction. DML statements can be run in a Transaction. Then we can COMMIT or ROLLBACK this group as a transaction. E.g. We can insert data in two tables and commit it together in a transaction.
+ Triggers: After DDL statements no triggers are fired. But after DML statements relevant triggers can be fired.

[Table of Contents](#SQL)

## Why do we use escape characters in sql queries?
In SQL, there are certain special characters and words that are reserved for special purpose. E.g. & is a reserved character. When we want to use these special characters in the context of our data, we have to use Escape characters to pass the message to database to interpret these as non Special / non Reserved characters.

[Table of Contents](#SQL)

## What is the difference between primary key and unique key in sql?
Main differences between Primary key and Unique key in SQL are:
+ Number: There can be only one Primary key in a table. There can be more than one Unique key in a table.
+ Null value: In some DBMS Primary key cannot be NULL. E.g. MySQL adds NOT NULL to Primary key. A Unique key can have null values.
+ Unique Identifier: Primary Key is a unique identifier of a record in database table. Unique key can be null and we may not be able to identify a record in a unique way by a unique key
+ Changes: It is not recommended to change a Primary key. A Unique key can be changed much easily.
+ Usage: Primary Key is used to identify a row in a table. A Unique key is used to prevent duplicate non-null values in a column.

[Table of Contents](#SQL)

## What is the difference between inner join and outer join in sql?
Let say we have two tables X and Y.
The result of an INNER JOIN of X and Y is X intersect. It is the INNER overlapping intersection part of a Venn diagram. The result of an OUTER JOIN of X and Y is X union Y. It is the OUTER parts of a Venn diagram. E.g. Consider following two tables, with just one column x and y:

x | y
- -|- -
  10 | 30
  20 | 40
  30 | 50
  40 | 60
  In above tables (10,20) are unique to table X, (30,40) are common, and (50,60) are unique to table Y.
  INNER JOIN An INNER JOIN by using following query will give the intersection of the two tables X and Y. The intersection is the common data between these tables.
  select * from X INNER JOIN Y on X.x =Y.y;
  x | y
  --+--
  30 | 30
  40 | 40

OUTER JOIN
A full OUTER JOIN by using following query will us the union of X and Y. It will have all the rows in X and all the rows in Y. If some row in X has not corresponding value in Y, then Y side will be null, and vice versa.
select * from X FULL OUTER JOIN Y on X.x = Y.y;

x| y
----- + -----
10 | null
20 | null

30 | 30
40 | 40
null | 60
null | 50

```sql
-- sample tables: customers(id, name), orders(id, customer_id, amount)
select c.name, o.amount
from customers c
inner join orders o on o.customer_id = c.id;      -- only matching pairs

select c.name, o.amount
from customers c
left join orders o on o.customer_id = c.id;       -- every customer, nulls when no order

select c.name, o.amount
from customers c
full outer join orders o on o.customer_id = c.id; -- every customer and every order
```

Trade-off: `inner join` lets the optimizer discard non-matching rows early and is the cheapest. A `full outer join` usually forces a sort or hash of both inputs. MySQL has no `full outer join`, so it is emulated with `left join union all right join ... where not exists`; Postgres, Snowflake, and BigQuery support it directly. State whether unmatched rows must be preserved before choosing the join.

[Table of Contents](#SQL)

## What is the difference between left outer join and right outer join?
Let say we have two tables X and Y.
The result of an LEFT OUTER JOIN of X and Y is all rows of X and common rows between X and Y.
The result of an RIGHT OUTER JOIN of X and Y is all rows of Y and common rows between X and Y.
E.g.
Consider following two tables, with just one column x and y:

x| y
- - -|- - 10 | 30
    20 | 40
    30 | 50
    40 | 60

In above tables (10,20) are unique to table X, (30,40) are common, and (50,60) are unique to table Y.
LEFT OUTER JOIN
A left OUTER JOIN by using following query will give us all rows in X and common rows in X and Y.
select * from X LEFT OUTER JOIN Y on X.x = Y.y;
x| y
-- -+-----
10 | null
20 | null
30 |30
40 |40
RIGHT OUTER JOIN
A right OUTER JOIN by using following query will give all rows in Y and common rows in X and Y.
select * from X RIGHT OUTER JOIN Y on X.x = Y.y;
x| y
----- +----
30 | 30
40 | 40
null | 50
null | 60

```sql
-- left join: the left table is preserved
select c.name, count(o.id) as orders
from customers c
left join orders o on o.customer_id = c.id
group by c.name;

-- right join: the right table is preserved (same as swapping and using left join)
select c.name, o.id
from orders o
right join customers c on o.customer_id = c.id;
```

Trade-off: a `right join` is a `left join` with the tables swapped. Most teams standardize on `left join` because the preserved table comes first, which makes "did this filter drop rows?" easier to answer in review. `count(o.id)` counts only real matches, while `count(*)` would count the null-padded rows as one.

[Table of Contents](#SQL)

## What is the datatype of rowid?
ROWID Pseudocolumn in Oracle is of ROWID datatype. It is a string that represents the address of a row in the database.

[Table of Contents](#SQL)

## What is the difference between where clause and having clause?
We use where clause to filter elements based on some criteria on individual records of a table.
E.g. We can select only employees with first name as John.
SELECT ID, Name FROM Employee WHERE name = "John"
We use having clause to filter the groups based on the values of aggregate functions.
E.g. We can group by department and only select departments that have more than 10 employees.
SELECT deptId, count(1) FROM Employee GROUP BY deptId HAVING count(*) > 10.

```sql
select dept_id, count(*) as employees, avg(salary) as avg_salary
from employees
where hire_date >= date '2020-01-01'   -- filters rows before grouping
group by dept_id
having count(*) > 10                   -- filters groups after aggregation
order by avg_salary desc;
```

Trade-off: `where` runs before `group by` and can use indexes; `having` runs after aggregation and works on aggregate results or group keys. Pushing every non-aggregate predicate into `where` lets the engine aggregate fewer rows, which is the most common single-query optimization.

[Table of Contents](#SQL)

## How will you calculate the number of days between two dates in mysql?
We can use DATEDIFF function for this purpose. The query to get the number of days between two dates in MySQL is as follows:
SELECT DATEDIFF("2016-12- 31", "2015-01-01");

```sql
select datediff('2016-12-31', '2015-01-01') as days;               -- MySQL
select date '2016-12-31' - date '2015-01-01' as days;              -- Postgres
select datediff(day, '2015-01-01', '2016-12-31') as days;          -- SQL Server
select date_diff(date '2016-12-31', date '2015-01-01', day) as days;  -- BigQuery
```

Trade-off: argument order and semantics differ by engine. BigQuery's `date_diff(end, start)` counts whole units (it truncates), MySQL's `datediff` ignores the time component, and Postgres returns an interval for timestamp subtraction but an integer for dates.

[Table of Contents](#SQL)

## What are the different types of triggers in mysql?
MySQL supports six types of triggers. These are as follows:
+ Before Insert: This trigger runs before inserting a new row in a table.
+ After Insert: This triggerruns after inserting a new row in a table.
+ Before Update: This trigger runs before updating an existing row in a table.
+ After Update: This trigger runs after updating an existing row in a table.
+ Before Delete: This trigger runs before deleting an existing row in a table.
+ After Delete: This trigger runs after deleting an existing row in a table.

[Table of Contents](#SQL)

## What are the differences between heap table and temporary table in mysql?
+ Duration: Heap tables are stored in memory. Therefore a Heap table remains in existence even if the session is disconnected. When we restart Database, Heap tables get cleaned up.
+ Temporary tables are valid only during a session. Once the session is disconnected, temporary table is cleaned up.
+ Privilege: We need special privilege to create a Temporary table. Heap tables are just another form of storage in MySQL.
+ Sharing: Temporary tables are not shared between clients. Each connection will have a unique temporary table. But Heap tables can be shared between clients.

[Table of Contents](#SQL)

## What is a heap table in mysql?
In MySQL there are tables that are present in memory. These are called Heap tables. During table creation we specify TYPE as HEAP for HEAP tables.
Heap tables provide very fast access to data. We can not store BLOB or TEXT datatype in a HEAP table. These tables also do not support AUTO_INCREMENT. Once we restart the Database, data in HEAP tables is lost.

[Table of Contents](#SQL)

## What is the difference between blob and text data type in mysql?
BLOB is a Binary large Object. We can store a large amount of binary data in a BLOB data type column.
TEXT is non-binary, character based string data type. We can store text data in TEXT column. We have to define a character set with a TEXT column.
TEXT can be easily converted into plain text.
BLOB has four types: TINYBLOB, BLOB, MEDIUMBLOB and LONGBLOB.
Where as, TEXT has its own four types: TINYTEXT,TEXT, MEDIUMTEXT, LONGTEXT.

[Table of Contents](#SQL)

## What will happen when auto increme on an integer column reaches max value in mysql?
Once a column reaches the MAX_VALUE,  the AUTO_INCREMENT stops working. It gives following error in log:
ERROR: 1467 (HY000): Failed to read auto-increment value from storage engine

[Table of Contents](#SQL)

## What are the advantages of mysql as compared with oracle db?
Some of the main advantages of MySQL over Oracle DB are as follows:
+ Cost: MySQL is an Open Source and free RDBMS software. Oracle is usually a paid option for RDBMS.
+ Space: MySQL uses around 1 MB to run whereas Oracle may need as high as 128 MB to run the database server.
+ Flexibility: MySQL can be used to run a small website as well as very large scale systems. Oracle is generally used in medium to large scale systems.
+ Management: In MySQL, database administration is much easier due to self- management features like- automatic space expansion,
+ auto-restart and dynamic configuration changes. In Oracle dedicated DBA has to work on managing the Database.
+ Portable: MySQL is easily portable to different hardware and operating system. Migrating Oracle from one platform to another is a tougher task.

[Table of Contents](#SQL)

## What are the disadvantages of mysql?
Some main disadvantages of MySQL are as follows:
Dependent on Additional S/W: MySQL has less number of features in standard out-of-box version. So we have to add additional software to get more features. It gets difficult to find, decide and use the additional software with MySQL. SQL Compliance: MySQL is not full SQL compliant. Due to this developers find it difficult to cope with the syntax of SQL in MySQL. Transaction handling: Some users complain that DB transactions are not handled properly in MySQL.

[Table of Contents](#SQL)

## What is the difference between char and varchar datatype in mysql?
Some main differences between CHAR and VARCHAR datatypes in MySQL are as follows:
+ Size: In CHAR type column, length is fixed. In a VARCHAR type column length can vary.
+ Storage: There are different mechanisms to store and retrieve CHAR and VARCHAR data types in MySQL.
+ Maximum Size: A CHAR data type can hold maximum 255 characters. A VARCHAR datatype can store up to 4000 characters.
+ Speed: CHAR datatype is 50% faster than VARCHAR datatype in MySQL.
+ Memory Allocation: A CHAR datatype column uses static memory allocation. Since the length of data stored in a VARCHAR can vary, this datatype uses dynamic memory allocation.

[Table of Contents](#SQL)

## What is the use of i am a dummy flag in mysql?
In MySQL, there is falg "ia_am_a_dummy" that can be used to save beginner developers from erroneous query like "DELETE FROM table_name". If we run this query it will delete all the data from table names table_name. With     "i_am_a_dummy      flag", MySQL will not permit running such a query. It will prompt user to create a query with WHERE clause so that only specific data is deleted. We can achieve similar functionality with "safe_updates" option in MySQL. This flag also works on UPDATE statement to restrict updates on a table without WHERE clause.

[Table of Contents](#SQL)

## How can we get current date and time in mysql?
We can use following query in MySQL to get the current date:
SELECT CURRENT_DATE();
We can use following query in MySQL to get the current time as well as date:
SELECT NOW();

```sql
select current_date()   as today,
       current_time()   as now_time,
       now()            as now_datetime,
       utc_timestamp()  as now_utc;

-- ANSI forms
select current_date, current_timestamp;
```

Trade-off: `now()` returns the session time zone, so the same server can produce different "current" times for different clients. Store timestamps in UTC (`utc_timestamp()` or `current_timestamp at time zone 'UTC'`) and convert only when presenting to users.

[Table of Contents](#SQL)

## What is the difference between timestamp in unix and mysql?
In Unix as well as in MySQL, timestamp is stored as a 32-bit integer.
A timestamp is the number of seconds from the Unix Epoch on January 1st, 1970 at UTC.
In MySQL we can represent the timestamp in a readable format.
Timestamp format in MySQL is YYYY-MM-DD HH:MM:SS

[Table of Contents](#SQL)

## How will you limit a mysql query to display only top 10 rows?
We can use LIMIT clause in MySQL to limit a query to a range of rows.
Following query will give top 10 rows from the table with table_name:
SELECT * FROM table_name LIMIT 0,10;
Following query will give 6 rows starting from the 4th row in table with table_name:
SELECT * FROM table_name LIMIT 3,6;

[Table of Contents](#SQL)

## What is automatic initialization and updating for timestamp in a mysql table?
In MySQL, there is a TIMESTAMP datatype that provides features like automatic initialization and updating to current time and date. If a column is auto-initialized, then it will be set to current timestamp on inserting a new row with no value for the column. If a column is auto-updated, then its value will be updated to current timestamp when the value of any other column in the same row is updated. We can mark a column as DEFAULT to prevent this auto- initialize and auto-update behavior.

[Table of Contents](#SQL)

## How can we get the list of all the indexes on a table?
We can use following command to get the list of all the indexes on a table in MySQL:
SHOW INDEX FROM table_name; At maximum we can use 16 columns in a multi-column index of table.

[Table of Contents](#SQL)

## What is savepoint in mysql?
SAVEPOINT is a statement in SQL. We can use SAVEPOINT savepoint_name statement to create a point of time in a Database transaction with a name. Later we can use this savepoint to rollback the transaction upto that point of time.

[Table of Contents](#SQL)

## What is the difference between rollback to savepoint and release savepoint?
We use ROLLBACK TO SAVEPOINT statement to undo the effect of a transaction upto the SAVEPOINT mentioned in ROLLBACK statement.
RELEASE SAVEPOINT is simply used to delete the SAVEPOINT with a name from a transaction. There is commit or rollback for SAVEPOINT in RELEASE statement.In both the cases we should have first created a SAVEPOINT. Else we will get the error while doing ROLLBACK or RELEASE of a SAVEPOINT.

[Table of Contents](#SQL)

## How will you search for a string in mysql column?
We can use REGEXP operator to search for a String in MySQL column. It is regular expression search on columns with text type value. We can define different types of regular expressions and search them in a text with the REGEXP expression that can match our crietria.

```sql
select * from articles where body like '%sql%';           -- contains, scans
select * from articles where body regexp '^sql';          -- regular expression
select * from articles where body like '%100!%%' escape '!';  -- literal wildcard

-- MySQL full-text search, able to use a fulltext index
select * from articles where match(body) against ('sql' in natural language mode);
```

Trade-off: a leading wildcard (`'%term'`) cannot use a normal index and reads every row. For large text corpora use a full-text index or a dedicated search engine. Postgres uses `ilike` for case-insensitive matching and `~` for regular expressions.

[Table of Contents](#SQL)

## How can we find the version of the mysql server and the name of the current database by select query?
We can use built in functions VERSION() and DATABASE() in MySQL to get the version of MySQL server and the name of database in MySQL.
Query is as follows: SELECT VERSION(), DATABASE();

[Table of Contents](#SQL)

## What is the use of ifnull operator in mysql?
We use IFNULL operator in MySQL to get a non-null value for a column with null value.
IFNULL(expr1, expr2)
If expr1 is not null then expr1 is returned. If expr1 is null then expr2 is returned.
Eg. SELECT name, IFNULL(id,"Unknown") AS "id" FROM user;
If id is not null then id is returned. If id is null then Unknown is returned.

```sql
select name, ifnull(id, 'Unknown') as id from user;

-- standard and portable
select name, coalesce(id, 'Unknown') as id from user;

-- nullif is the inverse: null when the two values are equal
select nullif(quantity, 0) as quantity from order_lines;
```

Dialect notes: `ifnull` is MySQL-only; SQL Server uses the two-argument `isnull`; Oracle uses `nvl`. `coalesce` is standard, accepts any number of arguments, and short-circuits, so prefer it in portable code. Make sure the fallback has the same type as the column or cast it explicitly.

[Table of Contents](#SQL)

## How will you check if a table exists in mysql?
We can use CHECK TABLE query to see the existence of a table in MySQL.
Query is as follows: CHECK TABLE table_name;

[Table of Contents](#SQL)

## How will you see the structure of a table in mysql?
We can use DESC query to see the structure of a table in MySQL. It will return the name of columns and their datatype in a table. Query is as follows: DESC table_name;

[Table of Contents](#SQL)

## What are the objects that can be created by create statement in mysql?
We can create following objects by CREATE statement in MySQL:
DATABASE USER TABLE INDEX
VIEW TRIGGER EVENT FUNCTION PROCEDURE

[Table of Contents](#SQL)

## How will you see the current user logged into mysql connection?
We can use USER() command to get the user logged into MySQL connection.
Command is as follows: SELECT USER();
How can you copy the structure of a table into another table without copying the data?
It is a  trick question. But it has practical use in day to day work.
Query for this is as follows: CREATE TABLE table_name AS SELECT * FROM USER WHERE 1 > 2;
In this example condition in WHERE clause will be always false. Due to this no data is retrieved by SELECT query.

[Table of Contents](#SQL)

## What is the difference between batch and interactive modes of mysql?
In Interactive mode, we use command line interface and enter queries one by one. MySQL will execute the query and return the result in command line interface. In Batch mode of MySQL we can write all the queries in a SQL file. Then we can run this SQL file from MySQL command line or from Scheduler Job. MySQL will execute all the queries and return the result.

[Table of Contents](#SQL)

## How can we get a random number between 1 and 100 in mysql?
In MySQL we have a RAND() function that returns a random number between 0 and 1.
SELECT RAND();
If we want to get a random number between 1 and 100, we can use following query:
SELECT RAND() * 100;

[Table of Contents](#SQL)

## What does sql in mysql stand for?
The SQL in MySQL stands for Structured Query Language. This language is also used in other databases such as Oracle and Microsoft SQL Server.  One can use commands such as the following to send requests from a database:
SELECT title FROM publications WHERE author = " J. K. Rowling";
Note that SQL is not case sensitive. However, it is a good practice to write the SQL keywords in CAPS and other names and variables in a small case.

[Table of Contents](#SQL)

## What does a mysql database contain?
A MySQL database contains one or more tables, each of which contains records or rows. Within these rows are various columns or fields that contain the data itself.

[Table of Contents](#SQL)

## How can you interact with mysql?
There are three main ways you can interact with MySQL:
+ using a command line
+ via a web interface
+ through a programming language

[Table of Contents](#SQL)

## What is mysql database queries?
A query is a specific request or a question. One can query a database for specific information and have a record returned.

[Table of Contents](#SQL)

## What are some common mysql commands?
+ ALTER To alter a database or table
+ BACKUP To back-up a table
+ \c To cancel Input
+ CREATE To create a database
+ DELETE To delete a row from a table
+ DESCRIBE To describe a table's columns
+ DROP To delete a database or table
+ EXIT(ctrl+c) To exit
+ GRANT To change user privileges
+ HELP (\h, \?) Display help
+ INSERT Insert data
+ LOCK Lock table(s)
+ QUIT(\q) Same as EXIT
+ RENAME Rename a Table
+ SHOW List details about an object
+ SOURCE Execute a file
+ STATUS (\s) Display the current status
+ TRUNCATE Empty a table
+ UNLOCK Unlock table(s)
+ UPDATE Update an existing record
+ USE Use a database

[Table of Contents](#SQL)

## How do you create a database in mysql?
Use the following command to create a new database called "books":
CREATE DATABASE books;

[Table of Contents](#SQL)

## How do you create a table using mysql?
Use the following to create a table using MySQL:
CREATE TABLE history (
author VARCHAR(128),
title VARCHAR(128),
type VARCHAR(16),
year CHAR(4)) ENGINE InnoDB;

```sql
create table history (
  id      int          not null auto_increment,
  author  varchar(128) not null,
  title   varchar(128) not null,
  type    varchar(16)  not null,
  year    char(4),
  primary key (id),
  key ix_author (author)
) engine = innodb;
```

Trade-off: name the engine explicitly (`engine = innodb`) so the table gets transactions and foreign keys; prefer `utf8mb4` and a `created_at timestamp default current_timestamp` on new tables.

[Table of Contents](#SQL)

## How do you insert data into mysql?
The INSERT INTO statement is used to add new records to a MySQL table:
INSERT INTO table_name (column1, column2, column3,...)
VALUES (value1, value2, value3,...)
If we want to add values for all the columns of the table, we do not need to specify the column names in the SQL query. However, the order of the values should be in the same order as the columns in the table. The INSERT INTO syntax would be as follows:
INSERT INTO table_name
VALUES (value1, value2, value3, ...);

```sql
insert into history (author, title, type, year)
values ('Tolkien', 'The Hobbit', 'novel', '1937');

-- multi-row insert: one round trip, much faster than many single inserts
insert into history (author, title, type, year)
values ('Orwell', '1984', 'novel', '1949'),
       ('Herbert', 'Dune', 'novel', '1965');

-- insert from a query: the standard bulk-move pattern
insert into history_archive (author, title, type, year)
select author, title, type, year from history where year < '1950';
```

Trade-off: `insert ... select` is how data moves and transforms in bulk. Batch rows (for example 1,000-10,000 per statement) to balance round trips against transaction size, and prefer a single multi-row insert over a loop of single inserts.

[Table of Contents](#SQL)

## How do you upsert with MERGE in SQL?

```sql
merge into analytics.customers as t
using staging.customers as s
  on t.customer_id = s.customer_id
when matched then update set
  t.name = s.name,
  t.email = s.email,
  t.updated_at = s.updated_at
when not matched then insert (customer_id, name, email, updated_at)
values (s.customer_id, s.name, s.email, s.updated_at);
```

Dialect notes: Postgres 15+ and SQL Server support `merge`; MySQL uses `insert ... on duplicate key update`; SQLite uses `insert ... on conflict do update`; BigQuery and Snowflake support `merge` but require the source to be unique per key or the statement fails. Always deduplicate `staging` first. Trade-off: `merge` is atomic and self-documenting, but an update-heavy merge rewrites many rows; for append-only facts a plain insert is cheaper.

[Table of Contents](#SQL)

## How do you remove a column from a database?
You can remove a column by using the DROP keyword:
ALTER TABLE classics DROP pages;

[Table of Contents](#SQL)

## How to create an index in mysql?
In MySQL, there are different index types, such as a regular INDEX, a PRIMARY KEY, or a FULLTEXT index. You can achieve fast searches with the help of an index. Indexes speed up performance by either ordering the data on disk so it's quicker to find your result or, telling the SQL engine where to go to find your data.
Example: Adding indexes to the history table:
+ ALTER TABLE history ADD INDEX(author(10));
+ ALTER TABLE history ADD INDEX(title(10));
+ ALTER TABLE history ADD INDEX(category(5));
+ ALTER TABLE history ADD INDEX(year);

```sql
create index ix_history_author on history (author);
create unique index ux_history_title on history (title);
alter table history add index ix_year (year);
```

Trade-off: a unique index both speeds lookups and enforces the rule; a plain index only speeds lookups. A composite index on `(author, year)` also serves queries that filter on `author` alone (leftmost prefix) but not on `year` alone. Every index adds storage and slows inserts.

[Table of Contents](#SQL)

## How to delete data from a mysql table?
In MySQL, the DELETE statement is used to delete records from a table:
DELETE FROM table_name
WHERE column_name = value_name

```sql
delete from history where year = '1937';
delete from history;                    -- all rows, table and indexes stay

-- delete using a join
delete h from history h
join history_archive a on a.title = h.title and a.author = h.author;
```

Trade-off: an unbounded `delete` on a large table holds locks and grows the undo log. Delete in key ranges (a batched retention job), or use `truncate` when every row can go. In production, always run the matching `select count(*)` first.

[Table of Contents](#SQL)

## How do you view a database in mysql?
One can view all the databases on the MySQL server host using the following command:
mysql> SHOW DATABASES;

[Table of Contents](#SQL)

## What are the numeric data types in mysql?
MySQL has numeric data types for integer, fixed-point, floating-point, and bit values, as shown in the table below. Numeric types can be signed or unsigned, except BIT. A special attribute enables the automatic generation of sequential integer or floating-point column values, which is useful for applications that require a series of unique identification numbers.

+ TINYINT Very Small Integer
+ SMALLINT Small Integer
+ MEDIUMINT Medium-sized Integer
+ INT Standard Integer
+ BIGINT Large Integer
+ DECIMAL Fixed-point number
+ FLOAT Single-precision floating-point number
+ DOUBLE Double-precision floating-point number
+ BIT Bit-field

[Table of Contents](#SQL)

## What are the string data types in mysql?
+ CHAR - fixed-length nonbinary(character) string
+ VARCHAR variable-length nonbinary string
+ BINARY fixed-length binary string
+ VARBINARY variable-length binary string
+ TINYBLOB Very small BLOB(binary large object)
+ BLOB Small BLOB
+ MEDIUMBLOB Medium-sized BLOB
+ LONGBLOB Large BLOB
+ TINYTEXT A very small nonbinary string
+ TEXT Small nonbinary string
+ MEDIUMTEXT Medium-sized nonbinary string
+ LONGTEXT Large nonbinary string
+ ENUM An enumeration; each column value is assigned, one enumeration member
+ SET A set; each column value is assigned zero or more set members
+ NULL NULL in SQL is the term used to represent a missing value. A NULL value in a table is a value in a field that appears to be blank. This value is different than a zero value or a field that contains spaces.

[Table of Contents](#SQL)

## What are the temporal data types in mysql?
+ DATE A date value, in " CCYY-MM-DD " Format
+ TIME A Time value, in " hh : mm :ss " format
+ DATETIME Date and time value, in " CCYY-MM-DD hh : mm :ss " format
+ TIMESTAMP A timestamp value, in " CCYY-MM-DD hh : mm :ss " format
+ YEAR A year value, in CCYY or YY format
  Example: To select the records with an Order Date of "2018-11-11" from a table:
  SELECT * FROM Orders WHERE OrderDate="2018-11-11"

[Table of Contents](#SQL)

## What is blob in mysql?
BLOB is an acronym that stands for a binary large object. It is used to hold a variable amount of data.
There are four types of BLOB:
+ TINYBLOB
+ BLOB
+ MEDIUMBLOB
+ LONGBLOB
  A BLOB can hold a very large amount of data. For example - documents, images, and even videos. You could store your complete novel as a file in a BLOB if needed.

[Table of Contents](#SQL)

## How to add users in mysql?
You can add a User by using the CREATE command and specifying the necessary credentials. For example:
CREATE USER "testuser" IDENTIFIED BY "sample password";

[Table of Contents](#SQL)

## What is mysql views?
In MySQL, a view consists of a set of rows that is returned if a particular query is executed. This is also known as a "virtual table". Views make it easy to retrieve the way of making the query available via an alias.
The advantages of views are:
+ Simplicity
+ Security
+ Maintainability

[Table of Contents](#SQL)

## How do you create and execute views in mysql?
Creating a view is accomplished with the CREATE VIEW statement. As an example:
CREATE [OR REPLACE] [ALGORITHM = {MERGE | TEMPTABLE | UNDEFINED }] [DEFINER = { user | CURRENT_USER }][SQL SECURITY { DEFINER | INVOKER }] VIEW view_name [(column_list)] AS select_statement [WITH [CASCADED | LOCAL] CHECK OPTION]

```sql
create or replace view v_monthly_revenue as
select date_trunc('month', order_date) as month,
       sum(amount) as revenue
from orders
where status = 'completed'
group by 1;

select * from v_monthly_revenue where month >= date '2026-01-01';
```

Trade-off: a plain view stores only the query text and re-executes on every read, so it costs no storage but precomputes nothing. A materialized view stores the result; Postgres and Snowflake support them directly, BigQuery refreshes them automatically, and MySQL does not (use a summary table refreshed by a job).

[Table of Contents](#SQL)

## What is mysql triggers?
A trigger is a task that executes in response to some predefined database event, such as after a new row is added to a particular table. Specifically, this event involves inserting, modifying, or deleting table data, and the task can occur either prior to or immediately following any such event.
Triggers have many purposes, including:
+ Audit Trails
+ Validation
+ Referential integrity enforcement

```sql
create trigger trg_orders_after_insert
after insert on orders
for each row
begin
  insert into order_audit (order_id, action, changed_at)
  values (new.id, 'insert', current_timestamp);
end;
```

A trigger runs inside the statement's transaction, so the audit row and the order commit or roll back together. Trade-off: triggers guarantee the side effect but are invisible to application developers, fire on every write, and are hard to test. Many teams prefer log-based CDC for auditing because it adds no write-path overhead.

[Table of Contents](#SQL)

## How many triggers are possible in mysql?
There are six Triggers allowed to use in the MySQL database:
+ Before Insert
+ After Insert
+ Before Update
+ After Update
+ Before Delete
+ After Delete

[Table of Contents](#SQL)

## What is the mysql server?
The server, mysqld, is the hub of a MySQL installation; it performs all manipulation of databases and tables.

[Table of Contents](#SQL)

## What are the mysql clients and utilities?
Several MySQL programs are available to help you communicate with the server. For administrative tasks, some of the most important ones are listed here:
• mysql—An interactive program that enables you to send SQL statements to the server and to view the results. You can also use mysql to execute batch scripts (text files containing SQL statements).
• mysqladmin—An administrative program for performing tasks such as shutting down the server, checking its configuration, or monitoring its status if it appears not to be functioning properly.
• mysqldump—A tool for backing up your databases or copying databases to another server.
• mysqlcheck and myisamchk—Programs that help you perform table checking, analysis, and optimization, as well as repairs if tables become damaged. mysqlcheck works with MyISAM tables and to some extent with tables for other storage engines. myisamchk is for use only with MyISAM tables.

[Table of Contents](#SQL)

## Can you explain the logical architecture of mysql?
The top layer contains the services most network-based client/server tools or servers need such as connection handling, authentication, security, and so forth.
The second layer contains much of MySQL's brains. This has the code for query parsing, analysis, optimization, caching, and all the built-in functions.
The third layer contains the storage engines that are responsible for storing and retrieving the data stored in MySQL.

[Table of Contents](#SQL)

## What is scaling in mysql?
In MySQL, scaling capacity is actually the ability to handle the load, and it's useful to think of load from several different angles such as:
Quantity of data
Number of users
User activity
Size of related datasets

[Table of Contents](#SQL)

## What is sharding in sql?
The process of breaking up large tables into smaller chunks (called shards) that are spread across multiple servers is called Sharding.
The advantage of Sharding is that since the sharded database is generally much smaller than the original; queries, maintenance, and all other tasks are much faster.

[Table of Contents](#SQL)

## What are transaction storage engines in mysql?
To be able to use MySQL's transaction facility, you have to be using MySQL's InnoDB storage engine (which is the default from version 5.5 onward). If you are not sure which version of MySQL your code will be running on, rather than assuming InnoDB is the default engine you can force its use when creating a table, as follows.

[Table of Contents](#SQL)

## What is mysql?
MySQL is a database management system for web servers. It can grow with the website as it is highly scalable. Most of the websites today are powered by MySQL.

[Table of Contents](#SQL)

## What are some advantages of using mysql?
Flexibility: MySQL runs on all operating systems
Power: MySQL focuses on performance
Enterprise-Level SQL Features: MySQL had for some time been lacking in advanced features such as subqueries, views, and stored procedures.
Full-Text Indexing and Searching
Query Caching: This helps enhance the speed of MySQL greatly
Replication: One MySQL server can be duplicated on another, providing numerous advantages
Configuration and Security

[Table of Contents](#SQL)

## What do you mean by databases?
A database is a structured collection of data stored in a computer system and organized in a way to be quickly searched. With databases, information can be rapidly retrieved.

[Table of Contents](#SQL)

## Query to find second highest marks of a student?
Based On the Below Student table We are Written All the Queries.
Student Table
SELECT marks FROM Student ORDER by marks DESC limit 1, 1;

[Table of Contents](#SQL)

## Query to find duplicate rows in table?
SELECT std_id, COUNT(std_id) as cnt FROM Student GROUP by std_id having cnt > 1

[Table of Contents](#SQL)

## What is the query to fetch first record from student table?
SELECT * from Student where id = 1;

[Table of Contents](#SQL)

## What is the query to fetch last record from student table?
SELECT * FROM Student order by id desc limit 1

[Table of Contents](#SQL)

## What is query to display first 4 records from student table?
SELECT *  FROM Student limit 4

[Table of Contents](#SQL)

## What is query to display last 3 records from student table?
SELECT *  FROM Student order by std_id Desc limit 3

[Table of Contents](#SQL)

## What is query to display nth record from student table?
Select * from Student  where id = $n;

[Table of Contents](#SQL)

## How to get 3 highest marks from student table?
SELECT distinct(marks) FROM Student ORDER BY marks DESC LIMIT 0,3

```sql
select student_id, marks
from (
  select student_id, marks,
         dense_rank() over (order by marks desc) as rnk
  from student
) ranked
where rnk <= 3;
```

Top-N per group uses the same shape with a partition:

```sql
select class_id, student_id, marks
from (
  select class_id, student_id, marks,
         row_number() over (partition by class_id order by marks desc) as rn
  from student
) ranked
where rn <= 3;
```

Trade-off: `row_number` returns exactly N rows per group even with ties; `rank`/`dense_rank` can return more than N when marks tie. Pick based on whether "top 3" means three rows or three scores.

[Table of Contents](#SQL)

## How to display odd rows in student table?
SELECT * FROM Student where MOD(id,2) = 1

[Table of Contents](#SQL)

## How to display even rows in student table?
SELECT * FROM Student where MOD(id,2) = 0

[Table of Contents](#SQL)

## How can i create table with same structure of student table?
Create table std as Select * from Student;

[Table of Contents](#SQL)

## Select all records from student table whose name is a and b.
Select * from Student  where Name in("a", "b");

[Table of Contents](#SQL)

## What is ddl and dml and dcl?
If you look at the large variety of SQL commands, they can be divided into three large subgroups. Data Definition Language deals with database schemas and descriptions of how the data should reside in the database, therefore language statements like CREATE TABLE or ALTER TABLE belong to DDL. DML deals with data manipulation, and therefore includes most common SQL statements such SELECT, INSERT, etc. Data Control Language includes commands such as GRANT, and mostly concerns with rights, permissions and other controls of the database system.

[Table of Contents](#SQL)

## How do you get the number of rows affected by query?
SELECT COUNT (user_id) FROM users would only return the number of user_id's.

```sql
-- MySQL
update orders set status = 'paid' where status = 'new';
select row_count();

-- Postgres: returning also tells you which rows changed
update orders set status = 'paid' where status = 'new' returning order_id;

-- SQL Server
update orders set status = 'paid' where status = 'new';
select @@rowcount;
```

Trade-off: `returning`/`output` gives both the count and the keys, which makes it the best choice for pipelines that must log exactly what changed. The session variable form (`row_count()`, `@@rowcount`) is easy to read but can be clobbered by an intervening statement.

[Table of Contents](#SQL)

## If the value in the column is repeatable and how do you find out unique values?
Use DISTINCT in the query, such as SELECT DISTINCT user_firstname FROM users; You can also ask for a number of distinct values by saying SELECT COUNT (DISTINCT user_firstname) FROM users;

[Table of Contents](#SQL)

## How do you return hundred books starting from 25th?
SELECT book_title FROM books LIMIT 25, 100. The first number in LIMIT is the offset, the second is the number.

```sql
select * from books order by id limit 100 offset 24;                 -- MySQL, Postgres
select * from books order by id
  offset 24 rows fetch next 100 rows only;                           -- ANSI, Oracle, SQL Server
```

`offset` is zero-based, so "starting from the 25th" means `offset 24`. Always pair pagination with a deterministic `order by`; without one the engine may return rows in any order and pages can repeat or skip rows.

[Table of Contents](#SQL)

## You wrote search engine that should retrieve 10 results at a time but at the same time you do like to know how many rows there are total.
SELECT SQL_CALC_FOUND_ROWS page_title FROM web_pages LIMIT 1,10; SELECT FOUND_ROWS(); The second query (not that COUNT() is never used) will tell you how many results there're total, so you can display a phrase "Found 13,450,600 results, displaying 1-10". Note that FOUND_ROWS does not pay attention to the LIMITs you specified and always returns the total number of rows affected by query.

```sql
select count(*) over () as total_rows,
       book_id, title, score
from search_results
order by score desc
limit 10 offset 20;
```

A window `count(*) over ()` returns the total alongside each page in one query. Trade-off: on very large result sets the window forces the engine to scan the full result, so a separate `select count(*)` (or an approximate count in BigQuery/Spark) can be cheaper. Keyset pagination (`where score < :last_score`) avoids the growing cost of a large `offset`.

[Table of Contents](#SQL)

## How would you write a query to select all teams that won either 2 and 4 and 6 or 8 games?
SELECT team_name FROM teams WHERE team_won IN (2, 4, 6, 8)

[Table of Contents](#SQL)

## How would you select all users whose phone number is null?
SELECT user_name FROM users WHERE ISNULL(user_phonenumber);

```sql
select * from users where phone_number is null;
-- never: where phone_number = null   (always unknown, returns no rows)

-- treat empty strings as missing too
select * from users where phone_number is null or phone_number = '';
```

Trade-off: `is null` can use a B-tree index in Postgres and Oracle; `= null` is always unknown. For a "missing or blank" rule, normalize blank strings to null at load time so every query can use the simple `is null` form.

[Table of Contents](#SQL)

## How do you find out which auto increment was assigned on the last insert?
SELECT LAST_INSERT_ID() will return the last value assigned by the auto_increment function. Note that you don't have to specify the table name.

[Table of Contents](#SQL)

## On executing delete statement i keep getting the error about foreign key constraint failing so what do i do?
What it means is that so of the data that you're trying to delete is still alive in another table. Like if you have a table for universities and a table for students, which contains the ID of the university they go to, running a delete on a university table will fail if the students table still contains people enrolled at that university. Proper way to do it would be to delete the offending data first, and then delete the university in question. Quick way would involve running SET foreign_key_checks=0 before the DELETE command, and setting the parameter back to 1 after the DELETE is done. If your foreign key was formulated with ON DELETE CASCADE, the data in dependent tables will be removed automatically.

[Table of Contents](#SQL)

## When would you use order by in delete statement?
When you're not deleting by row ID. Such as in DELETE FROM techpreparation_com_questions ORDER BY timestamp LIMIT 1.

```sql
-- MySQL: delete the oldest rows, capped per statement
delete from audit_log
order by created_at asc
limit 1000;
```

Standard SQL and Postgres do not allow `order by` in `delete`, so use a keyed subquery:

```sql
delete from audit_log
where id in (
  select id from audit_log order by created_at asc limit 1000
);
```

Ordered, limited deletes are the safe pattern for a retention job that must chew through a huge table without one giant transaction.

[Table of Contents](#SQL)

## How can you see all indexes defined for a table?
SHOW INDEX FROM techpreparation_questions;

[Table of Contents](#SQL)

## How would you delete column?
ALTER TABLE techpreparation_answers DROP answer_user_id.

[Table of Contents](#SQL)

## How would you change a table to innodb?
ALTER TABLE techpreparation_questions ENGINE innodb;

[Table of Contents](#SQL)

## How do you concatenate strings in mysql?
CONCAT (string1, string2, string3)

```sql
select concat(first_name, ' ', last_name) as full_name from users;   -- MySQL, Postgres, Snowflake
select first_name || ' ' || last_name as full_name from users;       -- ANSI, Postgres, Oracle
select concat_ws(' ', first_name, last_name) as full_name;           -- skips null parts
```

Trade-off: in MySQL `concat` returns null when any argument is null, so wrap nullable parts in `coalesce` or use `concat_ws`, which skips null arguments. In Postgres the `||` operator is idiomatic and treats null as null, so `coalesce` is still needed.

[Table of Contents](#SQL)

## How do you get a portion of string?
SELECT SUBSTR(title, 1, 10) from techpreparation_questions;

[Table of Contents](#SQL)

## What is the difference between char length and length?
The first is, naturally, the character count. The second is byte count. For the Latin characters the numbers are the same, but they're not the same for Unicode and other encodings.

[Table of Contents](#SQL)

## How do you convert string to utf-8?
SELECT (techpreparation_question USING utf8);

[Table of Contents](#SQL)

## How do you get month from timestamp?
SELECT MONTH(techpreparation_timestamp) from techpreparation_questions;

[Table of Contents](#SQL)

## How do you offload the time and date handling to mysql?
SELECT DATE_FORMAT(techpreparation_timestamp, "%Y-%m-%d") from techpreparation_questions; A similar TIME_FORMAT function deals with time.

[Table of Contents](#SQL)

## How do you add three minutes to a date?
ADDDATE(techpreparation_publication_date, INTERVAL 3 MINUTE)

```sql
select date_add(now(), interval 3 minute) as plus_three;                        -- MySQL
select now() + interval '3 minutes' as plus_three;                              -- Postgres
select dateadd(minute, 3, getdate()) as plus_three;                             -- SQL Server
select timestamp_add(current_timestamp(), interval 3 minute) as plus_three;     -- BigQuery
```

Trade-off: interval syntax is the least portable part of SQL. Keep all time arithmetic behind one shared macro or a small set of helper views so a warehouse migration does not require rewriting every query.

[Table of Contents](#SQL)

## What is the difference between unix timestamps and mysql timestamps?
Internally Unix timestamps are stored as 32-bit integers, while MySQL timestamps are stored in a similar manner, but represented in readable YYYY-MM-DD HH:MM:SS format.

[Table of Contents](#SQL)

## How do you convert between unix timestamps and mysql timestamps?
UNIX_TIMESTAMP converts from MySQL timestamp to Unix timestamp, FROM_UNIXTIME converts from Unix timestamp to MySQL timestamp.

```sql
-- epoch seconds -> timestamp
select from_unixtime(1767225600) as ts;              -- MySQL
select to_timestamp(1767225600)  as ts;              -- Postgres
select timestamp_seconds(1767225600) as ts;          -- BigQuery

-- timestamp -> epoch seconds
select unix_timestamp('2026-01-01 00:00:00') as epoch;   -- MySQL
select extract(epoch from timestamp '2026-01-01 00:00:00') as epoch;   -- Postgres
```

Trade-off: MySQL's `from_unixtime`/`unix_timestamp` operate in the session time zone, so the same stored value renders differently on servers with a different `time_zone` setting. Store UTC and keep the conversion explicit.

[Table of Contents](#SQL)

## What are enums used for in mysql?
You can limit the possible values that go into the table. CREATE TABLE months (month ENUM "January", "February", "March",…); INSERT months VALUES ("April");

[Table of Contents](#SQL)

## How are enums and sets represented internally?
As unique integers representing the powers of two, due to storage optimizations.

[Table of Contents](#SQL)

## How do you start and stop mysql on windows?
net start MySQL, net stop MySQL

[Table of Contents](#SQL)

## How do you start mysql on linux?
/etc/init.d/mysql start

[Table of Contents](#SQL)

## Explain the difference between mysql and mysql interfaces in php?
mysql is the object-oriented version of mysql library functions.

[Table of Contents](#SQL)

## What is the default port for mysql server?
3306 is the default port for MYSQL.

[Table of Contents](#SQL)

## What does tee command do in mysql?
tee followed by a filename turns on MySQL logging to a specified file. It can be stopped by command note.

[Table of Contents](#SQL)

## Can you save your connection settings to a conf file?
Yes, and name it ~/.my.conf. You might want to change the permissions on the file to 600, so that it's not readable by others.

[Table of Contents](#SQL)

## How do you change a password for an existing user via mysqladmin?
mysqladmin -u root -p password "newpassword"

[Table of Contents](#SQL)

## Use mysqldump to create a copy of the database?
mysqldump -h mysqlhost -u username -p mydatabasename > dbdump.sql

[Table of Contents](#SQL)

## Have you ever used mysql administrator and mysql query browser?
Describe the tasks you accomplished with these tools.

[Table of Contents](#SQL)

## What are some good ideas regarding user security in mysql?
There is no user without a password. There is no user without a user name. There is no user whose Host column contains % (which here indicates that the user can log in from anywhere in the network or the Internet). There are as few users as possible (in the ideal case only root) who have unrestricted access.

[Table of Contents](#SQL)

## Explain the difference between myisam static and myisam dynamic?
In MyISAM static all the fields have fixed width. The Dynamic MyISAM table would include fields such as TEXT, BLOB, etc. to accommodate the data types with various lengths. MyISAM Static would be easier to restore in case of corruption, since even though you might lose some data, you know exactly where to look for the beginning of the next record.

[Table of Contents](#SQL)

## What does myisamchk do?
It compressed the MyISAM tables, which reduces their disk usage.

[Table of Contents](#SQL)

## Explain advantages of innodb over myisam?
Row-level locking, transactions, foreign key constraints and crash recovery.

[Table of Contents](#SQL)

## Explain advantages of myisam over innodb?
Much more conservative approach to disk space management - each MyISAM table is stored in a separate file, which could be compressed then with myisamchk if needed. With InnoDB the tables are stored in tablespace, and not much further optimization is possible. All data except for TEXT and BLOB can occupy 8,000 bytes at most. No full text indexing is available for InnoDB. TRhe COUNT(*)s execute slower than in MyISAM due to tablespace complexity.

[Table of Contents](#SQL)

## What are heap tables in mysql?
HEAP tables are in-memory. They are usually used for high-speed temporary storage. No TEXT or
BLOB fields are allowed within HEAP tables. You can only use the comparison operators = and <=>. HEAP tables do not support AUTO_INCREMENT. Indexes must be NOT NULL.

[Table of Contents](#SQL)

## How do you control the max size of a heap table?
MySQL config variable max_heap_table_size.

[Table of Contents](#SQL)

## What are csv tables?
Those are the special tables, data for which is saved into comma-separated values files. They cannot be indexed.

[Table of Contents](#SQL)

## Explain federated tables?
Introduced in MySQL 5.0, federated tables allow access to the tables located on other databases on other servers.

[Table of Contents](#SQL)

## What is serial data type in mysql?
BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT
SERIAL is an alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE

[Table of Contents](#SQL)

## What happens when the column is set to auto increment and you reach the maximum value for that table?
It stops incrementing. It does not overflow to 0 to prevent data losses, but further inserts are going to produce an error, since the key has been used already.

[Table of Contents](#SQL)

## Explain the difference between bool, tinyint and bit?
Prior to MySQL 5.0.3: those are all synonyms. After MySQL 5.0.3: BIT data type can store 8 bytes of data and should be used for binary data.

[Table of Contents](#SQL)

## Explain the difference between float, double and real?
+ FLOATs store floating point numbers with 8 place accuracy and take up 4 bytes.
+ DOUBLEs store floating point numbers with 16 place accuracy and take up 8 bytes.
+ REAL is a synonym of FLOAT for now.

[Table of Contents](#SQL)

## What happens if a table has one column defined as timestamp?
That field gets the current timestamp whenever the row gets altered.

[Table of Contents](#SQL)

## But what if you really want to store the timestamp data, such as the publication date of the article?
Create two columns of type TIMESTAMP and use the second one for your real data.

[Table of Contents](#SQL)

## Explain data type timestamp default current_timestamp on update current_timestamp?
The column exhibits the same behavior as a single timestamp column in a table with no other timestamp columns.

[Table of Contents](#SQL)

## What does timestamp on update current_timestamp data type do?
On initialization places a zero in that column, on future updates puts the current value of the timestamp in.

[Table of Contents](#SQL)

## If I created a column with data type varchar(3) so what would I expect to see in mysql table?
CHAR(3), since MySQL automatically adjusted the data type.

[Table of Contents](#SQL)

## General information about mysql.
MySQL is a very fast, multi-threaded, multi-user, and robust SQL (Structured Query Language) database server.

W## hy Sql Is A Database Management System?
A database is a structured collection of data. It may be anything from a simple shopping list to a picture gallery or the vast amounts of information in a corporate network. To add, access, and process data stored in a computer database, you need a database management system such as MySQL. Since computers are very good at handling large amounts of data, database management plays a central role in computing, as stand-alone utilities, or as parts of other applications.

[Table of Contents](#SQL)

## Why use mysql?
MySQL is very fast, reliable, and easy to use. If that is what you are looking for, you should give it a try. MySQL also has a very practical set of features developed in very close cooperation with our users. You can find a performance comparison of MySQL to some other database managers on our benchmark page. See section 12.7 Using Your Own Benchmarks. MySQL was originally developed to handle very large databases much faster than existing solutions and has been successfully used in highly demanding production environments for several years. Though under constant development, MySQL today offers a rich and very useful set of functions. The connectivity, speed, and security make MySQL highly suited for accessing databases on the Internet.

[Table of Contents](#SQL)

## How mysql optimizes distinct?
DISTINCT is converted to a GROUP BY on all columns, DISTINCT combined with ORDER BY will in many cases also need a temporary table.
When combining LIMIT # with DISTINCT, MySQL will stop as soon as it finds # unique rows.
If you don't use columns from all used tables, MySQL will stop the scanning of the not used tables as soon as it has found the first match.
SELECT DISTINCT t1.a FROM t1,t2 where t1.a=t2.a;
In the case, assuming t1 is used before t2 (check with EXPLAIN), then MySQL will stop reading from t2 (for that particular row in t1) when the first row in t2 is found.

[Table of Contents](#SQL)

## How mysql optimizes limit?
In some cases MySQL will handle the query differently when you are using LIMIT # and not using HAVING:
+ If you are selecting only a few rows with LIMIT, MySQL will use indexes in some cases when it normally would prefer to do a full table scan.
+ If you use LIMIT # with ORDER BY, MySQL will end the sorting as soon as it has found the first # lines instead of sorting the whole table.
  When combining LIMIT # with DISTINCT, MySQL will stop as soon as it finds # unique rows.
  In some cases a GROUP BY can be resolved by reading the key in order (or do a sort on the key) and then calculate summaries until the key value changes. In this case LIMIT # will not calculate any unnecessary GROUP BY's.
  As soon as MySQL has sent the first # rows to the client, it will abort the query.
  LIMIT 0 will always quickly return an empty set. This is useful to check the query and to get the column types of the result columns.
  The size of temporary tables uses the LIMIT # to calculate how much space is needed to resolve the query.

[Table of Contents](#SQL)

## Mysql speed of delete queries ?
If you want to delete all rows in the table, you should use TRUNCATE TABLE table_name. The time to delete a record is exactly proportional to the number of indexes. To delete records more quickly, you can increase the size of the index cache.

[Table of Contents](#SQL)

## What is the difference between mysql_fetch_array and mysql_fetch_object?
+ mysql_fetch_array — Fetch a result row as an associative ARRAY, a numeric array, or both
+ mysql_fetch_object — Fetch a result row as an OBJECT.

[Table of Contents](#SQL)

## What are the different table present in mysql?
+ MyISAM : This is default. Based on Indexed Sequntial Access Method. The above SQL will create a MyISA table.
+ ISAM : same
+ HEAP : Fast data access, but will loose data if there is a crash. Cannot have BLOB, TEXT & AUTO INCRIMENT fields
+ BDB : Supports Transactions using COMMIT & ROLLBACK. Slower that others.
+ InnoDB : same as BDB

[Table of Contents](#SQL)

## What is primary key?
A primary key is a single column or multiple columns defined to have unique values that can be used as row identifications.

[Table of Contents](#SQL)

## What is foreign key?
A foreign key is a single column or multiple columns defined to have values that can be mapped to a primary key in another table.

[Table of Contents](#SQL)

## What is index?
An index is a single column or multiple columns defined to have values pre-sorted to speed up data retrieval speed.

[Table of Contents](#SQL)

## What is join?
Join is data retrieval operation that combines rows from multiple tables under certain matching conditions to form a single row.

A join combines rows from two inputs using a predicate. Beyond the textbook inner and outer joins, data engineers use semi-joins, anti-joins, and self-joins.

```sql
-- semi-join: customers with at least one order, without duplicating customers
select c.*
from customers c
where exists (select 1 from orders o where o.customer_id = c.id);

-- anti-join: customers with no orders
select c.*
from customers c
where not exists (select 1 from orders o where o.customer_id = c.id);

-- self-join: employee and manager from the same table
select e.name as employee, m.name as manager
from employees e
left join employees m on m.id = e.manager_id;
```

Trade-off: `exists` expresses "at least one match" without multiplying rows the way a plain join can. A self-join needs an alias on both sides and an index on the join key, or the table is scanned twice.

[Table of Contents](#SQL)

## What is union?
Join is data retrieval operation that combines multiple query outputs of the same structure into a single output. By default the MySQL UNION removes all duplicate rows from the result set even if you don't explicit using DISTINCT after the keyword UNION.
SELECT customerNumber id, contactLastname name FROM customers UNION SELECT employeeNurrber id, firstname name FROM employees

id name
103 Schmitt
112 King
114 Ferguson
119 Labrune
121 Bergulfsen

[Table of Contents](#SQL)

## What is isam?
ISAM (Indexed Sequential Access Method) was developed by IBM to store and retrieve data on secondary storage systems like tapes.

[Table of Contents](#SQL)

## What is innodb?
InnoDB is a transaction safe storage engine developed by Innobase Oy (an Oracle company now).

[Table of Contents](#SQL)

## What is bdb berkeleydb?
BDB (BerkeleyDB) is transaction safe storage engine originally developed at U.C. Berkeley. It is now developed by Sleepycat Software, Inc. (an Oracle company now).

[Table of Contents](#SQL)

## What is csv?
CSV (Comma Separated Values) is a file format used to store database table contents, where one table row is stored as one line in the file, and each data field is separated with comma.

[Table of Contents](#SQL)

## What is transaction?
A transaction is a logical unit of work requested by a user to be applied to the database objects. MySQL server introduces the transaction concept to allow users to group one or more SQL statements into a single transaction, so that the effects of all the SQL statements in a transaction can be either all committed (applied to the database) or all rolled back (undone from the database).

[Table of Contents](#SQL)

## What is commit?
Commit is a way to terminate a transaction with all database changes to be saved permanently to the database server.

[Table of Contents](#SQL)

## What is rollback?
Rollback is a way to terminate a transaction with all database changes not saving to the database server.

[Table of Contents](#SQL)

## How many groups of data types?
MySQL support 3 groups of data types as listed below:
+ String Data Types - CHAR, NCHAR, VARCHAR, NVARCHAR, BINARY, VARBINARY, TINYBLOB, TINYTEXT, BLOB, TEXT, MEDIUMBLOB, MEDIUMTEXT, LONGBLOB, LONGTEXT, ENUM, SET.
+ Numeric Data Types - BIT, TINYINT, BOOLEAN, SMALLINT, MEDIUMINT, INTEGER, BIGINT, FLOAT, DOUBLE, REAL, DECIMAL.
+ Date and Time Data Types - DATE, DATETIME, TIMESTAMP, TIME, YEAR.

[Table of Contents](#SQL)

## What is the differences between char and nchar?
Both CHAR and NCHAR are fixed length string data types. But they have the following differences:
+ CHARs full name is CHARACTER.
+ NCHARs full name is NATIONAL CHARACTER.
  By default, CHAR uses ASCII character set. So 1 character is always stored as 1 byte.
  By default, NCHAR uses Unicode character set. NCHAR data are stored in UTF8 format. So 1 character could be stored as 1 byte or upto 4 bytes.
  Both CHAR and NCHAR columns are defined with fixed lengths in units of characters.

[Table of Contents](#SQL)

## How to escape special characters in sql statements?
There are a number of special characters that needs to be escaped (protected), if you want to include them in a character string. Here are some basic character escaping rules:
The escape character () needs to be escaped as (\).
The single quote (") needs to be escaped as (") or (“) in single-quote quoted strings.
The double quote () needs to be escaped as (“) or (““) in double-quote quoted strings.
The wild card character for a single character () needs to be escaped as (_).
The wild card character for multiple characters (%) needs to be escaped as (%).
The tab character needs to be escaped as (t).
The new line character needs to be escaped as (n).
The carriage return character needs to be escaped as (r).

[Table of Contents](#SQL)

## How to concatenate two character strings?
If you want concatenate multiple character strings into one, you need to use the CONCAT() function. Here are some good examples:
SELECT CONCAT("Welcome"," to") FROM DUAL;
Welcome to
SELECT CONCAT(wj","center",".com") FROM DUAL;
wisdomjobs.com

[Table of Contents](#SQL)

## How to enter characters as hex numbers?
If you want to enter characters as HEX numbers, you can quote HEX numbers with single quotes and a prefix of (X), or just prefix HEX numbers with (Ox). A HEX number string will be automatically converted into a character string, if the expression context is a string. Here are some good examples:

SELECT X313233" FROM DUAL;
123
SELECT 0x414243 FROM DUAL;
ABC

[Table of Contents](#SQL)

## How to enter boolean values in sql statements?
If you want to enter Boolean values in SQL statements, you use (TRUE), (FALSE), (true), or (false). Here are some good examples:
SELECT TRUE, true, FALSE, false FROM DUAL;

[Table of Contents](#SQL)

## How to convert numeric values to character strings?
You can convert numeric values to character strings by using the CAST(value AS CHAR) function as shown in the following examples:
SELECT CAST(4123.45700 AS CHAR) FROM DUAL;
4123.45700

[Table of Contents](#SQL)

## How to use in conditions?
An IN condition is single value again a list of values. It returns TRUE, if the specified value is in the list. Otherwise, it returns FALSE. Some examples are :
SELECT 3 IN (1,2,3,4,5) FROM DUAL;
1
SELECT 3 NOT IN (1,2,3,4,5) FROM DUAL;
0
SELECT Y" IN ("F","Y",I) FROM DUAL;
1

```sql
select * from orders where status in ('new', 'paid');
select * from orders where status not in ('cancelled', 'refunded');
select * from orders where status in (select status from active_statuses);
```

Warning: `not in (subquery)` returns no rows at all when the subquery produces a single null, because every comparison becomes unknown. Use `not exists` for anti-joins, or add `where status is not null` to the subquery.

[Table of Contents](#SQL)

## How to use like conditions?
A LIKE condition is also called pattern patch. There are 3 main rules on using LIKE condition:
is used in the pattern to match any one character.
% is used in the pattern to match any zero or more characters.
ESCAPE clause is used to provide the escape character in the pattern.

```sql
select * from customers where name like 'A%';                 -- starts with A
select * from customers where name like '%son';               -- ends with son
select * from customers where name like '_ohn';               -- 4 chars ending in ohn
select * from customers where name like '%\%%' escape '\';    -- literal percent
```

Trade-off: a leading wildcard (`'%term'`) prevents index use, while a trailing wildcard (`'term%'`) can use an index. For case-insensitive matching use `ilike` or a case-insensitive collation rather than wrapping the column in `lower()`.

[Table of Contents](#SQL)

## How to present a past time in hours and minutes and seconds?
If you want show an article was posted “n hours n minutes and n seconds ago", you can use the TIMEDIFF(NOWO, pastTime) function as shown in the following are:

SELECT TIMEDIFF(NOWO, "2006-07-01 04:09:49") FROM DUAL;
06:42:58
SELECT TIM E_FORMAT(TI M EDI FF( NOWO, "2006-06-30 04:09:49"),"%H hours, %i minutes and %s seconds ago.") FROM DUAL;
30 hours, 45 minutes and 22 seconds ago.

[Table of Contents](#SQL)

## How to add a new column to an existing table in mysql?
ALTER TABLE tip ADD COLUMN author VARCHAR(40);
Query OK, 1 row affected (0.18 sec)
Records: 1 Duplicates: 0 Warnings: 0

[Table of Contents](#SQL)

## How to delete an existing column in a table?
ALTER TABLE tip DROP COLUMN create_date;
Query OK, 1 row affected (0.48 sec)
Records: 1 Duplicates: 0 Warnings: 0

[Table of Contents](#SQL)

## How to rename an existing column in a table?
ALTER TABLE tip CHANGE COLUMN subject title VARCHAR(60);

[Table of Contents](#SQL)

## How to rename an existing table in mysql?
ALTER TABLE tip RENAME TO faq;

[Table of Contents](#SQL)

## How to create a table index in mvsql?
If you have a table with a lots of rows, and you know that one of the columns will be used often as a search criteria, you can add an index for that column to improve the search performance. To add an index, you can use the “CREATE INDEX” statement as shown in the following script:

```text
mysql> CREATE TABLE tip (id INTEGER PRIMARY KEY,
subject VARCHAR(80) NOT NULL,
description VARCHAR(256) NOT NULL,
create_date DATE NULL);  Query OK,
0 rows affected (0.08 sec)
```

mysql> CREATE INDEX tip_subject ON tip(subject);
Query OK,
0 rows affected (0.19 sec)
Records: 0 Duplicates: 0 Warnings: 0

[Table of Contents](#SQL)

## How to get a list of indexes of an existing table?
If you want to see the index you have just created for an existing table, you can use the “SHOW INDEX FROM tableName” command to get a list of all indexes in a given table.

[Table of Contents](#SQL)

## How to drop an existing index in mysql?
If you don't need an existing index any more, you should delete it with the “DROP INDEX indexName ON tableName” statement. Here is an example SQL script :

mysqi> DROP INDEX tip_subject ON tip;
Query OK, 0 rows affected (0.13 sec)
Records: 0 Duplicates: 0 Warnings: 0

[Table of Contents](#SQL)

## How to drop an existing view in mysql?
If you have an existing view, and you dont want it anymore, you can delete it by using the “DROP VIEW viewName” statement

[Table of Contents](#SQL)

## How to create a new view in mysql?
You can create a new view based on one or more existing tables by using the
“CREATE VIEW viewName AS selectStatement” .

[Table of Contents](#SQL)

## How to increment dates by 1111 mysql?
If you have a date, and you want to increment it by 1 day, you can use the DATE_ADD(date, INTERVAL 1 DAY) function. You can also use the date interval add operation as “date + INTERVAL 1 DAY.

[Table of Contents](#SQL)

## Explain what is a database?
A database is a collection of information in an organized form for faster and better access, storage and manipulation. It can also be defined as a collection of tables, schema, views and other database objects.

[Table of Contents](#SQL)

## Explain what is dbms?
Database Management System is a collection of programs that enables a user to store, retrieve, update and delete information from a database.

[Table of Contents](#SQL)

## Explain what is rdbms?
RDBMS stands for Relational Database Management System. RDBMS is a database management system (DBMS) that is based on the relational model. Data from relational database can be accessed using Structured Query Language (SQL)

[Table of Contents](#SQL)

## What are the popular database management systems in it industry?
Oracle, MySQL, Microsoft SQL Server, PostgreSQL, Sybase, MongoDB, DB2, and Microsoft Access etc.,

[Table of Contents](#SQL)

## Explain what is sql?
SQL stands for Structured Query Language. It is an American National Standard Institute (ANSI) standard. It is a standard language for accessing and manipulating databases. Using SQL, some of the action we could do are to create databases, tables, stored procedures (SP's), execute queries, retrieve, insert, update, delete data against a database.

[Table of Contents](#SQL)

## Explain what is table in a database?
A table is a database object used to store records in a field in the form of columns and rows that holds data.

[Table of Contents](#SQL)

## Explain what is a field in a database and record in a database?
A field in a Database table is a space allocated to store a particular record within a table.
A record (also called a row of data) is an ordered set of related data in a table.

[Table of Contents](#SQL)

## What is the use of nvl function?
NVL function is used to convert the null value to its actual value.

[Table of Contents](#SQL)

## Explain what is a column in a table?
A column is a vertical entity in a table that contains all information associated with a specific field in a table.

[Table of Contents](#SQL)

## What are the different types of sql commands?
SQL commands are segregated into following types:
+ DDL – Data Definition Language
+ DML – Data Manipulation Language
+ DQL – Data Query Language
+ DCL – Data Control Language
+ TCL – Transaction Control Language

[Table of Contents](#SQL)

## What are the different ddl commands in sql?
DDL commands are used to define or alter the structure of the database.
+ CREATE: To create databases and database objects
+ ALTER: To alter existing database objects
+ DROP: To drop databases and databases objects
+ TRUNCATE: To remove all records from a table but not its database structure
+ RENAME: To rename database objects

[Table of Contents](#SQL)

## What are the different dml commands in sql?
DML commands are used for managing data present in the database.
+ SELECT: To select specific data from a database
+ INSERT: To insert new records into a table
+ UPDATE: To update existing records
+ DELETE: To delete existing records from a table

[Table of Contents](#SQL)

## What are the different dcl commands in sql?
DCL commands are used to create roles, grant permission and control access to the database objects.
+ GRANT: To provide user access
+ DENY: To deny permissions to users
+ REVOKE: To remove user access

[Table of Contents](#SQL)

## What are the different tcl commands in sql?
TCL commands are used to manage the changes made by DML statements.
+ COMMIT: To write and store the changes to the database
+ ROLLBACK: To restore the database since the last commit

[Table of Contents](#SQL)

## Explain what is an index?
An index is used to speed up the performance of queries. It makes faster retrieval of data from the table. The index can be created on one column or a group of columns.

[Table of Contents](#SQL)

## Explain what is a view?
A view is like a subset of a table which is stored logically in a database. A view is a virtual table. It contains rows and columns similar to a real table. The fields in the view are fields from one or more real tables. Views do not contain data of their own. They are used to restrict access to the database or to hide data complexity.

[Table of Contents](#SQL)

## Explain what is a subquery ?
A Subquery is a SQL query within another query. It is a subset of a Select statement whose return values are used in filtering the conditions of the main query.

```sql
-- scalar subquery
select (select max(amount) from orders) as max_amount;

-- correlated subquery: conceptually runs once per outer row
select o.*
from orders o
where o.amount > (select avg(amount) from orders x where x.customer_id = o.customer_id);

-- same logic with a window function, usually one pass
select *
from (
  select o.*, avg(amount) over (partition by customer_id) as customer_avg
  from orders o
) t
where amount > customer_avg;
```

Trade-off: correlated subqueries are readable but can execute once per row; a window function or a join to a pre-aggregated CTE lets the engine do one pass. Use `exists` for existence tests because it can stop at the first match.

[Table of Contents](#SQL)

## How do you write a CTE and a recursive CTE in SQL?

```sql
-- plain CTE: stage a heavy aggregation, then join to it
with daily_revenue as (
  select order_date, customer_id, sum(amount) as revenue
  from orders
  where status = 'completed'
  group by order_date, customer_id
)
select order_date, sum(revenue) as revenue
from daily_revenue
group by order_date
order by order_date;

-- recursive CTE: walk the management hierarchy from the top
with recursive org as (
  select id, name, manager_id, 0 as depth
  from employees
  where manager_id is null
  union all
  select e.id, e.name, e.manager_id, o.depth + 1
  from employees e
  join org o on e.manager_id = o.id
)
select * from org order by depth, name;
```

The `recursive` keyword is required in Postgres, Snowflake, and BigQuery; SQL Server omits it. A recursive CTE can loop forever on cyclic data, so cap it with a `depth < 10` predicate or carry a visited-path array. Trade-off: a CTE is mainly a readability and reuse tool — most optimizers inline it, so on some engines it is not a performance boundary at all.

[Table of Contents](#SQL)

## What is the difference between rename and alias?
+ "Rename" is a permanent name given to a table or column
+ "Alias" is a temporary name given to a table or column.

[Table of Contents](#SQL)

## What is a join?
Join is a query, which retrieves related columns or rows from multiple tables.

[Table of Contents](#SQL)

## What are the different types of joins?
Types of Joins are as follows:
+ INNER JOIN: It is also known as SIMPLE JOIN which returns all rows from BOTH tables when it has at least one column matched
+ + Syntax: SELECT column_name(s) FROM table_name1 INNER JOIN table_name2 ON column_name 1=column_name 2;
+ LEFT JOIN (LEFT OUTER JOIN): This join returns all rows from a LEFT table and its matched rows from a RIGHT table.
+ + Syntax: SELECT column_name(s) FROM table_name1 LEFT JOIN table_name2 ON column_name 1=column_name 2;
+ RIGHT JOIN (RIGHT OUTER JOIN): This joins returns all rows from the RIGHT table and its matched rows from a LEFT table.
+ + Syntax: SELECT column_name(s) FROM table_name1 RIGHT JOIN table_name2 ON column_name1=column_name2;
+ FULL JOIN (FULL OUTER JOIN): This joins returns all when there is a match either in the RIGHT table or in the LEFT table.
+ + Syntax: SELECT column_name(s) FROM table_name1 FULL OUTER JOIN table_name2 ON column_name1=column_name2;

```sql
-- cross join: every combination, use with care
select * from colors cross join sizes;

-- inner join
select * from a inner join b on a.id = b.id;

-- outer joins
select * from a left  join b on a.id = b.id;
select * from a right join b on a.id = b.id;
select * from a full  join b on a.id = b.id;

-- semi-join and anti-join
select * from a where exists     (select 1 from b where b.id = a.id);
select * from a where not exists (select 1 from b where b.id = a.id);
```

Dialect note: Postgres, Snowflake, and BigQuery support `full outer join`; MySQL does not, so emulate it with a union of the left and right joins. Always state whether unmatched rows must survive.

[Table of Contents](#SQL)

## What are sql constraints?
SQL constraints are the set of rules that enforced some restriction while inserting, deleting or updating of data in the databases.

[Table of Contents](#SQL)

## What are the constraints available in sql?
Some constraints in SQL are : Primary Key, Foreign Key, Unique Key, SQL Not Null, Default, Check and Index constraint.

```sql
create table orders (
  id           bigint primary key,
  order_number varchar(32) not null unique,
  customer_id  bigint not null references customers(id) on delete cascade,
  amount       numeric(12,2) not null check (amount >= 0),
  status       varchar(16) not null default 'new'
               check (status in ('new','paid','shipped','cancelled')),
  created_at   timestamp not null default current_timestamp
);
```

- `primary key`: unique and not null, one per table.
- `unique`: uniqueness rule, nulls allowed in most engines.
- `foreign key`: referential integrity with `on delete`/`on update` actions.
- `check`: a row-level boolean rule.
- `not null` and `default`: presence and fallback rules.

Trade-off: constraints catch bad data at the source and give the optimizer facts it can trust, but validating a check on a huge existing table can scan it. Oracle and Postgres let you add a constraint `not valid` first and validate later.

[Table of Contents](#SQL)

## What is a unique key and primary key and foreign key?
+ A UNIQUE KEY constraint is used to ensure that there are no duplication values in the field/column.
+ A PRIMARY KEY constraint uniquely identifies each record in a database table. All columns participating in a primary key constraint must not contain NULL values.
+ A FOREIGN KEY is a key used to link two tables together. A FOREIGN KEY in a table is linked with the PRIMARY KEY of another table.

```sql
create table orders (
  order_id     bigint primary key,                               -- row identity
  order_number varchar(32) unique not null,                      -- alternate unique key
  customer_id  bigint not null references customers(customer_id) -- foreign key
);
```

- Primary key: uniquely identifies the row, cannot be null, one per table.
- Unique key: enforces uniqueness, nulls allowed in most engines.
- Foreign key: a value that must exist in the referenced table, with `on delete`/`on update` behavior.

All three are enforced by the database and backed by an index, so they also speed up joins and lookups.

[Table of Contents](#SQL)

## What is the difference between unique and primary key constraints?
There should be only one PRIMARY KEY in a table whereas there can be any number of UNIQUE Keys.
PRIMARY KEY doesn't allow NULL values whereas Unique key allows NULL values.

[Table of Contents](#SQL)

## What is a null value?
A field with a NULL value is a field with no value. A NULL value is different from a zero value or a field that contains spaces. A field with a NULL value is one that has been left blank during record creation. Assume, there is a field in a table is optional and it is possible to insert a record without adding a value to the optional field then the field will be saved with a NULL value.

```sql
select
  count(*)                                                  as total_rows,
  count(phone_number)                                       as non_null_phones,
  sum(case when phone_number is null then 1 else 0 end)     as missing_phones
from users;
```

`null` means "unknown", not zero or blank: `null = null` is unknown, `null + 1` is null, and `not (null = null)` is also unknown. `count(*)` counts rows while `count(column)` skips nulls, which is the usual cause of totals that do not add up in a report.

[Table of Contents](#SQL)

## What is normalization?
Normalization is the process of table design to minimize the data redundancy.
There are different types of Noramalization forms in SQL:-
+ First Normal Form (1NF): It removes all duplicate columns from the table. Creates table for related data and identifies unique column values
+ First Normal Form (2NF): Follows 1NF and creates and places data subsets in an individual table and defines relationship between tables using primary key
+ Third Normal Form (3NF): Follows 2NF and removes those columns which are not related through primary key
+ Fourth Normal Form (4NF): Follows 3NF and do not define multi-valued dependencies. 4NF also known as BCNF

```sql
-- 1NF/2NF/3NF: every fact in exactly one place
create table customers (customer_id bigint primary key, name text, email text);
create table products  (product_id bigint primary key, name text, price numeric(12,2));
create table orders    (order_id bigint primary key, customer_id bigint references customers);
create table order_items (
  order_id   bigint references orders,
  product_id bigint references products,
  quantity   int not null,
  primary key (order_id, product_id)
);
```

1NF removes repeating groups, 2NF removes partial dependencies on part of a composite key, and 3NF removes transitive dependencies (a non-key column determined by another non-key column). Trade-off: normalization prevents update anomalies and saves storage, but analytics then needs more joins, so warehouses deliberately denormalize into star schemas for read performance.

[Table of Contents](#SQL)

## What is stored procedure?
A Stored Procedure is a collection of SQL statements that have been created and stored in the database to perform a particular task. The stored procedure accepts input parameters and processes them and returns a single value such as a number or text value or a result set (set of rows).

```sql
delimiter //
create procedure credit_account(in p_account_id bigint, in p_amount numeric(12,2))
begin
  update accounts set balance = balance + p_amount where id = p_account_id;
  insert into account_ledger (account_id, amount, created_at)
  values (p_account_id, p_amount, current_timestamp);
end //
delimiter ;

call credit_account(42, 100.00);
```

Syntax differs by engine: Postgres uses `create function ... language plpgsql`, SQL Server uses `create procedure ... as begin ... end`. Trade-off: procedures keep logic close to the data and cut round trips, but they are harder to version, test, and review than SQL models in dbt or Spark; most modern data teams keep procedural logic for operational tasks only.

[Table of Contents](#SQL)

## What is a trigger?
A Trigger is a SQL procedure that initiates an action in response to an event (Insert, Delete or Update) occurs. When a new Employee is added to an Employee_Details table, new records will be created in the relevant tables such as Employee Payroll, Employee Time Sheet etc.,

[Table of Contents](#SQL)

## List out the acid properties and explain?
Following are the four properties of ACID. These guarantees that the database transactions are processed reliably.
+ Atomicity
+ Consistency
+ Isolation
+ Durability

```sql
begin;
update accounts set balance = balance - 100 where id = 1;
update accounts set balance = balance + 100 where id = 2;
commit;   -- both updates land, or rollback undoes both
```

- Atomic: all statements in the transaction take effect or none do.
- Consistent: constraints hold before and after, so the transfer cannot create or destroy money.
- Isolated: concurrent transactions do not see each other's uncommitted changes (isolation level controls how strict this is).
- Durable: once committed, the change survives a crash, usually because a write-ahead log was flushed first.

In practice isolation is the property teams relax for throughput; durability is the one you never relax for money movement.

[Table of Contents](#SQL)

## What is the difference between delete, truncate and drop command?
The difference between the Delete, Truncate and Drop command is:
Delete command is a DML command, it is used to delete rows from a table. It can be rolled back.
Truncate is a DDL command, it is used to delete all the rows from the table and free the space containing the table. It cant be rolled back.
Drop is a DDL command, it removes the complete data along with the table structure(unlike truncate command that removes only the rows). All the tables" rows, indexes, and privileges will also be removed.

```sql
delete from orders;      -- removes rows; table, indexes, and identity stay
truncate table orders;   -- removes all rows fast; resets identity in MySQL
drop table orders;       -- removes the table definition and its data
```

`delete` is DML and can be rolled back and filtered; `truncate` is DDL in most engines, cannot be filtered, fires no row triggers, and is not rollback-able in MySQL/Oracle; `drop` removes the object entirely and in most engines cannot be rolled back.

[Table of Contents](#SQL)

## What is the difference between having and where clause?
Where clause is used to fetch data from a database that specifies particular criteria whereas a Having clause is used along with "GROUP BY" to fetch data that meets particular criteria specified by the Aggregate functions. Where clause cannot be used with Aggregate functions, but the Having clause can.

```sql
-- where removes rows, having removes groups
select customer_id, sum(amount) as revenue
from orders
where status = 'completed'
group by customer_id
having sum(amount) > 1000
order by revenue desc;
```

The same rule applies in every warehouse. Note that Hive and older Spark SQL versions cannot always resolve a select-list alias inside `having`, so repeat the aggregate expression or wrap the query in a CTE.

[Table of Contents](#SQL)

## What are aggregate functions in sql?
SQL aggregate functions return a single value, calculated from values in a column.
Some aggregate functions in SQL are as follows:
+ AVG() : This function returns the average value
+ COUNT() : This function returns the number of rows
+ MAX() : This function returns the largest value
+ MIN() : This function returns the smallest value
+ ROUND() : This function rounds a numeric field to the number of decimals specified
+ SUM() : This function returns the sum

[Table of Contents](#SQL)

## What are string functions in sql?
SQL string functions are used primarily for string manipulation.
Some widely used SQL string functions are:
+ LEN() : It returns the length of the value in a text field
+ LOWER() : It converts character data to lower case
+ UPPER() : It converts character data to upper case
+ SUBSTRING() : It extracts characters from a text field
+ LTRIM() : It is to remove all whitespace from the beginning of the string
+ RTRIM() : It is to remove all whitespace at the end of the string
+ CONCAT() : Concatenate function combines multiple character strings together
+ REPLACE() :To update the content of a string.

[Table of Contents](#SQL)

## Explain the working of sql privileges?
SQL GRANT and REVOKE commands are used to implement privileges in SQL multiple user environments.  The administrator of the database can grant or revoke privileges to or from users of database object like SELECT, INSERT, UPDATE, DELETE, ALL etc.
GRANT Command: This command is used provide database access to user apart from an administrator.
Syntax: GRANT privilege_name
ON object_name
TO {user_name|PUBLIC|role_name}
[WITH GRANT OPTION];
In above syntax WITH GRANT OPTIONS indicates that the user can grant the access to another user too.
REVOKE Command: This command is used provide database deny or remove access to database objects.
Syntax: REVOKE privilege_name
ON object_name
FROM {user_name|PUBLIC|role_name};

[Table of Contents](#SQL)

## How many types of privileges are available in sql?
There are two types of privileges used in SQL, such as
System Privilege: System privileges deal with an object of a particular type and specifies the right to perform one or more actions on it which include Admin allows a user to perform administrative tasks, ALTER ANY INDEX, ALTER ANY CACHE GROUP CREATE/ALTER/DELETE TABLE, CREATE/ALTER/DELETE VIEW etc.
Object Privilege: This allows to perform actions on an object or object of another user(s) viz. table, view, indexes etc. Some of the object privileges are EXECUTE, INSERT, UPDATE, DELETE, SELECT, FLUSH, LOAD, INDEX, REFERENCES etc.

[Table of Contents](#SQL)

## What is sql injection?
SQL Injection is a type of database attack technique where malicious SQL statements are inserted into an entry field of database such that once it is executed the database is opened for an attacker. This technique is usually used for attacking Data-Driven Applications to have an access to sensitive data and perform administrative tasks on databases.

```python
# vulnerable: user input is concatenated into the SQL text
cursor.execute("select * from users where email = '" + email + "'")

# safe: a bound parameter travels separately from the SQL statement
cursor.execute("select * from users where email = %s", (email,))
```

Parameter binding is the only reliable defense; escaping and blacklists are not. Also:
- grant the application role the least privilege it needs, so an injected statement cannot read other tables;
- never build table or column names from user input (they cannot be parameterized) — validate them against an allowlist;
- use an ORM or query builder that binds parameters by default.

[Table of Contents](#SQL)

## What is the difference between clustered and non-clustered indexes?
One table can have only one clustered index but multiple nonclustered indexes.
Clustered indexes can be read rapidly rather than non-clustered indexes.
Clustered indexes store data physically in the table or view and non-clustered indexes do not store data in table as it has separate structure from data row

[Table of Contents](#SQL)

## What is relationship and how many types of relationship are there?
The relationship can be defined as the connection between more than one tables in the database.
There are 4 types of relationships:
+ One to One Relationship
+ Many to One Relationship
+ Many to Many Relationship
+ One to Many Relationship

[Table of Contents](#SQL)

## What is collation?
Collation is set of rules that check how the data is sorted by comparing it. Such as Character data is stored using correct character sequence along with case sensitivity, type, and accent.

[Table of Contents](#SQL)

## What is database white box testing and black box testing?
+ Database White Box Testing involves:
+ + Database Consistency and ACID properties
+ + Database triggers and logical views
+ + Decision Coverage, Condition Coverage, and Statement Coverage
+ + Database Tables, Data Model, and Database Schema
+ + Referential integrity rules
+ Database Black Box Testing involves:
+ + Data Mapping
+ + Data stored and retrieved
+ + Use of Black Box techniques such as Equivalence Partitioning and Boundary Value Analysis (BVA)

[Table of Contents](#SQL)

## What are the advantages of views?
Advantages of Views:
Views restrict access to the data because the view can display selective columns from the table.
Views can be used to make simple queries to retrieve the results of complicated queries. For example, views can be used to query information from multiple tables without the user knowing.

```sql
-- expose only non-sensitive columns to the analyst role
create view v_customers_public as
select customer_id, segment, country, created_at
from customers;     -- intentionally omits email and phone

grant select on v_customers_public to analyst;
```

Trade-off: views simplify access control and freeze a stable interface, so a schema change lands in one place. But deeply nested views hide the real work from the optimizer and can block predicate pushdown, which is why warehouses often flatten them into tables or materialized views.

[Table of Contents](#SQL)

## What is schema?
A schema is a collection of database objects of a User.

[Table of Contents](#SQL)

## What is the difference between sql and mysql?
SQL is a structured query language that is used for manipulating and accessing the relational database, on the other hand, MySQL itself is a relational database that uses SQL as the standard database language.

[Table of Contents](#SQL)

## What is sql sandbox in sql server?
SQL Sandbox is the safe place in SQL Server Environment where untrusted scripts are executed. There are 3 types of SQL sandbox, such as
Safe Access Sandbox: Here a user can perform SQL operations such as creating stored procedures, triggers etc. but cannot have access to the memory and cannot create files.
External Access Sandbox: User can have access to files without having a right to manipulate the memory allocation.
Unsafe Access Sandbox: This contains untrusted codes where a user can have access to memory.

[Table of Contents](#SQL)

## What are the steps to take to improve performance of a poor performing query?
Maximum use of indexes, stored procures should be done.
Avoid excessive use of complicated joins and cursors.
Avoid using conditional operators using columns of different tables.
Make use of computed columns and rewriting the query.

[Table of Contents](#SQL)

## What is a deadlock and what is a live lock?
Deadlock occur in interconnection n/w when group of process are unable to act because of waiting each other to release some resource.
live lock packets continue to move through n/w, but does not advance towards destination.

[Table of Contents](#SQL)

## What is blocking and how would you troubleshoot it?
Blocking occurs when two or more rows are locked by one SQL connection and a second connection to the SQL server requires a conflicting on lock on those rows. This results in the second connection to wait until the first lock is released.
Troubleshooting blocking:

SQL scripts can be written that constantly monitor the state of locking and blocking on SQL Server
The common blocking scenarios must be identified and resolved.
The scripts output must be checked constantly.
The SQL profilers data must be examined regularly to detect blocking.

[Table of Contents](#SQL)

## Explain the different types of backups available in sql server.
Complete database backup: This type of backup will backup all the information in the database. Used most commonly for disaster recovery and takes the longest time to backup.
Differential databse backup: The database is divided into partitions that have been modified since last complete backup. Most suitable for large databases. The most recent differential backup contains the changes from previous backups.
Transaction log backups: Backups only the changes logged in the transaction log. The transaction log has all changes logged about a database. Once the changes are accommodated on the database, the log is truncated or backed up.
File/File Group backups: used to recover individual files or file groups. Each filegroup can be individually backed up. This helps in recovery only the required file or filegroup for disaster recovery.

[Table of Contents](#SQL)

## What is database isolation in sql server?
Isolation in database defines how and when changes made by one transaction can be visible to other transactions. Different isolation levels are:
+ Serializable
+ Repeatable read
+ Read committed
+ Read uncommitted

SQL Server runs `read committed` by default. Two settings change the behavior:

```sql
alter database sales set allow_snapshot_isolation on;
alter database sales set read_committed_snapshot on;
```

Snapshot isolation stores row versions in `tempdb`, so readers do not block writers, but a heavy update workload can put pressure on `tempdb`. In an interview, contrast this with Postgres's MVCC default (`read committed`) and MySQL/InnoDB's `repeatable read`.

[Table of Contents](#SQL)

## What is a schema in sql server 2005? explain how to create a new schema in a database?
A schema is used to create database objects. It can be created using CREATE SCHEMA statement. The objects created can be moved between schemas. Multiple database users can share a single default schema.
CREATE SCHEMA sample;
Table creation
Create table sample.sampleinfo
{
id int primary key,
name varchar(20)
}

[Table of Contents](#SQL)

## Explain how to create a scrollable cursor with the scroll option.
Using the SCROLL keyword while declaring a cursor allows fetching of rows in any sequence.
Example:
DECLARE employee_curs SCROLL CURSOR FOR SELECT * FROM employee;
The active set of the cursor is stored can be accessed in any order without the need of opening and closing the cursor. The Scroll cursors can be set for select and function cursors but not insert or update statements.

[Table of Contents](#SQL)

## Explain how to create a dynamic cursor with the dynamic option?
When a cursor is declared as DYNAMIC, the cursor reflects all changes made to the base tables as the cursor is scrolled around.
Declare cursor_name cursor
[ STATIC | KEYSET | DYNAMIC | FAST_FORWARD ]
FOR select_statement
The dynamic option does not support ABSOLUTE FETCH.

[Table of Contents](#SQL)

## What are database files and filegroups?
Database files are used for mapping the database over some operating system files. Data and log information are separate. SQL server database has three types of database files:
+ Primary: starting point of a database. It also points to other files in database.
+ + Extension: .mdf
+ Secondary: All data files except primary data file is a part of secondary files.
+ + Extension: .ndf
+ Log files: All log information used to recover database.
+ + Extension: .ldf

[Table of Contents](#SQL)

## Describe in brief databases and sql server databases architecture.
SQL Server consists of a set of various components which fulfill data storage and data analysis needs for enterprise applications. Database architecture: All the data is stored in databases which is organized into logical components visible to the end users. It's only the administrator who needs to actually deal with the physical storage aspect of the databases, whereas users only deal with database tables.
Every SQL Server instance has primarily 4 system database i.e. master, model, tempdb and msdb. All other databases are user created databases as per their needs and requirements.
A single SQL Server instance is capable of handling thousands of users working on multiple databases.

[Table of Contents](#SQL)

## What are the steps to improve the performance of a query?
+ Number of joins and use of complex views/cursors have to be reduced.
+ The use of the stored procedures and indexes have to be maximized.
+ The optimized use of the complex conditional checks and computer columns have to be in place.
+ Tracking of performance analysis for the query helps us in identifying the right aspects to optimize.

```sql
-- before: a function on an indexed column blocks index use
select * from orders where year(order_date) = 2026;

-- after: a half-open range can use ix_orders_date
select * from orders
where order_date >= date '2026-01-01'
  and order_date <  date '2027-01-01';
```

Trade-off: `year(col) = 2026` reads every row, while the range reads only the relevant index slice and works on every engine. The same idea applies to `where date(created_at) = current_date` and to implicit casts such as comparing a `varchar` column to a number.

[Table of Contents](#SQL)

## How do you read a query plan with EXPLAIN?

```sql
explain (analyze, buffers)          -- PostgreSQL
select c.name, sum(o.amount) as revenue
from customers c
join orders o on o.customer_id = c.id
where o.order_date >= date '2026-01-01'
group by c.name;
```

Read the plan from the innermost node out. Look for a sequential scan where you expected an index scan, an estimated row count far from the actual count (stale statistics), and `Sort`/`Hash`/`Shuffle` nodes that spill to disk. Engine notes: Postgres uses `explain (analyze, buffers)`, MySQL uses `explain format=json` or `explain analyze`, BigQuery exposes the execution plan in the console, and Snowflake shows the Query Profile. The plan is the evidence; rewriting without it is guesswork.

[Table of Contents](#SQL)

## How would you use the sp_ functions to identify the blocking problems?
Blocking is the deadlock situation when two SQL connections race to obtain the control over the same set of rows in conflicting terms. This can be tracked by the status of WAIT present in the SP_LOCK procedure's output. All the active LOCKS and the different rows that are being involved are shown in this output. The identification of the connections involved in the specific row contention lock can be identified with sp_who and sp_who2 procedures. This way the causal agents of the blocking is identifies. KILL command issued against the specific SQL connection causing the BLOCK can resolve the issue. But the permanent solution lies in the proper design of the application code to execute in concurrence across different connections.

[Table of Contents](#SQL)

## What are the different types of backups?
The SQL server offers 4 types of backups to suit the need of the administrator.

+ Complete backup- The complete back up is just zipping the content of the entire database in terms of the different tables and procedures etc. This back up can server as an independent entity that can be restored in different systems with just the base SQL server installed.
+ Transaction log backup: This is the mechanism of backing up the transaction logs that have been maintained in the server. This way the details of the database getting updated is obtained. This cannot be a stand-alone back up mechanism. But can save a lot of time if we already have the file system related to the DB backed up on the new deployment server.
+ Differential backup: This is a subset of the complete backup, where only the modified datasets are backed up. This can save the time when we are just trying to maintain a backup server to main server.
+ File backup: This is the quickest way to take the backup of entire database. Instead of taking in the data actually stored in DB, the files are backed up and the file system thus obtained when combined with the transaction logs of the original system will render the database that we are trying to back up.

[Table of Contents](#SQL)

## What are the different levels of isolation?
The isolation represents the way of separating the database from the effects of network accesses, thereby maintaining the consistency. The different levels of isolation are:
+ read committed: This level of isolation uses the shared locks and the reads to the database give the constant and consistent values.
+ read uncommitted: No locks implemented. This is the least effective isolation level.
+ repeatable read: There are locks over the rows and values but the updates are maintained as a separate phantom row which is the next set of values for the specific record. Values can change within a specific transaction of a SQL function.
+ SERIALIZABLE reads: This is the implementation of pure lock mechanism where one specific transaction is not allowed access to specific record before another one completes.

[Table of Contents](#SQL)

## How can you start the sql server in the single user mode and the minimal configuration mode?
The SQLServer.exe is the executable which can be called in the command prompt with the parameters -m and -f. These are the options that will start the SQL server in the user mode and minimal configuration mode respectively.

[Table of Contents](#SQL)

## How can you know that statistics should be updated?
Statistics represent the uniqueness for the indexes that are being used for selecting the records. This can make the query execution pretty efficient. The tables that we are dealing with if truncated and repopulated, there is a good chance that the indexes and statistics are out of sync and this is when we have to update the statistics. There are also other situations like when the table has been modified and lot of rows have been added recently or like when a server has been updated with different version of software. These also give us the reason to use the UPDATE_STATISTICS, DBCC SHOW_STATISTICS etc to update it accordingly.

[Table of Contents](#SQL)

## What is replication in sql server?
Replication refers to the moving or copying of the database elements from one system to another. This can be done in the SQL Server in one of the following methods:
+ Transactional.
+ Snapshot.
+ Merge replication.

[Table of Contents](#SQL)

## Can we initiate a external com object from within sql?
Yes we can use the stored procedure sp_OACreate to initiate the external COM object from the T-SQL.

[Table of Contents](#SQL)

## What is a schema? how is it useful in sql servers?
The Schema refers to the overall structure of the database with all related information like users, access privileges, interaction information between the different tables etc. The CREATE SCHEMA is the command that can be used to create the schema in the SQL Server. This when done can be used to re deploy the same database in another system for demonstrative or test purposes. This holds intact the underlying framework over which the database has been built.

[Table of Contents](#SQL)

## What is write ahead log?
The write-ahead log is the logging system that just updates the buffer cache of the database for the transactions and updates the logs and only then the actual changes are incorporated in the actual database. This is the reason why it is called “write ahead”. This helps in maintaining the consistency in the database. This can also be useful in getting the actual database values even in case of failures.

[Table of Contents](#SQL)

## What is the use of check points in the transaction logs?
The check points are restoration points that indicate the specific state of the database. When there is some failure in the database that is occurring before the next check point, the database can be reverted back to the previous check point and thus the database would still be consistent.

[Table of Contents](#SQL)

## What is a column with identity?
The column with a defined identity in turn means that there is an unique value that the system assigns to the specific column. This is similar to the AUTONumber property of the Access backend.

[Table of Contents](#SQL)

## What are scrollable cursors? how are they created?
The scrollable cursors are the ones that can get the entire set of rows as single entity, within which all the rows present can be accessed in any order without the open/close of cursor done for every row access. The scrollable cursors are created with the keyword SCROLL added to the CREATE Cursor statements. The scrollable cursors are useful for the access of information from different rows but not for the delete/insert of new rows.

[Table of Contents](#SQL)

## What is raid and how does it help storage of databases?
The RAID stands for Redundant Array of Independent Disks. With its own RAID controllers, the RAID implements a fail-safe storage mechanism with its own backup mechanisms. There are different configurations of the RAID that all give us the ACID properties of storage along with other such facilities. This kind of storage will make the SQL Server database to be failsafe and stable. This can sometimes mean that the backup mechanisms and other such reliability measures can be taken off from the SQL Server level of operations.

[Table of Contents](#SQL)

## How can you identify the version number of the sql server installed?
The global variable version has the build and version information for the SQL Server and the service packs.

[Table of Contents](#SQL)

## What is the use of cascade constraints?
cascading is used for maintaining referencial integrity rules, which says that foreign key attributes values should be either subset of primary key values or null.

```sql
create table order_items (
  order_id   bigint not null,
  product_id bigint not null,
  constraint fk_order foreign key (order_id)
    references orders(id) on delete cascade
);

delete from orders where id = 42;   -- removes its order_items rows too
```

Trade-off: `on delete cascade` keeps child tables consistent automatically but can delete far more than intended, so use it only when the child cannot exist without the parent. Many teams prefer `on delete restrict` plus an explicit, auditable cleanup job.

[Table of Contents](#SQL)

## What is the function of a odbc manager ?
The ODBC Manager manages all the data sources that exists in the system.

[Table of Contents](#SQL)

## What are the different types of indexes available in sql server?
“Clustered and Non-Clustered Indexes”. There are other types of Indexes such as Unique, XML, Spatial and Filtered Indexes.

```sql
create clustered index cx_orders on orders (id);
create nonclustered index ix_orders_customer on orders (customer_id);
create unique index ux_orders_number on orders (order_number);
create index ix_orders_open on orders (order_date) where status = 'open';  -- filtered
create columnstore index cci_orders on orders (order_date, amount);        -- analytics
```

Trade-off: B-tree indexes serve point lookups and ranges; columnstore indexes compress and scan well for analytics but are poor for single-row updates; filtered indexes are small but only help queries that repeat the same predicate.

[Table of Contents](#SQL)

## What is the difference between clustered and non-clustered index?
In a clustered index, the leaf level pages are the actual data pages of the table. When a clustered index is created on a table, the data pages are arranged accordingly based on the clustered index key. There can only be one Clustered index on a table.
In a Non-Clustered index, the leaf level pages does not contain data pages instread it contains pointers to the data pages. There can multiple non-clustered indexes on a single table.

```sql
-- MySQL/InnoDB: the primary key is the clustered index
create table orders (
  id          bigint primary key,        -- clustered
  customer_id bigint not null,
  key ix_customer (customer_id)          -- secondary index stores the primary key value
);
```

In InnoDB every secondary index stores the primary key value, so a long primary key inflates every other index. Prefer a compact surrogate key over a long natural key, and remember that a secondary-index lookup on InnoDB is really two lookups.

[Table of Contents](#SQL)

## What are the high-availability solutions in sql server?
Failover Clustering, Database Mirroring, Log Shipping and Replication are the High- Availability features available in SQL Server.

[Table of Contents](#SQL)

## What is denormalization and when would you go for it?
As the name indicates, denormalization is the reverse process of normalization. It's the controlled introduction of redundancy in to the database design. It helps improve the query performance as the number of joins could be reduced.

```sql
-- wide, pre-joined fact table optimized for scans
create table fact_order_lines as
select o.order_id,
       o.order_date,
       c.customer_id,
       c.segment,
       p.category,
       oi.quantity,
       oi.quantity * p.price as revenue
from orders o
join customers c  on c.customer_id = o.customer_id
join order_items oi on oi.order_id = o.order_id
join products p   on p.product_id = oi.product_id;
```

Denormalize when read performance or query simplicity matters more than write correctness and storage, and when the copy can be rebuilt from the source of truth. Keep the normalized tables authoritative and refresh the wide table from a pipeline.

[Table of Contents](#SQL)

## How do you implement one-to-one, one-to-many and many-to-many relationships while designing tables?
+ One-to-One relationship can be implemented as a single table and rarely as two tables with primary and foreign key relationships.
+ One-to-Many relationships are implemented by splitting the data into two tables with primary key and foreign key relationships.
+ Many-to-Many relationships are implemented using a junction table with the keys from both the tables forming the composite primary key of the junction table.

```sql
-- one-to-one: the child primary key is also the foreign key
create table user_profile (
  user_id    bigint primary key references users(id),
  bio        text,
  updated_at timestamp
);

-- one-to-many: the many side holds the foreign key
create table orders (
  id          bigint primary key,
  customer_id bigint not null references customers(id),
  amount      numeric(12,2) not null
);

-- many-to-many: a junction table with a composite primary key
create table order_products (
  order_id   bigint not null references orders(id),
  product_id bigint not null references products(id),
  quantity   int not null default 1,
  primary key (order_id, product_id)
);
```

Trade-off: the junction table's composite primary key prevents duplicate pairs for free; add an index on `product_id` as well if the relationship is queried from both directions.

[Table of Contents](#SQL)

## What is the difference between a primary key and a unique key?
Both primary key and unique enforce uniqueness of the column on which they are defined. But by default primary key creates a clustered index on the column, where are unique creates a nonclustered index by default. Another major difference is that, primary key doesn't allow NULLs, but unique key allows one NULL only.

[Table of Contents](#SQL)

## What are user defined datatypes and when you should go for them?
User defined datatypes let you extend the base SQL Server datatypes by providing a descriptive name, and format to the database. Take for example, in your database, there is a column called Flight_Num which appears in many tables. In all these tables it should be varchar(8). In this case you could create a user defined datatype called Flight_num_type of varchar(8) and use it across all your tables.

[Table of Contents](#SQL)

## What is bit datatype and what is the information that can be stored inside a bit column?
Bit datatype is used to store boolean information like 1 or 0 (true or false). Untill SQL Server 6.5 bit datatype could hold either a 1 or 0 and there was no support for NULL. But from SQL Server 7.0 onwards, bit datatype can represent a third state, which is NULL.

[Table of Contents](#SQL)

## Define candidate key and alternate key and composite key.
A candidate key is one that can identify each row of a table uniquely. Generally a candidate key becomes the primary key of the table. If the table has more than one candidate key, one of them will become the primary key, and the rest are called alternate keys.
A key formed by combining at least two or more columns is called composite key.

```sql
create table employees (
  employee_id bigint primary key,             -- the chosen candidate key
  email       varchar(255) unique not null,   -- candidate key -> alternate key
  first_name  varchar(100) not null,
  last_name   varchar(100) not null,
  constraint ux_name unique (first_name, last_name, email)   -- composite key
);
```

A candidate key is any minimal set of columns that uniquely identifies a row. The primary key is the candidate you choose; the other candidates are alternate keys. A composite key is a key made of more than one column, and it is often also the primary key of a junction table.

[Table of Contents](#SQL)

## What is a transaction and what are acid properties?
A transaction is a logical unit of work in which, all the steps must be performed or none. ACID stands for Atomicity, Consistency, Isolation, Durability. These are the properties of a transaction.

[Table of Contents](#SQL)

## Explain different isolation levels?
An isolation level determines the degree of isolation of data between concurrent transactions. The default SQL Server isolation level is Read Committed. Here are the other isolation levels (in the ascending order of isolation): Read Uncommitted, Read Committed, Repeatable Read, Serializable. See SQL Server books online for an explanation of the isolation levels. Be sure to read about SET TRANSACTION ISOLATION LEVEL, which lets you customize the isolation level at the connection level.
CREATE INDEX myIndex ON myTable(myColumn)

| Level | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| read uncommitted | yes | yes | yes |
| read committed | no | yes | yes |
| repeatable read | no | no | mostly prevented (InnoDB) |
| serializable | no | no | no |

```sql
begin transaction isolation level repeatable read;
select balance from accounts where id = 1;
-- another transaction commits an update here
select balance from accounts where id = 1;   -- same value: repeatable read
commit;
```

Trade-off: higher isolation prevents more anomalies but increases locking and retries. Postgres defaults to `read committed`, MySQL/InnoDB to `repeatable read`, and warehouses such as Snowflake and BigQuery give snapshot isolation without exposing the same knobs.

[Table of Contents](#SQL)

## What type of index will get created after executing the above statement?
Non-clustered index. Important thing to note: By default a clustered index gets created on the primary key, unless specified otherwise.

What's The Maximum Size Of A Row?
8060 bytes.

[Table of Contents](#SQL)

## Differences between active and active or active and passive cluster configurations?
+ Active/Active :
+ + It is the bassically use for the default nodes, Here first node will be default and second node will be named instance. Both node will be active.
+ + Its Move group from cluster administration is possible for both side.
+ + System performance will go down, if both resources are in one node.
+ Active/Passive :
+ + Its also basically use for nodes But in this case Only one Active node with default instance. No system performance degradation will be there for this case even if we switchover to the other node. Both have same configuration.

[Table of Contents](#SQL)

## What is lock escalation?
Lock escalation is the process of converting a lot of low level locks (like row locks, page locks) into higher level locks (like table locks). Every lock is a memory structure too many locks would mean, more memory being occupied by locks. To prevent this from happening, SQL Server escalates the many fine-grain locks to fewer coarse-grain locks. Lock escalation threshold was definable in SQL Server 6.5, but from SQL Server 7.0 onwards it's dynamically managed by SQL Server.

[Table of Contents](#SQL)

## What is the difference between delete table and truncate table commands?
DELETE TABLE is a logged operation, so the deletion of each row gets logged in the transaction log, which makes it slow. TRUNCATE TABLE also deletes all the rows in a table, but it won't log the deletion of each row, instead it logs the deallocation of the data pages of the table, which makes it faster. Of course, TRUNCATE TABLE can be rolled back.

[Table of Contents](#SQL)

## What are constraints?
Constraints enable the RDBMS enforce the integrity of the database automatically, without needing you to create triggers, rule or defaults.
Types of constraints: NOT NULL, CHECK, UNIQUE, PRIMARY KEY, FOREIGN KEY

[Table of Contents](#SQL)

## What is an index and what are the types of indexes and how many clustered indexes can be created on a table?
Indexes in SQL Server are similar to the indexes in books. They help SQL Server retrieve the data quicker.
Indexes are of two types. Clustered indexes and non-clustered indexes. When you craete a clustered index on a table, all the rows in the table are stored in the order of the clustered index key. So, there can be only one clustered index per table. Non-clustered indexes have their own storage separate from the table data storage. Non-clustered indexes are stored as B-tree structures (so do clustered indexes), with the leaf level nodes having the index key and it's row locater. The row located could be the RID or the Clustered index key, depending up on the absence or presence of clustered index on the table.
If you create an index on each column of a table, it improves the query performance, as the query optimizer can choose from all the existing indexes to come up with an efficient execution plan. At the same t ime, data modification operations (such as INSERT, UPDATE, DELETE) will become slow, as every time data changes in the table, all the indexes need to be updated. Another disadvantage is that, indexes need disk space, the more indexes you have, more disk space is used.

[Table of Contents](#SQL)

## How to restart sql server in single user mode and how to start sql server in minimal configuration mode?
SQL Server can be started from command line, using the SQLSERVR.EXE. This EXE has some very important parameters with which a DBA should be familiar with. -m is used for starting SQL Server in single user mode and -f is used to start the SQL Server in minimal confuguration mode.

[Table of Contents](#SQL)

## What are statistics under what circumstances they go out of date and how do you update them?
Statistics determine the selectivity of the indexes. If an indexed column has unique values then the selectivity of that index is more, as opposed to an index with non-unique values. Query optimizer uses these indexes in determining whether to choose an index or not while executing a query.
Some situations under which you should update statistics:

[Table of Contents](#SQL)

## If there is significant change in the key values in the index?
If a large amount of data in an indexed column has been added, changed, or removed (that is, if the distribution of key values has changed), or the table has been truncated using the TRUNCATE TABLE statement and then repopulated
Database is upgraded from a previous version
Look up SQL Server books online for the following commands: UPDATE STATISTICS, STATS_DATE, DBCC SHOW_STATISTICS, CREATE STATISTICS, DROP STATISTICS, sp_autostats, sp_createstats, sp_updatestats.

[Table of Contents](#SQL)

## What is database replication and what are the different types of replication you can set up in sql server?
Replication is the process of copying/moving data between databases on the same or different servers. SQL Server supports the following types of replication scenarios:
+ Snapshot replication
+ Transactional replication (with immediate updating subscribers, with queued updating subscribers)
+ Merge replication

[Table of Contents](#SQL)

## What are the components of physical database structure of oracle database?
Oracle database is comprised of three types of files. One or more datafiles, two are more redo log files, and one or more control files.

[Table of Contents](#SQL)

## What are the components of logical database structure of oracle database?
There are tablespaces and database's schema objects.

[Table of Contents](#SQL)

## What is a tablespace?
A database is divided into Logical Storage Unit called tablespaces. A tablespace is used to group related logical structures together.

[Table of Contents](#SQL)

## What is system tablespace and when is it created?
Every Oracle database contains a tablespace named SYSTEM, which is automatically created when the database is created. The SYSTEM tablespace always contains the data dictionary tables for the entire database.

[Table of Contents](#SQL)

## Explain the relationship among database and tablespace and data file.
Each databases logically divided into one or more tablespaces one or more data files are explicitly created for each tablespace.

[Table of Contents](#SQL)

## What is schema?
A schema is collection of database objects of a user.

[Table of Contents](#SQL)

## What are schema objects?
Schema objects are the logical structures that directly refer to the database's data. Schema objects include tables, views, sequences, synonyms, indexes, clusters, database triggers, procedures, functions packages and database links.

[Table of Contents](#SQL)

## Can objects of the same schema reside in different tablespaces?
Yes.

[Table of Contents](#SQL)

## Can a tablespace hold objects from different schemes?
Yes.

[Table of Contents](#SQL)

## What is oracle table?
A table is the basic unit of data storage in an Oracle database. The tables of a database hold all of the user accessible data. Table data is stored in rows and columns.

[Table of Contents](#SQL)

## What is an oracle view?
A view is a virtual table. Every view has a query attached to it. (The query is a SELECT statement that identifies the columns and rows of the table(s) the view uses.)

[Table of Contents](#SQL)

## What is partial backup?
A Partial Backup is any operating system backup short of a full backup, taken while the database is open or shut down.

[Table of Contents](#SQL)

## What is mirrored on line redo log?
A mirrored on-line redo log consists of copies of on-line redo log files physically located on separate disks, changes made to one member of the group are made to all members.

[Table of Contents](#SQL)

## What is full backup?
A full backup is an operating system backup of all data files, on-line redo log files and control file that constitute ORACLE database and the parameter.

[Table of Contents](#SQL)

## Can a view based on another view?
Yes.

[Table of Contents](#SQL)

## Can a tablespace hold objects from different schemes?
Yes.

[Table of Contents](#SQL)

## Can objects of the same schema reside in different tablespaces?
Yes.

[Table of Contents](#SQL)

## What is the use of control file?
When an instance of an ORACLE database is started, its control file is used to identify the database and redo log files that must be opened for database operation to proceed. It is also used in database recovery.

[Table of Contents](#SQL)

## Do view contain data?
Views do not contain or store data.

[Table of Contents](#SQL)

## What are the referential actions supported by foreign key integrity constraint?
UPDATE and DELETE Restrict - A referential integrity rule that disallows the update or deletion of referenced data.
DELETE Cascade - When a referenced row is deleted all associated dependent rows are deleted.

`on delete` and `on update` support `cascade`, `set null`, `set default`, `restrict`, and `no action`.

```sql
constraint fk_order foreign key (order_id)
  references orders(id) on delete cascade on update restrict
```

`restrict`/`no action` block the parent change, `cascade` propagates it, and `set null`/`set default` detach the child. The default is usually `no action`. Cascades are convenient but make it easy to delete a large subtree with one statement.

[Table of Contents](#SQL)

## What are the type of synonyms?
There are two types of Synonyms Private and Public.

[Table of Contents](#SQL)

## What is an index segment?
Each Index has an Index segment that stores all of its data.

[Table of Contents](#SQL)

## What are the different type of segments?
Data Segment, Index Segment, Rollback Segment and Temporary Segment.

[Table of Contents](#SQL)

## What are clusters?
Clusters are groups of one or more tables physically stores together to share common columns and are often used together.

[Table of Contents](#SQL)

## What is an integrity constrains?
An integrity constraint is a declarative way to define a business rule for a column of a table.

[Table of Contents](#SQL)

## What is an index?
An Index is an optional structure associated with a table to have direct access to rows, which can be created to increase the performance of data retrieval. Index can be created on one or more columns of a table.

```sql
create index ix_orders_customer_date
  on orders (customer_id, order_date desc);

-- covering index: the query can be answered from the index alone
create index ix_orders_covering
  on orders (customer_id, order_date) include (amount);
```

Trade-off: every index speeds reads on its leading columns and slows inserts, updates, and deletes while consuming storage. A composite index on `(customer_id, order_date)` also serves queries filtering on `customer_id` alone (leftmost prefix) but not queries filtering only on `order_date`.

[Table of Contents](#SQL)

## What is an extent?
An Extent is a specific number of contiguous data blocks, obtained in a single allocation, and used to store a specific type of information.

[Table of Contents](#SQL)

## What is a view?
A view is a virtual table. Every view has a Query attached to it. (The Query is a SELECT statement that identifies the columns and rows of the table(s) the view uses.)

[Table of Contents](#SQL)

## What is table?
A table is the basic unit of data storage in an ORACLE database. The tables of a database hold all of the user accessible data. Table data is stored in rows and columns.

[Table of Contents](#SQL)

## Can a view based on another view?
Yes.

[Table of Contents](#SQL)

## What are the advantages of views?
Provide an additional level of table security, by restricting access to a predetermined set of rows and columns of a table.
Hide data complexity.
Simplify commands for the user.
Present the data in a different perspective from that of the base table.
Store complex queries.

```sql
-- expose only non-sensitive columns to the analyst role
create view v_customers_public as
select customer_id, segment, country, created_at
from customers;     -- intentionally omits email and phone

grant select on v_customers_public to analyst;
```

Trade-off: views simplify access control and freeze a stable interface, so a schema change lands in one place. But deeply nested views hide the real work from the optimizer and can block predicate pushdown, which is why warehouses often flatten them into tables or materialized views.

[Table of Contents](#SQL)

## What is an oracle sequence?
A sequence generates a serial list of unique numbers for numerical columns of a database's tables.

[Table of Contents](#SQL)

## What is a synonym?
A synonym is an alias for a table, view, sequence or program unit.

[Table of Contents](#SQL)

## What are the types of synonyms?
There are two types of synonyms private and public.

[Table of Contents](#SQL)

## What is a private synonym?
Only its owner can access a private synonym.

[Table of Contents](#SQL)

## What is a public synonym?
Any database user can access a public synonym.

[Table of Contents](#SQL)

## What are synonyms used for?
Mask the real name and owner of an object.
Provide public access to an object
Provide location transparency for tables, views or program units of a remote database.
Simplify the SQL statements for database users.

[Table of Contents](#SQL)

## What is an oracle index?
An index is an optional structure associated with a table to have direct access to rows, which can be created to increase the performance of data retrieval. Index can be created on one or more columns of a table.

[Table of Contents](#SQL)

## How are the index updates?
Indexes are automatically maintained and used by Oracle. Changes to table data are automatically incorporated into all relevant indexes.

[Table of Contents](#SQL)

## What is rollback segment?
Database contains one or more Rollback Segments to temporarily store "undo" information.

[Table of Contents](#SQL)

## What are the characteristics of data files?
A data file can be associated with only one database. Once created a data file can't change size. One or more data files form a logical unit of database storage called a tablespace.

[Table of Contents](#SQL)

## How to define data block size?
A data block size is specified for each ORACLE database when the database is created. A database users and allocated free database space in ORACLE datablocks. Block size is specified in INIT.ORA file and can't be changed latter.

[Table of Contents](#SQL)

## What does a control file contain?
A Control file records the physical structure of the database. It contains the following information.
Database Name
Names and locations of a database's files and redolog files.
Time stamp of database creation.

[Table of Contents](#SQL)

## What is difference between unique constraint and primary key constraint?
A column defined as UNIQUE can contain Nulls while a column defined as PRIMARY KEY can't contain Nulls.

```sql
-- one primary key, many unique constraints
create table products (
  product_id bigint primary key,
  sku        varchar(64) unique not null,
  upc        varchar(14) unique
);
```

The practical differences are: primary key is the row identity used by foreign keys; unique constraints allow nulls; and a table can carry several unique constraints but only one primary key.

[Table of Contents](#SQL)

## What is index cluster?
A Cluster with an index on the Cluster Key.

[Table of Contents](#SQL)

## When does a transaction end?
When it is committed or Rollbacked.

[Table of Contents](#SQL)

## How does one create a new database?
One can create and modify Oracle databases using the Oracle "dbca" (Database Configuration Assistant) utility. The dbca utility is located in the $ORACLE_HOME/bin directory. The Oracle Universal Installer (oui) normally starts it after installing the database server software. One can also create databases manually using scripts. This option, however, is falling out of fashion, as it is quite involved and error prone. Look at this example for creating and Oracle 9i database:
CONNECT SYS AS SYSDBA
ALTER SYSTEM SET DB_CREATE_FILE_DEST="/u01/oradata/";
ALTER SYSTEM SET DB_CREATE_ONLINE_LOG_DEST_1="/u02/oradata/";
ALTER SYSTEM SET DB_CREATE_ONLINE_LOG_DEST_2="/u03/oradata/";
CREATE DATABASE;

[Table of Contents](#SQL)

## What database block size should I use?
Oracle recommends that your database block size match, or be multiples of your operating system block size. One can use smaller block sizes, but the performance cost is significant. Your choice should depend on the type of application you are running. If you have many small transactions as with OLTP, use a smaller block size. With fewer but larger transactions, as with a DSS application, use a larger block size. If you are using a volume manager, consider your "operating system block size" to be 8K. This is because volume manager products use 8K blocks (and this is not configurable).

[Table of Contents](#SQL)

## What are the different approaches used by optimizer in choosing an execution plan?
Rule-based and Cost-based.

[Table of Contents](#SQL)

## What does rollback do?
ROLLBACK retracts any of the changes resulting from the SQL statements in the transaction.

[Table of Contents](#SQL)

## What is cost based approach to optimization?
Considering available access paths and determining the most efficient execution plan based on statistics in the data dictionary for the tables accessed by the statement and their associated clusters and indexes.

[Table of Contents](#SQL)

## What does commit do?
COMMIT makes permanent changes resulting from all SQL statements in the transaction. The changes made by the SQL statements of a transaction become visible to other user sessions transactions that start only after transaction is committed.

[Table of Contents](#SQL)

## Define transaction?
A Transaction is a logical unit of work that comprises one or more SQL statements executed by a single user.

```sql
begin;
insert into orders (id, customer_id, amount, status) values (1, 42, 99.00, 'new');
insert into order_events (order_id, event) values (1, 'created');
commit;
```

A transaction is a unit of work that is atomic, consistent, isolated, and durable. Wrap all writes that must succeed or fail together; in MySQL use InnoDB, because MyISAM does not support transactions at all.

[Table of Contents](#SQL)

## What is read only transaction?
A Read-Only transaction ensures that the results of each query executed in the transaction are consistent with respect to the same point in time.

[Table of Contents](#SQL)

## What is a deadlock?
Two processes wating to update the rows of a table which are locked by the other process then deadlock arises. In a database environment this will often happen because of not issuing proper row lock commands. Poor design of front-end application may cause this situation and the performance of server will reduce drastically.
These locks will be released automatically when a commit/rollback operation performed or any one of this processes being killed externally.

[Table of Contents](#SQL)

## What is a schema?
The set of objects owned by user account is called the schema.

[Table of Contents](#SQL)

## What is a cluster key?
The related columns of the tables are called the cluster key. The cluster key is indexed using a cluster index and its value is stored only once for multiple tables in the cluster.

[Table of Contents](#SQL)

## What is parallel server?
Multiple instances accessing the same database (Only In Multi-CPU environments).

[Table of Contents](#SQL)

## What is cluster?
Group of tables physically stored together because they share common columns and are often used together is called Cluster.

[Table of Contents](#SQL)

## What is an index and how it is implemented in oracle database?
An index is a database structure used by the server to have direct access of a row in a table. An index is automatically created when a unique of primary key constraint clause is specified in create table comman (Ver 7.0)

[Table of Contents](#SQL)

## What is a database instance?
A database instance (Server) is a set of memory structure and background processes that access a set of database files.The process can be shared by all users. The memory structure that are used to store most queried data from database. This helps up to improve database performance by decreasing the amount of I/O performed against data file.

[Table of Contents](#SQL)

## What is the use of analyze command?
To perform one of these function on an index,table, or cluster:
+ To collect statistics about object used by the optimizer and store them in the data dictionary.
+ To delete statistics about the object used by object from the data dictionary.
+ To validate the structure of the object.
+ To identify migrated and chained rows of the table or cluster.

[Table of Contents](#SQL)

## What is default tablespace?
The Tablespace to contain schema objects created without specifying a tablespace name.

[Table of Contents](#SQL)

## What are the system resources that can be controlled through profile?
The number of concurrent sessions the user can establish the CPU processing time available to the user's session.
The CPU processing time available to a single call to ORACLE made by a SQL statement.
The amount of logical I/O available to the user's session.
The amout of logical I/O available to a single call to ORACLE made by a SQL statement.
The allowed amount of idle time for the user's session.
The allowed amount of connect time for the user's session.

[Table of Contents](#SQL)

## What is tablespace quota?
The collective amount of disk space available to the objects in a schema on a particular tablespace.

[Table of Contents](#SQL)

## What are the different levels of auditing?
Statement Auditing, Privilege Auditing and Object Auditing.

[Table of Contents](#SQL)

## What is statement auditing?
Statement auditing is the auditing of the powerful system privileges without regard to specifically named objects.

[Table of Contents](#SQL)

## What are the database administrators utilities available?
+ SQL * DBA - This allows DBA to monitor and control an ORACLE database.
+ SQL * Loader - It loads data from standard operating system files (Flat files) into ORACLE database tables. Export (EXP) and Import (imp) utilities allow you to move existing data in ORACLE format to and from ORACLE database.

[Table of Contents](#SQL)

## How can you enable automatic archiving?
Shut the database
Backup the database
Modify/Include LOG_ARCHIVE_START_TRUE in init.ora file.
Start up the database.

[Table of Contents](#SQL)

## What are roles and how can we implement roles?
Roles are the easiest way to grant and manage common privileges needed by different groups of database users. Creating roles and assigning provides to roles. Assign each role to group of users. This will simplify the job of assigning privileges to individual users.

[Table of Contents](#SQL)

## What are roles?
Roles are named groups of related privileges that are granted to users or other roles.

[Table of Contents](#SQL)

## What are the uses of roles?
+ REDUCED GRANTING OF PRIVILEGES - Rather than explicitly granting the same set of privileges to many users a database administrator can grant the privileges for a group of related user's granted to a role and then grant only the role to each member of the group.
+ DYNAMIC PRIVILEGE MANAGEMENT - When the privileges of a group must change, only the privileges of the role need to be modified. The security domains of all users granted the group's role automatically reflect the changes made to the role.
+ SELECTIVE AVAILABILITY OF PRIVILEGES - The roles granted to a user can be selectively enable (available for use) or disabled (not available for use). This allows specific control of a user's privileges in any given situation.
+ APPLICATION AWARENESS - A database application can be designed to automatically enable and disable selective roles when a user attempts to use the application.

[Table of Contents](#SQL)

## What is privilege auditing?
Privilege auditing is the auditing of the use of powerful system privileges without regard to specifically named objects.

[Table of Contents](#SQL)

## What is object auditing?
Object auditing is the auditing of accesses to specific schema objects without regard to user.

[Table of Contents](#SQL)

## What is auditing?
Monitoring of user access to aid in the investigation of database use.

[Table of Contents](#SQL)

## Where are my tempfiles?
Tempfiles, unlike normal datafiles, are not listed in v$datafile or dba_data_files. Instead query v$tempfile or dba_temp_files:
SELECT * FROM v$tempfile;
SELECT * FROM dba_temp_files;

[Table of Contents](#SQL)

## How do I find used or free space in a temporary tablespace?
Unlike normal tablespaces, true temporary tablespace information is not listed in DBA_FREE_SPACE. Instead use the V$TEMP_SPACE_HEADER view:
SELECT tablespace_name, SUM (bytes used), SUM (bytes free)
FROM V$temp_space_header
GROUP BY tablespace_name;

[Table of Contents](#SQL)

## What is a profile?
Each database user is assigned a Profile that specifies limitations on various system resources available to the user.

[Table of Contents](#SQL)

## How will you enforce security using stored procedures?
Don't grant user access directly to tables within the application. Instead grant the ability to access the procedures that access the tables. When procedure executed it will execute the privilege of procedures owner. Users cannot access tables except via the procedure.

[Table of Contents](#SQL)

## How does one get the view definition of fixed views or tables?
Query v$fixed_view_definition.
Example: SELECT * FROM v$fixed_view_definition WHERE view_name="V$SESSION";

[Table of Contents](#SQL)

## What are the dictionary tables used to monitor a database spaces?
+ DBA_FREE_SPACE
+ DBA_SEGMENTS
+ DBA_DATA_FILES.

[Table of Contents](#SQL)

## What is user account in oracle database?
A user account is not a physical structure in Database but it is having important relationship to the objects in the database and will be having certain privileges.

[Table of Contents](#SQL)

## What is dynamic data replication?
Updating or Inserting records in remote database through database triggers. It may fail if remote database is having any problem.

[Table of Contents](#SQL)

## What is two phase commit?
Two-phase commit is mechanism that guarantees a distributed transaction either commits on all involved nodes or rolls back on all involved nodes to maintain data consistency across the global distributed database. It has two phase, a Prepare Phase and a Commit Phase.

[Table of Contents](#SQL)

## How can you enforce referential integrity in snapshots?
Time the references to occur when master tables are not in use. Peform the reference manually immediately locking the master tables. We can join tables in snapshots by creating a complex snapshots that will be based on the master tables.

[Table of Contents](#SQL)

## What is a snapshot?
Snapshots are read-only copies of a master table located on a remote node which is periodically refreshed to reflect changes made to the master table.

[Table of Contents](#SQL)

## What is the mechanism provided by oracle for table replication?
Snapshots and SNAPSHOT LOGs.

[Table of Contents](#SQL)

## What are the various type of snapshots?
Simple and Complex.

[Table of Contents](#SQL)

## Describe two phases of two phase commit?
+ Prepare phase - The global coordinator (initiating node) ask a participants to prepare (to promise to commit or rollback the transaction, even if there is a failure.
+ Commit Phase - If all participants respond to the coordinator that they are prepared, the coordinator asks all nodes to commit the transaction, if all participants cannot prepare, the coordinator asks all nodes to roll back the transaction.

[Table of Contents](#SQL)

## What is snapshot log?
It is a table that maintains a record of modifications to the master table in a snapshot. It is stored in the same database as master table and is only available for simple snapshots. It should be created before creating snapshots.

[Table of Contents](#SQL)

## What are the benefits of distributed options in databases?
Database on other servers can be updated and those transactions can be grouped together with others in a logical unit.
Database uses a two phase commit.

[Table of Contents](#SQL)

## What are the options available to refresh snapshots?
+ COMPLETE - Tables are completely regenerated using the snapshots query and the master tables every time the snapshot referenced.
+ FAST - If simple snapshot used then a snapshot log can be used to send the changes to the snapshot tables.
+ FORCE - Default value. If possible it performs a FAST refresh; Otherwise it will perform a complete refresh.

[Table of Contents](#SQL)

## What is a snapshot log?
A snapshot log is a table in the master database that is associated with the master table. ORACLE uses a snapshot log to track the rows that have been updated in the master table. Snapshot logs are used in updating the snapshots based on the master table.

[Table of Contents](#SQL)

## What is distributed database?
A distributed database is a network of databases managed by multiple database servers that appears to a user as single logical database. The data of all databases in the distributed database can be simultaneously accessed and modified.

[Table of Contents](#SQL)

## How can we reduce the network traffic?
+ Replication of data in distributed environment.
+ Using snapshots to replicate data.
+ Using remote procedure calls.

[Table of Contents](#SQL)

## Differentiate simple and complex and snapshots?
+ A simple snapshot is based on a query that does not contains GROUP BY clauses, CONNECT BY clauses, JOINs, sub-query or snashot of operations.
+ A complex snapshots contain atleast any one of the above.

[Table of Contents](#SQL)

## What are the built-ins used for sending parameters to forms?
You can pass parameter values to a form when an application executes the call_form, New_form, Open_form or Run_product.

[Table of Contents](#SQL)

## Can You Have More Than One Content Canvas View Attached With A Window?
Yes. Each window you create must have atleast one content canvas view assigned to it. You can also create a window that has manipulated content canvas view. At run time only one of the content canvas views assign to a window is displayed at a time.

[Table of Contents](#SQL)

## Is the after report trigger fired if the report execution fails?
Yes.

[Table of Contents](#SQL)

## Does a before form trigger fire when the parameter form is suppressed?
Yes.

[Table of Contents](#SQL)

## What is sga?
The System Global Area in an Oracle database is the area in memory to facilitate the transfer of information between users. It holds the most recently requested structural information between users. It holds the most recently requested structural information about the database. The structure is database buffers, dictionary cache, redo log buffer and shared pool area.

[Table of Contents](#SQL)

## What is a shared pool?
The data dictionary cache is stored in an area in SGA called the shared pool. This will allow sharing of parsed SQL statements among concurrent users.

[Table of Contents](#SQL)

## What is mean by program global area?
It is area in memory that is used by a single Oracle user process.

[Table of Contents](#SQL)

## What is a data segment?
Data segment are the physical areas within a database block in which the data associated with tables and clusters are stored.

[Table of Contents](#SQL)

## What are the factors causing the reparsing of sql statements in sga?
Due to insufficient shared pool size.
Monitor the ratio of the reloads takes place while executing SQL statements. If the ratio is greater than 1 then increase the SHARED_POOL_SIZE.

[Table of Contents](#SQL)

## Does a view contain data?
Views do not contain or store data.

[Table of Contents](#SQL)

## What is trigger associated with the timer?
When-timer-expired.

[Table of Contents](#SQL)

## What are the triggers associated with image items?
When-image-activated fires, when the operators double clicks on an image item, when-image-pressed fires, when an operator clicks or double clicks on an image item.

[Table of Contents](#SQL)

## What are the different windows events activated at runtimes?
+ When_window_activated
+ When_window_closed
+ When_window_deactivated
+ When_window_resized

Within this triggers, you can examine the built in system variable system. event_window to determine the name of the window for which the trigger fired.

[Table of Contents](#SQL)

## When do you use data parameter type?
When the value of a data parameter being passed to a called product is always the name of the record group defined in the current form. Data parameters are used to pass data to produts invoked with the run_product built-in subprogram.

[Table of Contents](#SQL)

## What is difference between open_form and call_form?
when one form invokes another form by executing open_form the first form remains displayed, and operators can navigate between the forms as desired. when one form invokes another form by executing call_form, the called form is modal with respect to the calling form. That is, any windows that belong to the calling form are disabled, and operators cannot navigate to them until they first exit the called form.

[Table of Contents](#SQL)

## What is new_form built in?
When one form invokes another form by executing new_form oracle form exits the first form and releases its memory before loading the new form calling new form completely replace the first with the second. If there are changes pending in the first form, the operator will be prompted to save them before the new form is loaded.

[Table of Contents](#SQL)

## What is the difference when flex mode is mode on and when it is off?
When flex mode is on, reports automatically resizes the parent when the child is resized.

[Table of Contents](#SQL)

## What is the difference when confine mode is on and when it is off?
When confine mode is on, an object cannot be moved outside its parent in the layout.

[Table of Contents](#SQL)

## What are visual attributes?
Visual attributes are the font, color, pattern proprieties that you set for form and menu objects that appear in your application interface.

[Table of Contents](#SQL)

## What are the vbx controls?
Vbx control provide a simple method of building and enhancing user interfaces. The controls can use to obtain user inputs and display program outputs.vbx control where originally develop as extensions for the ms visual basic environments and include such items as sliders, rides and knobs.

[Table of Contents](#SQL)

## What is the use of transactional triggers?
Using transactional triggers we can control or modify the default functionality of the oracle forms.

[Table of Contents](#SQL)

## How do you create a new session while open a new form?
Using open_form built-in setting the session option Ex. Open_form("Stocks ",active,session). when invoke the mulitiple forms with open form and call_form in the same application, state whether the following are true/False

[Table of Contents](#SQL)

## What are the ways to monitor the performance of the report?
Use reports profile executable statement. Use SQL trace facility.

An Open Form Can Not Be Execute The Call_form Procedure If You Chain Of Called Forms Has Been Initiated By Another Open Form?
True.

[Table of Contents](#SQL)

## Explain about horizontal and vertical tool bar canvas views?
Tool bar canvas views are used to create tool bars for individual windows. Horizontal tool bars are display at the top of a window, just under its menu bar. Vertical Tool bars are displayed along the left side of a window

[Table of Contents](#SQL)

## What is the purpose of the product order option in the column property sheet?
To specify the order of individual group evaluation in a cross products.

[Table of Contents](#SQL)

## What is the use of image_zoom built-in?
To manipulate images in image items.

[Table of Contents](#SQL)

## What is a timer?
Timer is an "internal time clock" that you can programmatically create to perform an action each time the times.

[Table of Contents](#SQL)

## What are the two phases of block coordination?
There are two phases of block coordination: the clear phase and the population phase. During, the clear phase, Oracle Forms navigates internally to the detail block and flushes the obsolete detail records. During the population phase, Oracle Forms issues a SELECT statement to repopulate the detail block with detail records associated with the new master record. These operations are accomplished through the execution of triggers.

[Table of Contents](#SQL)

## What are most common types of complex master-detail relationships?
There are three most common types of complex master-detail relationships:
+ master with dependent details
+ master with independent details
+ detail with two masters

[Table of Contents](#SQL)

## What is a text list?
The text list style list item appears as a rectangular box which displays the fixed number of values. When the text list contains values that can not be displayed, a vertical scroll bar appears, allowing the operator to view and select undisplayed values.

[Table of Contents](#SQL)

## What is term?
The term is terminal definition file that describes the terminal form which you are using r20run.

[Table of Contents](#SQL)

## What is use of term?
The term file which key is correspond to which oracle report functions.

[Table of Contents](#SQL)

## What is pop list?
The pop list style list item appears initially as a single field (similar to a text item field). When the operator selects the list icon, a list of available choices appears.

[Table of Contents](#SQL)

## What is the maximum no. of chars the parameter can store?
The maximum no. of chars the parameter can store is only valid for char parameters, which can be upto 64K. No parameters default to 23Bytes and Date parameter default to 7Bytes.

[Table of Contents](#SQL)

## What are the default extensions of the files created by library module?
The default file extensions indicate the library module type and storage format .pll - pl/sql library module binary.

[Table of Contents](#SQL)

## How do you display console on a window?
The console includes the status line and message line, and is displayed at the bottom of the window to which it is assigned.To specify that the console should be displayed, set the console window form property to the name of any window in the form. To include the console, set console window to Null.

[Table of Contents](#SQL)

## What are the coordination properties in a master-detail relationship?
The coordination properties are
+ Deferred
+ Auto-Query
  These Properties determine when the population phase of block coordination should occur.

[Table of Contents](#SQL)

## What are the different parameter types?
+ Text Parameters
+ Data Parameters

[Table of Contents](#SQL)

## What are the types of calculated columns available?
Summary, Formula, Placeholder column.

[Table of Contents](#SQL)

## Explain about stacked canvas views?
Stacked canvas view is displayed in a window on top of, or "stacked" on the content canvas view assigned to that same window. Stacked canvas views obscure some part of the underlying content canvas view, and or often shown and hidden programmatically.

[Table of Contents](#SQL)

## What is the difference between show_editor and edit_textitem?
Show editor is the generic built-in which accepts any editor name and takes some input string and returns modified output string. Whereas the edit_textitem built-in needs the input focus to be in the text item before the built-in is executed.

[Table of Contents](#SQL)

## What are the different file extensions that are created by oracle reports?
Rep file and Rdf file.

[Table of Contents](#SQL)

## What is the basic data structure that is required for creating an lov?
Record Group.

[Table of Contents](#SQL)

## What is the maximum allowed length of record group column?
Record group column names cannot exceed 30 characters.

[Table of Contents](#SQL)

## Which parameter can be used to set read level consistency across multiple queries?
Read only.

[Table of Contents](#SQL)

## What are the different types of record groups?
+ Query Record Groups
+ NonQuery Record Groups
+ State Record Groups

[Table of Contents](#SQL)

## From which designation is it preferred to send the output to the printed?
Previewer.

[Table of Contents](#SQL)

## What is difference between post database commit and post-form commit?
Post-form commit fires once during the post and commit transactions process, after the database commit occurs. The post-form-commit trigger fires after inserts, updates and deletes have been posted to the database but before the transactions have been finalized in the issuing the command. The post-database-commit trigger fires after oracle forms issues the commit to finalized transactions.

[Table of Contents](#SQL)

## With which function of summary item is the compute at options required?
percentage of total functions.

[Table of Contents](#SQL)

## What are parameters?
Parameters provide a simple mechanism for defining and setting the values of inputs that are required by a form at startup. Form parameters are variables of type char,number,date that you define at design time.

[Table of Contents](#SQL)

## What are the three types of user exits available?
Oracle Precompiler exits, Oracle call interface, NonOracle user exits.

[Table of Contents](#SQL)

## How many windows in a form can have console?
Only one window in a form can display the console, and you cannot change the console assignment at runtime.

[Table of Contents](#SQL)

## Is it possible to modify an external query in a report which contains it?
No.

[Table of Contents](#SQL)

## Does a grouping done for objects in the layout editor affect the grouping done in the data model editor?
No.

[Table of Contents](#SQL)

## If a break order is set on a column would it affect columns which are under the column?
No.

[Table of Contents](#SQL)

## Can you pass data parameters to forms?
No.

[Table of Contents](#SQL)

## Is it possible to link two groups inside a cross products after the cross products group has been created?
No.

[Table of Contents](#SQL)

## What are the different modals of windows?
+ Modalless windows
+ Modal windows

[Table of Contents](#SQL)

## What are modal windows?
Modal windows are usually used as dialogs, and have restricted functionality compared to modelless windows. On some platforms for example operators cannot resize, scroll or iconify a modal window.

[Table of Contents](#SQL)

## What is the advantage of the library?
Libraries provide a convenient means of storing client-side program units and sharing them among multiple applications. Once you create a library, you can attach it to any other form, menu, or library modules. When you can call library program units from triggers menu items commands and user named routine, you write in the modules to which you have attach the library. When a library attaches another library, program units in the first library can reference program units in the attached library. Library support dynamic loading-that is library program units are loaded into an application only when needed. This can significantly reduce the run-time memory requirements of applications.

[Table of Contents](#SQL)

## What is lexical reference? how can it be created?
Lexical reference is place_holder for text that can be embedded in a sql statements. A lexical reference can be created using & before the column or parameter name.

[Table of Contents](#SQL)

## What is system.coordination_operation?
It represents the coordination causing event that occur on the master block in master-detail relation.

[Table of Contents](#SQL)

## What is synchronize?
It is a terminal screen with the internal state of the form. It updates the screen display to reflect the information that oracle forms has in its internal representation of the screen.

[Table of Contents](#SQL)

## What use of command line parameter cmd file?
It is a command line argument that allows you to specify a file that contain a set of arguments for r20run.

[Table of Contents](#SQL)

## What is a text_io package?
It allows you to read and write information to a file in the file system.

[Table of Contents](#SQL)

## What is forms_ddl?
Issues dynamic Sql statements at run time, including server side pl/SQl and DDL

[Table of Contents](#SQL)

## What are the built-ins used for processing rows?
+ Get_group_row_count(function)
+ Get_group_selection_count(function)
+ Get_group_selection(function)
+ Reset_group_selection(procedure)
+ Set_group_selection(procedure)
+ Unset_group_selection(procedure)

[Table of Contents](#SQL)

## What are the built-ins used for getting cell values?
+ GET_GROUP_CHAR_CELL (function)
+ GET_GROUPCELL(function)
+ GET_GROUP_NUMBET_CELL(function)

[Table of Contents](#SQL)

## At least how many set of data must a data model have before a data model can be based on it?
Four.

[Table of Contents](#SQL)

## To execute row from being displayed that still use column in the row which property can be used?
Format trigger.

[Table of Contents](#SQL)

## What is the remove on exit property?
For a modeless window, it determines whether oracle forms hides the window automatically when the operators navigates to an item in the another window.

[Table of Contents](#SQL)

## What is a difference between pre-select and pre-query?
Fires during to execute query and count query processing after oracle forms constructs the select statement to be issued, but before the statement is actually issued. The pre-query trigger fires just before oracle forms issues the select statement to the database after the operator as define the example records by entering the query criteria in enter query mode.Pre-query trigger fires before pre-select trigger.

[Table of Contents](#SQL)

## What are the built-ins used for finding object id function?
+ FIND_GROUP(function)
+ FIND_COLUMN(function)

[Table of Contents](#SQL)

## Any attempt to navigate programmatically to disabled form in a call_form stack is allowed?
False

[Table of Contents](#SQL)

## How can a break order be created on a column in an existing group? what are the various sub events a mouse double click event involves?
By dragging the column outside the group.

[Table of Contents](#SQL)

## What is the use of placeholder column? what are the various sub events a mouse double click event involves?
A placeholder column is used to hold calculated values at a specified place rather than allowing is to appear in the actual row where it has to appear.

[Table of Contents](#SQL)

## What are the built-ins used for creating and deleting groups?
+ CREATE-GROUP (function)
+ CREATE_GROUP_FROM_QUERY(function)
+ DELETE_GROUP(procedure)

[Table of Contents](#SQL)

## What are the different types of delete details we can establish in master-details?
+ Cascade
+ Isolate
+ Non-isolate

[Table of Contents](#SQL)

## Where is the external query executed at the client or the server?
At the server.

[Table of Contents](#SQL)

## Where is a procedure return in an external pl/sql library executed at the client or at the server?
At the client.

[Table of Contents](#SQL)

## What is coordination event?
Any event that makes a different record in the master block the current record is a coordination causing event.

[Table of Contents](#SQL)

## What is the difference between ole server & ole container?
An Ole server application creates ole Objects that are embedded or linked in ole Containers ex. Ole servers are ms_word & ms_excel. OLE containers provide a place to store, display and manipulate objects that are created by ole server applications. Ex. oracle forms is an example of an ole Container.

[Table of Contents](#SQL)

## What is an object group?
An object group is a container for a group of objects; you define an object group when you want to package related objects, so that you copy or reference them in other modules.

[Table of Contents](#SQL)

## What is the difference between the conventional and direct path loader?
The conventional path loader essentially loads the data by using standard INSERT statements. The direct path loader (DIRECT=TRUE) bypasses much of the logic involved with that, and loads directly into the Oracle data files.

[Table of Contents](#SQL)

## How does one load multi-line records?
One can create one logical record from multiple physical records using one of the following two clauses:
CONCATENATE: - use when SQL*Loader should combine the same number of physical records together to form one logical record.
CONTINUEIF - use if a condition indicates that multiple records should be treated as one. Eg. by having a "#" character in column 1.

[Table of Contents](#SQL)

## Why is where clause faster than group filter or format trigger?
Because, in a where clause the condition is applied during data retrieval then after retrieving the data.

[Table of Contents](#SQL)

## Difference between substr and instr?
INSTR (String1,String2(n,(m)),INSTR returns the position of the mth occurrence of the string 2 instring1. The search begins from nth position of string1.SUBSTR (String1 n,m)SUBSTR returns a character string of size m in string1, starting from nth position of string1.

```sql
select instr('data-engineering', '-')   as dash_pos,   -- 5
       substr('data-engineering', 6)    as suffix,     -- 'engineering'
       substr('data-engineering', 1, 4) as prefix;     -- 'data'
```

`instr` returns a position (0 when not found) and `substr` returns characters. Postgres spells them `position(... in ...)`/`strpos` and `substring`; BigQuery uses `strpos` and `substr`. Both are 1-based.

[Table of Contents](#SQL)

## What is rman?
Recovery Manager is a tool that manages the process of creating backups and also manages the process of restoring and recovering from them.

[Table of Contents](#SQL)

## What are two parts of procedure?
Procedure Specification and Procedure Body.

[Table of Contents](#SQL)

## What are the datatypes available in plsql?
Some scalar data types such as NUMBER, VARCHAR2, DATE, CHAR, LONG, BOOLEAN. Some composite data types such as RECORD & TABLE.

[Table of Contents](#SQL)

## What is overloading of procedures?
The Same procedure name is repeated with parameters of different datatypes and parameters in different positions, varying number of parameters is called overloading of procedures. e.g. DBMS_OUTPUT put_line

[Table of Contents](#SQL)

## What is master detail relationship?
A master detail relationship is an association between two base table blocks- a master block and a detail block. The relationship between the blocks reflects a primary key to foreign key relationship between the tables on which the blocks are based.

[Table of Contents](#SQL)

## How many number of columns a record group can have?
A record group can have an unlimited number of columns of type CHAR, LONG, NUMBER, or DATE provided that the total number of column does not exceed 64K.

[Table of Contents](#SQL)

## How do window functions help in data engineering SQL?
Window functions calculate values across related rows without collapsing the result set like `group by` does. They are useful for deduplication, latest-record selection, running totals, ranking, sessionization, and change detection.

Example: keep the latest event per user.

```sql
select user_id, event_type, event_time
from (
  select
    user_id,
    event_type,
    event_time,
    row_number() over (
      partition by user_id
      order by event_time desc
    ) as rn
  from events
) ranked
where rn = 1;
```

In interviews, explain the three parts: `partition by` defines the group, `order by` defines sequence inside the group, and the function (`row_number`, `lag`, `sum`, etc.) computes the value.

[Table of Contents](#SQL)

## How do you deduplicate data with SQL?
Deduplication usually means defining the business key, ordering duplicate records by trust or recency, and keeping one winner. Avoid `select distinct` unless every column must match exactly, because real duplicates often differ in ingestion time, source file, or metadata.

Example:

```sql
with ranked as (
  select
    *,
    row_number() over (
      partition by order_id
      order by updated_at desc, ingested_at desc
    ) as rn
  from raw_orders
)
select *
from ranked
where rn = 1;
```

For production pipelines, write rejected duplicates to an audit table or track duplicate counts as a data quality metric.

[Table of Contents](#SQL)

## How do you write incremental SQL models?
An incremental model processes only new or changed records instead of rebuilding the whole table. The model needs a reliable watermark, such as `updated_at`, ingestion timestamp, source offset, or partition date. The target is usually updated with `merge`, partition overwrite, or append-only inserts depending on the table design.

Example:

```sql
merge into analytics.orders as target
using (
  select *
  from staging.orders
  where updated_at > (
    select coalesce(max(updated_at), timestamp '1900-01-01')
    from analytics.orders
  )
) as source
on target.order_id = source.order_id
when matched then update set
  status = source.status,
  amount = source.amount,
  updated_at = source.updated_at
when not matched then insert (
  order_id, status, amount, updated_at
) values (
  source.order_id, source.status, source.amount, source.updated_at
);
```

The main risk is late-arriving data. Many teams use a lookback window, for example reprocess the last 2 or 7 days, then deduplicate by key.

[Table of Contents](#SQL)

## How do you optimize analytical SQL queries?
Start by reducing scanned data, then reducing shuffle/join work. Select only needed columns, filter early, use partition pruning, avoid exploding joins, and aggregate before joining when possible. Check the query plan to see whether the engine is scanning too much data or doing expensive repartitions.

Example improvement:

```sql
with daily_orders as (
  select customer_id, order_date, sum(amount) as revenue
  from fact_orders
  where order_date >= date '2026-01-01'
  group by customer_id, order_date
)
select c.customer_segment, d.order_date, sum(d.revenue) as revenue
from daily_orders d
join dim_customer c
  on d.customer_id = c.customer_id
group by c.customer_segment, d.order_date;
```

This aggregates the large fact table before joining to the dimension, which can be much cheaper than joining every raw order row first.

[Table of Contents](#SQL)

## Real world use cases for SQL

These scenarios show the full arc an interviewer wants: the business problem, the data volume, the table design, the query, and why that approach was chosen.

### 1. Daily revenue mart for a marketplace

Business context: finance needs a per-day, per-country revenue number by 07:00, and the number must reconcile with the payments ledger. Volume: 400 million orders, 3 billion order lines, 12 TB of raw data, one partition per day.

Design: `fact_order_lines` is partitioned by `order_date` and clustered by `country_code`; a small `dim_date` carries fiscal calendars; the mart is rebuilt incrementally for the last 2 days to absorb late-arriving refunds.

```sql
create table mart_daily_revenue as
select
  o.order_date,
  o.country_code,
  count(distinct o.order_id)              as orders,
  sum(oi.quantity * oi.unit_price)        as gross_revenue,
  sum(case when o.status = 'refunded'
           then -oi.quantity * oi.unit_price
           else oi.quantity * oi.unit_price end) as net_revenue
from fact_orders o
join fact_order_lines oi
  on oi.order_id = o.order_id
 and oi.order_date = o.order_date
where o.order_date between :run_date - interval '1 day' and :run_date
group by o.order_date, o.country_code;
```

Why this approach: the partition predicate prunes all but two days, so the daily job scans gigabytes instead of terabytes; `count(distinct order_id)` survives a join that multiplies order lines; and the explicit `case` keeps refunds negative instead of silently dropping them. Late-arriving data is handled by reprocessing a bounded window rather than by guessing.

### 2. Signup funnel and retention

Business context: the growth team wants conversion from landing to paid, and week-1 retention by signup cohort. Volume: 800 million clickstream events, 5 million users, 30 days of hot data.

Design: an `events` table partitioned by `event_date` with the user id in the clustering key; the funnel query counts distinct users per step rather than counting raw events.

```sql
with signups as (
  select user_id, min(event_date) as signup_date
  from events
  where event_name = 'signup'
  group by user_id
),
steps as (
  select
    e.user_id,
    s.signup_date,
    max(case when e.event_name = 'landing'      then 1 else 0 end) as saw_landing,
    max(case when e.event_name = 'trial_start'  then 1 else 0 end) as started_trial,
    max(case when e.event_name = 'purchase'     then 1 else 0 end) as purchased
  from events e
  join signups s on s.user_id = e.user_id
  where e.event_date >= date '2026-09-01'
  group by e.user_id, s.signup_date
)
select
  signup_date,
  count(*)                                        as signups,
  sum(saw_landing)                                as landed,
  sum(started_trial)                              as trials,
  sum(purchased)                                  as purchases,
  round(100.0 * sum(purchased) / count(*), 2)     as conversion_pct
from steps
group by signup_date
order by signup_date;
```

Why this approach: `max(case ...)` collapses each user's event history into one funnel row, so a user who triggers an event twice is counted once. Counting events instead of users is the classic funnel bug in interviews.

### 3. SCD2 history for a customer dimension

Business context: a warehouse must answer "what was this customer's segment on the date of the order?". Volume: 20 million customers, 300,000 attribute changes per day.

Design: `dim_customer_scd2` keeps one row per version with `valid_from`, `valid_to`, and `is_current`; a merge closes the old version and inserts the new one.

```sql
-- close the current version of changed customers
update dim_customer_scd2 as d
set valid_to = current_timestamp,
    is_current = false
where d.is_current
  and exists (
    select 1 from stg_customer_changes s
    where s.customer_id = d.customer_id
      and (s.segment <> d.segment or s.tier <> d.tier)
  );

-- insert the new versions
insert into dim_customer_scd2
  (customer_id, segment, tier, valid_from, valid_to, is_current)
select customer_id, segment, tier, current_timestamp, null, true
from stg_customer_changes;
```

Point-in-time join:

```sql
select o.order_id, o.order_date, c.segment
from fact_orders o
join dim_customer_scd2 c
  on c.customer_id = o.customer_id
 and o.order_date >= c.valid_from
 and o.order_date <  coalesce(c.valid_to, timestamp '9999-12-31');
```

Why this approach: an SCD2 join must be a range join on the validity window; joining on `customer_id` alone returns every historical version and multiplies the fact rows. A unique index on `(customer_id) where is_current` prevents two current rows per customer.

### 4. Deduplicating late-arriving events

Business context: mobile clients retry uploads, so the same event id can arrive up to 72 hours late and can arrive twice. Volume: 2 TB/day, 5% duplicate and late.

Design: land raw events append-only into `stg_events`, then deduplicate into `silver_events` by trust order: prefer the vendor's version, then the latest `ingested_at`.

```sql
insert into silver_events
select event_id, user_id, event_type, event_time, payload
from (
  select
    e.*,
    row_number() over (
      partition by event_id
      order by source_priority asc, ingested_at desc
    ) as rn
  from stg_events e
  where e.ingested_at >= current_timestamp - interval '72' hour
) ranked
where rn = 1;
```

Why this approach: `row_number` is deterministic because the ordering has a tiebreaker, and reprocessing a 72-hour window matches the late-arrival bound instead of rescanning all history. Writing reject counts to an audit table turns deduplication into a monitored data-quality metric.

### 5. Cohort retention by month

Business context: product wants the month-1, month-2, and month-3 retention of each signup cohort. Volume: 12 million users, 400 million activity rows.

Design: a `dim_user` table with `signup_month`, and `fact_activity` with one row per user per active month.

```sql
with activity as (
  select distinct
    u.signup_month,
    a.user_id,
    datediff(month, u.signup_date, a.activity_date) as month_number
  from fact_activity a
  join dim_user u on u.user_id = a.user_id
  where a.activity_date >= date '2026-01-01'
)
select
  signup_month,
  count(distinct case when month_number = 1 then user_id end) as month_1,
  count(distinct case when month_number = 2 then user_id end) as month_2,
  count(distinct case when month_number = 3 then user_id end) as month_3
from activity
group by signup_month
order by signup_month;
```

Why this approach: `datediff(month, ...)` creates the cohort index directly, and `count(distinct ...)` inside `case` returns each cohort's returning users without a self-join per period. Postgres and Snowflake both support `count(distinct ...) filter (where ...)`, which reads even cleaner.

### 6. Running balance and top-N per group in one report

Business context: operations wants each customer's running balance after every transaction, plus the three largest transactions per customer. Volume: 900 million ledger rows, queried for the last 90 days.

Design: `fact_ledger` is partitioned by `posting_date`; the report uses two window functions over the same scan.

```sql
with windowed as (
  select
    l.customer_id,
    l.posting_date,
    l.amount,
    sum(l.amount) over (
      partition by l.customer_id
      order by l.posting_date, l.ledger_id
      rows between unbounded preceding and current row
    ) as running_balance,
    row_number() over (
      partition by l.customer_id
      order by l.amount desc, l.ledger_id
    ) as amount_rank
  from fact_ledger l
  where l.posting_date >= current_date - interval '90' day
)
select
  customer_id,
  posting_date,
  amount,
  running_balance,
  case when amount_rank <= 3 then amount end as top3_amount
from windowed
order by customer_id, posting_date;
```

Why this approach: the explicit `rows between unbounded preceding and current row` frame makes the running total independent of ties in the ordering (the default `range` frame would include tied dates and produce a wrong balance). Both window functions share one scan of the partitioned range, which is why windowing beats a self-join per row here.

[Table of Contents](#SQL)
