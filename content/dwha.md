## [Main title](../README.md)
### [Interview questions](full.md)

# Data Warehousing Architecture

**Notebook:** [`notebooks/topics/dwha.ipynb`](../notebooks/topics/dwha.ipynb) - runnable version of this topic with self-checking exercises.

+ [What are the main layers in a data warehouse architecture?](#what-are-the-main-layers-in-a-data-warehouse-architecture)
+ [How do OLTP and OLAP systems differ?](#how-do-oltp-and-olap-systems-differ)
+ [What is the Main Difference between View and Materialized View?](#what-is-the-main-difference-between-view-and-materialized-view)
+ [What is Junk Dimension?](#what-is-junk-dimension)
+ [What is Data Warehouse architecture?](#what-is-data-warehouse-architecture)
+ [What is an integrity constraints and what are different types of integrity constraints?](#what-is-an-integrity-constraints-and-what-are-different-types-of-integrity-constraints)
+ [Why is that Data Architect actually monitor and enforce compliance data standards?](#why-is-that-data-architect-actually-monitor-and-enforce-compliance-data-standards)
+ [Explain the different data models that are available in detail?](#explain-the-different-data-models-that-are-available-in-detail)
+ [Differentiate between dimension and attribute?](#differentiate-between-dimension-and-attribute)
+ [Differentiate between Oltp and Olap?](#differentiate-between-oltp-and-olap)
+ [What is a Real time Data Warehouse and how is it different from near to Real time Data Warehouse?](#what-is-a-real-time-data-warehouse-and-how-is-it-different-from-near-to-real-time-data-warehouse)
+ [What is Type 2 Version Dimension?](#what-is-type-2-version-dimension)
+ [What are Data Modeling and Data Mining?](#what-are-data-modeling-and-data-mining)
+ [Where the Data Cube Technology is used?](#where-the-data-cube-technology-is-used)
+ [How can you implement many relations in Star Schema Model?](#how-can-you-implement-many-relations-in-star-schema-model)
+ [What is Critical Column?](#what-is-critical-column)
+ [What is the main difference between Star and Snowflake Star Schema and which one is better and why?](#what-is-the-main-difference-between-star-and-snowflake-star-schema-and-which-one-is-better-and-why)
+ [What is the difference between Dependent Data Warehouse and Independent Data Warehouse?](#what-is-the-difference-between-dependent-data-warehouse-and-independent-data-warehouse)
+ [Which technology should be used for interactive Data Querying across multiple dimensions for a decision making for a Dw?](#which-technology-should-be-used-for-interactive-data-querying-across-multiple-dimensions-for-a-decision-making-for-a-dw)
+ [What is Virtual Data Warehousing?](#what-is-virtual-data-warehousing)
+ [What is the difference between Metadata and Data Dictionary?](#what-is-the-difference-between-metadata-and-data-dictionary)
+ [What is the difference between Mapping Parameter and Mapping Variable in Data Warehousing?](#what-is-the-difference-between-mapping-parameter-and-mapping-variable-in-data-warehousing)
+ [Explain the advantages Of Raid 1 and 1/0 And 5 and what type of Raid setup would you put your Tx Logs.](#explain-the-advantages-of-raid-1-and-10-and-5-and-what-type-of-raid-setup-would-you-put-your-tx-logs)
+ [What are the characteristics of data files?](#what-are-the-characteristics-of-data-files)
+ [What is Rollback Segment?](#what-is-rollback-segment)
+ [What is a Table Space?](#what-is-a-table-space)
+ [What is Database Link?](#what-is-database-link)
+ [What is a Hash Cluster?](#what-is-a-hash-cluster)
+ [Describe referential Integrity?](#describe-referential-integrity)
+ [What is Schema?](#what-is-schema)
+ [What is Table?](#what-is-table)
+ [What is a View?](#what-is-a-view)
+ [What is an Extent?](#what-is-an-extent)
+ [What is an Index?](#what-is-an-index)
+ [What is an Integrity Constrains?](#what-is-an-integrity-constrains)
+ [What are Clusters?](#what-are-clusters)
+ [What are the different types of Segments?](#what-are-the-different-types-of-segments)
+ [Explain the Relationship among database and Table Space and Data File?](#explain-the-relationship-among-database-and-table-space-and-data-file)
+ [What is an Index Segment?](#what-is-an-index-segment)
+ [What are the Referential Actions supported by Foreign Key integrity constraint?](#what-are-the-referential-actions-supported-by-foreign-key-integrity-constraint)
+ [Do you View contain Data?](#do-you-view-contain-data)
+ [What is the use of Control File?](#what-is-the-use-of-control-file)
+ [Can Objects of the same Schema reside in different Table Spaces?](#can-objects-of-the-same-schema-reside-in-different-table-spaces)
+ [Can a Table Space hold objects from different Schemes?](#can-a-table-space-hold-objects-from-different-schemes)
+ [Can a View based on another View?](#can-a-view-based-on-another-view)
+ [What is a full Backup?](#what-is-a-full-backup)
+ [What is Mirrored on line redo Log?](#what-is-mirrored-on-line-redo-log)
+ [What is Partial Backup?](#what-is-partial-backup)
+ [What is Restricted Mode of Instance Startup?](#what-is-restricted-mode-of-instance-startup)
+ [What are the steps involved in Database Shutdown?](#what-are-the-steps-involved-in-database-shutdown)
+ [What are the advantages of Operating a Database in archivelog mode over operating it in no Archivelog Mode?](#what-are-the-advantages-of-operating-a-database-in-archivelog-mode-over-operating-it-in-no-archivelog-mode)
+ [What are the different modes of Mounting a Database with the Parallel Server?](#what-are-the-different-modes-of-mounting-a-database-with-the-parallel-server)
+ [Can Full Backup be performed when the Database is Open?](#can-full-backup-be-performed-when-the-database-is-open)
+ [What are the steps involved in instance Recovery?](#what-are-the-steps-involved-in-instance-recovery)
+ [What are the steps involved in Database Startup?](#what-are-the-steps-involved-in-database-startup)
+ [Which parameter specified in the Default Storage Clause of create Tablespace cannot be Altered after creating the Table Space?](#which-parameter-specified-in-the-default-storage-clause-of-create-tablespace-cannot-be-altered-after-creating-the-table-space)
+ [What is Online redo Log?](#what-is-online-redo-log)
+ [What is Log Switch?](#what-is-log-switch)
+ [What is Dimensional Modelling?](#what-is-dimensional-modelling)
+ [What are the difference between snow Flake and Star Schema and what are situations where Snow Flake Schema is better than Star Schema to use and when the opposite is True?](#what-are-the-difference-between-snow-flake-and-star-schema-and-what-are-situations-where-snow-flake-schema-is-better-than-star-schema-to-use-and-when-the-opposite-is-true)
+ [What is a Cube in Data Warehousing concept?](#what-is-a-cube-in-data-warehousing-concept)
+ [What are the differences between Star and Snowflake Schema?](#what-are-the-differences-between-star-and-snowflake-schema)
+ [What are Data Marts?](#what-are-data-marts)
+ [What is the Data Type of the Surrogate Key?](#what-is-the-data-type-of-the-surrogate-key)
+ [What are Fact and Dimension and Measure?](#what-are-fact-and-dimension-and-measure)
+ [What are the different Types of Data Warehousing?](#what-are-the-different-types-of-data-warehousing)
+ [What do you mean by Static and Local Variable?](#what-do-you-mean-by-static-and-local-variable)
+ [What is a Source Qualifier?](#what-is-a-source-qualifier)
+ [What are the Steps to Build the Data Warehouse?](#what-are-the-steps-to-build-the-data-warehouse)
+ [What is the advantages Data Mining over Traditional approaches?](#what-is-the-advantages-data-mining-over-traditional-approaches)
+ [What is the difference between View and Materialized View?](#what-is-the-difference-between-view-and-materialized-view)
+ [What is the main difference between Inmon and Kimball Philosophies of Data Warehousing?](#what-is-the-main-difference-between-inmon-and-kimball-philosophies-of-data-warehousing)
+ [What is Junk Dimension and what is the difference between Junk Dimension and Degenerated Dimension?](#what-is-junk-dimension-and-what-is-the-difference-between-junk-dimension-and-degenerated-dimension)
+ [Why Fact Table is in Normal Form?](#why-fact-table-is-in-normal-form)
+ [What is difference between Er Modeling and Dimensional Modeling?](#what-is-difference-between-er-modeling-and-dimensional-modeling)
+ [What is Conformed Fact?](#what-is-conformed-fact)
+ [What are the Methodologies of Data Warehousing?](#what-are-the-methodologies-of-data-warehousing)
+ [What is Bus Schema?](#what-is-bus-schema)
+ [What is Data Warehousing Hierarchy?](#what-is-data-warehousing-hierarchy)
+ [What are Data Validation Strategies for Data Mart Validation after loading process?](#what-are-data-validation-strategies-for-data-mart-validation-after-loading-process)
+ [What are the Data Types present in Bo and what happens if we implement View in the Designer N Report?](#what-are-the-data-types-present-in-bo-and-what-happens-if-we-implement-view-in-the-designer-n-report)
+ [What is Surrogate Key and where we use it?](#what-is-surrogate-key-and-where-we-use-it)
+ [What is a Linked Cube?](#what-is-a-linked-cube)
+ [What is meant by Metadata in Context of a Data Warehouse and how it is important?](#what-is-meant-by-metadata-in-context-of-a-data-warehouse-and-how-it-is-important)
+ [What are the possible Data Marts in Retail Sales?](#what-are-the-possible-data-marts-in-retail-sales)
+ [What are the various Etl Tools in the market?](#what-are-the-various-etl-tools-in-the-market)
+ [What is Dimensional Modeling?](#what-is-dimensional-modeling)
+ [What is Vldb?](#what-is-vldb)
+ [What is Degenerate Dimension Table?](#what-is-degenerate-dimension-table)
+ [What is Er Diagram?](#what-is-er-diagram)
+ [What is the difference between Snowflake and Star Schema and what are situations where Snowflake Schema is better than Star Schema?](#what-is-the-difference-between-snowflake-and-star-schema-and-what-are-situations-where-snowflake-schema-is-better-than-star-schema)
+ [Can a Dimension Table contain numeric values?](#can-a-dimension-table-contain-numeric-values)
+ [What is Hybrid Slowly Changing Dimension?](#what-is-hybrid-slowly-changing-dimension)
+ [How many clustered indexes can you create for a table in Dwh and in case Of Truncate and Delete command what happens to table which has unique Id.](#how-many-clustered-indexes-can-you-create-for-a-table-in-dwh-and-in-case-of-truncate-and-delete-command-what-happens-to-table-which-has-unique-id)
+ [What is Loop in Data Warehousing?](#what-is-loop-in-data-warehousing)
+ [What is an Error Log Table in Informatica occurs and how to maintain it in mapping?](#what-is-an-error-log-table-in-informatica-occurs-and-how-to-maintain-it-in-mapping)
+ [What is Drilling Across?](#what-is-drilling-across)
+ [Where the Cache Files stored?](#where-the-cache-files-stored)
+ [What is Dimension Modeling?](#what-is-dimension-modeling)
+ [What is Data Cleaning?](#what-is-data-cleaning)
+ [Can you explain the Hierarchies Level Data Warehousing?](#can-you-explain-the-hierarchies-level-data-warehousing)
+ [Can you explain about Core Dimension and Balanced Dimension and Dirty Dimension?](#can-you-explain-about-core-dimension-and-balanced-dimension-and-dirty-dimension)
+ [What is Core Dimension?](#what-is-core-dimension)
+ [After we create a Scd Table can we use that Particular Dimension as a Dimension Table for Star Schema?](#after-we-create-a-scd-table-can-we-use-that-particular-dimension-as-a-dimension-table-for-star-schema)
+ [Suppose you are filtering rows using a Filter Transformation and only rows meet the condition pass to the Target so tell me where rows will go that does not meet condition.](#suppose-you-are-filtering-rows-using-a-filter-transformation-and-only-rows-meet-the-condition-pass-to-the-target-so-tell-me-where-rows-will-go-that-does-not-meet-condition)
+ [What is Galaxy Schema?](#what-is-galaxy-schema)
+ [Briefly state different between Data Ware House and Data Mart?](#briefly-state-different-between-data-ware-house-and-data-mart)
+ [What is MetaData?](#what-is-metadata)
+ [What is the Definitions for Datawarehose And Datamart?](#what-is-the-definitions-for-datawarehose-and-datamart)
+ [What is Data Validation Strategies for Data Mart validation after Loading Process](#what-is-data-validation-strategies-for-data-mart-validation-after-loading-process)
+ [What is Data Mining?](#what-is-data-mining)
+ [What is Ods?](#what-is-ods)
+ [What is Etl?](#what-is-etl)
+ [Is Oltp Database is design optimal for Data Warehouse?](#is-oltp-database-is-design-optimal-for-data-warehouse)
+ [If Denormalized is improves Data Warehouse Processes and why Fact Table is in Normal Form?](#if-denormalized-is-improves-data-warehouse-processes-and-why-fact-table-is-in-normal-form)
+ [What are Lookup Tables?](#what-are-lookup-tables)
+ [What are Aggregate Tables?](#what-are-aggregate-tables)
+ [What is real time Datawarehousing?](#what-is-real-time-datawarehousing)
+ [What are Conformed Dimensions?](#what-are-conformed-dimensions)
+ [How do you load the Time Dimension?](#how-do-you-load-the-time-dimension)
+ [What is a Level of Granularity of a Fact Table?](#what-is-a-level-of-granularity-of-a-fact-table)
+ [What are Non additive facts?](#what-are-non-additive-facts)
+ [What is Factless Facts Table?](#what-is-factless-facts-table)
+ [Explain about Olap?](#explain-about-olap)
+ [Explain about the Functionality of Olap?](#explain-about-the-functionality-of-olap)
+ [Explain about Molap?](#explain-about-molap)
+ [Explain about Rolap?](#explain-about-rolap)
+ [Explain about Aggregations?](#explain-about-aggregations)
+ [Explain about the View Selection problem?](#explain-about-the-view-selection-problem)
+ [Explain about the role of Bitmap Indexes to solve Aggregation Problems?](#explain-about-the-role-of-bitmap-indexes-to-solve-aggregation-problems)
+ [Explain about Encoding Technique used in Bitmaps Indexes?](#explain-about-encoding-technique-used-in-bitmaps-indexes)
+ [Explain about Binning?](#explain-about-binning)
+ [Explain about Hybrid Olap?](#explain-about-hybrid-olap)
+ [Explain about Shared Features of Olap?](#explain-about-shared-features-of-olap)
+ [Explain about Analysis?](#explain-about-analysis)
+ [Explain about Multidimensional Features present in Olap?](#explain-about-multidimensional-features-present-in-olap)
+ [Explain about the Database Marketing Application of Olap?](#explain-about-the-database-marketing-application-of-olap)
+ [Compare Data Warehouse Database and Oltp Database.](#compare-data-warehouse-database-and-oltp-database)
+ [What is the difference between Etl Tool and Olap Tool and what are various Etl in the Market?](#what-is-the-difference-between-etl-tool-and-olap-tool-and-what-are-various-etl-in-the-market)
+ [Steps in building the Data Model.](#steps-in-building-the-data-model)
+ [Why is Data Modeling important?](#why-is-data-modeling-important)
+ [What Type of Indexing Mechanism do we need use for a typical Datawarehouse?](#what-type-of-indexing-mechanism-do-we-need-use-for-a-typical-datawarehouse)
+ [What are Semi additive and Factless Facts?](#what-are-semi-additive-and-factless-facts)
+ [Is it correct develop a Data Mart using an Ods?](#is-it-correct-develop-a-data-mart-using-an-ods)
+ [Explain degenerated dimension.](#explain-degenerated-dimension)
+ [What are the different methods of loading Dimension Tables?](#what-are-the-different-methods-of-loading-dimension-tables)
+ [What are Slowly Changing Dimensions?](#what-are-slowly-changing-dimensions)
+ [What is meant by Metadata in context of a Datawarehouse?](#what-is-meant-by-metadata-in-context-of-a-datawarehouse)
+ [What are Modeling Tools available in the Market](#what-are-modeling-tools-available-in-the-market)
+ [What is the main difference between Schema in Rdbms and Schemas in Datawarehouse?](#what-is-the-main-difference-between-schema-in-rdbms-and-schemas-in-datawarehouse)
+ [What is a general purpose Scheduling Tool?](#what-is-a-general-purpose-scheduling-tool)
+ [What is the need of Surrogate Key and why Primary Key not used as Surrogate Key?](#what-is-the-need-of-surrogate-key-and-why-primary-key-not-used-as-surrogate-key)
+ [What is Snow Flake Schema?](#what-is-snow-flake-schema)
+ [What is the difference between Oltp and Olap?](#what-is-the-difference-between-oltp-and-olap)
+ [How are the Dimension Tables designed?](#how-are-the-dimension-tables-designed)
+ [What are the advantages Data Mining over traditional approaches?](#what-are-the-advantages-data-mining-over-traditional-approaches)
+ [Which automation tool is used in Data Warehouse testing?](#which-automation-tool-is-used-in-data-warehouse-testing)
+ [Give examples of Degenerated Dimensions.](#give-examples-of-degenerated-dimensions)
+ [What is the datatype of the Surrogate Key?](#what-is-the-datatype-of-the-surrogate-key)
+ [What is the difference between scan Component and Rollup Component?](#what-is-the-difference-between-scan-component-and-rollup-component)
+ [What is M_dump?](#What-is-M_dump)
+ [What is Brodcasting and Replicate?](#what-is-brodcasting-and-replicate)
+ [What is Local and Formal Parameter?](#what-is-local-and-formal-parameter)
+ [What is the difference between Dml Expression and Xfr Expression?](#what-is-the-difference-between-dml-expression-and-xfr-expression)
+ [Have you used Rollup Component?](#have-you-used-rollup-component)
+ [What are Primary Keys and Foreign Keys?](#what-are-primary-keys-and-foreign-keys)
+ [What is Outer Join?](#what-is-outer-join)
+ [What are Cartesian Joins?](#what-are-cartesian-joins)
+ [What is the purpose of having Stored Procedures in a Database?](#what-is-the-purpose-of-having-stored-procedures-in-a-database)
+ [Why might you create a Stored Procedure with Recompile Option?](#why-might-you-create-a-stored-procedure-with-recompile-option)
+ [What is Cursor?](#what-is-cursor)
+ [Describe process steps you would perform when Defragmenting a Data Table and this table contains mission critical Data?](#describe-process-steps-you-would-perform-when-defragmenting-a-data-table-and-this-table-contains-mission-critical-data)
+ [Explain the difference between Truncate and Delete Commands?](#explain-the-difference-between-truncate-and-delete-commands)
+ [How would you find out whether Sql Query is using Indices you Expect?](#how-would-you-find-out-whether-sql-query-is-using-indices-you-expect)
+ [What are the Security Level used in Bo?](#what-are-the-security-level-used-in-bo)
+ [What are the Functional and Architectural differences between Business Objects and Web Intelligence Reports?](#what-are-the-functional-and-architectural-differences-between-business-objects-and-web-intelligence-reports)
+ [What is batch processing in Business Objects?](#what-is-batch-processing-in-business-objects)
+ [What is Data Cardinality?](#what-is-data-cardinality)
+ [What is Chained Data Replication?](#what-is-chained-data-replication)
+ [Explain in brief various fundamental stages of Data Warehousing.](#explain-in-brief-various-fundamental-stages-of-data-warehousing)
+ [What is the difference between Enterprise Data Warehouse and Data Warehouse?](#what-is-the-difference-between-enterprise-data-warehouse-and-data-warehouse)
+ [Give me any example of Semi and Non Additive Measures?](#give-me-any-example-of-semi-and-non-additive-measures)
+ [What are the options in the Target Session of Update Strategy Transformations?](#what-are-the-options-in-the-target-session-of-update-strategy-transformations)
+ [What are the Various Types of Transformation?](#what-are-the-various-types-of-transformation)
+ [What is the difference between Active Transformation and Passive Transformation?](#what-is-the-difference-between-active-transformation-and-passive-transformation)
+ [What is the difference between Static Cache and Dynamic Cache?](#what-is-the-difference-between-static-cache-and-dynamic-cache)
+ [How do we join Two tables without Joiner or Sql Override?](#how-do-we-join-two-tables-without-joiner-or-sql-override)
+ [Differences between Normalizer and Normalizer Transformation.](#differences-between-normalizer-and-normalizer-transformation)
+ [What is Business Intelligence?](#what-is-business-intelligence)
+ [What is a Universe in Business Intelligence?](#what-is-a-universe-in-business-intelligence)
+ [What is Olap in Business Intelligence?](#what-is-olap-in-business-intelligence)
+ [What are various Modules in Business Objects Product?](#what-are-various-modules-in-business-objects-product)
+ [What is Olap Molap Rolap Dolap Holap?](#what-is-olap-molap-rolap-dolap-holap)
+ [Why an Infocube has maximum of 16 dimensions?](#why-an-infocube-has-maximum-of-16-dimensions)
+ [Name some standard Business Intelligence Tools in the Market?](#name-some-standard-business-intelligence-tools-in-the-market)
+ [What are Dashboards?](#what-are-dashboards)
+ [What is Hierarchy Relationship in a Dimension.](#what-is-hierarchy-relationship-in-a-dimension)
+ [What are Adhoc reports and Static Reports?](#what-are-adhoc-reports-and-static-reports)
+ [What is the Importance of Surrogate Key in Data Warehousing?](#what-is-the-importance-of-surrogate-key-in-data-warehousing)
+ [What is a Query?](#what-is-a-query)
+ [What are the Features of a Physical Data Model?](#what-are-the-features-of-a-physical-data-model)
+ [What are the steps to design a Physical Model?](#what-are-the-steps-to-design-a-physical-model)
+ [What are the Features of Conceptual Data Model?](#what-are-the-features-of-conceptual-data-model)
+ [What are the difference between Logical Data Model and Conceptual Data Model?](#what-are-the-difference-between-logical-data-model-and-conceptual-data-model)
+ [What are the steps to design Logical Data Model?](#what-are-the-steps-to-design-logical-data-model)
+ [What is Etl?](#what-is-etl-1)
+ [What is a Three Tier Data Warehouse?](#what-is-a-three-tier-data-warehouse)
+ [What is Etl Process and how many steps Etl contains?](#what-is-etl-process-and-how-many-steps-etl-contains)
+ [What is Full Load and Incremental or Refresh Load?](#what-is-full-load-and-incremental-or-refresh-load)
+ [What is a Staging Area?](#what-is-a-staging-area)
+ [Compare Etl and Manual Development.](#compare-etl-and-manual-development)
+ [What is Rdbms?](#what-is-rdbms)
+ [What is Normalization?](#what-is-normalization)
+ [What are different Normalization Forms?](#what-are-different-normalization-forms)
+ [What is Stored Procedure?](#what-is-stored-procedure)
+ [What is Trigger?](#what-is-trigger)
+ [What is View?](#what-is-view)
+ [Advantages of Dbms?](#advantages-of-dbms)
+ [Disadvantage in File Processing System?](#disadvantage-in-file-processing-system)
+ [Describe Three Levels of Data Abstraction?](#describe-three-levels-of-data-abstraction)
+ [Define integrity Rules?](#define-integrity-rules)
+ [What is Extension and Intention?](#what-is-extension-and-intention)
+ [What is Data Independence?](#what-is-data-independence)
+ [What is a View and how it is related to Data Independence?](#what-is-a-view-and-how-it-is-related-to-data-independence)
+ [What is Data Model?](#what-is-data-model)
+ [What is Object Oriented Model?](#what-is-object-oriented-model)
+ [What is an Entity?](#what-is-an-entity)
+ [What is an Entity Type?](#what-is-an-entity-type)
+ [What is an Entity Set?](#what-is-an-entity-set)
+ [What is an Attribute?](#what-is-an-attribute)
+ [What is Relation Schema and Relation?](#what-is-relation-schema-and-relation)
+ [What is Degree of Relation?](#what-is-degree-of-relation)
+ [What is Relationship?](#what-is-relationship)
+ [What is Relationship Set?](#what-is-relationship-set)
+ [What is Relationship Type?](#what-is-relationship-type)
+ [What Is DDL?](#what-is-ddl)
+ [What Is Vdl?](#what-is-vdl)
+ [What is Sdl?](#what-is-sdl)
+ [What Is Data Storage Definition Language?](#what-is-data-storage-definition-language)
+ [What Is Dml?](#what-is-dml)
+ [What is Query Evaluation Engine?](#what-is-query-evaluation-engine)
+ [What is Ddl Interpreter?](#what-is-ddl-interpreter)
+ [What is Record at a time?](#what-is-record-at-a-time)
+ [What is Set at a time or Set oriented?](#what-is-set-at-a-time-or-set-oriented)
+ [What is Relational Algebra?](#what-is-relational-algebra)
+ [What is Relational Calculus?](#what-is-relational-calculus)
+ [How does Tuple oriented Relational calculus differ from Domain oriented Relational Calculus?](#how-does-tuple-oriented-relational-calculus-differ-from-domain-oriented-relational-calculus)
+ [What is Functional Dependency?](#what-is-functional-dependency)
+ [What is Multivalued Dependency?](#what-is-multivalued-dependency)
+ [What is Lossless Join Property?](#what-is-lossless-join-property)
+ [What Is 1 Nf?](#what-is-1-nf)
+ [What is Fully Functional Dependency?](#what-is-fully-functional-dependency)
+ [What is 2nf?](#what-is-2nf)
+ [What is 3nf?](#what-is-3nf)
+ [What is 4nf?](#what-is-4nf)
+ [What is 5nf?](#what-is-5nf)
+ [What is Domain key NF?](#what-is-domain-key-nf)
+ [What are Partial Alternate Artificial Compound and Natural Key?](#what-are-partial-alternate-artificial-compound-and-natural-key)
+ [What is Indexing and what are the different kinds of Indexing?](#what-is-indexing-and-what-are-the-different-kinds-of-indexing)
+ [What is meant by Query Optimization?](#what-is-meant-by-query-optimization)
+ [What is Join Dependency and Inclusion Dependency?](#what-is-join-dependency-and-inclusion-dependency)
+ [What is Durability in Dbms?](#what-is-durability-in-dbms)
+ [What do you mean by Atomicity and Aggregation?](#what-do-you-mean-by-atomicity-and-aggregation)
+ [What is Phantom Deadlock?](#what-is-phantom-deadlock)
+ [What is Checkpoint and when does it cccur?](#what-is-checkpoint-and-when-does-it-cccur)
+ [What are different Phases of Transaction?](#what-are-different-phases-of-transaction)
+ [What do you mean by Flat File Database?](#what-do-you-mean-by-flat-file-database)
+ [What is transparent Dbms?](#what-is-transparent-dbms)
+ [What do you mean by Correlated Subquery?](#what-do-you-mean-by-correlated-subquery)
+ [What are the Primitive Operations common to all record management systems?](#what-are-the-primitive-operations-common-to-all-record-management-systems)
+ [What are Unary Operations in Relational Algebra?](#what-are-unary-operations-in-relational-algebra)
+ [Are resulting Relations of Product and Join Operation the same?](#are-resulting-relations-of-product-and-join-operation-the-same)
+ [What is Rdbms Kernel?](#what-is-rdbms-kernel)
+ [Name the Sub systems of Rdbms?](#name-the-sub-systems-of-rdbms)
+ [What is Rowid?](#what-is-rowid)
+ [What is Storage Manager?](#what-is-storage-manager)
+ [What is Buffer Manager?](#what-is-buffer-manager)
+ [What is Transaction Manager?](#what-is-transaction-manager)
+ [What is File Manager?](#what-is-file-manager)
+ [What is Authorization and Integrity Manager?](#what-is-authorization-and-integrity-manager)
+ [What are Stand alone procedures?](#what-are-stand-alone-procedures)
+ [What are the different methods of loading dimension tables?](#what-are-the-different-methods-of-loading-dimension-tables-1)
+ [Describe the foreign key columns in fact tables and dimension tables?](#describe-the-foreign-key-columns-in-fact-tables-and-dimension-tables)
+ [What are the types of fact tables in a dimensional model?](#what-are-the-types-of-fact-tables-in-a-dimensional-model)
+ [How do you implement SCD Type 2 with a MERGE statement?](#how-do-you-implement-scd-type-2-with-a-merge-statement)
+ [How do you handle late-arriving facts and dimensions?](#how-do-you-handle-late-arriving-facts-and-dimensions)
+ [What is the medallion architecture (bronze, silver, gold)?](#what-is-the-medallion-architecture-bronze-silver-gold)
+ [What is a data vault and when would you use it?](#what-is-a-data-vault-and-when-would-you-use-it)
+ [What is a lakehouse and how does it differ from a data warehouse?](#what-is-a-lakehouse-and-how-does-it-differ-from-a-data-warehouse)
+ [How do you partition and cluster a large fact table?](#how-do-you-partition-and-cluster-a-large-fact-table)
+ [What is a bridge table and when do you need one?](#what-is-a-bridge-table-and-when-do-you-need-one)
+ [How do you test a data warehouse model?](#how-do-you-test-a-data-warehouse-model)
+ [Real world use cases for data warehousing architecture](#real-world-use-cases-for-data-warehousing-architecture)

## What are the main layers in a data warehouse architecture?

A common architecture has landing/raw, staging, integration, presentation, and consumption layers. Raw stores source-like data for audit and replay. Staging cleans and standardizes. Integration applies business rules and conformed dimensions. Presentation exposes marts, semantic models, and dashboards.

Example:

```text
raw_orders -> stg_orders -> fct_orders + dim_customer -> finance_mart
```

The purpose of layers is to separate concerns: ingestion, quality, business logic, and serving.

```text
source systems
   -> landing / raw        (source-shaped, immutable, replayable)
   -> staging              (typed, deduplicated, conformed names)
   -> integration          (business rules, conformed dimensions)
   -> presentation         (star schemas, marts, semantic layer)
   -> consumption          (BI, notebooks, reverse ETL)
```

```sql
-- Landing keeps source shape for replay.
CREATE TABLE landing.orders (
    ingest_ts   TIMESTAMP NOT NULL,
    source_file TEXT      NOT NULL,
    payload     TEXT      NOT NULL
);

-- Staging types and deduplicates.
CREATE TABLE staging.orders AS
SELECT
    payload::json ->> 'order_id'  AS order_id,
    (payload::json ->> 'amount')::numeric AS amount,
    ingest_ts
FROM landing.orders
WHERE ingest_ts >= CURRENT_DATE;

-- Presentation serves a stable contract.
CREATE VIEW presentation.v_orders AS
SELECT order_id, amount FROM staging.orders;
```

Interviews often ask "why so many copies". The answer is separation of concerns: raw for audit and replay, staging
for quality and typing, integration for business logic, presentation for performance and access control.

[Table of Contents](#Data-Warehousing-Architecture)

## How do OLTP and OLAP systems differ?

OLTP systems support operational transactions such as placing orders or updating accounts. They prioritize low-latency writes, normalization, and consistency. OLAP systems support analytics and reporting. They prioritize scans, aggregations, columnar storage, and dimensional models.

Example:

+ OLTP: application database for orders
+ OLAP: warehouse table for revenue by month and region

Data engineers often move data from OLTP to OLAP using batch ingestion, CDC, or event streams.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the Main Difference between View and Materialized View?

The main difference between view and materialized view is as follows:
+ View:
  + Data representation is provided by view where the data is accessed from its table.
  + View has a logical structure which does not occupy space
  + All the changes are affected in corresponding tables.
+ Materialized View:
  + Within materialized view, pre-calculated data is available
  + The materialized view has a physical structure which does occupy space
  + All the changes are not reflected in the corresponding tables.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Junk Dimension?

A junk dimension is nothing but a dimension where a certain type of data is stored which is not appropriate to store in the schema. The nature of the junk dimension is usually a Boolean has flag values.
A single dimension is formed by a group of small dimensions got together. This can be considered as junk dimension.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Data Warehouse architecture?

The data warehouse architecture is a three-tier architecture.
The following is the three-tier architecture:
+ Bottom Tier
+ Middle Tier
+ Upper Tier

It is nothing but a repository of integrating data which is extracted from different data sources.

The classic three-tier view maps cleanly onto the modern lakehouse layering.

```text
Bottom tier  : data sources, ingestion, storage (raw + staging)
Middle tier  : integration, warehouse/mart, semantic model
Upper tier   : BI tools, ad hoc SQL, dashboards, APIs
```

```sql
-- Bottom tier: land and stage.
COPY INTO landing.raw_orders FROM @ext_stage/orders/;

-- Middle tier: integrate into a mart.
CREATE OR REPLACE TABLE marts.fct_orders AS
SELECT o.order_id, c.customer_sk, d.date_sk, o.net_amount
FROM staging.orders o
JOIN dim_customer c ON c.customer_id = o.customer_id AND c.is_current
JOIN dim_date d     ON d.date = o.order_date;

-- Upper tier: expose a stable view for BI.
CREATE VIEW bi.v_order_revenue AS
SELECT date_sk, SUM(net_amount) AS revenue FROM marts.fct_orders GROUP BY date_sk;
```

[Table of Contents](#Data-Warehousing-Architecture)

## What is an integrity constraints and what are different types of integrity constraints?

An integrity constraint is nothing but a specific requirement that the data in the database has to meet. It is nothing but a business rule for a particular column in a table. In the data warehouse concept, they are 5 integrity constraints.
The following are the integrity constraints:
+ Null
+ Unique key
+ Primary key
+ Foreign key
+ Check

[Table of Contents](#Data-Warehousing-Architecture)

## Why is that Data Architect actually monitor and enforce compliance data standards?

The primary idea of keeping the standards high on compliance for data standards is because it will help to reduce the data redundancy and helps the team to have a quality data. As this information is actually carried out or used throughout the organization.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain the different data models that are available in detail?

There are three different kinds of data models that are available and they are as follows:
+ Conceptual
+ Logical
+ Physical

Conceptual data model:
+ As the name itself implies that this data model depicts the high-level design of the available physical data.

Logical data model:
+ Within the logical model, the entity names, entity relationships, attributes, primary keys and foreign keys will show up.

Physical data model:
+ Based on this data model, the view will give out more information and showcases how the model is implemented in the database. All the primary keys, foreign keys, tables names and column names will be showing up.

[Table of Contents](#Data-Warehousing-Architecture)

## Differentiate between dimension and attribute?

In short, dimensions are nothing but which represents qualitative data. For example data like a plan, product, class are all considered as dimensions.
The attribute is nothing but a subset of a dimension. Within a dimension table, we will have attributes. The attributes can be textual or descriptive. For example, product name and product category are nothing but an attribute of product dimensions.

[Table of Contents](#Data-Warehousing-Architecture)

## Differentiate between Oltp and Olap?

OLTP stands for Online Transaction Processing. It maintains current, transactional, highly normalized data (3NF) so writes stay consistent. OLAP stands for Online Analytical Processing. It maintains historical, denormalized, dimensional data (star or snowflake) so analytical reads and aggregations stay fast. The common interview trap is reversing these: OLTP is normalized, OLAP is dimensional.

```text
| Aspect        | OLTP                                  | OLAP                                  |
|---------------|---------------------------------------|---------------------------------------|
| Purpose       | Run the business                      | Analyze the business                  |
| Workload      | Many small reads and writes           | Few large scans and aggregations      |
| Schema        | Highly normalized (3NF)               | Dimensional (star or snowflake)       |
| Rows touched  | A handful per transaction             | Millions per query                    |
| Storage       | Row store                             | Column store with compression         |
| History       | Current state                         | Years of history                      |
| Latency       | Milliseconds                          | Seconds to minutes                     |
| Users         | Applications                          | Analysts and BI tools                 |
```

```sql
-- OLTP pattern: point lookup and update by primary key
SELECT * FROM orders WHERE order_id = 1042;
UPDATE orders SET status = 'shipped' WHERE order_id = 1042;

-- OLAP pattern: aggregate a large fact table by dimension
SELECT d.year, p.category, SUM(f.net_amount) AS revenue
FROM fct_sales f
JOIN dim_date d    ON d.date_sk = f.date_sk
JOIN dim_product p ON p.product_sk = f.product_sk
GROUP BY d.year, p.category;
```

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Real time Data Warehouse and how is it different from near to Real time Data Warehouse?

As the term suggests, a real-time data warehouse is a system, which reflects all changes to its sources in real time. As simple as it sounds, this is still an area of active research in the field. In traditional DWH, the operational system(s) are kept separate from the DWH for a good reason.
The Operational systems are designed to accept inputs or changes to data regularly, hence have a good chance of being regularly queried. On the other hand, a DWH is supposed to do just the opposite - it is used to query data for reports only. No changes to data, through user actions is expected (or designed). The only inputs could come from the ETL feed at stipulated times.
The ETL would source its data from the Operational systems just explained above.
To create a real-time DWH we would have to merge both systems (several ways are being explored), a concept that is against the reason of creating a DWH. Bigger challenges occur in terms of updating aggregated data in facts at real time, still maintaining the surrogate keys.
Besides, we would need lightening fast hardware to try this.Near Real time DWH is a trade-off between the conventional design and the dream of all clients today. The frequency of ETL updates in higher in this case for e.g. once in 2 hours. We can also analyze and use selective refreshes at shorter time intervals, while complete refreshes may still be kept further apart. Selective refreshes would look at only those tables that get updated regularly.

```text
| Mode          | Freshness          | Typical stack                          |
|---------------|--------------------|----------------------------------------|
| Batch         | Hours to a day     | Nightly ETL into the warehouse         |
| Micro-batch   | 1-15 minutes       | Spark Structured Streaming, Auto Loader|
| Near real time| Seconds            | Kafka + Flink + a fast store           |
| Real time     | Sub-second         | Streaming engine + serving layer       |
```

```sql
-- Micro-batch: append only new events, then merge.
MERGE INTO fct_events AS t
USING (SELECT * FROM staging.events_delta) AS s
   ON t.event_id = s.event_id
WHEN NOT MATCHED THEN INSERT (event_id, event_ts, amount) VALUES (s.event_id, s.event_ts, s.amount);

-- Near real time: a streaming sink keeps current aggregates.
INSERT INTO fct_revenue_minute
SELECT window_start, SUM(amount) FROM TABLE(TUMBLE(TABLE events, DESCRIPTOR(event_ts), INTERVAL '1' MINUTE))
GROUP BY window_start;
```

[Table of Contents](#Data-Warehousing-Architecture)

## What is Type 2 Version Dimension?

Version dimension is the SCD type II in real time it using because of it will maintain the current data and full historical data.

A Type 2 version dimension stores a new row for every change, with validity dates and a current flag. The surrogate
key is unique per version; the natural key repeats.

```sql
CREATE TABLE dim_customer (
    customer_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id TEXT   NOT NULL,             -- natural key, repeats per version
    name        TEXT   NOT NULL,
    city        TEXT   NOT NULL,
    segment     TEXT   NOT NULL,
    start_date  DATE   NOT NULL,
    end_date    DATE   NOT NULL DEFAULT DATE '9999-12-31',
    is_current  BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (customer_id, start_date),
    CHECK (end_date > start_date)
);

CREATE INDEX idx_dim_customer_current ON dim_customer (customer_id) WHERE is_current;
```

```text
customer_id | customer_sk | city      | start_date | end_date   | is_current
------------+-------------+-----------+------------+------------+-----------
C-100       |         501 | Bangalore | 2021-01-01 | 2024-06-30 | false
C-100       |         902 | Hyderabad | 2024-07-01 | 9999-12-31 | true
```

Facts join on the surrogate key that was current when the event happened, which is why the load must resolve the
version at load time.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Data Modeling and Data Mining?

Data modeling is the process of designing a data base model. In this data model data will be stored in two types of table fact table and dimension table.
Fact table contains the transaction data and dimension table contains the master data. Data mining is process of finding the hidden trends is called the data mining.

[Table of Contents](#Data-Warehousing-Architecture)

## Where the Data Cube Technology is used?

A multi-dimensional structure called the data cube. A data abstraction allows one to view aggregated data from a number of perspectives. Conceptually, the cube consists of a core or base cuboids, surrounded by a collection of sub-cubes/cuboids that represent the aggregation of the base cuboids along one or more dimensions. We refer to the dimension to be aggregated as the measure attribute, while the remaining dimensions are known as the feature attributes.

[Table of Contents](#Data-Warehousing-Architecture)

## How can you implement many relations in Star Schema Model?

Many-many relations can be implemented by using snowflake schema .With a max of n dimensions.

A many-to-many relationship needs a bridge (associative) table between the dimension and the fact, with a weighting
factor so measures are not double counted.

```text
dim_promotion --< bridge_promotion_order >-- fct_sales
```

```sql
CREATE TABLE bridge_order_promotion (
    order_id     BIGINT NOT NULL,
    promotion_sk BIGINT NOT NULL REFERENCES dim_promotion(promotion_sk),
    weight       NUMERIC(6, 4) NOT NULL,   -- allocation share, sums to 1 per order
    PRIMARY KEY (order_id, promotion_sk)
);

-- Allocate revenue across the promotions attached to each order.
SELECT p.promotion_name, SUM(f.net_amount * b.weight) AS allocated_revenue
FROM fct_sales f
JOIN bridge_order_promotion b ON b.order_id = f.sale_id
JOIN dim_promotion p ON p.promotion_sk = b.promotion_sk
GROUP BY p.promotion_name;
```

If the weight is unknown, give each row `1 / count(rows per order)` so allocations still sum to the order total.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Critical Column?

Let us take one ex: Suppose 'XYZ' is customer in Bangalore, he was residing in the city from the last 5 years, in the period of 5 years he has made purchases worth of 3 lacs. Now, he moved to 'HYD'. When you update the 'XYZ' city to 'HYD' in your Warehouse, all the purchases by him will show in city 'HYD' only. This makes warehouse inconsistent. Here CITY is the Critical Column. Solution is use Surrogate Key.

A critical column is the attribute whose change flips a Type 2 version. In the example below only `city` and
`segment` are critical, so a change to `phone` does not create a new version.

```sql
CREATE OR REPLACE VIEW v_customer_changes AS
SELECT s.customer_id, s.city, s.segment, s.effective_date
FROM   staging.customer_delta s
JOIN   dim_customer d
       ON d.customer_id = s.customer_id AND d.is_current
WHERE  (d.city, d.segment) IS DISTINCT FROM (s.city, s.segment);

SELECT * FROM v_customer_changes;
```

Choosing critical columns well keeps the dimension from exploding: version only what analysts actually need to see.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the main difference between Star and Snowflake Star Schema and which one is better and why?

If u have one to may relation ship in the data then only we choose snowflake schema, as per the performance-wise every-one go for the Star schema. Moreover, if the ETL is concerned with reporting means choose for snowflake because this schema provides more browsing capability than the former schema.

Worked example: one fact table and four dimensions.

Star schema keeps every dimension denormalized and one join away from the fact.

```text
                 dim_date
                    |
dim_store ---- fct_sales ---- dim_product
                    |
              dim_customer
```

Snowflake schema normalizes the dimensions into sub-dimensions, adding joins.

```text
dim_category --- dim_product ---+
                                |
dim_region --- dim_store --- fct_sales --- dim_date
                                |
                          dim_customer --- dim_geography
```

Star schema DDL (the dimension carries category inline):

```sql
CREATE TABLE dim_product (
    product_sk   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id   TEXT   NOT NULL UNIQUE,      -- natural key from the source
    product_name TEXT   NOT NULL,
    category     TEXT   NOT NULL,
    subcategory  TEXT   NOT NULL,
    brand        TEXT
);

CREATE TABLE fct_sales (
    sale_id     BIGINT NOT NULL,
    sale_date   DATE   NOT NULL,
    date_sk     BIGINT NOT NULL REFERENCES dim_date(date_sk),
    product_sk  BIGINT NOT NULL REFERENCES dim_product(product_sk),
    store_sk    BIGINT NOT NULL REFERENCES dim_store(store_sk),
    customer_sk BIGINT NOT NULL REFERENCES dim_customer(customer_sk),
    quantity    INTEGER NOT NULL,
    unit_price  NUMERIC(12, 2) NOT NULL,
    net_amount  NUMERIC(14, 2) NOT NULL,
    PRIMARY KEY (sale_id, sale_date)
) PARTITION BY RANGE (sale_date);
```

Snowflake variant: replace `dim_product` with a small `dim_product` plus a `dim_category` lookup.

```sql
CREATE TABLE dim_category (
    category_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category    TEXT NOT NULL,
    department  TEXT NOT NULL
);

CREATE TABLE dim_product (
    product_sk  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id  TEXT   NOT NULL UNIQUE,
    product_name TEXT  NOT NULL,
    category_sk BIGINT NOT NULL REFERENCES dim_category(category_sk)
);
```

The star query touches one dimension join. The snowflake query adds a join, which costs an extra shuffle on large
fact tables, but saves storage and removes update anomalies in the category attribute.

Practical guidance:

+ Choose star by default: it is simpler for BI tools, easier for users, and faster on columnar warehouses.
+ Choose snowflake when a sub-dimension is large, shared, or changes independently, or when storage is the constraint.
+ Do not normalize a dimension just for tidiness; every extra join is a repeated cost on the fact scan.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Dependent Data Warehouse and Independent Data Warehouse?

Dependent departments are those, which depend on a data ware to for their data.Independent department are those, which get their data directly from the operational data sources in the organization.

[Table of Contents](#Data-Warehousing-Architecture)

## Which technology should be used for interactive Data Querying across multiple dimensions for a decision making for a Dw?

MOLAP

[Table of Contents](#Data-Warehousing-Architecture)

## What is Virtual Data Warehousing?

A virtual or point-to-point data warehousing strategy means that end-users are allowed to get at operational databases directly using whatever tools are enabled to the "data access network".

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Metadata and Data Dictionary?

Meta data is nothing but information about data. It contains the information (i.e. data) about the graphs, its related files, abinitio commands, server information etc i.e. all kinds of information about project related information etc.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Mapping Parameter and Mapping Variable in Data Warehousing?

Mapping Parameter defines the constant value and it cannot change the value throughout the session. Mapping Variables defines the value and it can be change throughout the session.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain the advantages Of Raid 1 and 1/0 And 5 and what type of Raid setup would you put your Tx Logs.

The basic advantage of RAID is to speed up the data reading from permanent storage device (hard disk).

[Table of Contents](#Data-Warehousing-Architecture)

## What are the characteristics of data files?

A data file can be associated with only one database. Once created a data file can't change size. One or more data files form a logical unit of database storage called a table space.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Rollback Segment?

A Database contains one or more Rollback Segments to temporarily store "undo" information.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Table Space?

A database is divided into Logical Storage Unit called table spaces. A table space is used to grouped related logical structures together.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Database Link?

A database link is a named object that describes a "path" from one database to another.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Hash Cluster?

A row is stored in a hash cluster based on the result of applying a hash function to the row's cluster key value. All rows with the same hash key value are stores together on disk.

A hash cluster stores rows with the same hash key together on disk, so an equality lookup reads one block instead of
an index plus a table access. Warehouse engines call the same idea bucketing or clustering.

```sql
-- Hash-partitioned distribution in a distributed warehouse.
CREATE TABLE fct_events (
    event_id   BIGINT NOT NULL,
    tenant_id  BIGINT NOT NULL,
    event_date DATE   NOT NULL,
    payload    TEXT
) PARTITION BY RANGE (event_date);

-- Bucket by tenant so joins on tenant_id avoid a shuffle.
CREATE TABLE dim_tenant (
    tenant_id BIGINT NOT NULL,
    name      TEXT NOT NULL
) CLUSTERED BY (tenant_id) INTO 64 BUCKETS;
```

Trade-offs: hashing speeds equality joins and point lookups but does nothing for range scans, and a skewed hot key
concentrates all work on one bucket.

[Table of Contents](#Data-Warehousing-Architecture)

## Describe referential Integrity?

A rule defined on a column (or set of columns) in one table that allows the insert or update of a row only if the value for the column or set of columns (the dependent value) matches a value in a column of a related table (the referenced value). It also specifies the type of data manipulation allowed on referenced data and the action to be performed on dependent data as a result of any action on referenced data.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Schema?

A schema is collection of database objects of a User.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Table?

A table is the basic unit of data storage in an ORACLE database. The tables of a database hold all of the user accessible data. Table data is stored in rows and columns.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a View?

A view is a virtual table. Every view has a Query attached to it. (The Query is a SELECT statement that identifies the columns and rows of the table(s) the view uses.)

[Table of Contents](#Data-Warehousing-Architecture)

## What is an Extent?

An Extent is a specific number of contiguous data blocks, obtained in a single allocation, and used to store a specific type of information.

[Table of Contents](#Data-Warehousing-Architecture)

## What is an Index?

An Index is an optional structure associated with a table to have direct access to rows, which can be created to increase the performance of data retrieval. Index can be created on one or more columns of a table.

[Table of Contents](#Data-Warehousing-Architecture)

## What is an Integrity Constrains?

An integrity constraint is a declarative way to define a business rule for a column of a table.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Clusters?

Clusters are groups of one or more tables physically stores together to share common columns and are often used together.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the different types of Segments?

Data Segment,
Index Segment,
Rollback Segment and Temporary Segment.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain the Relationship among database and Table Space and Data File?

Each database logically divided into one or more table spaces one or more data files are explicitly created for each table space.

[Table of Contents](#Data-Warehousing-Architecture)

## What is an Index Segment?

Each Index has an Index segment that stores all of its data.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Referential Actions supported by Foreign Key integrity constraint?

Update And Delete Restrict - A referential integrity rule that disallows the update or deletion of referenced data. DELETE Cascade - When a referenced row is deleted all associated dependent rows are deleted.

[Table of Contents](#Data-Warehousing-Architecture)

## Do you View contain Data?

Views do not contain or store data.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the use of Control File?

When an instance of an ORACLE database is started, its control file is used to identify the database and redo log files that must be opened for database operation to proceed. It is also used in database recovery.

[Table of Contents](#Data-Warehousing-Architecture)

## Can Objects of the same Schema reside in different Table Spaces?

Yes

[Table of Contents](#Data-Warehousing-Architecture)

## Can a Table Space hold objects from different Schemes?

Yes

[Table of Contents](#Data-Warehousing-Architecture)

## Can a View based on another View?

Yes

[Table of Contents](#Data-Warehousing-Architecture)

## What is a full Backup?

A full backup is an operating system backup of all data files, on- line redo log files and control file that constitute ORACLE database and the parameter.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Mirrored on line redo Log?

A mirrored on-line redo log consists of copies of on-line redo log files physically located on separate disks; changes made to one member of the group are made to all members.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Partial Backup?

A Partial Backup is any operating system backup short of a full backup, taken while the database is open or shut down.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Restricted Mode of Instance Startup?

An instance can be started in (or later altered to be in) restricted mode so that when the database is open connections are limited only to those whose user accounts have been granted the RESTRICTED SESSION system privilege.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the steps involved in Database Shutdown?

Close the Database; Dismount the Database and Shutdown the Instance.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the advantages of Operating a Database in archivelog mode over operating it in no Archivelog Mode?

Complete database recovery from disk failure is possible only in ARCHIVELOG mode. Online database backup is possible only in ARCHIVELOG mode.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the different modes of Mounting a Database with the Parallel Server?

Exclusive Mode If the first instance that mounts a database does so in exclusive mode, only that Instance can mount the database. Parallel Mode If the first instance that mounts a database is started in parallel mode, other instances that are started in parallel mode can also mount the database.

[Table of Contents](#Data-Warehousing-Architecture)

## Can Full Backup be performed when the Database is Open?

No

[Table of Contents](#Data-Warehousing-Architecture)

## What are the steps involved in instance Recovery?

Rolling forward to recover data that has not been recorded in data files yet has been recorded in the on-line redo log, including the contents of rollback segments. Rolling back transactions that have been explicitly rolled back or have not been committed as indicated by the rollback segments regenerated in step a.
1) Releasing any resources (locks) held by transactions in process at the time of the failure.
2) Resolving any pending distributed transactions undergoing a two-phase commit at the time of the instance failure.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the steps involved in Database Startup?

Start an instance, Mount the Database and Open the Database.

[Table of Contents](#Data-Warehousing-Architecture)

## Which parameter specified in the Default Storage Clause of create Tablespace cannot be Altered after creating the Table Space?

All the default storage parameters defined for the table space can be changed using the ALTER TABLESPACE command. When objects are created their INITIAL and MINEXTENS values cannot be changed.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Online redo Log?

The On-line Redo Log is a set of tow or more on-line redo files that record all committed changes made to the database. Whenever a transaction is committed, the corresponding redo entries temporarily stores in redo log buffers of the SGA are written to an on-line redo log file by the background process LGWR. The on-line redo log files are used in cyclical fashion.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Log Switch?

The point at which ORACLE ends writing to one online redo log file and begins writing to another is called a log switch.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Dimensional Modelling?

Dimensional Modelling is a design concept used by many data warehouse designers to build their data warehouse. In this design model all the data is stored in two types of tables - Facts table and Dimension table. Fact table contains the facts/measurements of the business and the dimension table contains the context of measurements i.e., the dimensions on which the facts are calculated.

A dimensional model is a fact table at a declared grain surrounded by dimensions that carry the descriptive context.

```text
                   dim_date (when)
                        |
dim_store (where) -- fct_sales (what, how much) -- dim_product (what)
                        |
                dim_customer (who)
```

The four-step design process:

1. Choose the business process, for example "retail sales".
2. Declare the grain, for example "one row per order line".
3. Identify the dimensions that describe the grain.
4. Identify the numeric facts that are true at that grain.

```sql
CREATE TABLE fct_sales (
    sale_id     BIGINT NOT NULL,       -- degenerate dimension: the order line
    date_sk     BIGINT NOT NULL REFERENCES dim_date(date_sk),
    product_sk  BIGINT NOT NULL REFERENCES dim_product(product_sk),
    store_sk    BIGINT NOT NULL REFERENCES dim_store(store_sk),
    customer_sk BIGINT NOT NULL REFERENCES dim_customer(customer_sk),
    quantity    INTEGER NOT NULL,      -- additive
    net_amount  NUMERIC(14, 2) NOT NULL,
    PRIMARY KEY (sale_id)
);
```

[Table of Contents](#Data-Warehousing-Architecture)

## What are the difference between snow Flake and Star Schema and what are situations where Snow Flake Schema is better than Star Schema to use and when the opposite is True?

Star schema contains the dimension tables mapped around one or more fact tables. It is a renormalized model and no need to use complicated joins. Also queries results fast.Snowflake schema: It is the normalized form of Star schema. It contains in-depth joins, because the tables are split in to many pieces. We can easily do modification directly in the tables. We have to use complicated joins, since we have more tables.There will be some delay in processing the query.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Cube in Data Warehousing concept?

Cubes are logical representation of multidimensional data. The edge of the cube contains dimension members and the body of the cube contains data values.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the differences between Star and Snowflake Schema?

Star schema: A single fact table with N number of DimensionSnowflake schema: Any dimensions with extended dimensions are known as snowflake schema.

A compact comparison:

```text
| Aspect        | Star schema                          | Snowflake schema                     |
|---------------|--------------------------------------|--------------------------------------|
| Dimensions    | Denormalized                         | Normalized into sub-dimensions       |
| Joins         | 1 hop from fact to each dimension    | Multiple hops                         |
| Query speed   | Faster, fewer joins                  | Slower, more joins                    |
| Storage       | More redundancy                      | Less redundancy                       |
| ETL           | Simpler loads                        | More tables to load and reconcile     |
| Best for      | BI and aggregate-heavy marts         | Large shared or independently managed |
|               |                                      | dimensions                            |
```

```sql
-- Star: category and subcategory live on dim_product
SELECT p.category, SUM(f.net_amount) AS revenue
FROM fct_sales f
JOIN dim_product p ON p.product_sk = f.product_sk
GROUP BY p.category;

-- Snowflake: category lives on dim_category, reached through dim_product
SELECT c.category, SUM(f.net_amount) AS revenue
FROM fct_sales f
JOIN dim_product p  ON p.product_sk = f.product_sk
JOIN dim_category c ON c.category_sk = p.category_sk
GROUP BY c.category;
```

[Table of Contents](#Data-Warehousing-Architecture)

## What are Data Marts?

A data mart is a collection of tables focused on specific business group/department. It may have multi-dimensional or normalized. Data marts are usually built from a bigger data warehouse or from operational data.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the Data Type of the Surrogate Key?

A surrogate key has no business meaning, but it does have a storage type: an integer. Use `BIGINT` in warehouses that can exceed two billion rows, and generate values with an identity column, a sequence, or a monotonically increasing counter. The only hard requirements are that it is unique, non-null, and stable for the lifetime of the row version.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Fact and Dimension and Measure?

Fact is key performance indicator to analyze the business. Dimension is used to analyze the fact. Without dimension there is no meaning for fact.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the different Types of Data Warehousing?

Types of data warehousing are:
1. Enterprise Data warehousing
2. ODS (Operational Data Store)
3. Data Mart

[Table of Contents](#Data-Warehousing-Architecture)

## What do you mean by Static and Local Variable?

Static variable is not created on function stack but is created in the initialized data segment and hence the variable can be shared across the multiple call of the same function. Usage of static variables within a function is not thread safe.On the other hand, local variable or auto variable is created on function stack and valid only in the context of the function call and is not shared across function calls.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Source Qualifier?

When you add a relational or a flat file source definition to a mapping, you need to connect it to a Source Qualifier transformation. The Source Qualifier represents the rows that the Informatica Server reads when it executes a session.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Steps to Build the Data Warehouse?

Gathering business requirements>>Identifying Sources>>Identifying Facts>>Defining Dimensions>>Define Attributes>>Redefine Dimensions / Attributes>>Organize Attribute Hierarchy>>Define Relationship>>Assign Unique Identifiers.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the advantages Data Mining over Traditional approaches?

Data Mining is used for the estimation of future. For example, if we take a company/business organization, by using the concept of Data Mining, we can predict the future of business in terms of Revenue (or) Employees (or) Customers (or) Orders etc.Traditional approaches use simple algorithms for estimating the future. However, it does not give accurate results when compared to Data Mining.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between View and Materialized View?

View - store the SQL statement in the database and let you use it as a table. Every time you access the view, the SQL statement executes. Materialized view - stores the results of the SQL in table form in the database. SQL statement only executes once and after that every time you run the query, the stored result set is used. Pros include quick query results.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the main difference between Inmon and Kimball Philosophies of Data Warehousing?

Both build the same end state but in opposite directions. Kimball (bottom-up): model each business process as a
dimensional star, then integrate the marts through conformed dimensions and a bus matrix; delivery is fast and queries
stay simple. Inmon (top-down): build one integrated, subject-oriented, non-volatile, time-variant enterprise data
warehouse in normalized (3NF) form first, then derive departmental data marts from it; enterprise integration and a
single version of the truth come first, at the cost of a longer initial build.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Junk Dimension and what is the difference between Junk Dimension and Degenerated Dimension?

Junk dimension: Grouping of Random flags and text attributes in a dimension and moving them to a separate sub dimension. Degenerate Dimension: Keeping the control information on Fact table ex: Consider a Dimension table with fields like order number and order line number and have 1:1 relationship with Fact table, In this case this dimension is removed and the order information will be directly store.

[Table of Contents](#Data-Warehousing-Architecture)

## Why Fact Table is in Normal Form?

The fact table consists of the Index keys of the dimension/look up tables and the measures. So whenever we have the keys in a table. That it implies that the table is in the normal form.

[Table of Contents](#Data-Warehousing-Architecture)

## What is difference between Er Modeling and Dimensional Modeling?

Basic difference is E-R modeling will have logical and physical model. Dimensional model will have only physical model. E-R modeling is used for normalizing the OLTP database design.Dimensional modeling is used for de-normalizing the ROLAP/MOLAP design.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Conformed Fact?

A conformed fact is a fact (measure) that is defined identically - same name, same grain, and same business rule - in more than one fact table or data mart, so the numbers can be compared and added across processes. For example, `net_amount` must mean the same thing in the sales mart and the finance mart. Conformed facts and conformed dimensions together are what make drilling across possible; without them, two reports with the same label can disagree.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Methodologies of Data Warehousing?

Every company has methodology of their own. However, to name a few SDLC Methodology, AIM methodology is standard used.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Bus Schema?

BUS Schema is composed of a master suite of confirmed dimension and standardized definition if facts.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Data Warehousing Hierarchy?

Hierarchies are logical structures that use ordered levels as a means of organizing data. A hierarchy can be used to define data aggregation. For example, in a time dimension, a hierarchy might aggregate data from the month level to the quarter level to the year level. A hierarchy can also be used to define a navigational drill path and to establish a family structure.Within a hierarchy, each level is logically connected to the levels above and below it. Data values at lower levels aggregate into the data values at higher levels. A dimension can be composed of more than one hierarchy. For example, in the product dimension, there might be two hierarchies--one for product categories and one for product suppliers.Dimension hierarchies also group levels from general to granular. Query tools use hierarchies to enable you to drill down into your data to view different levels of granularity. This is one of the key benefits of a data warehouse.When designing hierarchies, you must consider the relationships in business structures. Hierarchies impose a family structure on dimension values. For a particular level value, a value at the next higher level is its parent, and values at the next lower level are its children. These familial relationships enable analysts to access data quickly.

A hierarchy is an ordered set of levels inside a dimension, for example country -> region -> city. Storing all levels
on the dimension row makes aggregation a simple `GROUP BY`.

```sql
SELECT country, region, city, SUM(net_amount) AS revenue
FROM fct_sales f
JOIN dim_store s ON s.store_sk = f.store_sk
GROUP BY ROLLUP (country, region, city)
ORDER BY country, region, city;
```

`GROUPING()` tells a subtotal row from a real value and is useful when rendering the result in a report.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Data Validation Strategies for Data Mart Validation after loading process?

Data validation is to make sure that the loaded data is accurate and meets the business requirements. Strategies are different methods followed to meet the validation requirements.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Data Types present in Bo and what happens if we implement View in the Designer N Report?

Three different data types: Dimensions, Measure, and DetailView is nothing but an alias and it can be used to resolve the loops in the universe.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Surrogate Key and where we use it?

Surrogate key is a substitution for the natural primary key.It is just a unique identifier or number for each row that can be used for the primary key to the table. The only requirement for a surrogate primary key is that it is unique for each row in the table.
Data warehouses typically use a surrogate, (also known as artificial or identity key), key for the dimension tables primary keys. They can use Info sequence generator, or Oracle sequence, or SQL Server Identity values for the surrogate key.
It is useful because the natural primary key (i.e. Customer Number in Customer table) can change and this makes updates more difficult.
Some tables have columns such as AIRPORT_NAME OR CITY_NAME which are stated as the primary keys (according to the business users) but ,not only can these change, indexing on a numerical value is probably better and you could consider creating a surrogate key called, say, AIRPORT_ID. This would be internal to the system and as far as the client is concerned, you may display only the AIRPORT_NAME.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Linked Cube?

Linked cube in which a sub-set of the data can be analyzed into detail. The linking ensures that the data in the cubes remain consistent.

[Table of Contents](#Data-Warehousing-Architecture)

## What is meant by Metadata in Context of a Data Warehouse and how it is important?

Metadata is the data about data; Business Analyst or data modeler usually capture information about data - the source (where and how the data is originated), nature of data (char, varchar, nullable, existence, valid values etc) and behavior of data (how it is modified / derived and the life cycle) in data dictionary.
Metadata is also presented at the Datamart level, subsets, fact and dimensions, ODS etc. For a DW user, metadata provides vital information for analysis / DSS.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the possible Data Marts in Retail Sales?

Product information and sales information.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the various Etl Tools in the market?

Various ETL tools used in market are Informatica Data Stage Oracle Warehouse Builder Ab Initio Data Junction.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Dimensional Modeling?

Dimensional Modeling is a design concept used by many data warehouse designers to build their data warehouse. In this design model all the data is stored in two types of tables - Facts table and Dimension table. Fact table contains the facts/measurements of the business and the dimension table contains the context of measurements i.e., the dimensions on which the facts are calculated.Dimension modeling is a method for designing data warehouse. Three types of modeling are there
1. Conceptual modeling
2. Logical modeling
3. Physical modeling.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Vldb?

VLDB stands for Very Large Database. The threshold keeps moving: a one-terabyte database was a VLDB in the 1990s, while today warehouses routinely hold petabytes. VLDBs matter because they force different techniques: partitioning, columnar storage, parallel execution, and partition-level maintenance instead of row-level updates.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Degenerate Dimension Table?

Degenerate Dimensions: If a table contains the values, which r neither dimension nor measures is called degenerate dimensions. For example invoice id, employee no.A degenerate dimension is data that is dimensional in nature but stored in a fact table.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Er Diagram?

The Entity-Relationship (ER) model was originally proposed in 1976 as a way to unify the network and relational database views. Simply stated the ER model is a conceptual data model that views the real world as entities and relationships. A basic component of the model is the Entity-Relationship diagram, which is used to visually represent data objects. Since Chen wrote his paper the model has been extended and today it is commonly used for database design for the database designer, the utility of the ER model is: it maps well to the relational model. The constructs used in the ER model can easily be transformed into relational tables. It is simple and easy to understand with a minimum of training. Therefore, the database designer to communicate the design to the end user can use the model. In addition, the model can be used as a design plan by the database developer to implement a data model in specific database management software.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Snowflake and Star Schema and what are situations where Snowflake Schema is better than Star Schema?

Star schema contains the dimension tables mapped around one or more fact tables.It is a renormalized model and no need to use complicated joins. Also Queries results fast.Snowflake schema is the normalized form of Star schema. It contains in-depth joins, because the tables are spited in to many pieces. We can easily do modification directly in the tables.We have to use complicated joins, since we have more tables. There will be some delay in processing the Query.

[Table of Contents](#Data-Warehousing-Architecture)

## Can a Dimension Table contain numeric values?

Yes. However, those data type will be char (only the values can numeric/char).Yes, dimensions even contain numerical because these are descriptive elements of our business.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Hybrid Slowly Changing Dimension?

Hybrid SCDs are combination of both SCD 1 and SCD 2.It may happen that in a table, some columns are important and we need to track changes for them i.e. capture the historical data for them whereas in some columns even if the data changes, we don't care.For such tables we implement Hybrid SCDs, where in some columns are Type 1 and some are Type 2.You can add that it is not an intelligent key but similar to a sequence number and tied to a timestamp typically!

A hybrid SCD tracks history for some columns (Type 2) and overwrites others (Type 1) in the same dimension, usually
with a separate "history" flag per attribute group.

```sql
CREATE TABLE dim_customer (
    customer_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id TEXT NOT NULL,
    city        TEXT NOT NULL,      -- Type 2: history matters
    segment     TEXT NOT NULL,      -- Type 1: correct in place
    credit_tier TEXT NOT NULL,      -- Type 1
    start_date  DATE NOT NULL,
    end_date    DATE NOT NULL DEFAULT DATE '9999-12-31',
    is_current  BOOLEAN NOT NULL DEFAULT TRUE
);

-- Type 1 part: overwrite all versions of the segment.
UPDATE dim_customer d
SET    segment = s.segment
FROM   staging.customer_delta s
WHERE  d.customer_id = s.customer_id
  AND  d.segment IS DISTINCT FROM s.segment;

-- Type 2 part: version the city change.
UPDATE dim_customer d
SET    end_date = s.effective_date - INTERVAL '1 day', is_current = FALSE
FROM   staging.customer_delta s
WHERE  d.customer_id = s.customer_id AND d.is_current
  AND  d.city IS DISTINCT FROM s.city;
```

[Table of Contents](#Data-Warehousing-Architecture)

## How many clustered indexes can you create for a table in Dwh and in case Of Truncate and Delete command what happens to table which has unique Id.

You can have only one clustered index per table. If you use delete command, you can rollback... it fills your redo log files.
If you do not want records, you may use truncate command, which will be faster and does not fill your redo log file.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Loop in Data Warehousing?

In DWH loops may exist between the tables. If loops exist, then query generation will take more time, because more than one path is available. It creates ambiguity also. Loops can be avoided by creating aliases of the table or by context.
Example: 4 Tables - Customer, Product, Time, Cost forming a close loop. Create alias for the cost to avoid loop.

[Table of Contents](#Data-Warehousing-Architecture)

## What is an Error Log Table in Informatica occurs and how to maintain it in mapping?

Error Log in Informatica is a one of output file created by Informatica Server while running the session for error messages. It is created in Informatica home directory.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Drilling Across?

Drill across corresponds to switching from 1 classification in 1 dimension to a different classification in different dimension.

[Table of Contents](#Data-Warehousing-Architecture)

## Where the Cache Files stored?

Caches are stored in Repository.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Dimension Modeling?

A logical design technique that seeks to present the data in a standard, intuitive framework that allows for high-performance access. There are different data modeling concepts like ER Modeling (Entity Relationship modeling), DM (Dimensional modeling), Hierarchal Modeling, Network modeling. However, popular are ER and DM only.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Data Cleaning?

Data cleaning is a self-explanatory term. Most of the data warehouses in the world source data from multiple systems - systems that were created long before data warehousing was well understood, and hence without the vision to consolidate the same in a single repository of information. In such a scenario, the possibilities of the following are there:
► Missing information for a column from one of the data sources;
► Inconsistent information among different data sources;
► Orphan records;
► Outlier data points;
► Different data types for the same information among various data sources, leading to improper conversion;
► Data breaching business rules
In order to ensure that the data warehouse is not infected by any of these discrepancies, it is important to cleanse the data using a set of business rules, before it makes its way into the data warehouse.

[Table of Contents](#Data-Warehousing-Architecture)

## Can you explain the Hierarchies Level Data Warehousing?

In Data warehousing, levels are columns available in dimension table. Levels are having attributes. Hierarchies are used for navigational purpose; there are two types of Hierarchies. You can define hierarchies in top down or bottom up.
1. Natural Hierarchy: Best example is Time Dimension - Year, Month, Day etc. In natural Hierarchy definite relationship exists between each level
2. Navigational Hierarchy: You can have levels like
   Ex - Production cost of Product, Sales Cost of Product.
   Ex - Lead Time defined to procure, Actual Procurement time,
   In this, two levels need not to have relationship. This Hierarchy is created for navigational purpose.

[Table of Contents](#Data-Warehousing-Architecture)

## Can you explain about Core Dimension and Balanced Dimension and Dirty Dimension?

Dirty Dimension is nothing but Junk Dimensions. Core Dimensions are dedicated for a fact table or Data mart. Conformed Dimensions are used across fact tables or Data marts.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Core Dimension?

Core Dimension is a Dimension table, which is used dedicated for single fact table or Datamart. Conform Dimension is a Dimension table which is used across fact tables or Data marts.

[Table of Contents](#Data-Warehousing-Architecture)

## After we create a Scd Table can we use that Particular Dimension as a Dimension Table for Star Schema?

Yes.

[Table of Contents](#Data-Warehousing-Architecture)

## Suppose you are filtering rows using a Filter Transformation and only rows meet the condition pass to the Target so tell me where rows will go that does not meet condition.

Informatica filter transformation default value is 1 i.e. true. If you place a break point on filter transformation and run the mapping in a debugger mode, you will find these values 1 or 0 for each row passing through filter. If you change 0 to 1, the particular row will be passed to next stage.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Galaxy Schema?

Galaxy schema is also known as fact constellation scheme. It requires no of fact tables to share dimension tables. In data, wares housing mainly the people are using the conceptual hierarchy.

[Table of Contents](#Data-Warehousing-Architecture)

## Briefly state different between Data Ware House and Data Mart?

Data warehouse is made up of many datamarts. DWH contain many subject areas. However, data mart focuses on one subject area generally. E.g. If there will be DHW of bank then there can be one data mart for accounts, one for Loans etc. This is high-level definitions.

[Table of Contents](#Data-Warehousing-Architecture)

## What is MetaData?

Metadata is data about data. E.g. if in data mart we are receiving any file. Then metadata will contain information like how many columns, file is fix width/limited, ordering of fields, data types of field etc.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the Definitions for Datawarehose And Datamart?

Datamart is subset of Datawarehouse we can say a datamart is collection of individual departmental information...Where as datawarehouse in collection of datamart.
Data mart is a single subject and datawarehouse is a integration of multiple subjects.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Data Validation Strategies for Data Mart validation after Loading Process

Data validation is generally done manually in DWH in this case if source and TGT are relational you need to create SQL scripts to validate source and target data and if source isFlat file or non relational database you can use excel if data is very less or create dummy tables to validate your ETL code.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Data Mining?

Data Mining is the process of analyzing data from different perspectives and summarizing it into useful information.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Ods?

ODS is abbreviation of Operational Data Store. A database structure that is a repository for near real-time operational data rather than long term trend data. The ODS may further become the enterprise shared operational database, allowing operational systems that are being re-engineered to use the ODS as there operation databases.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Etl?

ETL is abbreviation of extract, transform, and load. ETL is software that enables businesses to consolidate their disparate data while moving it from place to place, and it doesn’t really matter that that data is in different forms or formats. The data can come from any source.ETL is powerful enough to handle such data disparities. First, the extract function reads data from a specified source database and extracts a desired subset of data. Next, the transform function works with the acquired data – using rules orlookup tables, or creating combinations with other data – to convert it to the desired state. Finally, the load function is used to write the resulting data to a target database.

ETL extracts from sources, transforms in a staging engine, and loads a dimensional target. ELT pushes the transform
into the warehouse after the load.

```text
Extract -> Transform (clean, conform, dedupe) -> Load (MERGE into dims and facts)
```

```sql
-- Extract and transform in one statement.
WITH extracted AS (
    SELECT * FROM staging.raw_orders WHERE ingest_date = CURRENT_DATE
),
cleaned AS (
    SELECT order_id, TRIM(UPPER(status)) AS status,
           CAST(amount AS NUMERIC(14, 2)) AS amount, order_date
    FROM extracted
    WHERE order_id IS NOT NULL
)
-- Load idempotently.
MERGE INTO fct_orders AS t
USING cleaned AS s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET status = s.status, amount = s.amount
WHEN NOT MATCHED THEN INSERT (order_id, status, amount, order_date)
    VALUES (s.order_id, s.status, s.amount, s.order_date);
```

[Table of Contents](#Data-Warehousing-Architecture)

## Is Oltp Database is design optimal for Data Warehouse?

No. OLTP database tables are normalized, and it will add additional time to query to return results. Additionally, OLTP database is smaller, and it does not contain longer period (many years) data, which needs to be analyzed. A OLTP system is basically ER model and not Dimensional Model. If a complex query is executed on a OLTP system, it may cause a heavy overhead on the OLTP server that will affect the normal business processes.

[Table of Contents](#Data-Warehousing-Architecture)

## If Denormalized is improves Data Warehouse Processes and why Fact Table is in Normal Form?

Foreign keys of facts tables are primary keys of Dimension tables. It is clear that fact table contains columns which are primary key to other table that itself make normal form table.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Lookup Tables?

A lookup table is the table placed on the target table based upon the primary key of the target, it just updates the table by allowing only modified (new or updated) records based on lookup condition.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Aggregate Tables?

Aggregate table contains the summary of existing warehouse data which is grouped to certain levels of dimensions. It is always easy to retrieve data from aggregated tables than visiting original table which has million records. Aggregate tables reduces the load in the database server and increases the performance of the query and can retrieve the result quickly.

[Table of Contents](#Data-Warehousing-Architecture)

## What is real time Datawarehousing?

Data warehousing captures business activity data. Real-time data warehousing captures business activity data as it occurs. As soon as the business activity is complete and there is data about it, the completed activity data flows into the data warehouse and becomes available instantly.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Conformed Dimensions?

Conformed dimensions mean the exact same thing with every possible fact table to which they are joined. They are common to the cubes.

A conformed dimension has identical keys, column names, and values in every fact table that uses it, so results can be
compared and drilled across.

```sql
-- One physical dimension, shared by sales, returns, and inventory.
CREATE TABLE dim_date (
    date_sk    BIGINT PRIMARY KEY,
    date       DATE   NOT NULL UNIQUE,
    year       INTEGER NOT NULL,
    quarter    INTEGER NOT NULL,
    month      INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL
);

SELECT 'sales' AS process, d.year, SUM(f.net_amount) AS amount
FROM fct_sales f JOIN dim_date d USING (date_sk) GROUP BY d.year
UNION ALL
SELECT 'returns', d.year, SUM(f.refund_amount)
FROM fct_returns f JOIN dim_date d USING (date_sk) GROUP BY d.year;
```

[Table of Contents](#Data-Warehousing-Architecture)

## How do you load the Time Dimension?

Time dimensions are usually loaded by a program that loops through all possible dates that may appear in the data. 100 years may be represented in a time dimension, with one row per day.

A date dimension is generated once for a fixed range rather than loaded from a source. One row per day, with
precomputed attributes, lets analysts filter by fiscal periods and holidays without functions on the fact column.

```sql
INSERT INTO dim_date (date_sk, date, year, quarter, month, month_name, day_of_week, is_weekend, fiscal_year)
SELECT
    CAST(TO_CHAR(d, 'YYYYMMDD') AS BIGINT) AS date_sk,
    d::date                                AS date,
    EXTRACT(YEAR FROM d)                   AS year,
    EXTRACT(QUARTER FROM d)                AS quarter,
    EXTRACT(MONTH FROM d)                  AS month,
    TO_CHAR(d, 'Mon')                      AS month_name,
    EXTRACT(ISODOW FROM d)                 AS day_of_week,
    EXTRACT(ISODOW FROM d) IN (6, 7)       AS is_weekend,
    CASE WHEN EXTRACT(MONTH FROM d) >= 4
         THEN EXTRACT(YEAR FROM d) ELSE EXTRACT(YEAR FROM d) - 1 END AS fiscal_year
FROM generate_series(DATE '2020-01-01', DATE '2030-12-31', INTERVAL '1 day') AS d;
```

Python equivalent when the warehouse has no `generate_series`:

```python
from datetime import date, timedelta

start, end = date(2020, 1, 1), date(2030, 12, 31)
rows = []
day = start
while day <= end:
    rows.append({
        "date_sk": int(day.strftime("%Y%m%d")),
        "date": day.isoformat(),
        "year": day.year,
        "quarter": (day.month - 1) // 3 + 1,
        "is_weekend": day.weekday() >= 5,
    })
    day += timedelta(days=1)
assert len(rows) == 4018
```

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Level of Granularity of a Fact Table?

Level of granularity means level of detail that you put into the fact table in a data warehouse. Level of granularity would mean what detail are you willing to put for each transactional fact.

Grain is the exact meaning of one fact row. Declare it before choosing dimensions or measures, and never mix grains in
one table.

```text
Coarse: one row per day per store per product    -> fct_sales_daily
Fine:   one row per order line                   -> fct_order_line
```

```sql
-- Declared grain: one row per order line, per event.
CREATE TABLE fct_order_line (
    order_number TEXT    NOT NULL,
    line_number  INTEGER NOT NULL,
    date_sk      BIGINT  NOT NULL,
    product_sk   BIGINT  NOT NULL,
    quantity     INTEGER NOT NULL,
    net_amount   NUMERIC(14, 2) NOT NULL,
    PRIMARY KEY (order_number, line_number)
);
```

A fact table is at the finest grain you can afford. Coarser aggregate tables can be built from it, but a coarse fact
can never be drilled back to the detail you did not store.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Non additive facts?

Non-additive facts are facts that cannot be summed up for any of the dimensions present in the fact table. However, they are not considered as useless. If there is changes in dimensions the same facts can be useful.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Factless Facts Table?

A fact table which does not contain numeric fact columns it is called factless facts table.

A factless fact table stores only dimension keys, so `COUNT(*)` is the measure. It answers coverage and
eligibility questions that measures cannot.

```sql
-- Which products were on promotion in which store, even if nothing sold?
CREATE TABLE fct_promotion_coverage (
    date_sk      BIGINT NOT NULL,
    product_sk   BIGINT NOT NULL,
    store_sk     BIGINT NOT NULL,
    promotion_sk BIGINT NOT NULL,
    PRIMARY KEY (date_sk, product_sk, store_sk, promotion_sk)
);

SELECT COUNT(DISTINCT product_sk) AS promoted_products
FROM fct_promotion_coverage
WHERE date_sk = 20261004;
```

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Olap?

OLAP is known as online analytical processing which provides answers to queries which are multi dimensional in nature. It composes relational reporting and data mining for providing solutions to business intelligence. This term OLAP is created from the term OLTP.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about the Functionality of Olap?

Hyper cube or multidimensional cube forms the core of OLAP system. This consists of measures which are arranged according to dimensions. Hyper cube Meta data is created by star or snow flake schema of tables in RDBMS. Dimensions are extracted from dimension table and measures from the fact table.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Molap?

Classic form of OLAP is known as MOLAP and it is often called as OLAP. Simple database structures such as time period, product, location, etc. are used. Functioning of each and every dimension or data structure is defined by one or more hierarchies.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Rolap?

Functioning of ROLAP occurs simultaneously with relational databases. Data and tables are stored as relational tables. To hold new information or data new tables are created. Functioning of ROLAP depends upon specialized schema design.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Aggregations?

OLAP can process complex queries and give the output in less than 0.1 seconds, for it to achieve such a performance OLAP uses aggregations. Aggregations are built by aggregating and changing the data along the dimensions. Possible combination of aggregations can be determined by the combination possibilities of dimension granularities.

```sql
-- Three useful aggregation shapes in one query.
SELECT
    COALESCE(p.category, 'ALL')        AS category,
    COALESCE(d.year, 0)                AS year,
    SUM(f.net_amount)                  AS revenue,
    COUNT(DISTINCT f.customer_sk)      AS customers
FROM fct_sales f
JOIN dim_product p ON p.product_sk = f.product_sk
JOIN dim_date d    ON d.date_sk = f.date_sk
GROUP BY GROUPING SETS ((p.category, d.year), (p.category), ());
```

Distinct counts do not re-aggregate from a coarser table, so either keep them at the detail grain or use a
sketch such as HyperLogLog.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about the View Selection problem?

Often calculating all the data is not possible by aggregations for this reason some complex data problems are solved. In order to determine which data should be solved and calculated, developers use View selection application. This solution is often used to reduce calculation problem.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about the role of Bitmap Indexes to solve Aggregation Problems?

Bitmaps are very useful in start schema to join large databases to small databases. Answer queries and bit arrays are used to perform logical operations on the databases. Bit map indexes are very efficient in handling Gender differentiation; also repetitive tasks are performed with much larger efficiency.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Encoding Technique used in Bitmaps Indexes?

Bitmaps commonly use one bitmap for every single distinct value. Number of bitmaps used can be reduced by opting for a different type of encoding. Space can be optimized but when a query is generated bitmaps have to be accessed.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Binning?

Binning process is very useful to save space. Performance may vary depending upon the query generated sometimes solution to a query can come within few seconds and sometimes it may take longer time. Binning process holds multiple values in the same bin.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Hybrid Olap?

When a database developer uses Hybrid OLAP it divides the data between relational and specialized storage. In some particular modifications a HOLAP database may store huge amounts of data in its relational tables. Specialized data storage is used to store data which is less detailed and more aggregate.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Shared Features of Olap?

Shared implements most of the security features into OLAP. If multiple accesses are required admin can make necessary changes. The default security level for all OLAP products is read only. For multiple updates it is predominant to make necessary security changes.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Analysis?

Analysis defines about the logical and statistical analysis required for an efficient output. This involves writing of code and performing calculations, but most part of these languages does not require complex programming language knowledge. There are many specific features which are included such as time analysis, currency translation, etc.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about Multidimensional Features present in Olap?

Multidimensional support is very essential if we are to include multiple hierarchies in our data analysis. Multidimensional feature allows a user to analyze business and organization. OLAP efficiently handles support for multidimensional features.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain about the Database Marketing Application of Olap?

Database marketing tool or application helps a user or marketing professional in determining the right tool or strategy for his valuable add campaign. This tool collects data from all sources and gives relevant information the specialist with their add campaign. It gives a complete picture to the developer.

[Table of Contents](#Data-Warehousing-Architecture)

## Compare Data Warehouse Database and Oltp Database.

The data warehouse and the OLTP data base are bothrelational databases. However, the objectives of both these databases are different.
The OLTP database records transactions in real time and aims to automate clerical data entry processes of a business entity. Addition, modification and deletion of data in the OLTP database is essential and the semantics of the applicationused in the front end impact on the organization of the data in the database.
The data warehouse on the other hand does not cater to real time operational requirements of the enterprise. It is more a storehouse of current and historical data and may alsocontain data extracted from external data sources.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Etl Tool and Olap Tool and what are various Etl in the Market?

ETL is an extraction,transformation,loading tool i.e u can extract , u can transform using different transformations available in tool and aggreagte the data. The output of thisETL tool is used as input to OLAP tool.
OLAP is online analytical process, where u can get online reports after doing some joines,creating some cubes

ETL tools in market
1 INFORMATICA-- univeral tool ,good market
2 ABINITO -- fastest loading tool,very good market
3 DATASTAGE-- difficult work, no good market
4 BODI-- good market
5 ORACLE WAREHOUSE BUILDER-- good market.

[Table of Contents](#Data-Warehousing-Architecture)

## Steps in building the Data Model.

While ER model lists and defines the constructs required to build a data model, there is no standard process for doing so. Some methodologies, such as IDEFIX, specify a bottom-up.

[Table of Contents](#Data-Warehousing-Architecture)

## Why is Data Modeling important?

Data modeling is probably the most labor-intensive and time-consuming part of the development process. Why bother especially if you are pressed for time? A common.

[Table of Contents](#Data-Warehousing-Architecture)

## What Type of Indexing Mechanism do we need use for a typical Datawarehouse?

On the fact table it is best to use bitmap indexes. Dimension tables can use bitmap and/or the other types of clustered/non-clustered, unique/non-unique indexes.
To my knowledge, SQLServer does not support bitmap indexes. Only Oracle supports bitmaps.

Typical warehouse strategy:

+ Fact table: partition by date, cluster or sort by the most common join/filter keys, rely on zone maps and statistics.
+ Dimension tables: primary key on the surrogate key, unique index on the natural key, B-tree on frequently filtered attributes.
+ Low-cardinality flags: bitmap indexes where the engine supports them.
+ Skip indexes: min/max statistics and bloom filters in Snowflake, BigQuery, and Delta/Iceberg.

```sql
-- Clustering key drives micro-partition pruning in Snowflake.
ALTER TABLE fct_sales CLUSTER BY (sale_date, store_sk);

-- Zone maps are built from sort order in many MPP warehouses.
CREATE TABLE fct_sales_ordered AS
SELECT * FROM fct_sales ORDER BY sale_date, store_sk;
```

[Table of Contents](#Data-Warehousing-Architecture)

## What are Semi additive and Factless Facts?

Semi-Additive: Semi-additive facts are facts that can be summed up for some dimensions in the fact table, but not the others. For example:
Current_Balance and Profit_Margin are the facts. Current_Balance is a semi-additive fact, as it makes sense to add them up for all accounts (what's the total current balance for all accounts in the bank?), but it does not make sense to add them up through time (adding up all current balances for a given account for each day of the month does not give us any useful information A factless fact table captures the many-to-many relationships between dimensions, but contains no numeric or textual facts. They are often used to record events or coverage information.
Common examples of factless fact tables include:

- Identifying product promotion events (to determine promoted products that didn?t sell)
- Tracking student attendance or registration events
- Tracking insurance-related accident events
- Identifying building, facility, and equipment schedules for a hospital or university.

[Table of Contents](#Data-Warehousing-Architecture)

## Is it correct develop a Data Mart using an Ods?

Yes it is correct to develop a Data Mart using an ODS.becoz ODS which is used to?store transaction data and few Days (less historical data) this is what datamart is required, so it is coct to develop datamart using ODS .

[Table of Contents](#Data-Warehousing-Architecture)

## Explain degenerated dimension.

A Degenerate dimension?is a?Dimension which has only a single attribute.
This dimension is typically represented as a single field in a fact table.
The data items thar are not facts and data items that do not fit into the existing dimensions are termed as Degenerate Dimensions.
Degenerate Dimensions are the fastest way to group similar transactions.
Degenerate Dimensions are used when fact tables represent transactional data.
They can be used as primary key for the fact table but they cannot act as foreign keys.

A degenerate dimension is a dimension key with no dimension table, kept on the fact row itself. Order number and
invoice number are the classic examples.

```sql
CREATE TABLE fct_order_line (
    order_number TEXT   NOT NULL,      -- degenerate dimension
    line_number  INTEGER NOT NULL,
    date_sk      BIGINT NOT NULL REFERENCES dim_date(date_sk),
    product_sk   BIGINT NOT NULL REFERENCES dim_product(product_sk),
    quantity     INTEGER NOT NULL,
    net_amount   NUMERIC(14, 2) NOT NULL,
    PRIMARY KEY (order_number, line_number)
);

-- Group by the degenerate key without joining a dimension.
SELECT order_number, COUNT(*) AS lines, SUM(net_amount) AS order_total
FROM fct_order_line
GROUP BY order_number
HAVING SUM(net_amount) > 1000;
```

[Table of Contents](#Data-Warehousing-Architecture)

## What are the different methods of loading Dimension Tables?

Conventional Load:
Before loading the data, all the Table constraints will be checked against the data.
Direct load:(Faster Loading)
All the Constraints will be disabled. Data will be loaded directly.Later the data will be checked against the table constraints and the bad data won't be indexed.

Two loading styles dominate: full rebuild and incremental merge.

```sql
-- Full rebuild: simple, safe for small dimensions, swaps the table atomically.
CREATE TABLE dim_product_new AS
SELECT
    ROW_NUMBER() OVER (ORDER BY product_id) AS product_sk,
    product_id, product_name, category, subcategory
FROM   staging.product_snapshot;

BEGIN;
ALTER TABLE dim_product RENAME TO dim_product_old;
ALTER TABLE dim_product_new RENAME TO dim_product;
COMMIT;

-- Incremental MERGE: upsert new and changed attributes into a Type 1 dimension.
MERGE INTO dim_product AS d
USING staging.product_delta AS s
   ON d.product_id = s.product_id
WHEN MATCHED AND (d.product_name, d.category) IS DISTINCT FROM (s.product_name, s.category)
    THEN UPDATE SET
        product_name = s.product_name,
        category     = s.category,
        updated_at   = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
    INSERT (product_id, product_name, category, updated_at)
    VALUES (s.product_id, s.product_name, s.category, CURRENT_TIMESTAMP);
```

Conventional load validates constraints before inserting; direct-path load disables them for speed and validates
afterwards. Use direct-path only when you can prove the data is clean.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Slowly Changing Dimensions?

Dimensions that change over time are called Slowly Changing Dimensions. For instance, a product price changes over time; People change their names for some reason; Country and State names may change over time. These are a few examples of Slowly Changing Dimensions since some changes are happening to them over a period of time.
If the data in the Dimension table happen to change very rarely,then it is called as slowly changing dimension.
ex: changing the name and address of a person,which happens rerely.

The three classic SCD strategies, with SQL.

SCD Type 1 overwrites the attribute and loses history.

```sql
UPDATE dim_customer
SET    city = s.city,
       updated_at = CURRENT_TIMESTAMP
FROM   staging.customer_delta s
WHERE  dim_customer.customer_id = s.customer_id
  AND  dim_customer.is_current
  AND  dim_customer.city IS DISTINCT FROM s.city;
```

SCD Type 2 closes the current row and inserts a new version.

```sql
-- 1. Close the rows that changed.
UPDATE dim_customer d
SET    end_date   = s.effective_date - INTERVAL '1 day',
       is_current = FALSE
FROM   staging.customer_delta s
WHERE  d.customer_id = s.customer_id
  AND  d.is_current
  AND  (d.city, d.segment) IS DISTINCT FROM (s.city, s.segment);

-- 2. Insert the new current versions.
INSERT INTO dim_customer
       (customer_sk, customer_id, city, segment, start_date, end_date, is_current)
SELECT nextval('dim_customer_sk_seq'),
       s.customer_id, s.city, s.segment, s.effective_date,
       DATE '9999-12-31', TRUE
FROM   staging.customer_delta s
JOIN   dim_customer d
       ON d.customer_id = s.customer_id
      AND d.is_current = FALSE
      AND d.end_date = s.effective_date - INTERVAL '1 day'
WHERE  NOT EXISTS (
           SELECT 1 FROM dim_customer c
           WHERE c.customer_id = s.customer_id
             AND c.is_current
             AND c.city = s.city
             AND c.segment = s.segment
       );
```

SCD Type 3 keeps only the previous value in an extra column.

```sql
ALTER TABLE dim_customer
    ADD COLUMN previous_city  TEXT,
    ADD COLUMN city_changed_at TIMESTAMP;

UPDATE dim_customer
SET    previous_city = city,
       city = s.city,
       city_changed_at = CURRENT_TIMESTAMP
FROM   staging.customer_delta s
WHERE  dim_customer.customer_id = s.customer_id;
```

Choose Type 1 for corrections, Type 2 when the business must reproduce history, and Type 3 only for a single
"before vs after" comparison where full history is not required.

[Table of Contents](#Data-Warehousing-Architecture)

## What is meant by Metadata in context of a Datawarehouse?

Metadata or Meta Data Metadata is data about data. Examples of metadata include data element descriptions, data type descriptions, attribute/property descriptions, range/domain descriptions, and process/method descriptions. The repository environment encompasses all corporate metadata resources: database catalogs, data dictionaries, and navigation services. Metadata includes things like the name, length, valid values, and description of a data element. Metadata is stored in a data dictionary and repository. It insulates the data warehouse from changes in the schema of operational systems. Metadata Synchronization The process of consolidating, relating and synchronizing data elements with the same or similar meaning from different systems. Metadata synchronization joins these differing elements together in the data warehouse to allow for easier access.

Metadata describes the data: schemas, owners, freshness, lineage, and quality. Warehouses store it in the catalog.

```sql
-- Technical metadata stored alongside the model.
INSERT INTO meta.table_catalog (table_name, layer, owner, grain, freshness_sla_minutes)
VALUES ('fct_sales', 'gold', 'revenue-team', 'one row per order line', 60);

-- Lineage edges power impact analysis.
INSERT INTO meta.lineage (upstream, downstream)
VALUES ('staging.orders', 'marts.fct_orders'),
       ('marts.fct_orders', 'bi.v_order_revenue');

SELECT downstream FROM meta.lineage WHERE upstream = 'staging.orders';
```

[Table of Contents](#Data-Warehousing-Architecture)

## What are Modeling Tools available in the Market

These tools are used for Data/dimension modeling
Oracle Designer
ERWin (Entity Relationship for windows)
Informatica (Cubes/Dimensions)
Embarcadero
Power Designer Sybase.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the main difference between Schema in Rdbms and Schemas in Datawarehouse?

RDBMS Schema
* Used for OLTP systems
* Traditional and old schema
* Normalized
* Difficult to understand and navigate
* Cannot solve extract and complex problems
* Poorly modelled
  DWH Schema
* Used for OLAP systems
* New generation schema
* De Normalized
* Easy to understand and navigate
* Extract and complex problems can be easily solved
* Very good model.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a general purpose Scheduling Tool?

The basic purpose of the scheduling tool in a DW Application is to streamline the flow of data from Source To Target at specific time or based on some condition.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the need of Surrogate Key and why Primary Key not used as Surrogate Key?

Surrogate Key is an artificial identifier for an entity. In surrogate key values are generated by the system sequentially(Like Identity property in SQL Server and Sequence in Oracle). They do not describe anything. Primary Key is a natural identifier for an entity. In Primary keys all the values are entered manually by the user which are uniquely identified. There will be no repetition of data.

The primary key of a source table identifies one current row; a warehouse needs a stable key that also identifies
historical versions and survives source migrations.

```sql
-- Natural key changes: the source reuses customer IDs after a merger.
INSERT INTO dim_customer (customer_id, name, start_date)
VALUES ('C-100', 'Acme (legacy)', DATE '2024-01-01'),
       ('C-100', 'Acme (merged)',  DATE '2026-01-01');

-- The surrogate key disambiguates both versions.
SELECT customer_sk, customer_id, name, start_date, is_current
FROM dim_customer
WHERE customer_id = 'C-100'
ORDER BY start_date;
```

[Table of Contents](#Data-Warehousing-Architecture)

## What is Snow Flake Schema?

Snowflake schemas normalize dimensions to eliminate redundancy. That is, the dimension data has been grouped into multiple tables instead of one large table. For example, a product dimension table in a star schema might be normalized into a products table, a product_category table, and a product_manufacturer table in a snowflake schema. While this saves space, it increases the number of dimension tables and requires more foreign key joins. The result is more complex queries and reduced query performance.

```sql
-- Normalized dimension chain: geography <- store <- fact
CREATE TABLE dim_geography (
    geography_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country      TEXT NOT NULL,
    region       TEXT NOT NULL,
    city         TEXT NOT NULL
);

CREATE TABLE dim_store (
    store_sk     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    store_id     TEXT NOT NULL UNIQUE,
    store_name   TEXT NOT NULL,
    geography_sk BIGINT NOT NULL REFERENCES dim_geography(geography_sk)
);

SELECT g.region, SUM(f.net_amount) AS revenue
FROM fct_sales f
JOIN dim_store s     ON s.store_sk = f.store_sk
JOIN dim_geography g ON g.geography_sk = s.geography_sk
GROUP BY g.region;
```

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Oltp and Olap?

OLTP is nothing but OnLine Transaction Processing ,which contains a normalised tables and online data,which have frequent insert/updates/delete.

[Table of Contents](#Data-Warehousing-Architecture)

## How are the Dimension Tables designed?

Find where data for this dimension are located.
Figure out how to extract this data.
Determine how to maintain changes to this dimension.
Change fact table and DW population routines.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the advantages Data Mining over traditional approaches?

Data Mining is used for?the estimation of future. For example,?if we take a company/business organization, by using the concept of Data Mining, we can predict the future of business interms of Revenue (or) Employees (or) Cutomers (or) Orders etc.
Traditional approaches use?simple algorithms?for estimating the future. But, it does not give accurate results when compared to Data Mining.

[Table of Contents](#Data-Warehousing-Architecture)

## Which automation tool is used in Data Warehouse testing?

Testing is automated like any other software layer. Common choices are dbt tests for model-level assertions, Great Expectations or Soda for data quality suites, and a scheduler (Airflow, dbt Cloud) to run them as pipeline gates. Reconciliation between source and target is usually a SQL script that compares aggregates and fails on a variance above a documented tolerance.

[Table of Contents](#Data-Warehousing-Architecture)

## Give examples of Degenerated Dimensions.

Degenerated Dimension is a dimension key without corresponding dimension. Example:
In the PointOfSale Transaction Fact table, we have:
Date Key (FK), Product Key (FK), Store Key (FK), Promotion Key?(FP),?and POS Transaction Number?? Date Dimension corresponds to Date Key, Production Dimension corresponds to Production Key. In a traditional parent-child database, POS Transactional Number would be?the key to the transaction header record that contains all the info valid for the transaction as a whole, such as the transaction date and store?identifier.?But in this?dimensional model, we have already extracted this info into other dimension. Therefore, POS Transaction Number?looks like a dimension key in the fact table but does not have the corresponding dimension table.
Therefore, POS Transaction Number is a degenerated dimension.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the datatype of the Surrogate Key?

Normally Surrogate keys are sequencers which keep on increasing with new records being injected into the table. The standard datatype is integer.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between scan Component and Rollup Component?

Rollup is for group by and Scan is for successive total. Basically, when we need to produce summary then we use scan. Rollup is used to aggregate data.

[Table of Contents](#Data-Warehousing-Architecture)

## What is M_dump?

m_dump command prints the data in a formatted way.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Brodcasting and Replicate?

Broadcast - Takes data from multiple inputs, combines it and sends it to all the output ports.
Eg - You have 2 incoming flows (This can be data parallelism or component parallelism) on Broadcast component, one with 10 records & other with 20 records. Then on all the outgoing flows (it can be any number of flows) will have 10 + 20 = 30 records.
Replicate - It replicates the data for a particular partition and send it out to multiple out ports of the component, but maintains the partition integrity.
Eg - Your incoming flow to replicate has a data parallelism level of 2. with one partition having 10 recs & other one having 20 recs. Now suppose you have 3 output flos from replicate. Then each flow will have 2 data partitions with 10 & 20 records respectively.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Local and Formal Parameter?

Two are graph level parameters but in local you need to initialize the value at the time of declaration where as globle no need to initialize the data it will promt at the time of running the graph for that parameter.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Dml Expression and Xfr Expression?

The main difference b/w dml & xfr is that
DML represent format of the metadata.
XFR represent the tranform functions.which will contain business rules

[Table of Contents](#Data-Warehousing-Architecture)

## Have you used Rollup Component?

If the user wants to group the records on particular field values then rollup is best way to do that. Rollup is a multi-stage transform function and it contains the following mandatory functions.
1. initialise
2. rollup
3. finalise
   Also need to declare one temporary variable if you want to get counts of a particular group.

For each of the group, first it does call the initialise function once, followed by rollup function calls for each of the records in the group and finally calls the finalise function once at the end of last rollup call.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Primary Keys and Foreign Keys?

In RDBMS the relationship between the two tables is represented as Primary key and foreign key relationship. Whereas the primary key table is the parent table and foreignkey table is the child table.The criteria for both the tables is there should be a matching column.

```sql
CREATE TABLE dim_customer (
    customer_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id TEXT   NOT NULL UNIQUE
);

CREATE TABLE fct_sales (
    sale_id     BIGINT NOT NULL,
    sale_date   DATE   NOT NULL,
    customer_sk BIGINT NOT NULL REFERENCES dim_customer(customer_sk),
    net_amount  NUMERIC(14, 2) NOT NULL,
    PRIMARY KEY (sale_id, sale_date)
);
```

Warehouse nuance: some columnar engines do not enforce foreign keys, but declaring them still documents the model
and lets optimizers use them for join elimination and pruning.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Outer Join?

An outer join is used when one wants to select all the records from a port - whether it has satisfied the join criteria or not.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Cartesian Joins?

A Cartesian join will get you a Cartesian product. A Cartesian join is when you join every row of one table to every row of another table. You can also get one by joining every row of a table to every row of itself.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the purpose of having Stored Procedures in a Database?

Main Purpose of Stored Procedure for reduse the network trafic and all sql statement executing in cursor so speed too high.

[Table of Contents](#Data-Warehousing-Architecture)

## Why might you create a Stored Procedure with Recompile Option?

Recompile is useful when the tables referenced by the stored proc undergoes a lot of modification/ deletion/ addition of data. Due to the heavy modification activity the execute plan becomes outdated and hence the stored proc performance goes down. If we create the stored proc with recompile option, the sql server wont cache a plan for this stored proc and it will be recompiled every time it is run.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Cursor?

The oracle engine uses work areas for internal processing in order to the execute sql statement is called cursor.There are two types of cursors like Implecit cursor and Explicit cursor.Implicit cursor is using for internal processing and Explicit cursor is using for user open for data required.

[Table of Contents](#Data-Warehousing-Architecture)

## Describe process steps you would perform when Defragmenting a Data Table and this table contains mission critical Data?

There are several ways to do this:
1) We can move the table in the same or other tablespace and rebuild all the indexes on the table.
   alter table move this activity reclaims the defragmented space in the table
   analyze table table_name compute statistics to capture the updated statistics.
   2)Reorg could be done by taking a dump of the table, truncate the table and import the dump back into the table.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain the difference between Truncate and Delete Commands?

Truncate :
+ It is a DDL command, used to delete tables or clusters. Since it is a DDL command hence it is auto commit and Rollback can't be performed. It is faster than delete.

Delete:
+ It is DML command, generally used to delete a record, clusters or tables. Rollback command can be performed , in order to retrieve the earlier deleted things. To make deleted things permanently, "commit" command should be used.

+ `DELETE` is DML: it is transactional, filterable, fires triggers, and can be rolled back, but it writes undo.
+ `TRUNCATE` is DDL: it deallocates all rows, is much faster, and usually cannot be rolled back. It cannot filter.

```sql
-- DELETE: remove one partition worth of rows with a predicate.
DELETE FROM fct_sales WHERE sale_date < DATE '2020-01-01';

-- TRUNCATE: rebuild a staging table.
TRUNCATE TABLE staging.orders;

-- Best of both in a partitioned warehouse: drop the partition.
ALTER TABLE fct_sales DROP PARTITION fct_sales_2020_01;
```

[Table of Contents](#Data-Warehousing-Architecture)

## How would you find out whether Sql Query is using Indices you Expect?

Explain plan can be reviewed to check the execution plan of the query. This would guide if the expected indexes are used or not.

Read the plan, not the SQL. `EXPLAIN` shows the chosen access path; `EXPLAIN ANALYZE` shows actual row counts and
timings so you can spot a bad estimate.

```sql
EXPLAIN ANALYZE
SELECT c.customer_id, SUM(o.amount) AS revenue
FROM fct_orders o
JOIN dim_customer c ON c.customer_sk = o.customer_sk
WHERE o.order_date >= DATE '2026-01-01'
GROUP BY c.customer_id;

-- Look for: index scan vs sequential scan, partition pruning, and estimated vs actual rows.
```

Common causes of an ignored index: a function applied to the indexed column, a stale statistic, an implicit type
cast, or a predicate that matches most of the table anyway.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Security Level used in Bo?

We have securities in business objects
Like
1.Windows authentication
2.RDBMS securities
3.supervisor level securities, ie Username/ password.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Functional and Architectural differences between Business Objects and Web Intelligence Reports?

Functional differences
• Business objects, for building or accessing reports, needs to be installed on every pc. On the other hand, Web intelligence reports needs a browser and a URL of the server from where Business objects will be accessed.
• BOMain.key needs to be copied on every pc using BO client. This is not required for Web Intelligence Reports.
• Business objects expect you to use the same pc where they are installed. Web Intelligence reports can be accessed from anywhere, provided internet is available.

Architectural differences
For BO client, for sending info to BO Server BOMain.key, uses the key of the local drive. Once the information is sent, it is validated and checked into the repository upon which the user can access the BO services. On the other hand, Web Intelligence the web servers BOMain.key is used to check privilege of the user and then sending information to the BO Server BOMain.key.

[Table of Contents](#Data-Warehousing-Architecture)

## What is batch processing in Business Objects?

Batch processing can be used to schedule reports. Objects can be also be used for batch processing. Batch processing can be used to also select the objects to be processed. The batch can be run as a transaction in which if one process fails, the entire batch is rolled back or it can be run as a series of jobs.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Data Cardinality?

Cardinality is the term used in database relations to denote the occurrences of data on either side of the relation.
There are 3 basic types of cardinality:
High data cardinality:
Values of a data column are very uncommon.
e.g.: email ids and the user names

Normal data cardinality:
Values of a data column are somewhat uncommon but never unique.
e.g.: A data column containing LAST_NAME (there may be several entries of the same last name)

Low data cardinality:
Values of a data column are very usual.
e.g.: flag statuses: 0/1

[Table of Contents](#Data-Warehousing-Architecture)

## What is Chained Data Replication?

In Chain Data Replication, the non-official data set distributed among many disks provides for load balancing among the servers within the data warehouse.
Blocks of data are spread across clusters and each cluster can contain a complete set of replicated data. All data block in every cluster is a unique permutation of the data in other clusters.
When a disk fails then all the calls made to the data in that disk are redirected to the other disks when the data has been replicated.
At times replicas and disks are added online without having to move around the data in the existing copy or affect the arm movement of the disk.
In load balancing, Chain Data Replication has multiple servers within the data warehouse share data request processing since data already have replicas in each server disk.

[Table of Contents](#Data-Warehousing-Architecture)

## Explain in brief various fundamental stages of Data Warehousing.

The following are the stages of data warehousing:
Offline Operational Database: It is the stage where copying the data off an operational system to another server where the report processing load against the copied data takes place and OS performance does not impact.
Offline Data Warehouse: In this stage, data warehouses are updated from data in the OS and the data of data warehouse is stored in a data structure that is designed for facilitating reports.
Real time Data Warehouse: The data warehouses are updated often when an OS performs a transaction.
Integrated Data Warehouse: The data warehouses are updated by OS, at the time of performing a transaction. Then transactions are generated which are passed back into the operational systems.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Enterprise Data Warehouse and Data Warehouse?

Big Organizations have a lot of diversified sources of data.There might be a dataware house exclusively for transport and others for data related to the project the company runs.In such case the complete enterprise's(company's) date ware house is a big combination of all and is known the Enterprise data Warehouse(EDW)

[Table of Contents](#Data-Warehousing-Architecture)

## Give me any example of Semi and Non Additive Measures?

Semi-Additive: Semi-additive facts are facts that can be summed up for some dimensions in the fact table, but not the others. Non-Additive: Non-additive facts are facts that cannot be summed up for any of the dimensions present in the fact table. Current Balance and Profit Margin are the facts.Current Balance is a semi-additive fact, as it makes sense to add them up for all accounts (what's the total current balance for all accounts in the bank?), but it does not make sense to add them up through time (adding up all current balances for a given account for each day of the month does not give us any useful information). Profit Margin is a non-additive fact, for it does not make sense to add them up for the account level or the day level.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the options in the Target Session of Update Strategy Transformations?

+ Insert
+ Delete
+ Update
+ Update as update
+ Update as insert
+ Update else insert
+ Truncate table

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Various Types of Transformation?

Various types of transformation are: Aggregator Transformation, Expression Transformation, Filter
Transformation, Joiner Transformation, Lookup Transformation, Normalizer Transformation, Rank Transformation,
Router Transformation, Sequence Generator Transformation, Stored Procedure Transformation, Sorter
Transformation, Update Strategy Transformation, XML Source Qualifier Transformation, Advanced External
Procedure Transformation, External Transformation.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Active Transformation and Passive Transformation?

An active transformation can change the number of rows that pass through it, but a passive transformation can not change the number of rows that pass through it.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the difference between Static Cache and Dynamic Cache?

In case of dynamic cache, when we are inserting a new row it checks the lookup cache to see if it exists, if not inserts it into the target as well as the cache but in case of static cache the new row is written only in the target and not the lookup cache. The lookup cache remains static and does not change during the session but incase of dynamic cache the server inserts, updates in the cache during session.

[Table of Contents](#Data-Warehousing-Architecture)

## How do we join Two tables without Joiner or Sql Override?

We can join the tables using lookup transformation and making a cartesian product.

[Table of Contents](#Data-Warehousing-Architecture)

## Differences between Normalizer and Normalizer Transformation.

Normalizer: It is a transformation mainly using for cobol sources,
it's change the rows into columns and columns into rows
Normalization:To remove the redundancy and inconsistency.

What Is The Use Of Incremental Aggregation? Explain Me In Brief With An Example.
It's a session option. when the informatica server performs incremental aggr. it passes new source data through the mapping and uses historical cache data to perform new aggregation caluculations incrementaly. for performance we will use it.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Business Intelligence?

Business Intelligence is a process for increasing the competitive advantage of a business by intelligent use of available data in decision-making.
The five key stages of Business Intelligence:
► Data Sourcing
► Data Analysis
► Situation Awareness
► Risk Assessment
► Decision Support.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Universe in Business Intelligence?

"universe" is a "Business object" terminology. Business objects also happens to be the name of the company. The universe is the interfacing layer between the client and the datawarehouse . The universe defines the relationship among the various tables in the datawarehouse.
Or Universe is a semantic layer between the database and the user interface (reports).

[Table of Contents](#Data-Warehousing-Architecture)

## What is Olap in Business Intelligence?

Online Analytical Processing, a category of software tools that provides analysis of data stored in a database. OLAP tools enable users to analyze different dimensions of multidimensional data. For example, it provides time series and trend analysis views. The chief component of OLAP is the OLAP server, which sits between a client and a database management systems (DBMS). The OLAP server understands how data is organized in the database and has special functions analyzing the data.
A good OLAP interface has writes an efficient sql and reads an accurate data from db.To design and architect having good knowledge on DB understanding the report requirements.

[Table of Contents](#Data-Warehousing-Architecture)

## What are various Modules in Business Objects Product?

► Business Objects Reporter
► Reporting & Analyzing tool
► Designer
► Universe creation
► database interaction
► connectivity
Supervisor - For Administrative purposes
Webintelligence - Access of report data through internet
BroadCast Agent - For scheduling the reports
Data Integrator - The ETL tool of Business Objects, designed to handle huge amounts of data.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Olap Molap Rolap Dolap Holap?

OLAP - On-Line Analytical Processing.
Designates a category of applications and technologies that allow the collection, storage, manipulation and reproduction of multidimensional data, with the goal of analysis.

MOLAP - Multidimensional OLAP.
This term designates a cartesian data structure more specifically. In effect, MOLAP contrasts with ROLAP. Inb the former, joins between tables are already suitable, which enhances performances. In the latter, joins are computed during the request.
Targeted at groups of users because it's a shared environment. Data is stored in an exclusive server-based format. It performs more complex analysis of data.

DOLAP - Desktop OLAP.
Small OLAP products for local multidimensional analysis Desktop OLAP. There can be a mini multidimensional database (using Personal Express), or extraction of a datacube (using Business Objects).
Designed for low-end, single, departmental user. Data is stored in cubes on the desktop. It's like having your own spreadsheet. Since the data is local, end users dont have to worry about performance hits against the server.
ROLAP - Relational OLAP.
Designates one or several star schemas stored in relational databases. This technology permits multidimensional analysis with data stored in relational databases.
Used for large departments or groups because it supports large amounts of data and users.
HOLAP:Hybridization of OLAP, which can include any of the above.

[Table of Contents](#Data-Warehousing-Architecture)

## Why an Infocube has maximum of 16 dimensions?

It depends upon the Database limits provided to define the Foreign key constraint, e.g. in Sql Server 2005, the recommended max limit for foreign keys is 253, but you can define more.

[Table of Contents](#Data-Warehousing-Architecture)

## Name some standard Business Intelligence Tools in the Market?

Some standard Business Intelligence tools in the market According to their performance
► MICROSTRATEGY
► BUSINESS OBJECTS,CRYSTAL REPORTS
► COGNOS REPORT NET
► MS-OLAP SERVICES
Or
► Seagate Crystal report
► SAS
► Business objects
► Microstrategy
► Cognos
► Microsoft OLAP
Hyperion
Microsoft integrated services.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Dashboards?

A management reporting tool to gauge how well the organization company is performing. It normally uses "traffic-lights" or "smiley faces" to determine the status.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Hierarchy Relationship in a Dimension.

whether it is:
1. 1:1
2. 1:m
3. m:m
   1:M

[Table of Contents](#Data-Warehousing-Architecture)

## What are Adhoc reports and Static Reports?

Adhoc reports run in real time based on the input parameters provided by the user at the run time.In Microstrategy, adhoc reports are created using Prompts.
In static reports, users won't be provide any input parameters.These reports are usaully schedule to run overnight and ready to view immediatley in the mornings using cache.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the Importance of Surrogate Key in Data Warehousing?

Surrogate Key is a Primary Key for a Dimension table. Most importance of using it is it is independent of underlying database. i.e Surrogate Key is not affected by the changes going on with a database.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Query?

A query is one or more statements that request data from a database. If the data is available, then the requested data returns in the form of a table which contains rows and columns. Queries are sent to the databases in a language called SQL. However, when using the Report Panel, SQL knowledge is not required.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Features of a Physical Data Model?

Features of a physical data model include:
+ Specification all tables and columns.
+ Foreign keys are used to identify relationships between tables.
+ Denormalization may occur based on user requirements.
+ Physical considerations may cause the physical data model to be quite different from the logical data model.
+ Physical data model will be different for different RDBMS. For example, data type for a column may be different between MySQL and SQL Server.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the steps to design a Physical Model?

The steps for physical data model design are as follows:
Convert entities into tables.
Convert relationships into foreign keys.
Convert attributes into columns.
Modify the physical data model based on physical constraints / requirements.
IDMS (Integrated Database Management System) Interview Questions

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Features of Conceptual Data Model?

Features of conceptual data model include:
Includes the important entities and the relationships among them.
No attribute is specified.
No primary key is specified.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the difference between Logical Data Model and Conceptual Data Model?

In a logical data model, primary keys are present, whereas in a conceptual data model, no primary key is present.
In a logical data model, all attributes are specified within an entity. No attributes are specified in a conceptual data model.
Relationships between entities are specified using primary keys and foreign keys in a logical data model. In a conceptual data model, the relationships are simply stated, not specified, so we simply know that two entities are related, but we do not specify what attributes are used for this relationship.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the steps to design Logical Data Model?

The steps for designing the logical data model are as follows:
+ Specify primary keys for all entities.
+ Find the relationships between different entities.
+ Find all attributes for each entity.
+ Resolve many-to-many relationships.
+ Normalization.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Etl?

ETL stands for extraction transformation and loading
ETL provide developers with an interface for designing source-to-target mappings, transformation and job control parameter
* Extraction
  + Take data from an external source and move it to the warehouse pre-processor database
* Transformation
  + Transform data task allows point-to-point generating, modifying and transforming data
* Loading
  + Load data task adds records to a database table in a warehouse.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Three Tier Data Warehouse?

A data warehouse can be thought of as a three-tier system in which a middle system provides usable data in a secure way to end users. On either side of this middle system are the end users and the back-end data stores.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Etl Process and how many steps Etl contains?

ETL is extraction , transforming , loading process , you will extract data from the source and apply the business role on it then you will load it in the target
The steps are :
+ 1-define the source (create the odbc and the connection to the source DB)
+ 2-define the target (create the odbc and the connection to the target DB)
+ 3-create the mapping ( you will apply the business role here by adding transformations , and define how the data flow will go from the source to the target )
+ 4-create the session (its a set of instruction that run the mapping )
+ 5-create the work flow (instruction that run the session)

[Table of Contents](#Data-Warehousing-Architecture)

## What is Full Load and Incremental or Refresh Load?

Full Load: completely erasing the contents of one or more tables and reloading with fresh data.
Incremental Load: applying ongoing changes to one or more tables based on a predefined schedule.

A full load rebuilds the target; an incremental load applies only changed rows. Incremental is cheaper but needs a
reliable watermark and idempotent writes.

```sql
-- Full load: truncate and rebuild a small dimension.
TRUNCATE TABLE dim_country;
INSERT INTO dim_country SELECT * FROM staging.countries;

-- Incremental load: apply only rows newer than the stored watermark.
MERGE INTO fct_orders AS t
USING staging.orders_delta AS s
   ON t.order_id = s.order_id
WHEN MATCHED AND s.updated_at > t.updated_at
    THEN UPDATE SET amount = s.amount, updated_at = s.updated_at
WHEN NOT MATCHED
    THEN INSERT (order_id, amount, updated_at) VALUES (s.order_id, s.amount, s.updated_at);

SELECT MAX(updated_at) FROM staging.orders_delta;  -- next watermark
```

[Table of Contents](#Data-Warehousing-Architecture)

## What is a Staging Area?

Data staging is actually a collection of processes used to prepare source system data for loading a data warehouse. Staging includes the following steps:
Source data extraction, Data transformation (restructuring),
Data transformation (data cleansing, value transformations),
Surrogate key assignments

A staging area is the short-lived zone between sources and the warehouse where typing, deduplication, and
reconciliation happen. It is the "silver" layer in medallion terms.

```sql
CREATE TABLE staging.orders (
    order_id    TEXT,
    customer_id TEXT,
    amount      NUMERIC(14, 2),
    order_date  DATE,
    ingest_ts   TIMESTAMP,
    source_file TEXT
);

-- Deduplicate the landing data on the way into staging.
INSERT INTO staging.orders
SELECT order_id, customer_id, amount, order_date, ingest_ts, source_file
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ingest_ts DESC) AS rn
    FROM landing.orders_raw
) ranked
WHERE rn = 1;
```

[Table of Contents](#Data-Warehousing-Architecture)

## Compare Etl and Manual Development.

ETL - The process of extracting data from multiple sources.(ex. flat files, XML, COBOL, SAP etc) is simpler with the help of tools.
Manual - Loading the data other than flat files and oracle table need more effort.
ETL - High and clear visibility of logic.
Manual - complex and not so user friendly visibility of logic.
ETL - Contains Meta data and changes can be done easily.
Manual - No Meta data concept and changes needs more effort.
ETL- Error handling, log summary and load progress makes life easier for developer and maintainer.
Manual - need maximum effort from maintenance point of view.
ETL - Can handle Historic data very well.
Manual - as data grows the processing time degrades.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Rdbms?

Relational Data Base Management Systems (RDBMS) are database management systems that maintain data records and indices in tables. Relationships may be created and maintained across and among the data and tables. In a relational database, relationships between data items are expressed by means of tables. Interdependencies among these tables are expressed by data values rather than by pointers. This allows a high degree of data independence. An RDBMS has the capability to recombine the data items from different files, providing powerful tools for data usage.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Normalization?

Database normalization is a data design and organization process applied to data structures based on rules that help build relational databases. In relational database design, the process of organizing data to minimize redundancy. Normalization usually involves dividing a database into two or more tables and defining relationships between the tables. The objective is to isolate data so that additions, deletions, and modifications of a field can be made in just one table and then propagated through the rest of the database via the defined relationships.

[Table of Contents](#Data-Warehousing-Architecture)

## What are different Normalization Forms?

+ 1NF: Eliminate Repeating Groups Make a separate table for each set of related attributes, and give each table a primary key. Each field contains at most one value from its attribute domain.
+ 2NF: Eliminate Redundant Data If an attribute depends on only part of a multi-valued key, remove it to a separate table.
+ 3NF: Eliminate Columns Not Dependent On Key If attributes do not contribute to a description of the key, remove them to a separate table. All attributes must be directly dependent on the primary key.
+ BCNF: Boyce-Codd Normal Form If there are non-trivial dependencies between candidate key attributes, separate them out into distinct tables.
+ 4NF: Isolate Independent Multiple Relationships No table may contain two or more 1:n or n:m relationships that are not directly related.
+ 5NF: Isolate Semantically Related Multiple Relationships There may be practical constrains on information that justify separating logically related many-to-many relationships.
+ ONF: Optimal Normal Form A model limited to only simple (elemental) facts, as expressed in Object Role Model notation.
+ DKNF: Domain-Key Normal Form A model free from all modification anomalies. Remember, these normalization guidelines are cumulative. For a database to be in 3NF, it must first fulfill all the criteria of a 2NF and 1NF database.

```sql
-- 1NF: atomic values, no repeating groups in a single column.
CREATE TABLE order_line_1nf (
    order_id   INTEGER NOT NULL,
    line_no    INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity   INTEGER NOT NULL,
    PRIMARY KEY (order_id, line_no)
);

-- 2NF: remove partial dependencies on part of a composite key.
CREATE TABLE product_2nf (
    product_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    category   TEXT NOT NULL
);

-- 3NF: remove transitive dependencies (category -> department moves out).
CREATE TABLE category_3nf (
    category   TEXT PRIMARY KEY,
    department TEXT NOT NULL
);

ALTER TABLE product_2nf ADD COLUMN category_ref TEXT REFERENCES category_3nf(category);

-- BCNF: every determinant is a candidate key.
CREATE TABLE product_bcnf (
    product_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    category   TEXT NOT NULL REFERENCES category_3nf(category)
);
```

Quick definitions:

+ 1NF: every column holds a single atomic value.
+ 2NF: 1NF plus no non-prime attribute depends on part of a composite key.
+ 3NF: 2NF plus no non-prime attribute depends transitively on the key.
+ BCNF: every determinant is a candidate key.
+ 4NF/5NF: eliminate multivalued and join dependencies.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Stored Procedure?

A stored procedure is a named group of SQL statements that have been previously created and stored in the server database. Stored procedures accept input parameters so that a single procedure can be used over the network by several clients using different input data. And when the procedure is modified, all clients automatically get the new version. Stored procedures reduce network traffic and improve performance. Stored procedures can be used to help ensure the integrity of the database.
e.g. sp_helpdb, sp_renamedb, sp_depends etc.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Trigger?

A trigger is an SQL procedure that initiates an action when an event (INSERT, DELETE or UPDATE) occurs. Triggers are stored in and managed by the DBMS. Triggers are used to maintain the referential integrity of data by changing the data in a systematic fashion. A trigger cannot be called or executed; the DBMS automatically fires the trigger as a result of a data modification to the associated table. Triggers can be viewed as similar to stored procedures in that both consist of procedural logic that is stored at the database level. Stored procedures, however, are not event-drive and are not attached to a specific table as triggers are. Stored procedures are explicitly executed by invoking a CALL to the procedure while triggers are implicitly executed. In addition, triggers can also execute stored procedures.

[Table of Contents](#Data-Warehousing-Architecture)

## What is View?

A simple view can be thought of as a subset of a table. It can be used for retrieving data, as well as updating or deleting rows. Rows updated or deleted in the view are updated or deleted in the table the view was created with. It should also be noted that as data in the original table changes, so does data in the view, as views are the way to look at part of the original table. The results of using a view are not permanently stored in the database. The data accessed through a view is actually constructed using standard T-SQL select command and can come from one to many different base tables or even other views.

[Table of Contents](#Data-Warehousing-Architecture)

## Advantages of Dbms?

+ Redundancy is controlled.
+ Unauthorised access is restricted.
+ Providing multiple user interfaces.
+ Enforcing integrity constraints.
+ Providing backup and recovery.

[Table of Contents](#Data-Warehousing-Architecture)

## Disadvantage in File Processing System?

+ Data redundancy & inconsistency.
+ Difficult in accessing data.
+ Data isolation.
+ Data integrity.
+ Concurrent access is not possible.
+ Security Problems.

[Table of Contents](#Data-Warehousing-Architecture)

## Describe Three Levels of Data Abstraction?

There are three levels of abstraction:
Physical level: The lowest level of abstraction describes how data are stored.
Logical level: The next higher level of abstraction, describes what data are stored in database and what relationship among those data.
View level: The highest level of abstraction describes only part of entire database.
Oracle 11g Tutorial

[Table of Contents](#Data-Warehousing-Architecture)

## Define integrity Rules?

There are two Integrity rules.
+ Entity Integrity: States that “Primary key cannot have NULL value”.
+ Referential Integrity: States that “Foreign Key can be either a NULL value or should be Primary Key value of other relation.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Extension and Intention?

+ Extension : It is the number of tuples present in a table at any instance. This is time dependent.
+ Intention : It is a constant value that gives the name, structure of table and the constraints laid on it.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Data Independence?

Data independence means that “the application is independent of the storage structure and access strategy of data”. In other words, The ability to modify the schema definition in one level should not affect the schema definition in the next higher level.
Two types of Data Independence:
Physical Data Independence: Modification in physical level should not affect the logical level.
Logical Data Independence: Modification in logical level should affect the view level.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a View and how it is related to Data Independence?

A view may be thought of as a virtual table, that is, a table that does not really exist in its own right but is instead derived from one or more underlying base table. In other words, there is no stored file that direct represents the view instead a definition of view is stored in data dictionary. Growth and restructuring of base tables is not reflected in views. Thus the view can insulate users from the effects of restructuring and growth in the database. Hence accounts for logical data independence.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Data Model?

A collection of conceptual tools for describing data, data relationships data semantics and constraints.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Object Oriented Model?

This model is based on collection of objects. An object contains values stored in instance variables with in the object. An object also contains bodies of code that operate on the object. These bodies of code are called methods. Objects that contain same types of values and the same methods are grouped together into classes.

[Table of Contents](#Data-Warehousing-Architecture)

## What is an Entity?

It is a 'thing' in the real world with an independent existence.

[Table of Contents](#Data-Warehousing-Architecture)

## What is an Entity Type?

It is a collection (set) of entities that have same attributes.

[Table of Contents](#Data-Warehousing-Architecture)

## What is an Entity Set?

It is a collection of all entities of particular entity type in the database.

[Table of Contents](#Data-Warehousing-Architecture)

## What is an Attribute?

It is a particular property, which describes the entity.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Relation Schema and Relation?

A relation Schema denoted by R(A1, A2, …, An) is made up of the relation name R and the list of attributes Ai that it contains.
A relation is defined as a set of tuples. Let r be the relation which contains set tuples (t1, t2, t3, ..., tn). Each tuple is an ordered list of n-values t=(v1,v2, ..., vn).

[Table of Contents](#Data-Warehousing-Architecture)

## What is Degree of Relation?

It is the number of attribute of its relation schema.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Relationship?

It is an association among two or more entities.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Relationship Set?

The collection (or set) of similar relationships.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Relationship Type?

Relationship type defines a set of associations or a relationship set among a given set of entity types.

[Table of Contents](#Data-Warehousing-Architecture)

## What Is DDL?

A data base schema is specifies by a set of definitions expressed by a special language called DDL.

[Table of Contents](#Data-Warehousing-Architecture)

## What Is Vdl?

It specifies user views and their mappings to the conceptual schema.  (view Definition Language)

[Table of Contents](#Data-Warehousing-Architecture)

## What is Sdl?

This language is to specify the internal schema. This language may specify the mapping between two schemas. (storage Definition Language)

[Table of Contents](#Data-Warehousing-Architecture)

## What Is Data Storage Definition Language?

The storage structures and access methods used by database system are specified by a set of definition in a special type of DDL called data storage-definition language.

[Table of Contents](#Data-Warehousing-Architecture)

## What Is Dml?

This language that enable user to access or manipulate data as organized by appropriate data model.
Procedural DML or Low level: DML requires a user to specify what data are needed and how to get those data.
Non-Procedural DML or High level: DML requires a user to specify what data are needed without specifying how to get those data.
(data Manipulation Language)

[Table of Contents](#Data-Warehousing-Architecture)

## What is Query Evaluation Engine?

It executes low-level instruction generated by compiler.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Ddl Interpreter?

It interprets DDL statements and record them in tables containing metadata.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Record at a time?

The Low level or Procedural DML can specify and retrieve each record from a set of records. This retrieve of a record is said to be Record-at-a-time.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Set at a time or Set oriented?

The High level or Non-procedural DML can specify and retrieve many records in a single DML statement. This retrieve of a record is said to be Set-at-a-time or Set-oriented.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Relational Algebra?

It is procedural query language. It consists of a set of operations that take one or two relations as input and produce a new relation.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Relational Calculus?

It is an applied predicate calculus specifically tailored for relational databases proposed by E.F. Codd.
E.g. of languages based on it are DSL ALPHA, QUEL.

[Table of Contents](#Data-Warehousing-Architecture)

## How does Tuple oriented Relational calculus differ from Domain oriented Relational Calculus?

The tuple-oriented calculus uses a tuple variables i.e., variable whose only permitted values are tuples of that relation. E.g. QUEL
The domain-oriented calculus has domain variables i.e., variables that range over the underlying domains instead of over relation. E.g. ILL, DEDUCE.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Functional Dependency?

A Functional dependency is denoted by X Y between two sets of attributes X and Y that are subsets of R specifies a constraint on the possible tuple that can form a relation state r of R. The constraint is for any two tuples t1 and t2 in r if t1[X] = t2[X] then they have t1[Y] = t2[Y]. This means the value of X component of a tuple uniquely determines the value of component Y.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Multivalued Dependency?

Multivalued dependency denoted by X Y specified on relation schema R, where X and Y are both subsets of R, specifies the following constraint on any relation r of R: if two tuples t1 and t2 exist in r such that t1[X] = t2[X] then t3 and t4 should also exist in r with the following properties

t3[x] = t4[X] = t1[X] = t2[X]
t3[Y] = t1[Y] and t4[Y] = t2[Y]
t3[Z] = t2[Z] and t4[Z] = t1[Z]
where [Z = (R-(X U Y)) ]

[Table of Contents](#Data-Warehousing-Architecture)

## What is Lossless Join Property?

It guarantees that the spurious tuple generation does not occur with respect to relation schemas after decomposition.

[Table of Contents](#Data-Warehousing-Architecture)

## What Is 1 Nf?

The domain of attribute must include only atomic (simple, indivisible) values.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Fully Functional Dependency?

It is based on concept of full functional dependency. A functional dependency X Y is full functional dependency if removal of any attribute A from X means that the dependency does not hold any more.

[Table of Contents](#Data-Warehousing-Architecture)

## What is 2nf?

A relation schema R is in 2NF if it is in 1NF and every non-prime attribute A in R is fully functionally dependent on primary key.

[Table of Contents](#Data-Warehousing-Architecture)

## What is 3nf?

A relation schema R is in 3NF if it is in 2NF and for every FD X A either of the following is true

X is a Super-key of R.
A is a prime attribute of R.
In other words, if every non prime attribute is non-transitively dependent on primary key.

What Is Bcnf (boyce-codd Normal Form)?
A relation schema R is in BCNF if it is in 3NF and satisfies an additional constraint that for every FD X A, X must be a candidate key.

[Table of Contents](#Data-Warehousing-Architecture)

## What is 4nf?

A relation schema R is said to be in 4NF if for every Multivalued dependency X Y that holds over R, one of following is true
X is subset or equal to (or) XY = R.
X is a super key.

[Table of Contents](#Data-Warehousing-Architecture)

## What is 5nf?

A Relation schema R is said to be 5NF if for every join dependency {R1, R2, ..., Rn} that holds R, one the following is true
Ri = R for some i.
The join dependency is implied by the set of FD, over R in which the left side is key of R.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Domain key NF?

A relation is said to be in DKNF if all constraints and dependencies that should hold on the constraint can be enforced by simply enforcing the domain constraint and key constraint on the relation.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Partial Alternate Artificial Compound and Natural Key?

+ Partial Key:
  + It is a set of attributes that can uniquely identify weak entities and that are related to same owner entity. It is sometime called as Discriminator.
+ Alternate Key:
  + All Candidate Keys excluding the Primary Key are known as Alternate Keys.
+ Artificial Key:
  + If no obvious key, either stand alone or compound is available, then the last resort is to simply create a key, by assigning a unique number to each record or occurrence. Then this is known as developing an artificial key.
+ Compound Key:
  + If no single data element uniquely identifies occurrences within a construct, then combining multiple elements to create a unique identifier for the construct is known as creating a compound key.
+ Natural Key:
  + When one of the data elements stored within a construct is utilized as the primary key, then it is called the natural key.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Indexing and what are the different kinds of Indexing?

Indexing is a technique for determining how quickly specific data can be found.
Types:
+ Binary search style indexing
+ B-Tree indexing
+ Inverted list indexing
M+ emory resident table
+ Table indexing

```sql
-- B-tree index: equality and range predicates, high selectivity.
CREATE INDEX idx_customer_email ON dim_customer (email);

-- Composite index: column order matters, left-most prefix is usable.
CREATE INDEX idx_fct_sales_date_product ON fct_sales (sale_date, product_sk);

-- Bitmap index: low-cardinality columns on a read-mostly warehouse (Oracle, some MPPs).
CREATE BITMAP INDEX bm_fct_sales_channel ON fct_sales (channel);

-- Covering index: every selected column lives in the index.
CREATE INDEX idx_orders_covering ON fct_orders (customer_sk) INCLUDE (net_amount);

-- Check what the planner actually uses.
EXPLAIN ANALYZE
SELECT product_sk, SUM(net_amount)
FROM fct_sales
WHERE sale_date BETWEEN DATE '2026-01-01' AND DATE '2026-03-31'
GROUP BY product_sk;
```

Rules of thumb:

+ Index columns used in selective `WHERE`, join keys, and `ORDER BY`.
+ Bitmap indexes are good for low-cardinality filters; B-tree for unique and high-cardinality.
+ Every index slows writes and uses storage, so index the queries you actually run.

[Table of Contents](#Data-Warehousing-Architecture)

## What is meant by Query Optimization?

The phase that identifies an efficient execution plan for evaluating a query that has the least estimated cost is referred to as query optimization.

Query optimization chooses an execution plan with the lowest estimated cost. The levers you control are statistics,
predicates, join order, and physical layout.

```sql
-- Good: filter before the join, keep predicates sargable.
SELECT p.category, SUM(f.net_amount) AS revenue
FROM fct_sales f
JOIN dim_product p ON p.product_sk = f.product_sk
WHERE f.sale_date >= DATE '2026-01-01'
  AND f.sale_date <  DATE '2026-04-01'
GROUP BY p.category;

-- Bad: a function on the filter column disables partition pruning.
SELECT p.category, SUM(f.net_amount) AS revenue
FROM fct_sales f
JOIN dim_product p ON p.product_sk = f.product_sk
WHERE EXTRACT(YEAR FROM f.sale_date) = 2026
GROUP BY p.category;

EXPLAIN ANALYZE
SELECT p.category, SUM(f.net_amount)
FROM fct_sales f
JOIN dim_product p ON p.product_sk = f.product_sk
WHERE f.sale_date >= DATE '2026-01-01'
GROUP BY p.category;
```

Checklist: refresh statistics, avoid `SELECT *`, push filters into the scan, reduce the row count before the join, and
verify that the plan prunes partitions.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Join Dependency and Inclusion Dependency?

Join Dependency:
A Join dependency is generalization of Multivalued dependency.A JD {R1, R2, ..., Rn} is said to hold over a relation R if R1, R2, R3, ..., Rn is a lossless-join decomposition of R . There is no set of sound and complete inference rules for JD.
Inclusion Dependency:
An Inclusion Dependency is a statement of the form that some columns of a relation are contained in other columns. A foreign key constraint is an example of inclusion dependency.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Durability in Dbms?

Once the DBMS informs the user that a transaction has successfully completed, its effects should persist even if the system crashes before all its changes are reflected on disk. This property is called durability.

[Table of Contents](#Data-Warehousing-Architecture)

## What do you mean by Atomicity and Aggregation?

Atomicity:
Either all actions are carried out or none are. Users should not have to worry about the effect of incomplete transactions. DBMS ensures this by undoing the actions of incomplete transactions.
Aggregation:
A concept which is used to model a relationship between a collection of entities and relationships. It is used when we need to express a relationship among relationships.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Phantom Deadlock?

In distributed deadlock detection, the delay in propagating local information might cause the deadlock detection algorithms to identify deadlocks that do not really exist. Such situations are called phantom deadlocks and they lead to unnecessary aborts.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Checkpoint and when does it cccur?

A Checkpoint is like a snapshot of the DBMS state. By taking checkpoints, the DBMS can reduce the amount of work to be done during restart in the event of subsequent crashes.

[Table of Contents](#Data-Warehousing-Architecture)

## What are different Phases of Transaction?

Different phases are
Analysis phase
Redo Phase
Undo phase

[Table of Contents](#Data-Warehousing-Architecture)

## What do you mean by Flat File Database?

It is a database in which there are no programs or user access languages. It has no cross-file capabilities but is user-friendly and provides user-interface management.

[Table of Contents](#Data-Warehousing-Architecture)

## What is transparent Dbms?

It is one, which keeps its Physical Structure hidden from user.

[Table of Contents](#Data-Warehousing-Architecture)

## What do you mean by Correlated Subquery?

Subqueries, or nested queries, are used to bring back a set of rows to be used by the parent query. Depending on how the subquery is written, it can be executed once for the parent query or it can be executed once for each row returned by the parent query. If the subquery is executed for each row of the parent, this is called a correlated subquery.
A correlated subquery can be easily identified if it contains any references to the parent subquery columns in its WHERE clause. Columns from the subquery cannot be referenced anywhere else in the parent query. The following example demonstrates a non-correlated subquery.
E.g. Select * From CUST Where '10/03/1990' IN (Select ODATE From ORDER Where CUST.CNUM = ORDER.CNUM)

A correlated subquery references the outer row and is evaluated once per outer row. It is often clearer, but a window
function usually runs faster on a warehouse.

```sql
-- Correlated: latest order per customer.
SELECT c.customer_id, o.order_id, o.amount
FROM dim_customer c
JOIN fct_orders o ON o.customer_id = c.customer_id
WHERE o.order_date = (
    SELECT MAX(o2.order_date)
    FROM fct_orders o2
    WHERE o2.customer_id = c.customer_id
);

-- Window function: usually the better plan.
SELECT customer_id, order_id, amount
FROM (
    SELECT customer_id, order_id, amount,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM fct_orders
) ranked
WHERE rn = 1;
```

[Table of Contents](#Data-Warehousing-Architecture)

## What are the Primitive Operations common to all record management systems?

Addition, deletion and modification.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Unary Operations in Relational Algebra?

PROJECTION and SELECTION.

[Table of Contents](#Data-Warehousing-Architecture)

## Are resulting Relations of Product and Join Operation the same?

No.
PRODUCT: Concatenation of every row in one relation with every row in another.
JOIN: Concatenation of rows from one relation and related rows from another.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Rdbms Kernel?

Two important pieces of RDBMS architecture are the kernel, which is the software, and the data dictionary, which consists of the system-level data structures used by the kernel to manage the database
You might think of an RDBMS as an operating system (or set of subsystems), designed specifically for controlling data access; its primary functions are storing, retrieving, and securing data. An RDBMS maintains its own list of authorized users and their associated privileges; manages memory caches and paging; controls locking for concurrent resource usage; dispatches and schedules user requests; and manages space usage within its table-space structures.

[Table of Contents](#Data-Warehousing-Architecture)

## Name the Sub systems of Rdbms?

I/O, Security, Language Processing, Process Control, Storage Management, Logging and Recovery, Distribution Control, Transaction Control, Memory Management, Lock Management.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Rowid?

The ROWID is a unique database-wide physical address for every row on every table. Once assigned (when the row is first inserted into the database), it never changes until the row is deleted or the table is dropped.
The ROWID consists of the following three components, the combination of which uniquely identifies the physical storage location of the row.
Oracle database file number, which contains the block with the rows
Oracle block address, which contains the row
The row within the block (because each block can hold many rows)
The ROWID is used internally in indexes as a quick means of retrieving rows with a particular key value. Application developers also use it in SQL statements as a quick way to access a row once they know the ROWID.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Storage Manager?

It is a program module that provides the interface between the low-level data stored in database, application programs and queries submitted to the system.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Buffer Manager?

It is a program module, which is responsible for fetching data from disk storage into main memory and deciding what data to be cache in memory.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Transaction Manager?

It is a program module, which ensures that database, remains in a consistent state despite system failures and concurrent transaction execution proceeds without conflicting.

[Table of Contents](#Data-Warehousing-Architecture)

## What is File Manager?

It is a program module, which manages the allocation of space on disk storage and data structure used to represent information stored on a disk.

[Table of Contents](#Data-Warehousing-Architecture)

## What is Authorization and Integrity Manager?

It is the program module, which tests for the satisfaction of integrity constraint and checks the authority of user to access data.

[Table of Contents](#Data-Warehousing-Architecture)

## What are Stand alone procedures?

Procedures that are not part of a package are known as stand-alone because they independently defined. A good example of a stand-alone procedure is one written in a SQL*Forms application. These types of procedures are not available for reference from other Oracle tools. Another limitation of stand-alone procedures is that they are compiled at run time, which slows execution.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the different methods of loading dimension tables?

There are two different methods to load data in dimension tables:
+ Conventional (slow): All the constraints and keys are validated against the information before, it is loaded, and this method data integrity is maintained.
+ Direct (fast): All the constraints and keys are disabled before the information is loaded. Once the information is loaded, it is validated against all the constraints and keys. If the data is found invalid, it is not contained in the index, and all the future processes are skipped in this data.

[Table of Contents](#Data-Warehousing-Architecture)

## Describe the foreign key columns in fact tables and dimension tables?

A dimension table has a surrogate primary key plus one or more natural keys from the source. A fact table stores those surrogate keys as foreign keys, so each fact row can be sliced by every dimension. In a Type 2 dimension the fact stores the surrogate key of the version that was current when the event happened, not the key of the current row.

[Table of Contents](#Data-Warehousing-Architecture)

## What are the types of fact tables in a dimensional model?

There are three fact table patterns, and the grain decides which one you use.

+ Transaction fact: one row per event, the most detailed and flexible.
+ Periodic snapshot: one row per entity per period, used for balances and inventory.
+ Accumulating snapshot: one row per process instance, updated as the process advances.

```text
Transaction        : one row per sale
Periodic snapshot  : one row per account per day
Accumulating       : one row per order, with order/made/shipped/delivered milestones
```

```sql
-- Transaction fact
CREATE TABLE fct_sales (
    sale_id    BIGINT NOT NULL,
    sale_date  DATE   NOT NULL,
    product_sk BIGINT NOT NULL,
    quantity   INTEGER NOT NULL,
    net_amount NUMERIC(14, 2) NOT NULL,
    PRIMARY KEY (sale_id, sale_date)
) PARTITION BY RANGE (sale_date);

-- Periodic snapshot fact
CREATE TABLE fct_account_balance_daily (
    date_sk    BIGINT NOT NULL,
    account_sk BIGINT NOT NULL,
    balance    NUMERIC(18, 2) NOT NULL,   -- semi-additive: do not sum across days
    PRIMARY KEY (date_sk, account_sk)
);

-- Accumulating snapshot fact
CREATE TABLE fct_order_fulfilment (
    order_id       BIGINT PRIMARY KEY,
    order_date_sk  BIGINT NOT NULL,
    ship_date_sk   BIGINT,
    deliver_date_sk BIGINT,
    days_to_ship   INTEGER,       -- recomputed on each update
    days_to_deliver INTEGER
);
```

Interview guidance: transaction facts are the default; use a periodic snapshot only when the business asks for
point-in-time state; use an accumulating snapshot when the question is process latency (order to ship to deliver).

[Table of Contents](#Data-Warehousing-Architecture)

## How do you implement SCD Type 2 with a MERGE statement?

A MERGE folds the Type 2 load into fewer statements than the update-then-insert dance. The pattern is: detect changed
rows, close the old version, and insert the new version with a fresh surrogate key.

```sql
MERGE INTO dim_customer AS t
USING (
    SELECT
        s.customer_id,
        s.name,
        s.city,
        s.segment,
        s.effective_date,
        d.customer_sk AS current_sk
    FROM staging.customer_delta s
    LEFT JOIN dim_customer d
           ON d.customer_id = s.customer_id
          AND d.is_current
) AS s
   ON t.customer_sk = s.current_sk
WHEN MATCHED AND (t.city, t.segment) IS DISTINCT FROM (s.city, s.segment)
    THEN UPDATE SET
        t.end_date   = s.effective_date - INTERVAL '1 day',
        t.is_current = FALSE
WHEN NOT MATCHED THEN
    INSERT (customer_sk, customer_id, name, city, segment, start_date, end_date, is_current)
    VALUES (nextval('dim_customer_sk_seq'), s.customer_id, s.name, s.city, s.segment,
            s.effective_date, DATE '9999-12-31', TRUE);
```

Caveats worth raising in an interview:

+ A single MERGE cannot both close the old row and insert the new row for the same natural key in every
  engine; the two-step form (close, then insert) is safest. The example above closes changed rows and inserts new
  business keys, so the new version of a changed key lands on the next pass, once its old row is no longer current.
+ `IS DISTINCT FROM` handles NULL-safe comparisons; plain `<>` silently misses NULL changes.
+ Re-running the same delta must not create duplicate versions, so guard the close with `is_current = TRUE`.
+ Late-arriving changes need an additional pass that restates the affected versions rather than appending blindly.

[Table of Contents](#Data-Warehousing-Architecture)

## How do you handle late-arriving facts and dimensions?

A late fact is an event that arrives after the period it belongs to; a late dimension is a change that arrives after
facts referencing the old version were already loaded. Both need an explicit reconciliation step.

For late dimensions, insert an inferred "unknown" member so facts never fail their lookup, then repair it when the
real record arrives.

```sql
INSERT INTO dim_customer (customer_sk, customer_id, name, start_date, is_current)
VALUES (-1, 'UNKNOWN', 'Unknown customer', DATE '1900-01-01', TRUE);

-- Stage facts with an unresolved member rather than dropping them.
INSERT INTO fct_sales (sale_id, sale_date, customer_sk, net_amount)
SELECT s.sale_id, s.sale_date, COALESCE(d.customer_sk, -1), s.net_amount
FROM staging.sales s
LEFT JOIN dim_customer d ON d.customer_id = s.customer_id AND d.is_current;
```

For late facts, load them into the correct partition and then refresh only the affected aggregates.

```sql
-- Facts are partitioned by event date, so a late event still lands in its own partition.
INSERT INTO fct_sales PARTITION (sale_date)
SELECT * FROM staging.late_sales;

-- Recompute only the affected dates in the aggregate.
DELETE FROM agg_sales_daily
WHERE date IN (SELECT DISTINCT sale_date FROM staging.late_sales);

INSERT INTO agg_sales_daily
SELECT sale_date, SUM(net_amount) FROM fct_sales
WHERE sale_date IN (SELECT DISTINCT sale_date FROM staging.late_sales)
GROUP BY sale_date;
```

Trade-off: reprocessing affected partitions is correct but costs a rescan; use a late-arrival window (for example
7 days) and treat anything older as a correction that must be explicitly approved.

[Table of Contents](#Data-Warehousing-Architecture)

## What is the medallion architecture (bronze, silver, gold)?

Medallion architecture is a layering convention on a lakehouse: bronze keeps raw data, silver cleans and conforms,
gold serves business marts.

```text
bronze (raw, append-only, replayable)
   -> silver (typed, deduplicated, conformed keys)
   -> gold (star schemas, marts, aggregates)
```

```sql
-- Bronze: append raw events, never mutate.
INSERT INTO bronze.events
SELECT current_timestamp(), metadata.file_path, value
FROM read_files('/mnt/landing/events/', format => 'json');

-- Silver: deduplicate and type.
CREATE OR REPLACE TABLE silver.events AS
SELECT event_id, tenant_id, event_ts, CAST(amount AS DECIMAL(14, 2)) AS amount
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY ingested_at DESC) AS rn
    FROM bronze.events
) ranked
WHERE rn = 1;

-- Gold: business mart.
CREATE OR REPLACE TABLE gold.fct_revenue_minute AS
SELECT date_trunc('minute', event_ts) AS minute, tenant_id, SUM(amount) AS revenue
FROM silver.events
GROUP BY 1, 2;
```

Rules that keep the layers useful:

+ Bronze is append-only, so any silver or gold table can be rebuilt from it.
+ Silver is the only place that deduplicates and applies typing; gold never re-parses raw payloads.
+ Each layer has an owner, a freshness SLO, and a schema contract.
+ Do not skip silver: landing straight into gold is how duplicated and untyped data reaches dashboards.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a data vault and when would you use it?

Data Vault models an enterprise warehouse as hubs (business keys), links (relationships), and satellites (descriptive
history). It is insert-only, highly auditable, and designed for many changing sources.

```text
hub_customer (customer_hk, customer_id, load_ts, record_source)
   |
link_order_customer (link_hk, order_hk, customer_hk, load_ts)
   |
sat_customer (customer_hk, load_ts, hash_diff, name, city, segment)
```

```sql
CREATE TABLE hub_customer (
    customer_hk  TEXT PRIMARY KEY,     -- hash of the business key
    customer_id  TEXT NOT NULL UNIQUE,
    load_ts      TIMESTAMP NOT NULL,
    record_source TEXT NOT NULL
);

CREATE TABLE sat_customer (
    customer_hk  TEXT NOT NULL REFERENCES hub_customer(customer_hk),
    load_ts      TIMESTAMP NOT NULL,
    hash_diff    TEXT NOT NULL,         -- hash of the descriptive columns
    name         TEXT,
    city         TEXT,
    segment      TEXT,
    PRIMARY KEY (customer_hk, load_ts)
);

-- Insert only when the description actually changed.
INSERT INTO sat_customer
SELECT s.customer_hk, s.load_ts, s.hash_diff, s.name, s.city, s.segment
FROM staging.customer s
LEFT JOIN sat_customer c
       ON c.customer_hk = s.customer_hk
      AND c.hash_diff = s.hash_diff
WHERE c.customer_hk IS NULL;
```

When to use it:

+ Many sources that must be onboarded incrementally without reworking the model.
+ Auditors need a full, immutable history with provenance.
+ You can tolerate more tables and the need for a business vault or star layer on top for BI.

When not to use it: a small, stable number of sources where a Kimball star is enough. Data Vault is an integration
pattern, not a replacement for dimensional marts; most teams expose gold stars on top of the vault.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a lakehouse and how does it differ from a data warehouse?

A lakehouse stores data as open files in object storage and adds a transactional table format (Delta, Iceberg, Hudi)
for ACID writes, schema evolution, and time travel. A classic warehouse couples storage and compute in a proprietary
engine.

```text
| Aspect       | Data warehouse                    | Lakehouse                              |
|--------------|-----------------------------------|----------------------------------------|
| Storage      | Proprietary, managed              | Open files (Parquet) plus table format |
| Compute      | Coupled to the engine             | Pluggable (Spark, Trino, Flink, SQL)   |
| Schema       | Schema-on-write                   | Schema-on-read with enforcement option |
| Transactions | Native                            | Table-format ACID and snapshots        |
| Data types   | Structured, some semi-structured  | Structured, semi- and unstructured     |
| Cost model   | Storage + warehouse compute       | Object storage + elastic compute       |
| Governance   | Mature RBAC and lineage           | Improving; needs a catalog             |
```

```sql
-- Same table, multiple engines, because the metadata is open.
CREATE TABLE IF NOT EXISTS silver.events (
    event_id   STRING,
    tenant_id  BIGINT,
    event_ts   TIMESTAMP,
    amount     DECIMAL(14, 2)
)
USING iceberg
PARTITIONED BY (days(event_ts));

SELECT tenant_id, SUM(amount)
FROM silver.events VERSION AS OF 42       -- time travel to snapshot 42
WHERE event_ts >= TIMESTAMP '2026-10-01'
GROUP BY tenant_id;
```

Interview framing: the lakehouse is not "warehouse versus lake", it is "warehouse semantics on lake storage". Choose
it when you need open formats and many engines; choose a classic warehouse when you want a fully managed,
high-concurrency BI service with less operational overhead.

[Table of Contents](#Data-Warehousing-Architecture)

## How do you partition and cluster a large fact table?

Partitioning splits a table into files by a low-to-medium cardinality key, usually a date. Clustering or sorting
orders rows inside partitions so the engine can skip data with min/max statistics.

```text
partitions: one directory per month
  sale_date=2026-01/
  sale_date=2026-02/
cluster key inside each partition: store_sk, product_sk
```

```sql
-- Range partition by month on a date column.
CREATE TABLE fct_sales (
    sale_id    BIGINT NOT NULL,
    sale_date  DATE   NOT NULL,
    store_sk   BIGINT NOT NULL,
    product_sk BIGINT NOT NULL,
    net_amount NUMERIC(14, 2) NOT NULL,
    PRIMARY KEY (sale_id, sale_date)
) PARTITION BY RANGE (sale_date);

-- Snowflake-style cluster key.
ALTER TABLE fct_sales CLUSTER BY (sale_date, store_sk);

-- Iceberg allows partition evolution: change the strategy without rewriting history.
ALTER TABLE fct_sales SET PARTITION SPEC (month(sale_date));

-- Verify pruning.
EXPLAIN
SELECT store_sk, SUM(net_amount)
FROM fct_sales
WHERE sale_date BETWEEN DATE '2026-10-01' AND DATE '2026-10-31'
GROUP BY store_sk;
```

Guidelines:

+ Partition on the column that almost every query filters, and keep partitions large (hundreds of MB to a few GB).
+ Do not partition on a high-cardinality column such as `customer_id`; that creates millions of tiny files.
+ Cluster or sort on the next most selective predicates and on join keys.
+ Over-partitioning is worse than none: metadata overhead and small files dominate the runtime.

[Table of Contents](#Data-Warehousing-Architecture)

## What is a bridge table and when do you need one?

A bridge table resolves many-to-many relationships between a dimension and a fact. It stores one row per pairing plus
a weight so measures can be allocated without double counting.

```text
dim_diagnosis --< bridge_visit_diagnosis >-- fct_visit
```

```sql
CREATE TABLE bridge_visit_diagnosis (
    visit_id      BIGINT NOT NULL,
    diagnosis_sk  BIGINT NOT NULL REFERENCES dim_diagnosis(diagnosis_sk),
    weight        NUMERIC(6, 4) NOT NULL DEFAULT 1.0,
    PRIMARY KEY (visit_id, diagnosis_sk)
);

-- Allocate the visit cost across its diagnoses.
SELECT d.diagnosis_name, SUM(v.cost * b.weight) AS allocated_cost
FROM fct_visit v
JOIN bridge_visit_diagnosis b ON b.visit_id = v.visit_id
JOIN dim_diagnosis d ON d.diagnosis_sk = b.diagnosis_sk
GROUP BY d.diagnosis_name;
```

Rules: weights for one fact row should sum to 1, and the bridge should be rebuilt whenever the relationship changes.
If you only need counts of pairings, a weighted bridge still works but a factless fact table is simpler.

[Table of Contents](#Data-Warehousing-Architecture)

## How do you test a data warehouse model?

Test the model at three levels: schema, data quality, and business result. Automated tests should fail the pipeline,
not just log a warning.

```sql
-- Uniqueness of the declared grain
SELECT order_number, line_number, COUNT(*)
FROM fct_order_line
GROUP BY order_number, line_number
HAVING COUNT(*) > 1;

-- Referential integrity in both directions
SELECT COUNT(*) FROM fct_sales f
LEFT JOIN dim_customer d ON d.customer_sk = f.customer_sk
WHERE d.customer_sk IS NULL;

-- Type 2 invariants: exactly one current row, and valid date ranges
SELECT customer_id, COUNT(*) FROM dim_customer WHERE is_current GROUP BY customer_id HAVING COUNT(*) <> 1;

SELECT * FROM dim_customer WHERE end_date <= start_date;

-- Reconciliation against the source
SELECT (SELECT SUM(net_amount) FROM fct_sales WHERE sale_date = DATE '2026-10-04')
     - (SELECT SUM(amount)     FROM staging.orders WHERE order_date = DATE '2026-10-04') AS variance;
```

Test checklist:

+ Grain uniqueness and non-null keys.
+ No orphan foreign keys.
+ Measure reconciliation with a documented tolerance.
+ SCD invariants and no overlapping validity ranges.
+ Row-count and freshness checks per partition, plus a duplicate check on the natural key.

[Table of Contents](#Data-Warehousing-Architecture)

## Real world use cases for data warehousing architecture

These are the scenarios that show up repeatedly in interviews and in production. Each one names the pattern and the
artifacts you would build.

+ Daily revenue mart: a transaction fact at order-line grain, conformed date/product/store/customer dimensions, and a
  daily aggregate refreshed incrementally.
+ SCD2 customer history: a Type 2 customer dimension with validity ranges and a current flag, joined by the version
  that was active when the order happened.
+ Inventory snapshot fact: a periodic snapshot at one row per product per store per day, with a semi-additive
  on-hand measure.
+ Clickstream sessionization: event-level facts grouped into sessions with a window function, then a session fact and
  a path bridge.
+ Late-arriving facts: partition-scoped loads plus a targeted refresh of the affected aggregate partitions.
+ Medallion rebuild: bronze is append-only, so any silver or gold table can be rebuilt end to end after a logic bug.

Example: the daily revenue mart, built from raw orders to a gold aggregate.

```sql
-- Silver: deduplicate and conform.
CREATE OR REPLACE TABLE silver.orders AS
SELECT order_id, customer_id, product_id, store_id, order_ts, quantity, net_amount
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ingest_ts DESC) AS rn
    FROM bronze.orders
) ranked
WHERE rn = 1;

-- Gold: daily revenue at the grain the dashboard needs.
CREATE OR REPLACE TABLE gold.revenue_daily AS
SELECT
    CAST(order_ts AS DATE) AS revenue_date,
    store_id,
    SUM(net_amount) AS revenue,
    SUM(quantity)   AS units,
    COUNT(DISTINCT order_id) AS orders
FROM silver.orders
GROUP BY 1, 2;

-- Incremental refresh of just the last two days.
DELETE FROM gold.revenue_daily WHERE revenue_date >= CURRENT_DATE - INTERVAL '2' DAY;
INSERT INTO gold.revenue_daily
SELECT CAST(order_ts AS DATE), store_id, SUM(net_amount), SUM(quantity), COUNT(DISTINCT order_id)
FROM silver.orders
WHERE order_ts >= CURRENT_DATE - INTERVAL '2' DAY
GROUP BY 1, 2;
```

Example: sessionize clickstream events so a session fact can be joined to the revenue fact.

```sql
WITH ordered AS (
    SELECT
        session_id,
        user_id,
        event_ts,
        LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts) AS prev_ts
    FROM silver.click_events
),
flagged AS (
    SELECT *,
           CASE WHEN prev_ts IS NULL
                     OR event_ts > prev_ts + INTERVAL '30' MINUTE
                THEN 1 ELSE 0 END AS is_new_session
    FROM ordered
),
sessionised AS (
    SELECT *,
           SUM(is_new_session) OVER (PARTITION BY user_id ORDER BY event_ts) AS session_number
    FROM flagged
)
SELECT user_id, session_number,
       MIN(event_ts) AS session_start,
       MAX(event_ts) AS session_end,
       COUNT(*)      AS events
FROM sessionised
GROUP BY user_id, session_number;
```

Interview trade-offs to state out loud:

+ Star versus snowflake: star by default, snowflake when a sub-dimension is large and shared.
+ Partition versus cluster: partition on the common date filter, cluster on the join keys inside the partition.
+ Batch versus streaming: batch for reconciliations and history, streaming for operational freshness and alerts.
+ Warehouse versus lakehouse: warehouse for a managed high-concurrency BI service, lakehouse for open formats and
  multiple engines.

Example: SCD2 customer history that keeps the version that was active when each order happened.

```sql
-- Close the changed versions and insert the new current version.
UPDATE dim_customer d
SET    end_date = s.effective_date - INTERVAL '1 day',
       is_current = FALSE
FROM   staging.customer_delta s
WHERE  d.customer_id = s.customer_id
  AND  d.is_current
  AND  (d.city, d.segment) IS DISTINCT FROM (s.city, s.segment);

-- Facts store the surrogate key of the version valid at event time, not the current row.
INSERT INTO fct_orders (order_id, order_date, customer_sk, net_amount)
SELECT o.order_id, o.order_date, d.customer_sk, o.net_amount
FROM   staging.orders o
JOIN   dim_customer d
       ON d.customer_id = o.customer_id
      AND o.order_date BETWEEN d.start_date AND d.end_date;
```

Example: inventory snapshot fact, one row per product per store per day.

```sql
INSERT INTO fct_inventory_daily (date_sk, product_sk, store_sk, units_on_hand, inventory_value)
SELECT d.date_sk,
       p.product_sk,
       s.store_sk,
       i.units_on_hand,
       i.units_on_hand * p.unit_cost AS inventory_value
FROM   staging.inventory_snapshot i
JOIN   dim_date d    ON d.date = i.snapshot_date
JOIN   dim_product p ON p.product_id = i.product_id
JOIN   dim_store s   ON s.store_id = i.store_id;
```

`units_on_hand` is semi-additive: sum it across products and stores, but never across days, because stock levels are
point-in-time balances.

[Table of Contents](#Data-Warehousing-Architecture)
