## [Main title](../README.md)
### [Interview questions](full.md)

# Data Structures

**Notebook:** [`notebooks/topics/data-structure.ipynb`](../notebooks/topics/data-structure.ipynb) - runnable version of this topic with self-checking exercises.

+ [What is data structure?](#what-is-data-structure)
+ [What are the goals of data structure?](#what-are-the-goals-of-data-structure)
+ [What does abstract data type mean?](#what-does-abstract-data-type-mean)
+ [What is the difference between a stack and an array?](#what-is-the-difference-between-a-stack-and-an-array)
+ [What do you mean by recursive definition?](#what-do-you-mean-by-recursive-definition)
+ [What is sequential search?](#what-is-sequential-search)
+ [What actions are performed when a function is called?](#what-actions-are-performed-when-a-function-is-called)
+ [What actions are performed when a function returns?](#what-actions-are-performed-when-a-function-returns)
+ [What is a linked list?](#what-is-a-linked-list)
+ [What are the advantages of linked list over array (static data structure)?](#what-are-the-advantages-of-linked-list-over-array-static-data-structure)
+ [We apply binary search algorithm to a sorted linked list why?](#we-apply-binary-search-algorithm-to-a-sorted-linked-list-why)
+ [What do you mean by free pool?](#what-do-you-mean-by-free-pool)
+ [What do you mean by garbage collection?](#what-do-you-mean-by-garbage-collection)
+ [What do you mean by overflow and underflow?](#what-do-you-mean-by-overflow-and-underflow)
+ [What are the disadvantages array implementations of linked list?](#what-are-the-disadvantages-array-implementations-of-linked-list)
+ [What is a queue?](#what-is-a-queue)
+ [What is a priority queue?](#what-is-a-priority-queue)
+ [What are the disadvantages of sequential storage?](#what-are-the-disadvantages-of-sequential-storage)
+ [What are the disadvantages of representing a stack or queue by a linked list?](#what-are-the-disadvantages-of-representing-a-stack-or-queue-by-a-linked-list)
+ [What is dangling pointer and how to avoid it?](#what-is-dangling-pointer-and-how-to-avoid-it)
+ [What are the disadvantages of linear list?](#what-are-the-disadvantages-of-linear-list)
+ [Define circular list?](#define-circular-list)
+ [What are the disadvantages of circular list?](#what-are-the-disadvantages-of-circular-list)
+ [Define double linked list?](#define-double-linked-list)
+ [Is it necessary to sort a file before searching a particular item?](#is-it-necessary-to-sort-a-file-before-searching-a-particular-item)
+ [What are the issues that hamper the efficiency in sorting a file?](#what-are-the-issues-that-hamper-the-efficiency-in-sorting-a-file)
+ [Calculate the efficiency of sequential search?](#calculate-the-efficiency-of-sequential-search)
+ [Is any implicit arguments are passed to a function when it is called?](#is-any-implicit-arguments-are-passed-to-a-function-when-it-is-called)
+ [Parenthesis is never required in postfix or prefix expressions and why?](#parenthesis-is-never-required-in-postfix-or-prefix-expressions-and-why)
+ [List out the areas in which data structures are applied extensively?](#list-out-the-areas-in-which-data-structures-are-applied-extensively)
+ [What are the major data structures used in the following areas network data model and hierarchical data model?](#what-are-the-major-data-structures-used-in-the-following-areas-network-data-model-and-hierarchical-data-model)
+ [If you are using c language to implement the heterogeneous linked list and what pointer type will you use?](#if-you-are-using-c-language-to-implement-the-heterogeneous-linked-list-and-what-pointer-type-will-you-use)
+ [Minimum number of queues needed to implement the priority queue?](#minimum-number-of-queues-needed-to-implement-the-priority-queue)
+ [What is the data structures used to perform recursion?](#what-is-the-data-structures-used-to-perform-recursion)
+ [What are the notations used in evaluation of arithmetic expressions using prefix and postfix forms?](#what-are-the-notations-used-in-evaluation-of-arithmetic-expressions-using-prefix-and-postfix-forms)
+ [List out few of the application of tree data structure?](#list-out-few-of-the-application-of-tree-data-structure)
+ [List out few of the applications that make use of multilinked structures?](#list-out-few-of-the-applications-that-make-use-of-multilinked-structures)
+ [What is the type of the algorithm used in solving the 8 queens problem?](#what-is-the-type-of-the-algorithm-used-in-solving-the-8-queens-problem)
+ [In an avl tree, at what condition the balancing is to be done?](#in-an-avl-tree-at-what-condition-the-balancing-is-to-be-done)
+ [In rdbms  what is the efficient data structure used in the internal storage representation?](#in-rdbms-what-is-the-efficient-data-structure-used-in-the-internal-storage-representation)
+ [What is a spanning tree?](#what-is-a-spanning-tree)
+ [Does the minimal spanning tree of a graph give the shortest distance between any 2 specified nodes?](#does-the-minimal-spanning-tree-of-a-graph-give-the-shortest-distance-between-any-2-specified-nodes)
+ [Difference between calloc and malloc?](#difference-between-calloc-and-malloc)
+ [Which file contains the definition of member functions?](#which-file-contains-the-definition-of-member-functions)
+ [How is any data structure application is classified among files?](#how-is-any-data-structure-application-is-classified-among-files)
+ [What member function places a new node at the end of the linked list?](#what-member-function-places-a-new-node-at-the-end-of-the-linked-list)
+ [What is linked list?](#what-is-linked-list)
+ [What does each entry in the link list called?](#what-does-each-entry-in-the-link-list-called)
+ [How is the front of the queue calculated?](#how-is-the-front-of-the-queue-calculated)
+ [Which process places data at the back of the queue?](#which-process-places-data-at-the-back-of-the-queue)
+ [What is the relationship between a queue and its underlying array?](#what-is-the-relationship-between-a-queue-and-its-underlying-array)
+ [What is a queue?](#what-is-a-queue-1)
+ [What does isempty member method determines?](#what-does-isempty-member-method-determines)
+ [What method is used to place a value onto the top of a stack?](#what-method-is-used-to-place-a-value-onto-the-top-of-a-stack)
+ [Run time memory allocation is known as?](#run-time-memory-allocation-is-known-as)
+ [How do you assign an address to an element of a pointer array?](#how-do-you-assign-an-address-to-an-element-of-a-pointer-array)
+ [Why do we use a multidimensional array?](#why-do-we-use-a-multidimensional-array)
+ [Is pointer a variable?](#is-pointer-a-variable)
+ [How many parts are there in a declaration statement?](#how-many-parts-are-there-in-a-declaration-statement)
+ [What is impact of signed numbers on the memory?](#what-is-impact-of-signed-numbers-on-the-memory)
+ [What is precision?](#what-is-precision)
+ [What is the difference between null and void pointer?](#what-is-the-difference-between-null-and-void-pointer)
+ [What is the difference between array and stack?](#what-is-the-difference-between-array-and-stack)
+ [Tell how to check whether a linked list is circular?](#tell-how-to-check-whether-a-linked-list-is-circular)
+ [Whether linked list is linear or non-linear data structure?](#whether-linked-list-is-linear-or-non-linear-data-structure)
+ [If you are using c language to implement the heterogeneous linked list and what pointer type will you use?](#if-you-are-using-c-language-to-implement-the-heterogeneous-linked-list-and-what-pointer-type-will-you-use-1)
+ [What is a node class?](#what-is-a-node-class)
+ [When can you tell that a memory leak will occur?](#when-can-you-tell-that-a-memory-leak-will-occur)
+ [How many trees are possible with 10 nodes?](#how-many-trees-are-possible-with-10-nodes)
+ [How can i search for data in a linked list?](#how-can-i-search-for-data-in-a-linked-list)
+ [Define data structures?](#define-data-structures)
+ [Define primary data structures?](#define-primary-data-structures)
+ [Define static data structures?](#define-static-data-structures)
+ [Define dynamic data structures?](#define-dynamic-data-structures)
+ [List some dynamic data structures in c?](#list-some-dynamic-data-structures-in-c)
+ [Define linear data structures?](#define-linear-data-structures)
+ [Define non-linear data structures?](#define-non-linear-data-structures)
+ [Define linked lists?](#define-linked-lists)
+ [State the different types of linked lists?](#state-the-different-types-of-linked-lists)
+ [List the basic operations carried out in a linked list?](#list-the-basic-operations-carried-out-in-a-linked-list)
+ [List out the advantages of using a linked list?](#list-out-the-advantages-of-using-a-linked-list)
+ [List out the disadvantages of using a linked list?](#list-out-the-disadvantages-of-using-a-linked-list)
+ [List out the applications of a linked list?](#list-out-the-applications-of-a-linked-list)
+ [Define a stack?](#define-a-stack)
+ [List out the basic operations that can be performed on a stack?](#list-out-the-basic-operations-that-can-be-performed-on-a-stack)
+ [State the different ways of representing expressions?](#state-the-different-ways-of-representing-expressions)
+ [State the advantages of using infix notations?](#state-the-advantages-of-using-infix-notations)
+ [State the advantages of using postfix notations?](#state-the-advantages-of-using-postfix-notations)
+ [State the rules to be followed during infix to postfix conversions?](#state-the-rules-to-be-followed-during-infix-to-postfix-conversions)
+ [State the rules to be followed during infix to prefix conversions?](#state-the-rules-to-be-followed-during-infix-to-prefix-conversions)
+ [State the difference between stacks and linked lists?](#state-the-difference-between-stacks-and-linked-lists)
+ [Mention the advantages of representing stacks using linked lists than arrays?](#mention-the-advantages-of-representing-stacks-using-linked-lists-than-arrays)
+ [Define a queue?](#define-a-queue)
+ [Define a priority queue?](#define-a-priority-queue)
+ [State the difference between queues and linked lists?](#state-the-difference-between-queues-and-linked-lists)
+ [Which data structures are most useful in data engineering interviews?](#which-data-structures-are-most-useful-in-data-engineering-interviews)
+ [How would you find the top K records in a large stream?](#how-would-you-find-the-top-k-records-in-a-large-stream)
+ [Define a deque?](#define-a-deque)
+ [Why you need a data structure?](#why-you-need-a-data-structure)
+ [What do you mean by shortest path?](#what-do-you-mean-by-shortest-path)
+ [What do you mean by articulation point?](#what-do-you-mean-by-articulation-point)
+ [Define biconnectivity?](#define-biconnectivity)
+ [What do you mean by back edge?](#what-do-you-mean-by-back-edge)
+ [What do you mean by tree edge?](#what-do-you-mean-by-tree-edge)
+ [What do you mean by breadth first search?](#what-do-you-mean-by-breadth-first-search)
+ [List the two important key points of depth first search?](#list-the-two-important-key-points-of-depth-first-search)
+ [Define graph traversals?](#define-graph-traversals)
+ [Name two algorithms two find minimum spanning tree?](#name-two-algorithms-two-find-minimum-spanning-tree)
+ [What is a minimum spanning tree?](#what-is-a-minimum-spanning-tree)
+ [What are the two traversal strategies used in traversing a graph?](#what-are-the-two-traversal-strategies-used-in-traversing-a-graph)
+ [When is a graph said to be weakly connected?](#when-is-a-graph-said-to-be-weakly-connected)
+ [What is meant by strongly connected in a graph?](#what-is-meant-by-strongly-connected-in-a-graph)
+ [What is an acyclic graph?](#what-is-an-acyclic-graph)
+ [What is a cycle or a circuit?](#what-is-a-cycle-or-a-circuit)
+ [What is a simple path?](#what-is-a-simple-path)
+ [Define path in a graph?](#define-path-in-a-graph)
+ [Define indegree of a graph?](#define-indegree-of-a-graph)
+ [Define outdegree of a graph?](#define-outdegree-of-a-graph)
+ [What is a weighted graph?](#what-is-a-weighted-graph)
+ [What is a simple graph?](#what-is-a-simple-graph)
+ [What is a loop?](#what-is-a-loop)
+ [What is undirected graph?](#what-is-undirected-graph)
+ [What is a directed graph?](#what-is-a-directed-graph)
+ [Define adjacent nodes?](#define-adjacent-nodes)
+ [Define graph?](#define-graph)
+ [What is the need for path compression?](#what-is-the-need-for-path-compression)
+ [What do you mean by union by weight?](#what-do-you-mean-by-union-by-weight)
+ [List the abstract operations in the set?](#list-the-abstract-operations-in-the-set)
+ [Define a set?](#define-a-set)
+ [What do you mean by disjoint set adt?](#what-do-you-mean-by-disjoint-set-adt)
+ [List the applications of set adt?](#list-the-applications-of-set-adt)
+ [Define an equivalence relation?](#define-an-equivalence-relation)
+ [Define a relation?](#define-a-relation)
+ [Mention one advantage and disadvantage of using quadratic probing?](#mention-one-advantage-and-disadvantage-of-using-quadratic-probing)
+ [List the limitations of linear probing?](#list-the-limitations-of-linear-probing)
+ [What is the need for extendable hashing?](#what-is-the-need-for-extendable-hashing)
+ [What do you mean by rehashing?](#what-do-you-mean-by-rehashing)
+ [What do you mean by double hashing?](#what-do-you-mean-by-double-hashing)
+ [What do you mean by secondary clustering?](#what-do-you-mean-by-secondary-clustering)
+ [What do you mean by quadratic probing?](#what-do-you-mean-by-quadratic-probing)
+ [What do you mean by primary clustering?](#what-do-you-mean-by-primary-clustering)
+ [What do you mean by linear probing?](#what-do-you-mean-by-linear-probing)
+ [What do you mean by probing?](#what-do-you-mean-by-probing)
+ [What are the types of collision resolution strategies in open addressing?](#what-are-the-types-of-collision-resolution-strategies-in-open-addressing)
+ [What do you mean by open addressing?](#what-do-you-mean-by-open-addressing)
+ [Write the disadvantages of separate chaining?](#write-the-disadvantages-of-separate-chaining)
+ [Write the advantage of separate chaining?](#write-the-advantage-of-separate-chaining)
+ [What do you mean by separate chaining?](#what-do-you-mean-by-separate-chaining)
+ [What are the collision resolution methods?](#what-are-the-collision-resolution-methods)
+ [What do you mean by collision in hashing?](#what-do-you-mean-by-collision-in-hashing)
+ [Write the importance of hashing?](#write-the-importance-of-hashing)
+ [What do you mean by hash function?](#what-do-you-mean-by-hash-function)
+ [What do you mean by hash table?](#what-do-you-mean-by-hash-table)
+ [Define hashing?](#define-hashing)
+ [What do you mean by the term percolate down?](#what-do-you-mean-by-the-term-percolate-down)
+ [What do you mean by the term percolate up?](#what-do-you-mean-by-the-term-percolate-up)
+ [What are the applications of priority queues?](#what-are-the-applications-of-priority-queues)
+ [What do you mean by heap order property?](#what-do-you-mean-by-heap-order-property)
+ [What do you mean by structure property in a heap?](#what-do-you-mean-by-structure-property-in-a-heap)
+ [What are the properties of binary heap?](#what-are-the-properties-of-binary-heap)
+ [What is the need for priority queue?](#what-is-the-need-for-priority-queue)
+ [What are the applications of b-tree?](#what-are-the-applications-of-b-tree)
+ [What do you mean by 2-3-4 tree?](#what-do-you-mean-by-2-3-4-tree)
+ [What do you mean by 2-3 tree?](#what-do-you-mean-by-2-3-tree)
+ [Define b tree of order m?](#define-b-tree-of-order-m)
+ [What is the minimum number of nodes in an avl tree of height h?](#what-is-the-minimum-number-of-nodes-in-an-avl-tree-of-height-h)
+ [Define heap?](#define-heap)
+ [List the types of rotations available in splay tree?](#list-the-types-of-rotations-available-in-splay-tree)
+ [What is the idea behind splaying?](#what-is-the-idea-behind-splaying)
+ [Define splay tree?](#define-splay-tree)
+ [What do you mean by balance factor of a node in avl tree?](#what-do-you-mean-by-balance-factor-of-a-node-in-avl-tree)
+ [What are the categories of avl rotations?](#what-are-the-categories-of-avl-rotations)
+ [What do you mean by balanced trees?](#what-do-you-mean-by-balanced-trees)
+ [Define avl tree?](#define-avl-tree)
+ [Define left in threaded tree?](#define-left-in-threaded-tree)
+ [Define right in threaded tree?](#define-right-in-threaded-tree)
+ [What is an expression tree?](#what-is-an-expression-tree)
+ [What is the use of threaded binary tree?](#what-is-the-use-of-threaded-binary-tree)
+ [Why it is said that searching a node in a binary search tree is efficient than that of a simple binary tree?](#why-it-is-said-that-searching-a-node-in-a-binary-search-tree-is-efficient-than-that-of-a-simple-binary-tree)
+ [Define ancestor and descendant?](#define-ancestor-and-descendant)
+ [What do you mean by general trees?](#what-do-you-mean-by-general-trees)
+ [Define a binary search tree?](#define-a-binary-search-tree)
+ [State the demerits of linked representation of binary trees?](#state-the-demerits-of-linked-representation-of-binary-trees)
+ [State the merit of linked representation of binary trees?](#state-the-merit-of-linked-representation-of-binary-trees)
+ [State the demerit of linear representation of binary trees?](#state-the-demerit-of-linear-representation-of-binary-trees)
+ [State the merits of linear representation of binary trees?](#state-the-merits-of-linear-representation-of-binary-trees)
+ [What are the tasks performed during postorder traversal?](#what-are-the-tasks-performed-during-postorder-traversal)
+ [What are the tasks performed during inorder traversal?](#what-are-the-tasks-performed-during-inorder-traversal)
+ [What are the tasks performed during preorder traversal?](#what-are-the-tasks-performed-during-preorder-traversal)
+ [What are the tasks performed while traversing a binary tree?](#what-are-the-tasks-performed-while-traversing-a-binary-tree)
+ [What are the different binary tree traversal techniques?](#what-are-the-different-binary-tree-traversal-techniques)
+ [What is meant by binary tree traversal?](#what-is-meant-by-binary-tree-traversal)
+ [State the properties of a binary tree?](#state-the-properties-of-a-binary-tree)
+ [Define a right-skewed binary tree?](#define-a-right-skewed-binary-tree)
+ [Define a complete binary tree?](#define-a-complete-binary-tree)
+ [Define a full binary tree ?](#define-a-full-binary-tree)
+ [Define non-terminal nodes in a tree?](#define-non-terminal-nodes-in-a-tree)
+ [Define terminal nodes in a tree?](#define-terminal-nodes-in-a-tree)
+ [Define a path in a tree?](#define-a-path-in-a-tree)
+ [Define a binary tree?](#define-a-binary-tree)
+ [Define forest?](#define-forest)
+ [What do you mean by level of the tree?](#what-do-you-mean-by-level-of-the-tree)
+ [Define depth and height of a tree?](#define-depth-and-height-of-a-tree)
+ [Define depth and height of a node?](#define-depth-and-height-of-a-node)
+ [Define parent node?](#define-parent-node)
+ [Define internal nodes?](#define-internal-nodes)
+ [Define leaves?](#define-leaves)
+ [Define degree of the node?](#define-degree-of-the-node)
+ [Define root?](#define-root)
+ [Define a tree?](#define-a-tree)
+ [Why we need cursor implementation of linked lists?](#why-we-need-cursor-implementation-of-linked-lists)
+ [List the applications of queues?](#list-the-applications-of-queues)
+ [List the applications of stacks?](#list-the-applications-of-stacks)
+ [What are the types of queues?](#what-are-the-types-of-queues)
+ [What are the objectives of studying data structures?](#what-are-the-objectives-of-studying-data-structures)
+ [State the difference between persistent and ephemeral data structure?](#state-the-difference-between-persistent-and-ephemeral-data-structure)
+ [State the difference between primitive and non-primitive data types?](#state-the-difference-between-primitive-and-non-primitive-data-types)
+ [What are the advantages of modularity?](#what-are-the-advantages-of-modularity)
+ [Define an abstract data type?](#define-an-abstract-data-type)
+ [Define data type and what are the types of data type?](#define-data-type-and-what-are-the-types-of-data-type)
+ [Difference between abstract data type and data type and data structure?](#difference-between-abstract-data-type-and-data-type-and-data-structure)
+ [State the difference between queues and linked lists?](#state-the-difference-between-queues-and-linked-lists-1)
+ [How do you deduplicate records at scale?](#how-do-you-deduplicate-records-at-scale)
+ [How do you order tasks with a dependency graph (DAG)?](#how-do-you-order-tasks-with-a-dependency-graph-dag)
+ [How do you find connected components for data lineage?](#how-do-you-find-connected-components-for-data-lineage)
+ [How do you compute a streaming median?](#how-do-you-compute-a-streaming-median)
+ [When should you use a hash map instead of a join?](#when-should-you-use-a-hash-map-instead-of-a-join)
+ [Real world use cases for data structures in data engineering](#real-world-use-cases-for-data-structures-in-data-engineering)

## What is data structure?

A data structure is a way of organizing data that considers not only the items stored, but also their relationship to each other. Advance knowledge about the relationship between data items allows designing of efficient algorithms for the manipulation of data.

[Table of Contents](#Data-Structures)

## What are the goals of data structure?

It must rich enough in structure to reflect the actual relationship of data in real world. The structure should be simple enough for efficient processing of data.

[Table of Contents](#Data-Structures)

## What does abstract data type mean?

Data type is a collection of values and a set of operations on these values. Abstract data type refer to the mathematical concept that define the data type.
It is a useful tool for specifying the logical properties of a data type.
ADT consists of two parts
1) Values definition
2) Operation definition
   Example:-The value definition for the ADT RATIONAL states that RATIONAL value consists of two integers, second doesnt equal to zero.
   The operator definition for ADT RATIONAL includes the operation of creation (make rational) addition, multiplication and test for equality.

[Table of Contents](#Data-Structures)

## What is the difference between a stack and an array?

STACK:
i) Stack is a ordered collection of items.
ii) Stack is a dynamic object whose size is constantly changing as items are pushed and popped.
iii) Stack may contain different data types.
iv) Stack is declared as a structure containing an array to hold the element of the stack, and an integer to indicate the current stack top within the array.
ARRAY:
i) Array is an ordered collection of items.
ii) Array is a static object i.e. no of item is fixed and is assigned by the declaration of the array.
iii) It contains same data types.
iv) Array can be home of a stack i.e. array can be declared large enough for maximum size of the stack.

Python example: an array supports random access by index, while a stack only exposes the top.

```python
from array import array

values = array("i", [10, 20, 30])
assert values[1] == 20          # O(1) random access
values[1] = 25                  # mutable by index

stack = []
stack.append(10)                # push
stack.append(20)
assert stack[-1] == 20          # peek
assert stack.pop() == 20        # pop, LIFO
```

[Table of Contents](#Data-Structures)

## What do you mean by recursive definition?

The definition which defines an object in terms of simpler cases of itself is called recursive definition.

[Table of Contents](#Data-Structures)

## What is sequential search?

In sequential search each item in the array is compared with the item being searched until a match occurs. It is applicable to a table organized either as an array or as a linked list.

Python example: linear search returns the first matching index and costs O(n) comparisons.

```python
def linear_search(values, target):
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1

assert linear_search([3, 1, 4, 1, 5], 4) == 2
assert linear_search([3, 1, 4], 9) == -1
```

[Table of Contents](#Data-Structures)

## What actions are performed when a function is called?

When a function is called
i) arguments are passed.
ii) local variables are allocated and initialized.
ii) transferring control to the function.

[Table of Contents](#Data-Structures)

## What actions are performed when a function returns?

i) Return address is retrieved.
ii) Functions data area is freed.
iii) Branch is taken to the return address.

[Table of Contents](#Data-Structures)

## What is a linked list?

A linked list is a linear collection of data elements, called nodes, where the linear order is given by pointers. Each node has two parts first part contain the information of the element second part contains the address of the next node in the list.

Python example: a node holds a value and a reference to the next node. Traversal is O(n) and insertion at the head is O(1).

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    value: int
    next: Optional["Node"] = None

def to_list(head):
    values = []
    while head:
        values.append(head.value)
        head = head.next
    return values

head = Node(1, Node(2, Node(3)))
assert to_list(head) == [1, 2, 3]
```

[Table of Contents](#Data-Structures)

## What are the advantages of linked list over array (static data structure)?

The disadvantages of array are:
i) unlike linked list it is expensive to insert and delete elements in the array.
ii) One cant double or triple the size of array as it occupies block of memory space.
In linked list
i) each element in list contains a field, called a link or pointer which contains the address of the next element.
ii) Successive elements need not occupy adjacent space in memory.

Insertion and deletion are O(1) once you hold the predecessor, while an array shifts every later element.

```python
def insert_after(node, value):
    node.next = type(node)(value, node.next)

head = Node(1, Node(3))
insert_after(head, 2)
print([n for n in (lambda h: [h.value, h.next.value, h.next.next.value])(head)])
```

[Table of Contents](#Data-Structures)

## We apply binary search algorithm to a sorted linked list why?

No we cannot apply binary search algorithm to a sorted linked list, since there is no way of indexing the middle element in the list. This is the drawback in using linked list as a data structure.

Binary search needs random access to the middle element. A linked list only supports sequential traversal, so the conversion to an indexable list first is O(n). Use binary search on an array-like structure instead.

```python
import bisect

def binary_search(values, target):
    i = bisect.bisect_left(values, target)
    return i if i < len(values) and values[i] == target else -1

assert binary_search([1, 3, 4, 7, 9], 7) == 3
```

[Table of Contents](#Data-Structures)

## What do you mean by free pool?

Pool is a list consisting of unused memory cells which has its own pointer.

A free pool is the list of unused nodes that an allocator can hand out again.

```python
class Pool:
    def __init__(self, nodes):
        self.free = list(nodes)

    def acquire(self):
        return self.free.pop() if self.free else None

    def release(self, node):
        node.next = None
        self.free.append(node)

pool = Pool([Node(1), Node(2)])
node = pool.acquire()
pool.release(node)
assert len(pool.free) == 2
```

[Table of Contents](#Data-Structures)

## What do you mean by garbage collection?

It is a technique in which the operating system periodically collects all the deleted space onto the free storage list.
It takes place when there is minimum amount of space left in storage list or when CPU is ideal.
The alternate method to this is to immediately reinsert the space into free storage list which is time consuming.

Python uses reference counting plus a cycle collector, so dropping the last reference to a list frees it.

```python
import gc

class Node:
    def __init__(self):
        self.next = None

a, b = Node(), Node()
a.next, b.next = b, a          # reference cycle
del a, b
collected = gc.collect()       # breaks the cycle
print("collected", collected >= 0)
```

[Table of Contents](#Data-Structures)

## What do you mean by overflow and underflow?

When new data is to be inserted into the data structure but there is no available space i.e. free storage list is empty this situation is called overflow.
When we want to delete data from a data structure that is empty this situation is called underflow.

```python
class BoundedStack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def push(self, value):
        if len(self.items) == self.capacity:
            raise OverflowError("stack overflow")
        self.items.append(value)

    def pop(self):
        if not self.items:
            raise IndexError("stack underflow")
        return self.items.pop()

stack = BoundedStack(1)
stack.push(1)
try:
    stack.push(2)
except OverflowError as exc:
    print(exc)
```

[Table of Contents](#Data-Structures)

## What are the disadvantages array implementations of linked list?

i) The no of nodes needed cant be predicted when the program is written.
ii) The no of nodes declared must remain allocated throughout its execution.

[Table of Contents](#Data-Structures)

## What is a queue?

A queue is an ordered collection of items from which items may be deleted at one end (front end) and items inserted at the other end (rear end).
It obeys FIFO rule there is no limit to the number of elements a queue contains.

[Table of Contents](#Data-Structures)

## What is a priority queue?

The priority queue is a data structure in which the intrinsic ordering of the elements (numeric or alphabetic)
Determines the result of its basic operation. It is of two types:
i) Ascending priority queue- Here smallest item can be removed (insertion is arbitrary).
ii) Descending priority queue- Here largest item can be removed (insertion is arbitrary).

Python's `heapq` is a binary min-heap. Push and pop are O(log n).

```python
import heapq

tasks = []
heapq.heappush(tasks, (3, "low"))
heapq.heappush(tasks, (1, "high"))
heapq.heappush(tasks, (2, "medium"))
assert heapq.heappop(tasks) == (1, "high")
```

[Table of Contents](#Data-Structures)

## What are the disadvantages of sequential storage?

i) Fixed amount of storage remains allocated to the data structure even if it contains less element.
ii) No more than fixed amount of storage is allocated causing overflow.

[Table of Contents](#Data-Structures)

## What are the disadvantages of representing a stack or queue by a linked list?

i) A node in a linked list (info and next field) occupies more storage than a corresponding element in an array.
ii) Additional time spent in managing the available list.
Object Oriented Analysis and Design Tutorial

[Table of Contents](#Data-Structures)

## What is dangling pointer and how to avoid it?

After a call to free(p) makes a subsequent reference to *p illegal, i.e. though the storage to p is freed but the value of p(address) remain unchanged .so the object at that address may be used as the value of *p (i.e. there is no way to detect the illegality).Here p is called dangling pointer.
To avoid this it is better to set p to NULL after executing free(p).The null pointer value doesnt reference a storage location it is a pointer that doesnt point to anything.

[Table of Contents](#Data-Structures)

## What are the disadvantages of linear list?

i) We cannot reach any of the nodes that precede node (p).
ii) If a list is traversed, the external pointer to the list must be persevered in order to reference the list again.

[Table of Contents](#Data-Structures)

## Define circular list?

In linear list the next field of the last node contain a null pointer, when a next field in the last node contain a pointer back to the first node it is called circular list.
Advantages – From any point in the list it is possible to reach at any other point.

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

a, b, c = Node(1), Node(2), Node(3)
a.next, b.next, c.next = b, c, a     # circular

def is_circular(head):
    walker, runner = head, head
    while runner and runner.next:
        walker, runner = walker.next, runner.next.next
        if walker is runner:
            return True
    return False

assert is_circular(a)
```

[Table of Contents](#Data-Structures)

## What are the disadvantages of circular list?

i) We cant traverse the list backward.
ii) If a pointer to a node is given we cannot delete the node.
Computer architecture Interview Questions

[Table of Contents](#Data-Structures)

## Define double linked list?

It is a collection of data elements called nodes,
where each node is divided into three parts:
An info field that contains the information stored in the node.
Left field that contain pointer to node on left side.
Right field that contain pointer to node on right side.
Adv Java Interview Questions

```python
class DNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

a, b = DNode(1), DNode(2)
a.next, b.prev = b, a
assert b.prev.value == 1 and a.next.value == 2
```

[Table of Contents](#Data-Structures)

## Is it necessary to sort a file before searching a particular item?

If less work is involved in searching a element than to sort and then extract, then we dont go for sort.
If frequent use of the file is required for the purpose of retrieving specific element, it is more efficient to sort the file.
Thus it depends on situation.

[Table of Contents](#Data-Structures)

## What are the issues that hamper the efficiency in sorting a file?

The issues are:
Length of time required by the programmer in coding a particular sorting program.
Amount of machine time necessary for running the particular program.
The amount of space necessary for the particular program .
Object Oriented Analysis and Design Interview Questions

Python's built-in sort is O(n log n) and stable, which matters when you sort by one key but want ties to keep the
original order.

```python
rows = [
    {"tenant": "b", "amount": 5},
    {"tenant": "a", "amount": 9},
    {"tenant": "a", "amount": 3},
]
rows.sort(key=lambda row: row["tenant"])                       # stable
rows.sort(key=lambda row: row["amount"], reverse=True)         # stable, so equal amounts keep tenant order
assert rows[0]["amount"] == 9

# External sort for a file larger than memory: sort chunks, then k-way merge.
import heapq

def merge_sorted_chunks(chunks):
    return list(heapq.merge(*chunks))

assert merge_sorted_chunks([[1, 4], [2, 3]]) == [1, 2, 3, 4]
```

The classic efficiency issues are the same as in the prose: coding time, machine time, and memory. Use a key function
so the comparison is cheap, and for datasets larger than RAM use external merge sort or let the warehouse spill.

[Table of Contents](#Data-Structures)

## Calculate the efficiency of sequential search?

The number of comparisons depends on where the record with the argument key appears in the table.

Complexity summary for a table of `n` records:

+ Best case: 1 comparison (target is the first record).
+ Worst case: `n` comparisons (target is last or absent).
+ Average case: `(n + 1) / 2` comparisons for a successful search.

```python
def comparisons_for_linear_search(values, target):
    count = 0
    for value in values:
        count += 1
        if value == target:
            return count
    return count

assert comparisons_for_linear_search([1, 2, 3, 4], 4) == 4
assert comparisons_for_linear_search([1, 2, 3, 4], 99) == 4
```

[Table of Contents](#Data-Structures)

## Is any implicit arguments are passed to a function when it is called?

Yes there is a set of implicit arguments that contain information necessary for the function to execute and return correctly. One of them is return address which is stored within the functions data area, at the time of returning to calling program the address is retrieved and the function branches to that location.

[Table of Contents](#Data-Structures)

## Parenthesis is never required in postfix or prefix expressions and why?

Parenthesis is not required because the order of the operators in the postfix /prefix expressions determines the actual order of operations in evaluating the expression.

[Table of Contents](#Data-Structures)

## List out the areas in which data structures are applied extensively?

Compiler Design,
Operating System,
Database Management System,
Statistical analysis package,
Numerical Analysis,
Graphics,
Artificial Intelligence,
Simulation.

Data engineering example: a pipeline scheduler stores its task graph as an adjacency list, uses a queue for breadth-first execution, and a heap for priority scheduling by SLA.

```python
tasks = {"extract": ["clean"], "clean": ["load"], "load": []}
indegree = {node: 0 for node in tasks}
for children in tasks.values():
    for child in children:
        indegree[child] += 1
print(indegree)  # {'extract': 0, 'clean': 1, 'load': 1}
```

[Table of Contents](#Data-Structures)

## What are the major data structures used in the following areas network data model and hierarchical data model?

RDBMS – Array (i.e. Array of structures)
Network data model – Graph
Hierarchical data model – Trees

[Table of Contents](#Data-Structures)

## If you are using c language to implement the heterogeneous linked list and what pointer type will you use?

The heterogeneous linked list contains different data types in its nodes and we need a link, pointer to connect them. It is not possible to use ordinary pointers for this. So we go for void pointer. Void pointer is capable of storing pointer to any type as it is a generic pointer type.

[Table of Contents](#Data-Structures)

## Minimum number of queues needed to implement the priority queue?

Two. One queue is used for actual storing of data and another for storing priorities.

Two plain FIFO queues are enough: one holds the values and one holds the matching priorities. Real implementations use a heap instead, which gives O(log n) inserts and O(1) peeks at the minimum.

```python
import heapq
heap = []
heapq.heappush(heap, (2, "two"))
heapq.heappush(heap, (1, "one"))
assert heap[0] == (1, "one")    # O(1) peek at the highest priority
```

[Table of Contents](#Data-Structures)

## What is the data structures used to perform recursion?

Stack. Because of its LIFO (Last In First Out) property it remembers its caller so knows whom to return when the function has to return. Recursion makes use of system stack for storing the return addresses of the function calls.
Every recursive function has its equivalent iterative (non-recursive) function. Even when such equivalent iterative procedures are written, explicit stack is to be used.

The call stack holds one frame per unfinished call. That is why a deep recursion can overflow, and why the same
recurrence can be rewritten as a loop or as dynamic programming.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

assert fib(30) == 832040

# Bottom-up DP: the same recurrence with a table instead of the call stack.
def fib_dp(n):
    table = [0, 1]
    for i in range(2, n + 1):
        table.append(table[i - 1] + table[i - 2])
    return table[n]

assert fib_dp(30) == 832040
```

Data engineering link: counting session paths in clickstream data is the same DP shape, with a table of path
counts per page instead of Fibonacci numbers.

[Table of Contents](#Data-Structures)

## What are the notations used in evaluation of arithmetic expressions using prefix and postfix forms?

Polish and Reverse Polish notations.

[Table of Contents](#Data-Structures)

## List out few of the application of tree data structure?

The manipulation of Arithmetic expression, Symbol Table construction & Syntax analysis.

[Table of Contents](#Data-Structures)

## List out few of the applications that make use of multilinked structures?

Sparse matrix, Index generation.

[Table of Contents](#Data-Structures)

## What is the type of the algorithm used in solving the 8 queens problem?

Backtracking.

Backtracking with pruning: place one queen per row and reject a column or diagonal already attacked.

```python
def solve_n_queens(n):
    solutions, board = [], []

    def safe(row, col):
        return all(col != c and abs(row - r) != abs(col - c) for r, c in board)

    def place(row):
        if row == n:
            solutions.append(list(board))
            return
        for col in range(n):
            if safe(row, col):
                board.append((row, col))
                place(row + 1)
                board.pop()

    place(0)
    return solutions

assert len(solve_n_queens(4)) == 2
```

[Table of Contents](#Data-Structures)

## In an avl tree, at what condition the balancing is to be done?

If the pivotal value (or the Height factor) is greater than 1 or less than –1.

[Table of Contents](#Data-Structures)

## In rdbms  what is the efficient data structure used in the internal storage representation?

B+ tree. Because in B+ tree, all the data is stored only in leaf nodes, that makes searching easier. This corresponds to the records that shall be stored in leaf nodes.

[Table of Contents](#Data-Structures)

## What is a spanning tree?

A spanning tree is a tree associated with a network. All the nodes of the graph appear on the tree once. A minimum spanning tree is a spanning tree organized so that the total edge weight between nodes is minimized.

A spanning tree connects all vertices with exactly `V - 1` edges and no cycles. A minimum spanning tree minimises the
total edge weight.

```python
nodes = ["a", "b", "c"]
edges = [(1, "a", "b"), (2, "b", "c"), (5, "a", "c")]
total, tree = kruskal(nodes, edges)
assert len(tree) == len(nodes) - 1
```

[Table of Contents](#Data-Structures)

## Does the minimal spanning tree of a graph give the shortest distance between any 2 specified nodes?

No! Minimal spanning tree assures that the total weight of the tree is kept at its minimum. But it doesnt mean that the distance between any two nodes involved in the minimal-spanning tree is minimum.

[Table of Contents](#Data-Structures)

## Difference between calloc and malloc?

malloc: allocate n bytes.
calloc: allocate m times n bytes initialized to 0.

[Table of Contents](#Data-Structures)

## Which file contains the definition of member functions?

Definitions of member functions for the Linked List class are contained in the LinkedList.cpp file.

[Table of Contents](#Data-Structures)

## How is any data structure application is classified among files?

A linked list application can be organized into a header file, source file and main application file. The first file is the header file that contains the definition of the NODE structure and the LinkedList class definition. The second file is a source code file containing the implementation of member functions of the LinkedList class. The last file is the application file that contains code that creates and uses the LinkedList class.

[Table of Contents](#Data-Structures)

## What member function places a new node at the end of the linked list?

The appendNode() member function places a new node at the end of the linked list. The appendNode() requires an integer representing the current data of the node.

[Table of Contents](#Data-Structures)

## What is linked list?

Linked List is one of the fundamental data structures. It consists of a sequence of ? nodes, each containing arbitrary data fields and one or two (”links”) pointing to the next and/or previous nodes. A linked list is a self-referential datatype because it contains a pointer or link to another data of the same type. Linked lists permit insertion and removal of nodes at any point in the list in constant time, but do not allow random access.

[Table of Contents](#Data-Structures)

## What does each entry in the link list called?

Each entry in a linked list is called a node. Think of a node as an entry that has three sub entries. One sub entry contains the data, which may be one attribute or many attributes. Another points to the previous node, and the last points to the next node. When you enter a new item on a linked list, you allocate the new node and then set the pointers to previous and next nodes.

[Table of Contents](#Data-Structures)

## How is the front of the queue calculated?

The front of the queue is calculated by front = (front+1) % size.

[Table of Contents](#Data-Structures)

## Which process places data at the back of the queue?

Enqueue is the process that places data at the back of the queue.

[Table of Contents](#Data-Structures)

## What is the relationship between a queue and its underlying array?

Data stored in a queue is actually stored in an array. Two indexes, front and end will be used to identify the start and end of the queue.
When an element is removed front will be incremented by 1. In case it reaches past the last index available it will be reset to 0. Then it will be checked with end. If it is greater than end queue is empty.
When an element is added end will be incremented by 1. In case it reaches past the last index available it will be reset to 0. After incrementing it will be checked with front. If they are equal queue is full.

A circular buffer maps a logical queue onto a fixed array using modulo indices, which avoids shifting elements.

```python
def front_index(front, size):
    return front % size

front, size = 7, 5
assert front_index(front, size) == 2
```

[Table of Contents](#Data-Structures)

## What is a queue?

A Queue is a sequential organization of data. A queue is a first in first out type of data structure. An element is inserted at the last position and an element is always taken out from the first position.

[Table of Contents](#Data-Structures)

## What does isempty member method determines?

isEmpty() checks if the stack has at least one element. This method is called by Pop() before retrieving and returning the top element.

[Table of Contents](#Data-Structures)

## What method is used to place a value onto the top of a stack?

push() method, Push is the direction that data is being added to the stack. push() member method places a value onto the top of a stack.

[Table of Contents](#Data-Structures)

## Run time memory allocation is known as?

Allocating memory at runtime is called a dynamically allocating memory. In this, you dynamically allocate memory by using the new operator when declaring the array.

for example : int grades[] = new int[10];

[Table of Contents](#Data-Structures)

## How do you assign an address to an element of a pointer array?

We can assign a memory address to an element of a pointer array by using the address operator, which is the ampersand (&), in an assignment statement such as ptemployee[0] = &projects[2];

[Table of Contents](#Data-Structures)

## Why do we use a multidimensional array?

A multidimensional array can be useful to organize subgroups of data within an array. In addition to organizing data stored in elements of an array, a multidimensional array can store memory addresses of data in a pointer array and an array of pointers.
Multidimensional arrays are used to store information in a matrix form.
e.g; a railway timetable, schedule cannot be stored as a single dimensional array. One can use a 3-D array for storing height, width and length of each room on each floor of a building.

[Table of Contents](#Data-Structures)

## Is pointer a variable?

Yes, a pointer is a variable and can be used as an element of a structure and as an attribute of a class in some programming languages such as C++, but not Java. However, the contents of a pointer is a memory address of another location of memory, which is usually the memory address of another variable, element of a structure, or attribute of a class.

[Table of Contents](#Data-Structures)

## How many parts are there in a declaration statement?

There are two main parts, variable identifier and data type and the third type is optional which is type qualifier like signed/unsigned.

[Table of Contents](#Data-Structures)

## What is impact of signed numbers on the memory?

Sign of the number is the first bit of the storage allocated for that number. So you get one bit less for storing the number. For example if you are storing an 8-bit number, without sign, the range is 0-255. If you decide to store sign you get 7 bits for the number plus one bit for the sign. So the range is -128 to +127.

[Table of Contents](#Data-Structures)

## What is precision?

Precision is the total number of significant digits a value can hold, while scale is the number of digits kept after the decimal point. In SQL, `NUMERIC(10, 2)` has precision 10 and scale 2, so it stores up to 99,999,999.99. In Python floating point, precision describes how many significant decimal digits a float can represent without loss (about 15-17 for a 64-bit float).

[Table of Contents](#Data-Structures)

## What is the difference between null and void pointer?

NULL is a value that a pointer of any type may hold to mean "points to nothing". void is a type with no size; a `void *` is a generic pointer that can hold the address of any object type and must be cast before it is dereferenced. They are not the same thing: `void *ptr = NULL;` declares a generic pointer whose value is NULL.

[Table of Contents](#Data-Structures)

## What is the difference between array and stack?

STACK follows LIFO. Thus the item that is first entered would be the last removed.
In array the items can be entered or removed in any order. Basically each member access is done using index. No strict order is to be followed here to remove a particular element.
Array may be multidiamensional or onediamensional but stack should be onediamensional. but both are linear data structure.

[Table of Contents](#Data-Structures)

## Tell how to check whether a linked list is circular?

Create two pointers, each set to the start of the list. Update each as follows:

while (pointer1)
{
pointer1 = pointer1->next;
pointer2 = pointer2->next;
if(pointer2)pointer2=pointer2->next;
if (pointer1 == pointer2)
{
print (”circularn”);
}
}

Floyd's tortoise-and-hare detects a cycle in O(n) time and O(1) space.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

node = Node(1)
node.next = Node(2)
node.next.next = node          # points back to the head
assert has_cycle(node)
```

[Table of Contents](#Data-Structures)

## Whether linked list is linear or non-linear data structure?

According to Access strategies Linked list is a linear one.
According to Storage Linked List is a Non-linear one.

[Table of Contents](#Data-Structures)

## If you are using c language to implement the heterogeneous linked list and what pointer type will you use?

The heterogeneous linked list contains different data types in its nodes and we need a link, pointer to connect them. It is not possible to use ordinary pointers for this. So we go for void pointer. Void pointer is capable of storing pointer to any type as it is a generic pointer type.

[Table of Contents](#Data-Structures)

## What is a node class?

A node class is a class that, relies on the base class for services and implementation, provides a wider interface to users than its base class, relies primarily on virtual functions in its public interface depends on all its direct and indirect base class can be understood only in the context of the base class can be used as base for further derivation can be used to create objects. A node class is a class that has added new services or functionality beyond the services inherited from its base class.

In data engineering code the "node class" is usually a lightweight record for a graph or a linked structure. A
`dataclass` gives value equality for free, which is handy when nodes are used inside sets and dicts.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Task:
    name: str
    deps: tuple = field(default=())

extract = Task("extract")
clean = Task("clean", (extract.name,))
assert clean.deps == ("extract",)
```

[Table of Contents](#Data-Structures)

## When can you tell that a memory leak will occur?

A memory leak occurs when a program loses the ability to free a block of dynamically allocated memory.

[Table of Contents](#Data-Structures)

## How many trees are possible with 10 nodes?

Cayley's formula gives the number of labelled trees on n nodes as n^(n-2). For n = 10 that is 10^8 = 100,000,000 labelled trees. For n = 3 the formula gives 3^1 = 3 labelled trees, which are the three ways to choose the single internal node.

[Table of Contents](#Data-Structures)

## How can i search for data in a linked list?

Unfortunately, the only way to search a linked list is with a linear search, because the only way a linked list is members can be accessed is sequentially. Sometimes it is quicker to take the data from a linked list and store it in a different data structure so that searches can be more efficient.

A linked list only supports linear search, because you cannot index into the middle.

```python
def find(head, target):
    index = 0
    while head:
        if head.value == target:
            return index
        head = head.next
        index += 1
    return -1

assert find(Node(1, Node(2, Node(3))), 3) == 2
```

[Table of Contents](#Data-Structures)

## Define data structures?

Data Structures is defined as the way of organizing all data items that consider not only the elements stored but also stores the relationship between the elements.

[Table of Contents](#Data-Structures)

## Define primary data structures?

Primary data structures are the basic data structures that directly operate upon the machine instructions. All the basic constants (integers, floating-point numbers, character constants, string constants) and pointers are considered as primary data structures.

[Table of Contents](#Data-Structures)

## Define static data structures?

A data structure formed when the number of data items are known in advance is referred as static data structure or fixed size data structure.

[Table of Contents](#Data-Structures)

## Define dynamic data structures?

A data structure formed when the number of data items are not known in advance is known as dynamic data structure or variable size data structure.

[Table of Contents](#Data-Structures)

## List some dynamic data structures in c?

Some dynamic data structures in C are linked lists, stacks, queues, trees etc.

[Table of Contents](#Data-Structures)

## Define linear data structures?

Linear data structures are data structures having a linear relationship between its adjacent elements.
Eg; Linked lists.

[Table of Contents](#Data-Structures)

## Define non-linear data structures?

Non-linear data structures are data structures that dont have a linear relationship between its adjacent elements but have a hierarchical relationship between the elements.
Eg; Trees and Graphs.

[Table of Contents](#Data-Structures)

## Define linked lists?

Linked list consists of a series of structures, which are not necessarily adjacent in memory. Each structure contains the element and a pointer to a structure containing its successor. We call this the Next Pointer. The last cells Next pointer points to NULL.

[Table of Contents](#Data-Structures)

## State the different types of linked lists?

The different types of linked list include singly linked list, doubly linked list and circular linked list.

+ Singly linked: one `next` pointer.
+ Doubly linked: `prev` and `next`, needed for O(1) removal given only the node.
+ Circular: the last node points back to the head.

```python
class Singly:
    def __init__(self, value):
        self.value = value
        self.next = None

class Doubly(Singly):
    def __init__(self, value):
        super().__init__(value)
        self.prev = None

circular_tail = Singly(3)
circular_tail.next = circular_tail      # self loop, degenerate circular list
print(Singly(1).next, Doubly(1).prev, circular_tail.next is circular_tail)
```

[Table of Contents](#Data-Structures)

## List the basic operations carried out in a linked list?

The basic operations carried out in a linked list include:
Creation of a list.
Insertion of a node.
Deletion of a node.
Modification of a node.
Traversal of the list.

Create, insert, delete, modify, and traverse. The Python example below does all five on a singly linked list.

```python
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        node = Node(value)
        if not self.head:
            self.head = node
            return
        tail = self.head
        while tail.next:
            tail = tail.next
        tail.next = node

    def remove(self, value):
        dummy = Node(0, self.head)
        prev, cur = dummy, self.head
        while cur:
            if cur.value == value:
                prev.next = cur.next
                break
            prev, cur = cur, cur.next
        self.head = dummy.next

    def values(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

ll = LinkedList()
for v in (1, 2, 3):
    ll.append(v)
ll.remove(2)
assert ll.values() == [1, 3]
```

[Table of Contents](#Data-Structures)

## List out the advantages of using a linked list?

It is not necessary to specify the number of elements in a linked list during its declaration.
Linked list can grow and shrink in size depending upon the insertion and deletion that occurs in the list.
Insertions and deletions at any place in a list can be handled easily and efficiently.
A linked list does not waste any memory space.

Dynamic size, O(1) head insertion, and no shifting. The trade-off is O(n) search and pointer overhead per node.

```python
ll = LinkedList()
ll.append(1)
ll.append(2)
assert ll.values() == [1, 2]
```

[Table of Contents](#Data-Structures)

## List out the disadvantages of using a linked list?

Searching a particular element in a list is difficult and time consuming.
A linked list will use more storage space than an array to store the same number of elements.

[Table of Contents](#Data-Structures)

## List out the applications of a linked list?

Some important applications of linked lists are manipulation of polynomials, sparse matrices, stacks and queues.

A common data engineering use is an LRU cache: a hash map plus a doubly linked list gives O(1) get and eviction.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = OrderedDict()

    def get(self, key):
        if key not in self.items:
            return None
        self.items.move_to_end(key)
        return self.items[key]

    def put(self, key, value):
        if key in self.items:
            self.items.move_to_end(key)
        self.items[key] = value
        if len(self.items) > self.capacity:
            self.items.popitem(last=False)

cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")
cache.put("c", 3)
assert cache.get("b") is None and cache.get("a") == 1
```

[Table of Contents](#Data-Structures)

## Define a stack?

Stack is an ordered collection of elements in which insertions and deletions are restricted to one end. The end from which elements are added and/or removed is referred to as top of the stack. Stacks are also referred as piles, push-down lists and last-in-first-out (LIFO) lists.

Python example: a list is the simplest stack because `append` and `pop` are both O(1).

```python
stack = []
for value in (1, 2, 3):
    stack.append(value)
assert stack.pop() == 3
assert stack[-1] == 2
```

[Table of Contents](#Data-Structures)

## List out the basic operations that can be performed on a stack?

The basic operations that can be performed on a stack are
Push operation.
Pop operation.
Peek operation.
Empty check.
Fully occupied check.

```python
class Stack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if not self.items:
            raise IndexError("empty stack")
        return self.items.pop()

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return not self.items

    def is_full(self):
        return False   # unbounded, list-backed stack

s = Stack()
s.push("a")
assert s.peek() == "a" and not s.is_empty()
```

[Table of Contents](#Data-Structures)

## State the different ways of representing expressions?

The different ways of representing expressions are
Infix Notation.
Prefix Notation.
Postfix Notation.

[Table of Contents](#Data-Structures)

## State the advantages of using infix notations?

It is the mathematical way of representing the expression.
It is easier to see visually which operation is done from first to last.

[Table of Contents](#Data-Structures)

## State the advantages of using postfix notations?

Need not worry about the rules of precedence.
Need not worry about the rules for right to left associativity.
Need not need parenthesis to override the above rules.

Postfix needs no parentheses and no precedence table at evaluation time.

```python
def eval_postfix(tokens):
    stack = []
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            right, left = stack.pop(), stack.pop()
            stack.append({"+": left + right, "-": left - right,
                          "*": left * right, "/": left / right}[token])
    return stack[0]

assert eval_postfix(["3", "4", "+", "2", "*"]) == 14
```

[Table of Contents](#Data-Structures)

## State the rules to be followed during infix to postfix conversions?

Fully parenthesize the expression starting from left to right. During parenthesizing, the operators having higher precedence are first parenthesized.
Move the operators one by one to their right, such that each operator replaces their corresponding right parenthesis.
The part of the expression, which has been converted into postfix is to be treated as single operand.
Once the expression is converted into postfix form, remove all parenthesis.

The shunting-yard algorithm implements the precedence and associativity rules in one pass.

```python
def infix_to_postfix(tokens):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output, operators = [], []
    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()
        else:
            while (operators and operators[-1] != "("
                   and precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
    while operators:
        output.append(operators.pop())
    return output

assert infix_to_postfix(["a", "+", "b", "*", "c"]) == ["a", "b", "c", "*", "+"]
```

[Table of Contents](#Data-Structures)

## State the rules to be followed during infix to prefix conversions?

Fully parenthesize the expression starting from left to right. During parenthesizing, the operators having higher precedence are first parenthesized.
Move the operators one by one to their left, such that each operator replaces their corresponding left  parenthesis.
The part of the expression, which has been converted into prefix is to be treated as single operand.
Once the expression is converted into prefix form, remove all parenthesis.

[Table of Contents](#Data-Structures)

## State the difference between stacks and linked lists?

The difference between stacks and linked lists is that insertions and deletions may occur anywhere in a linked list, but only at the top of the stack.

A stack restricts insert and delete to one end (LIFO). A linked list allows insert and delete anywhere. A stack is
often implemented with a linked list, so they are complementary rather than alternatives.

```python
ll = LinkedList()
for v in (1, 2, 3):
    ll.append(v)
print(ll.values())     # linked list keeps insertion order
```

[Table of Contents](#Data-Structures)

## Mention the advantages of representing stacks using linked lists than arrays?

It is not necessary to specify the number of elements to be stored in a stack during its declaration, since memory is allocated dynamically at run time when an element is added to the stack.
Insertions and deletions can be handled easily and efficiently.
Linked list representation of stacks can grow and shrink in size without wasting memory space, depending upon the insertion and deletion that occurs in the list.
Multiple stacks can be represented efficiently using a chain for each stack.

[Table of Contents](#Data-Structures)

## Define a queue?

Queue is an ordered collection of elements in which insertions are restricted to one end called the rear end and deletions are restricted to other end called the front end. Queues are also referred as First-In-First-Out (FIFO) Lists.

Use `collections.deque`; popping from the front of a list is O(n).

```python
from collections import deque

queue = deque(["a", "b"])
queue.append("c")          # enqueue at the rear
assert queue.popleft() == "a"   # dequeue from the front
assert list(queue) == ["b", "c"]
```

[Table of Contents](#Data-Structures)

## Define a priority queue?

Priority queue is a collection of elements, each containing a key referred as the priority for that element. Elements can be inserted in any order (i.e., of alternating priority), but are arranged in order of their priority value in the queue. The elements are deleted from the queue in the order of their priority (i.e., the elements with the highest priority is deleted first). The elements with the same priority are given equal importance and processed accordingly.

```python
import heapq

class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, priority, item):
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        return heapq.heappop(self._heap)[1]

    def __len__(self):
        return len(self._heap)

pq = PriorityQueue()
pq.push(5, "batch")
pq.push(1, "stream")
assert pq.pop() == "stream"
```

[Table of Contents](#Data-Structures)

## State the difference between queues and linked lists?

The difference between queues and linked lists is that insertions and deletions may occur anywhere in the linked list, but in queues insertions can be made only in the rear end and deletions can be made only in the front end.

A queue is FIFO and only touches the two ends; a linked list supports arbitrary positions.

```python
from collections import deque

queue = deque()
queue.append("first")
queue.append("second")
assert queue.popleft() == "first"
```

[Table of Contents](#Data-Structures)

## Which data structures are most useful in data engineering interviews?

The most common are arrays/lists, hash maps, sets, heaps, queues, stacks, trees, and graphs. Data engineering interviews often use them in practical tasks such as deduplication, top-k aggregation, dependency ordering, and streaming windows.

Examples:

+ hash map: count events by user id
+ set: detect duplicates
+ heap: keep top 100 largest transactions
+ queue: process messages in arrival order
+ graph: model job dependencies in an orchestrator

The best answer links the structure to complexity. For example, a hash map lookup is usually O(1), which is why it is useful for joins and dedupe in memory.

The data engineering twist is that the same ideas appear as SQL operators and distributed primitives:

+ Hash map -> `GROUP BY`, broadcast hash join, and Spark's `groupByKey`/`reduceByKey`.
+ Heap -> `ORDER BY ... LIMIT k` per group and streaming top-k.
+ Queue/deque -> rate limiting and sliding-window aggregations.
+ Graph -> lineage, DAG scheduling, and connected components for entity resolution.

SQL example: deduplicate a change feed, keeping the latest row per key.

```sql
WITH ranked AS (
    SELECT
        customer_id,
        email,
        updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY updated_at DESC, ingest_ts DESC
        ) AS rn
    FROM raw.customer_changes
)
SELECT customer_id, email, updated_at
FROM ranked
WHERE rn = 1;
```

Python equivalent using a hash map keyed by `customer_id`:

```python
def dedupe_latest(rows):
    latest = {}
    for row in rows:
        current = latest.get(row["customer_id"])
        if current is None or row["updated_at"] > current["updated_at"]:
            latest[row["customer_id"]] = row
    return list(latest.values())

rows = [
    {"customer_id": 1, "email": "old@x.com", "updated_at": 10},
    {"customer_id": 1, "email": "new@x.com", "updated_at": 20},
]
assert dedupe_latest(rows)[0]["email"] == "new@x.com"
```

[Table of Contents](#Data-Structures)

## How would you find the top K records in a large stream?

Use a min-heap of size K. For each incoming record, push it if the heap has fewer than K items. If the heap is full and the new value is larger than the smallest value in the heap, replace the smallest. This avoids sorting the whole stream.

Example:

```python
import heapq

def top_k(values, k):
    heap = []
    for value in values:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)
    return sorted(heap, reverse=True)
```

The complexity is O(n log k), which is efficient when K is much smaller than the total number of records.

Python example with a bounded min-heap. Memory is O(k) and each item costs O(log k), so the stream can be unbounded.

```python
import heapq

def top_k(stream, k):
    heap = []
    for value in stream:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)
    return sorted(heap, reverse=True)

assert top_k([5, 1, 9, 3, 7, 2], 3) == [9, 7, 5]
```

Per-tenant top-N in SQL, and the equivalent PySpark window:

```sql
SELECT tenant_id, order_id, revenue
FROM (
    SELECT
        tenant_id,
        order_id,
        revenue,
        ROW_NUMBER() OVER (PARTITION BY tenant_id ORDER BY revenue DESC) AS rn
    FROM fact_orders
) ranked
WHERE rn <= 10;
```

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

window = Window.partitionBy("tenant_id").orderBy(F.col("revenue").desc())
top10 = (
    fact_orders
    .withColumn("rn", F.row_number().over(window))
    .filter("rn <= 10")
    .drop("rn")
)
```

Trade-off: if `k` is small and the data is distributed, use a heap per partition and merge the partial heaps on the
driver; a global sort shuffles all rows and is far more expensive.

[Table of Contents](#Data-Structures)

## Define a deque?

Deque (Double-Ended Queue) is another form of a queue in which insertions and deletions are made at both the front and rear ends of the queue. There are two variations of a deque, namely, input restricted deque and output restricted deque. The input restricted deque allows insertion at one end (it can be either front or rear) only. The output restricted deque allows deletion at one end (it can be either front or rear) only.

A deque powers sliding-window problems such as maximum value in a moving window in O(n).

```python
from collections import deque

def max_sliding_window(values, k):
    window, result = deque(), []
    for i, value in enumerate(values):
        while window and values[window[-1]] <= value:
            window.pop()
        window.append(i)
        if window[0] <= i - k:
            window.popleft()
        if i >= k - 1:
            result.append(values[window[0]])
    return result

assert max_sliding_window([1, 3, -1, -3, 5, 3], 3) == [3, 3, 5, 5]
```

[Table of Contents](#Data-Structures)

## Why you need a data structure?

A data structure helps you to understand the relationship of one data element with the other and organize it within the memory. Sometimes the organization might be simple and can be very clearly visioned.
Eg; List of names of months in a year –Linear Data Structure, List of historical places in the world- Non-Linear Data Structure. A data structure helps you to analyze the data, store it and organize it in a logical and mathematical manner.

[Table of Contents](#Data-Structures)

## What do you mean by shortest path?

A path having minimum weight between two vertices is known as shortest path, in which weight is always a positive number.

Dijkstra's algorithm relaxes edges from the closest unvisited node, using a heap for the frontier.

```python
import heapq

def dijkstra(graph, source):
    distances = {source: 0}
    heap = [(0, source)]
    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distances.get(node, float("inf")):
            continue
        for neighbour, weight in graph.get(node, []):
            candidate = dist + weight
            if candidate < distances.get(neighbour, float("inf")):
                distances[neighbour] = candidate
                heapq.heappush(heap, (candidate, neighbour))
    return distances

graph = {"a": [("b", 1), ("c", 4)], "b": [("c", 2)], "c": []}
assert dijkstra(graph, "a") == {"a": 0, "b": 1, "c": 3}
```

[Table of Contents](#Data-Structures)

## What do you mean by articulation point?

If a graph is not biconnected, the vertices whose removal would disconnect the graph are known as articulation points.

[Table of Contents](#Data-Structures)

## Define biconnectivity?

A connected graph G is said to be biconnected, if it remains connected after removal of any one vertex and the edges that are incident upon that vertex. A connected graph is biconnected, if it has no articulation points.

[Table of Contents](#Data-Structures)

## What do you mean by back edge?

If w is the ancestor of v, then vw is called a back edge.

[Table of Contents](#Data-Structures)

## What do you mean by tree edge?

If w is undiscovered at the time vw is explored, then vw is called a tree edge and v becomes the parent of w.

[Table of Contents](#Data-Structures)

## What do you mean by breadth first search?

BFS performs simultaneous explorations starting from a common point and spreading out independently.

BFS explores by distance from the source using a queue. It finds shortest paths in unweighted graphs and is the basis
of ripple-style lineage traversal.

```python
from collections import deque

def bfs(graph, start):
    visited, order, queue = {start}, [], deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return order

assert bfs({"a": ["b"], "b": ["c"], "c": []}, "a") == ["a", "b", "c"]
```

[Table of Contents](#Data-Structures)

## List the two important key points of depth first search?

i) If path exists from one node to another node, walk across the edge – exploring the edge.
ii) If path does not exist from one specific node to any other node, return to the previous node where we have been before – backtracking.

1. Explore an edge as deep as possible from the current node.
2. When there is no unvisited edge, backtrack to the previous node.

```python
def dfs(graph, start, visited=None):
    visited = visited if visited is not None else set()
    visited.add(start)
    for neighbour in graph.get(start, []):
        if neighbour not in visited:
            dfs(graph, neighbour, visited)
    return visited

assert dfs({"a": ["b"], "b": ["c"], "c": []}, "a") == {"a", "b", "c"}
```

[Table of Contents](#Data-Structures)

## Define graph traversals?

Traversing a graph is an efficient way to visit each vertex and edge exactly once.

[Table of Contents](#Data-Structures)

## Name two algorithms two find minimum spanning tree?

Kruskals algorithm.
Prims algorithm.

[Table of Contents](#Data-Structures)

## What is a minimum spanning tree?

A minimum spanning tree of an undirected graph G is a tree formed from graph edges that connects all the vertices of G at the lowest total cost.

Kruskal's algorithm sorts edges by weight and adds them when they connect two different components (union-find).

```python
def kruskal(nodes, edges):
    parent = {node: node for node in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, used = 0, []
    for weight, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += weight
            used.append((u, v, weight))
    return total, used

total, used = kruskal(["a", "b", "c"], [(1, "a", "b"), (2, "b", "c"), (5, "a", "c")])
assert total == 3 and len(used) == 2
```

[Table of Contents](#Data-Structures)

## What are the two traversal strategies used in traversing a graph?

Breadth first search
Depth first search

BFS uses a queue and gives level-by-level order; DFS uses a stack (or recursion) and gives path-oriented order.

```python
def traverse(graph, start, strategy="bfs"):
    stack = [start]
    visited, order = {start}, []
    while stack:
        node = stack.pop(0) if strategy == "bfs" else stack.pop()
        order.append(node)
        stack.extend(n for n in graph.get(node, []) if n not in visited)
        visited.update(n for n in graph.get(node, []))
    return order

graph = {"a": ["b", "c"], "b": ["d"], "c": [], "d": []}
assert traverse(graph, "a", "bfs")[0] == "a"
assert traverse(graph, "a", "dfs")[0] == "a"
```

[Table of Contents](#Data-Structures)

## When is a graph said to be weakly connected?

When a directed graph is not strongly connected but the underlying graph is connected, then the graph is said to be weakly connected.

[Table of Contents](#Data-Structures)

## What is meant by strongly connected in a graph?

An undirected graph is connected, if there is a path from every vertex to every other vertex. A directed graph with this property is called strongly connected.

[Table of Contents](#Data-Structures)

## What is an acyclic graph?

A simple diagram which does not have any cycles is called an acyclic graph.

[Table of Contents](#Data-Structures)

## What is a cycle or a circuit?

A path which originates and ends in the same node is called a cycle or circuit.

[Table of Contents](#Data-Structures)

## What is a simple path?

A path in a diagram in which the edges are distinct is called a simple path. It is also called as edge simple.

[Table of Contents](#Data-Structures)

## Define path in a graph?

The path in a graph is the route taken to reach terminal node from a starting node.

[Table of Contents](#Data-Structures)

## Define indegree of a graph?

In a directed graph, for any node v, the number of edges which have v as their terminal node is called the indegree of the node v.

```python
def indegrees(edges):
    counts = {}
    for _, target in edges:
        counts[target] = counts.get(target, 0) + 1
    return counts

assert indegrees([("a", "b"), ("c", "b")])["b"] == 2
```

[Table of Contents](#Data-Structures)

## Define outdegree of a graph?

In a directed graph, for any node v, the number of edges which have v as their initial node is called the out degree of the node v.

```python
def outdegrees(edges):
    counts = {}
    for source, _ in edges:
        counts[source] = counts.get(source, 0) + 1
    return counts

assert outdegrees([("a", "b"), ("a", "c")])["a"] == 2
```

[Table of Contents](#Data-Structures)

## What is a weighted graph?

A graph in which weights are assigned to every edge is called a weighted graph.

```python
adjacency = {"a": [("b", 2.5)], "b": [("a", 2.5)]}
assert adjacency["a"][0][1] == 2.5
```

[Table of Contents](#Data-Structures)

## What is a simple graph?

A simple graph is a graph, which has not more than one edge between a pair of nodes than such a graph is called a simple graph.

[Table of Contents](#Data-Structures)

## What is a loop?

An edge of a graph which connects to itself is called a loop or sling.

[Table of Contents](#Data-Structures)

## What is undirected graph?

A graph in which every edge is undirected is called an undirected graph. An undirected edge (u, v) may be traversed in either direction, and the adjacency list stores each neighbour on both sides.

[Table of Contents](#Data-Structures)

## What is a directed graph?

A graph in which every edge is directed is called a directed graph.

[Table of Contents](#Data-Structures)

## Define adjacent nodes?

Any two nodes which are connected by an edge in a graph are called adjacent nodes. For example, if an edge x ε E is associated with a pair of nodes (u,v) where u, v ε V, then we say that the edge x connects the nodes u and v.

[Table of Contents](#Data-Structures)

## Define graph?

A graph G consist of a nonempty set V which is a set of nodes of the graph, a set E which is the set of edges of the graph, and a mapping from the set for edge E to a set of pairs of elements of V. It can also be represented as G=(V, E).

```python
from collections import defaultdict

def build_graph(edges):
    graph = defaultdict(list)
    for source, target in edges:
        graph[source].append(target)
        graph[target].append(source)
    return graph

graph = build_graph([("a", "b"), ("b", "c")])
assert sorted(graph["b"]) == ["a", "c"]
```

[Table of Contents](#Data-Structures)

## What is the need for path compression?

Path compression is performed during a Find operation. Suppose if we want to perform Find(X), then the effect of path compression is that every node on the path from X to the root has its parent changed to the root.

Path compression flattens the tree during `find`, so later lookups are nearly O(1). Combined with union by rank the
amortized cost is O(alpha(n)), which is effectively constant.

```python
parent = {"a": "b", "b": "c", "c": "c"}

def find(x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:      # compress the path
        parent[x], x = root, parent[x]
    return root

assert find("a") == "c"
assert parent["a"] == "c"          # flattened after the call
```

[Table of Contents](#Data-Structures)

## What do you mean by union by weight?

Keep track of the weight ie; size of each tree and always append the smaller tree to the larger one when performing UNION.

Always attach the smaller tree under the larger one so the height grows logarithmically.

```python
parent = {i: i for i in range(6)}
size = {i: 1 for i in range(6)}

def union(a, b):
    ra, rb = a, b
    while parent[ra] != ra:
        ra = parent[ra]
    while parent[rb] != rb:
        rb = parent[rb]
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]

union(0, 1)
union(1, 2)
assert parent[0] == parent[1] or parent[1] == parent[2]
print(size)
```

[Table of Contents](#Data-Structures)

## List the abstract operations in the set?

Let S and T be sets and e be an element.
SINGLETON(e) returns {e}.
UNION(S,T) returns S Ụ T.
INTERSECTION(S,T) returns S ∩ T.
FIND returns the name of the set containing a given element.

[Table of Contents](#Data-Structures)

## Define a set?

A set S is an unordered collection of elements from a universe. An element cannot appear more than once in S. The cardinality of S is the number of elements in S. An empty set is a set whose cardinality is zero. A singleton set is a set whose cardinality is one.

Python example: a set stores unique, unordered elements and answers membership in average O(1).

```python
seen = set()
for event_id in ["e1", "e2", "e1", "e3"]:
    seen.add(event_id)
assert seen == {"e1", "e2", "e3"}
assert "e2" in seen
```

[Table of Contents](#Data-Structures)

## What do you mean by disjoint set adt?

A collection of non-empty disjoint sets S=S1,S2,….,Sk i.e;each Si is a non-empty set that has no element in common with any other Sj. In mathematical notation this is: Si∩Sj=Ф. Each set is identified by a unique element called its representative.

Disjoint sets (union-find) track which elements belong to the same group. It is the standard way to find connected
components, for example customer accounts that resolve to the same entity.

```python
class DisjointSet:
    def __init__(self, items):
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

ds = DisjointSet(["a", "b", "c", "d"])
ds.union("a", "b")
ds.union("c", "d")
assert ds.find("a") == ds.find("b")
assert ds.find("a") != ds.find("c")
```

[Table of Contents](#Data-Structures)

## List the applications of set adt?

Maintaining a set of connected components of a graph.
Maintain list of duplicate copies of web pages.
Constructing a minimum spanning tree for a graph.

[Table of Contents](#Data-Structures)

## Define an equivalence relation?

An equivalence relation is a relation R that satisfies three properties:
(Reflexive) aRa, for all a ε S.
(Symmetric) aRb if and only if bRa.
(Transitive) aRb and bRc implies that aRc.

A relation is an equivalence relation when it is reflexive, symmetric, and transitive. Grouping records by a
normalized key (for example, email lower-cased) relies on exactly those properties.

```python
def key(record):
    return record["email"].strip().lower()

records = [{"email": "A@x.com"}, {"email": "a@x.com"}, {"email": "b@x.com"}]
groups = {}
for record in records:
    groups.setdefault(key(record), []).append(record)
assert len(groups) == 2
```

[Table of Contents](#Data-Structures)

## Define a relation?

A relation R is defined on a set S if for every pair of elements (a,b), a,b ε S, aRb is either true or false. If aRb is true, then we say that a is related to b.

[Table of Contents](#Data-Structures)

## Mention one advantage and disadvantage of using quadratic probing?

Advantage: The problem of primary clustering is eliminated.
Disadvantage: There is no guarantee of finding an unoccupied cell once the table is nearly half full.

[Table of Contents](#Data-Structures)

## List the limitations of linear probing?

Time taken for finding the next available cell is large.
In linear probing, we come across a problem known as clustering.

[Table of Contents](#Data-Structures)

## What is the need for extendable hashing?

If either open addressing hashing or separate chaining hashing is used, the major problem is that collisions could cause several blocks to be examined during a Find, even for a well-distributed hash table. Extendible hashing allows a find to be performed in two disk accesses. Insertions also require few disk accesses.

Extendable hashing grows the directory one bit at a time as buckets overflow, so a database index can grow without a full rebuild.

```python
def bucket_index(key, depth):
    return hash(key) % (2 ** depth)

depth = 1
keys = ["a", "b", "c", "d"]
buckets = {}
for key in keys:
    buckets.setdefault(bucket_index(key, depth), []).append(key)
full = [b for b, items in buckets.items() if len(items) > 2]
if full:
    depth += 1
print("depth", depth, "buckets", buckets)
```

[Table of Contents](#Data-Structures)

## What do you mean by rehashing?

If the table gets too full, the running time for the operations will start taking too long and inserts might fail for open addressing with quadratic resolution. A solution to this is to build another table that is about twice as big with the associated new hash function and scan down the entire original hash table, computing the new hash value for each element and inserting it in the new table. This entire operation is called rehashing.

```python
def rehash(old_table):
    new_size = len(old_table) * 2
    new_table = [None] * new_size
    for key in old_table:
        if key is None:
            continue
        i = hash(key) % new_size
        while new_table[i] is not None:
            i = (i + 1) % new_size
        new_table[i] = key
    return new_table

print(len(rehash(["a", None, "b", None])))
```

[Table of Contents](#Data-Structures)

## What do you mean by double hashing?

Double hashing is an open addressing collision resolution strategy in which F(i)=i.hash2(X). This formula says that we apply a second hash function to X and probe at a distance hash2(X), 2hash2(X),….,and so on. A function such as hash2(X)=R-(XmodR), with R a prime smaller than Tablesize.

Double hashing uses a second hash function to choose the probe step, which reduces secondary clustering.

```python
def double_hash(table, key):
    size = len(table)
    h1 = hash(key) % size
    h2 = 1 + (hash(key) % (size - 1))
    for step in range(size):
        i = (h1 + step * h2) % size
        if table[i] is None or table[i] == key:
            return i, h2
    raise OverflowError("table full")

print(double_hash([None] * 11, "user-7"))
```

[Table of Contents](#Data-Structures)

## What do you mean by secondary clustering?

Although quadratic probing eliminates primary clustering, elements that hash to the same position will probe the same alternative cells. This is known as secondary clustering.

[Table of Contents](#Data-Structures)

## What do you mean by quadratic probing?

Quadratic probing is an open addressing collision resolution strategy in which F(i)=i2. There is no guarantee of finding an empty cell once the table gets half full if the table size is not prime. This is because at most half of the table can be used as alternative locations to resolve collisions.

Quadratic probing uses offsets `1, 4, 9, ...` so keys that collide do not walk the same contiguous run.

```python
def quadratic_probe(table, key):
    size = len(table)
    base = hash(key) % size
    for step in range(size):
        i = (base + step * step) % size
        if table[i] is None or table[i] == key:
            return i
    raise OverflowError("table full")

table = ["a", "b", None, None, None, None, None]
print(quadratic_probe(table, "b"))
```

[Table of Contents](#Data-Structures)

## What do you mean by primary clustering?

In linear probing collision resolution strategy, even if the table is relatively empty, blocks of occupied cells start forming. This effect is known as primary clustering means that any key hashes into the cluster will require several attempts to resolve the collision and then it will add to the cluster.

[Table of Contents](#Data-Structures)

## What do you mean by linear probing?

Linear probing is an open addressing collision resolution strategy in which F is a linear function of i, F(i)=i. This amounts to trying sequentially in search of an empty cell. If the table is big enough, a free cell can always be found, but the time to do so can get quite large.

```python
def linear_probe(table, key):
    size = len(table)
    i = hash(key) % size
    probes = 0
    while table[i] is not None and table[i] != key:
        i = (i + 1) % size
        probes += 1
    return i, probes

table = ["a", None, None, "d", None, None, None]
print(linear_probe(table, "d"))
```

[Table of Contents](#Data-Structures)

## What do you mean by probing?

Probing is the process of getting next available hash table array cell.

[Table of Contents](#Data-Structures)

## What are the types of collision resolution strategies in open addressing?

Linear probing.
Quadratic probing.
Double hashing.

[Table of Contents](#Data-Structures)

## What do you mean by open addressing?

Open addressing is a collision resolving strategy in which, if collision occurs alternative cells are tried until an empty cell is found. The cells h0(x), h1(x), h2(x),…. are tried in succession, where hi(x)=(Hash(x)+F(i))mod Tablesize with F(0)=0. The function F is the collision resolution strategy.

Open addressing keeps every entry inside the table array and probes forward on collision.

```python
def insert_open_addressing(keys, size=7):
    table = [None] * size
    for key in keys:
        i = hash(key) % size
        while table[i] is not None:
            i = (i + 1) % size
        table[i] = key
    return table

print(insert_open_addressing(["a", "b", "c"]))
```

[Table of Contents](#Data-Structures)

## Write the disadvantages of separate chaining?

The elements are evenly distributed. Some elements may have more elements and some may not have anything.
It requires pointers. This leads to slow the algorithm down a bit because of the time required to allocate new cells, and also essentially requires the implementation of a second data structure.

[Table of Contents](#Data-Structures)

## Write the advantage of separate chaining?

Number of elements can be inserted as it uses linked lists.

[Table of Contents](#Data-Structures)

## What do you mean by separate chaining?

Separate chaining is a collision resolution technique to keep the list of all elements that hash to the same value. This is called separate chaining because each hash table element is a separate chain (linked list). Each linked list contains all the elements whose keys hash to the same index.

Python example: each bucket holds a list, so collisions append to the chain.

```python
class ChainedHashTable:
    def __init__(self, size=8):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def put(self, key, value):
        chain = self.buckets[hash(key) % self.size]
        for pair in chain:
            if pair[0] == key:
                pair[1] = value
                return
        chain.append([key, value])

    def get(self, key):
        for k, v in self.buckets[hash(key) % self.size]:
            if k == key:
                return v
        return None

table = ChainedHashTable()
table.put("x", 10)
assert table.get("x") == 10
```

[Table of Contents](#Data-Structures)

## What are the collision resolution methods?

Separate chaining or External hashing.
Open addressing or Closed hashing.

Quick comparison you can give in an interview:

+ Separate chaining: simple, tolerates high load factors, needs extra pointers.
+ Open addressing: cache friendly, must keep the load factor below about 0.7.
+ Extendable hashing: grows a directory, used by database storage engines.

```python
load_factor = lambda entries, slots: entries / slots
print(load_factor(70, 100))  # 0.7, the usual open-addressing ceiling
```

[Table of Contents](#Data-Structures)

## What do you mean by collision in hashing?

When an element is inserted, it hashes to the same value as an already inserted element, and then it produces collision.

Detecting and counting collisions while inserting keys:

```python
def collisions(keys, buckets=8):
    table = {}
    count = 0
    for key in keys:
        bucket = hash(key) % buckets
        if bucket in table:
            count += 1
            table[bucket].append(key)
        else:
            table[bucket] = [key]
    return count, table

count, buckets = collisions(["a", "b", "c", "d", "e", "f", "g", "h"])
print(count, buckets)
```

[Table of Contents](#Data-Structures)

## Write the importance of hashing?

Maps key with the corresponding value using hash function.
Hash tables support the efficient addition of new entries and the time spent on searching for the required data is independent of the number of items stored.

Hashing gives average O(1) lookup, which is why it powers dictionaries, sets, group-by aggregation, and distributed partitioning.

```python
def group_by(rows, key):
    groups = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)
    return groups

rows = [{"tenant": "a", "v": 1}, {"tenant": "b", "v": 2}, {"tenant": "a", "v": 3}]
assert len(group_by(rows, "tenant")["a"]) == 2
```

[Table of Contents](#Data-Structures)

## What do you mean by hash function?

A hash function is a key to address transformation which acts upon a given key to compute the relative position of the key in an array. The choice of hash function should be simple and it must distribute the data evenly. A simple hash function is hash_key=key mod tablesize.

A good hash function is deterministic, fast, and spreads keys evenly. Never rely on Python's built-in `hash` for persisted data because it is randomized per process for strings.

```python
import hashlib

def stable_hash(key: str, buckets: int) -> int:
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()
    return int(digest, 16) % buckets

assert stable_hash("user-1", 8) == stable_hash("user-1", 8)
```

[Table of Contents](#Data-Structures)

## What do you mean by hash table?

The hash table data structure is merely an array of some fixed size, containing the keys. A key is a string with an associated value. Each key is mapped into some number in the range 0 to tablesize-1 and placed in the appropriate cell.

Python example: a minimal open-addressing hash table with linear probing.

```python
class HashTable:
    def __init__(self, size=8):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size

    def _probe(self, key):
        i = hash(key) % self.size
        while self.keys[i] is not None and self.keys[i] != key:
            i = (i + 1) % self.size
        return i

    def put(self, key, value):
        i = self._probe(key)
        self.keys[i] = key
        self.values[i] = value

    def get(self, key):
        i = self._probe(key)
        return self.values[i] if self.keys[i] == key else None

table = HashTable()
table.put("a", 1)
assert table.get("a") == 1
assert table.get("missing") is None
```

[Table of Contents](#Data-Structures)

## Define hashing?

Hashing is the transformation of string of characters into a usually shorter fixed length value or key that represents the original string. Hashing is used to index and retrieve items in a database because it is faster to find the item using the short hashed key than to find it using the original value.

Python example: a dict applies a hash function and stores each key in a bucket.

```python
key = "customer:42"
bucket = hash(key) % 16
print(bucket)

counts = {}
for word in "the quick brown fox the lazy dog the".split():
    counts[word] = counts.get(word, 0) + 1
assert counts["the"] == 3
```

[Table of Contents](#Data-Structures)

## What do you mean by the term percolate down?

When the minimum element is removed, a hole is created at the root. Since the heap now becomes one smaller, it follows that the last element X in the heap must move somewhere in the heap. If X can be placed in the hole, then we are done.. This is unlikely, so we slide the smaller of the holes children into the hole, thus pushing the hole down one level. We repeat this step until X can be placed in the hole. Thus, our action is to place X in its correct spot along a path from the root containing minimum children. This general strategy is known as percolate down.

`percolate down` moves a value from the root toward the leaves until the heap order is restored.

```python
def sift_down(heap, index):
    size = len(heap)
    while True:
        smallest = index
        left, right = 2 * index + 1, 2 * index + 2
        if left < size and heap[left] < heap[smallest]:
            smallest = left
        if right < size and heap[right] < heap[smallest]:
            smallest = right
        if smallest == index:
            return heap
        heap[index], heap[smallest] = heap[smallest], heap[index]
        index = smallest

assert sift_down([9, 3, 5], 0) == [3, 9, 5]
```

[Table of Contents](#Data-Structures)

## What do you mean by the term percolate up?

To insert an element, we have to create a hole in the next available heap location. Inserting an element in the hole would sometimes violate the heap order property, so we have to slide down the parent into the hole. This strategy is continued until the correct location for the new element is found. This general strategy is known as a percolate up; the new element is percolated up the heap until the correct location is found.

```python
def sift_up(heap, index):
    while index > 0:
        parent_index = (index - 1) // 2
        if heap[parent_index] <= heap[index]:
            break
        heap[parent_index], heap[index] = heap[index], heap[parent_index]
        index = parent_index
    return heap

assert sift_up([3, 9, 5, 1], 3) == [1, 3, 5, 9]
```

[Table of Contents](#Data-Structures)

## What are the applications of priority queues?

The selection problem.
Event simulation.

+ Dijkstra's shortest path.
+ Top-k and streaming median.
+ Event simulation and SLA-aware scheduling.
+ Huffman coding.

```python
import heapq

def k_smallest(values, k):
    return heapq.nsmallest(k, values)

assert k_smallest([9, 1, 5, 3], 2) == [1, 3]
```

[Table of Contents](#Data-Structures)

## What do you mean by heap order property?

In a heap, for every node X, the key in the parent of X is smaller than (or equal to) the key in X, with the exception of the root (which has no parent).

```python
import heapq

heap = [1, 3, 5, 8, 9, 7]
assert all(heap[0] <= value for value in heap)
# after each pop the smallest remaining value surfaces at the root
heapq.heappop(heap)
assert heap[0] == 3
```

[Table of Contents](#Data-Structures)

## What do you mean by structure property in a heap?

A heap is a binary tree that is completely filled with the possible exception at the bottom level, which is filled from left to right. Such a tree is known as a complete binary tree.

A complete binary tree maps onto an array with no gaps: children of index `i` are `2i + 1` and `2i + 2`.

```python
def parent(i):
    return (i - 1) // 2

def children(i):
    return 2 * i + 1, 2 * i + 2

assert parent(4) == 1
assert children(1) == (3, 4)
```

[Table of Contents](#Data-Structures)

## What are the properties of binary heap?

Structure Property.
Heap Order Property.

Structure property (complete tree in an array) plus heap order property (parent <= children). Building a heap from
`n` items costs O(n), while `n` individual pushes cost O(n log n).

```python
import heapq

values = [9, 4, 7, 1, 8]
heapq.heapify(values)      # O(n) build
assert values[0] == 1
```

[Table of Contents](#Data-Structures)

## What is the need for priority queue?

In a multiuser environment, the operating system scheduler must decide which of the several processes to run only for a fixed period of time. One algorithm uses queue. Jobs are initially placed at the end of the queue. The scheduler will repeatedly take the first job on the queue, run it until either it finishes or its time limit is up and place it at the end of the queue if it does not finish. This strategy is not appropriate, because very short jobs will soon to take a long time because of the wait involved in the run.
Generally, it is important that short jobs finish as fast as possible, so these jobs should have precedence over jobs that have already been running. Further more, some jobs that are not short are still very important and should have precedence. This particular application seems to require a special kind of queue, known as priority queue. Priority queue is also called as Heap or Binary Heap.

[Table of Contents](#Data-Structures)

## What are the applications of b-tree?

Database implementation.
Indexing on non-primary key fields.

B+ trees back database indexes because a high fan-out keeps the height at 3-4 for billions of rows, so a lookup costs
a handful of page reads. LSM engines (Cassandra, HBase) instead use a sorted memtable plus SSTables.

`text` sketch of a B+ tree of order 3:

```text
        [ 20 | 40 ]
       /     |      \
 [10|15]  [25|30]  [45|50]
   ^          ^        ^   keys live in the leaves, which are linked for range scans
```

[Table of Contents](#Data-Structures)

## What do you mean by 2-3-4 tree?

A B-tree of order 4 is called 2-3-4 tree. A B-tree of order 4 is a tree that is not binary with the following structural properties:
The root is either a leaf or has between 2 and 4 children.
All non-leaf nodes (except the root) have between 2 and 4 children.
All leaves are at the same depth.

[Table of Contents](#Data-Structures)

## What do you mean by 2-3 tree?

A B-tree of order 3 is called 2-3 tree. A B-tree of order 3 is a tree that is not binary with the following structural properties:
The root is either a leaf or has between 2 and 3 children.
All non-leaf nodes (except the root) have between 2 and 3 children.
All leaves are at the same depth.

A 2-3 tree is a B-tree of order 3: every internal node has 2 or 3 children and all leaves are at the same depth, so
lookups, inserts, and deletes are O(log n) with no rotations.

```python
# A 2-3 tree node holds one or two keys and 2 or 3 children.
class TwoThreeNode:
    def __init__(self, keys=None, children=None):
        self.keys = keys or []
        self.children = children or []

node = TwoThreeNode([10, 20], [TwoThreeNode([5]), TwoThreeNode([15]), TwoThreeNode([25])])
assert len(node.keys) == 2 and len(node.children) == 3
```

[Table of Contents](#Data-Structures)

## Define b tree of order m?

A B-tree of order M is a tree that is not binary with the following structural properties:
The root is either a leaf or has between 2 and M children.
All non-leaf nodes (except the root) have between [M/2] and M children.
All leaves are at the same depth.

[Table of Contents](#Data-Structures)

## What is the minimum number of nodes in an avl tree of height h?

The minimum number of nodes S(h), in an AVL tree of height h is given by S(h)=S(h-1)+S(h-2)+1. For h=0, S(h)=1.

[Table of Contents](#Data-Structures)

## Define heap?

A heap is defined to be a complete binary tree with the property that the value of each node is atleast as small as the value of its child nodes, if they exist. The root node of the heap has the smallest value in the tree.

```python
import heapq

heap = [5, 3, 8, 1]
heapq.heapify(heap)
assert heap[0] == 1                 # min-heap property
heapq.heappush(heap, 0)
assert heapq.heappop(heap) == 0
```

[Table of Contents](#Data-Structures)

## List the types of rotations available in splay tree?

Let us assume that the splay is performed at vertex v, whose parent and grandparent are p and g respectively. Then, the three rotations are named as:
Zig: If p is the root and v is the left child of p, then left-left rotation at p would suffice. This case always terminates the splay as v reaches the root after this rotation.
Zig-Zig: If p is not the root, p is the left child and v is also a left child, then a left-left rotation at g followed by a left-left rotation at p, brings v as an ancestor of g as well as p.
Zig-Zag: If p is not the root, p is the left child and v is a right child, perform a left-right rotation at g and bring v as an ancestor of p as well as g.

[Table of Contents](#Data-Structures)

## What is the idea behind splaying?

Splaying reduces the total accessing time if the most frequently accessed node is moved towards the root. It does not require to maintain any information regarding the height or balance factor and hence saves space and simplifies the code to some extent.

[Table of Contents](#Data-Structures)

## Define splay tree?

A splay tree is a binary search tree in which restructuring is done using a scheme called splay. The splay is a heuristic method which moves a given vertex v to the root of the splay tree using a sequence of rotations.

[Table of Contents](#Data-Structures)

## What do you mean by balance factor of a node in avl tree?

The height of left subtree minus height of right subtree is called balance factor of a node in AVL tree.The balance factor may be either 0 or +1 or -1.The height of an empty tree is -1.

```python
def balance_factor(node):
    if node is None:
        return 0
    return height(node.left) - height(node.right)

node = AVLNode(10)
node.left = AVLNode(5)
assert balance_factor(node) == 1
```

[Table of Contents](#Data-Structures)

## What are the categories of avl rotations?

Let A be the nearest ancestor of the newly inserted nod which has the balancing factor ±2. Then the rotations can be classified into the following four categories:
Left-Left: The newly inserted node is in the left subtree of the left child of A.
Right-Right: The newly inserted node is in the right subtree of the right child of A.
Left-Right: The newly inserted node is in the right subtree of the left child of A.
Right-Left: The newly inserted node is in the left subtree of the right child of A.

+ Left-Left -> single right rotation.
+ Right-Right -> single left rotation.
+ Left-Right -> left rotation on the child, then right on the node.
+ Right-Left -> right rotation on the child, then left on the node.

```python
def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    x.height = 1 + max(height(x.left), height(x.right))
    y.height = 1 + max(height(y.left), height(y.right))
    return y

def rebalance(node):
    node.height = 1 + max(height(node.left), height(node.right))
    factor = balance_factor(node)
    if factor > 1 and balance_factor(node.left) >= 0:
        return rotate_right(node)
    if factor < -1 and balance_factor(node.right) <= 0:
        return rotate_left(node)
    return node
```

[Table of Contents](#Data-Structures)

## What do you mean by balanced trees?

Balanced trees have the structure of binary trees and obey binary search tree properties. Apart from these properties, they have some special constraints, which differ from one data structure to another. However, these constraints are aimed only at reducing the height of the tree, because this factor determines the time complexity.
Eg: AVL trees, Splay trees.

[Table of Contents](#Data-Structures)

## Define avl tree?

An empty tree is height balanced. If T is a non-empty binary tree with TL and TR as its left and right subtrees, then T is height balanced if
TL and TR are height balanced and
│hL - hR│≤ 1
Where hL and hR are the heights of TL and TR respectively.

An AVL tree keeps `height(left) - height(right)` in `{-1, 0, 1}` by rotating after inserts. The example below is a
minimal right rotation for a left-heavy node.

```python
def height(node):
    return node.height if node else 0

class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = self.right = None
        self.height = 1

def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    y.height = 1 + max(height(y.left), height(y.right))
    x.height = 1 + max(height(x.left), height(x.right))
    return x

y = AVLNode(3)
y.left = AVLNode(2)
y.left.left = AVLNode(1)
root = rotate_right(y)
assert root.value == 2 and root.right.value == 3
```

[Table of Contents](#Data-Structures)

## Define left in threaded tree?

Left-in threaded binary tree is defined as one in which each NULL pointers is altered to contain a thread to that nodes inorder predecessor.

[Table of Contents](#Data-Structures)

## Define right in threaded tree?

Right-in threaded binary tree is defined as one in which threads replace NULL pointers in nodes with empty right sub-trees.

[Table of Contents](#Data-Structures)

## What is an expression tree?

An expression tree is a tree which is build from infix or prefix or postfix expression. Generally, in such a tree, the leaves are operands and other nodes are operators.

```python
def evaluate(node):
    if node.left is None and node.right is None:
        return float(node.value)
    left, right = evaluate(node.left), evaluate(node.right)
    return {"+": left + right, "-": left - right,
            "*": left * right, "/": left / right}[node.value]

expr = BinNode("*", BinNode("+", BinNode("3"), BinNode("4")), BinNode("2"))
assert evaluate(expr) == 14.0
```

[Table of Contents](#Data-Structures)

## What is the use of threaded binary tree?

In threaded binary tree, the NULL pointers are replaced by some addresses. The left pointer of the node points to its predecessor and the right pointer of the node points to its successor.

[Table of Contents](#Data-Structures)

## Why it is said that searching a node in a binary search tree is efficient than that of a simple binary tree?

In binary search tree, the nodes are arranged in such a way that the left node is having less data value than root node value and the right nodes are having larger value than that of root. Because of this while searching any node the value of the target node will be compared with the parent node and accordingly either left sub branch or right sub branch will be searched. So, one has to compare only particular branches. Thus searching becomes efficient.

[Table of Contents](#Data-Structures)

## Define ancestor and descendant?

If there is a path from node n1 to n2, then n1 is the ancestor of n2 and n2 is the descendant of n1.

[Table of Contents](#Data-Structures)

## What do you mean by general trees?

General tree is a tree with nodes having any number of children.

[Table of Contents](#Data-Structures)

## Define a binary search tree?

A binary search tree is a special binary tree, which is either empty or it should satisfy the following characteristics:
Every node has a value and no two nodes should have the same value i.e) the values in the binary search tree are distinct.
The values in any left sub-tree is less than the value of its parent node.
The values in any right sub-tree is greater than the value of its parent node.
The left and right sub-trees of each node are again binary search trees.

```python
class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return BinNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node

    def contains(self, value):
        node = self.root
        while node:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

bst = BST()
for value in (5, 3, 8, 1):
    bst.insert(value)
assert bst.contains(3) and not bst.contains(9)
```

[Table of Contents](#Data-Structures)

## State the demerits of linked representation of binary trees?

Given a node structure, it is difficult to determine its parent node.
Memory spaces are wasted for storing null pointers for the nodes, which have one or no sub-trees.
It requires dynamic memory allocation, which is not possible in some programming language.

[Table of Contents](#Data-Structures)

## State the merit of linked representation of binary trees?

Insertions and deletions in a node involve no data movement except the rearrangement of pointers, hence less processing time.

[Table of Contents](#Data-Structures)

## State the demerit of linear representation of binary trees?

Insertions and deletions in a node take an excessive amount of processing time due to data movement up and down the array.

[Table of Contents](#Data-Structures)

## State the merits of linear representation of binary trees?

Storage method is easy and can be easily implemented in arrays.
When the location of a parent/child node is known, other one can be determined easily.
It requires static memory allocation so it is easily implemented in all programming language.

[Table of Contents](#Data-Structures)

## What are the tasks performed during postorder traversal?

Traverse the left sub-tree.
Traverse the right sub-tree.
Process the root node.

[Table of Contents](#Data-Structures)

## What are the tasks performed during inorder traversal?

Traverse the left sub-tree.
Process the root node.
Traverse the right sub-tree.

Inorder traversal of a binary search tree visits keys in sorted order.

```python
assert inorder(bst.root) == [1, 3, 5, 8]
```

[Table of Contents](#Data-Structures)

## What are the tasks performed during preorder traversal?

Process the root node.
Traverse the left sub-tree.
Traverse the right sub-tree.

[Table of Contents](#Data-Structures)

## What are the tasks performed while traversing a binary tree?

Visiting a node.
Traverse the left sub-tree.
Traverse the right sub-tree.

[Table of Contents](#Data-Structures)

## What are the different binary tree traversal techniques?

Preorder traversal.
Inorder traversal.
Postorder traversal.
Levelorder traversal.

```python
def preorder(node):
    return [] if node is None else [node.value] + preorder(node.left) + preorder(node.right)

def inorder(node):
    return [] if node is None else inorder(node.left) + [node.value] + inorder(node.right)

def postorder(node):
    return [] if node is None else postorder(node.left) + postorder(node.right) + [node.value]

from collections import deque
def levelorder(node):
    queue, out = deque([node]), []
    while queue:
        current = queue.popleft()
        out.append(current.value)
        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)
    return out

tree = BinNode(2, BinNode(1), BinNode(3))
assert inorder(tree) == [1, 2, 3]
assert preorder(tree) == [2, 1, 3]
assert postorder(tree) == [1, 3, 2]
assert levelorder(tree) == [2, 1, 3]
```

Iterative inorder avoids recursion depth limits on skewed trees:

```python
def inorder_iterative(node):
    stack, out = [], []
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.value)
        node = node.right
    return out
```

[Table of Contents](#Data-Structures)

## What is meant by binary tree traversal?

Traversing a binary tree means moving through all the nodes in the binary tree, visiting each node in the tree only once.

[Table of Contents](#Data-Structures)

## State the properties of a binary tree?

The maximum number of nodes on level n of a binary tree is 2^(n-1), where n≥1.
The maximum number of nodes in a binary tree of height n is 2^n - 1, where n≥1.
For any non-empty tree, nl=nd+1 where nl is the number of leaf nodes and nd is the number of nodes of degree 2.

Key formulas and a quick check:

+ Maximum nodes on level `n` (1-based) is `2 ** (n - 1)`.
+ Maximum nodes in a binary tree of height `h` is `2 ** h - 1`.
+ For any non-empty tree, `leaves = nodes_with_two_children + 1`.

```python
def max_nodes(height):
    return 2 ** height - 1

assert max_nodes(3) == 7
assert max_nodes(1) == 1
```

[Table of Contents](#Data-Structures)

## Define a right-skewed binary tree?

A right-skewed binary tree is a tree, which has only right child nodes.

[Table of Contents](#Data-Structures)

## Define a complete binary tree?

A complete binary tree is filled at every level except possibly the last, and the last level is filled strictly from left to right. This shape lets a heap be stored in an array with no gaps: the children of index i are at 2i + 1 and 2i + 2.

[Table of Contents](#Data-Structures)

## Define a full binary tree ?

A full binary tree (also called a proper or strictly binary tree) is a tree in which every node has either zero or two children; there are no nodes with exactly one child. A tree in which all leaves are on the same level and every non-leaf node has two children is a perfect binary tree.

[Table of Contents](#Data-Structures)

## Define non-terminal nodes in a tree?

All intermediate nodes that traverse the given tree from its root node to the terminal nodes are referred as non-terminal nodes.

[Table of Contents](#Data-Structures)

## Define terminal nodes in a tree?

A node that has no children is called a terminal node. It is also referred to as leaf node.

[Table of Contents](#Data-Structures)

## Define a path in a tree?

A path in a tree is a sequence of distinct nodes in which successive nodes are connected by edges in the tree.

[Table of Contents](#Data-Structures)

## Define a binary tree?

A binary tree is a finite set of nodes which is either empty or consists of a root and two disjoint binary trees called the left sub-tree and right sub-tree.

```python
class BinNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinNode(1, BinNode(2), BinNode(3))
assert [tree.value, tree.left.value, tree.right.value] == [1, 2, 3]
```

[Table of Contents](#Data-Structures)

## Define forest?

A tree may be defined as a forest in which only a single node (root) has no predecessors. Any forest consists of a collection of trees.

[Table of Contents](#Data-Structures)

## What do you mean by level of the tree?

The root node is always considered at level zero, then its adjacent children are supposed to be at level 1 and so on.
Here, node A is at level 0, nodes B and C are at level 1 and nodes D and E are at level 2.

Level-order (breadth-first) traversal prints the tree level by level.

```python
from collections import deque

def levels(root):
    queue, out = deque([root]), []
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.value)
            queue.extend(node.children)
        out.append(level)
    return out

assert levels(root) == [["company"], ["sales", "eng"]]
```

[Table of Contents](#Data-Structures)

## Define depth and height of a tree?

The depth of the tree is the depth of the deepest leaf. The height of the tree is equal to the height of the root. Always depth of the tree is equal to height of the tree.

```python
def depth(node):          # edges from the root down to this node
    return node.depth

def height(node):         # longest downward path to a leaf
    if not node.children:
        return 0
    return 1 + max(height(child) for child in node.children)

assert height(root) == 1
```

[Table of Contents](#Data-Structures)

## Define depth and height of a node?

For any node ni, the depth of ni is the length of the unique path from the root to ni. The height of ni is the length of the longest path from ni to a leaf.

[Table of Contents](#Data-Structures)

## Define parent node?

The node which is having further sub-branches is called the parent node of those sub-branches.
Here C is the parent node of D and E.

[Table of Contents](#Data-Structures)

## Define internal nodes?

The nodes other than the root and the leaves are called internal nodes.

[Table of Contents](#Data-Structures)

## Define leaves?

These are the terminal nodes of the tree. The nodes with degree 0 are always the leaves.
Here C and B are the leave nodes.

[Table of Contents](#Data-Structures)

## Define degree of the node?

The total number of sub-trees attached to that node is called the degree of the node.

```python
def degree(node):
    return len(node.children)

assert degree(root) == 2
assert degree(root.children[0]) == 0     # a leaf has degree 0
```

[Table of Contents](#Data-Structures)

## Define root?

This is the unique node in the tree to which further sub-trees are attached.

[Table of Contents](#Data-Structures)

## Define a tree?

A tree is a collection of nodes. The collection can be empty; otherwise, a tree consists of a  distinguished node r, called the root, and zero or more nonempty (sub) trees T1, T2,…,Tk, each of whose roots are connected by a directed edge from r.

```python
class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

root = TreeNode("company", [TreeNode("sales"), TreeNode("eng")])
def size(node):
    return 1 + sum(size(child) for child in node.children)

assert size(root) == 3
```

[Table of Contents](#Data-Structures)

## Why we need cursor implementation of linked lists?

Many languages such as BASIC and FORTRAN do not support pointers. If linked lists are required and pointers are not available, then an alternative implementation must be used known as cursor implementation.

[Table of Contents](#Data-Structures)

## List the applications of queues?

Jobs submitted to printer
Real lifeline
Calls to large companies
Access to limited resources in Universities
Accessing files from file server

[Table of Contents](#Data-Structures)

## List the applications of stacks?

Towers of Hanoi
Reversing a string
Balanced parenthesis
Recursion using stack
Evaluation of arithmetic expressions

[Table of Contents](#Data-Structures)

## What are the types of queues?

Linear Queues – The queue has two ends, the front end and the rear end. The rear end is where we insert elements and front end is where we delete elements. We can traverse in a linear queue in only one direction ie) from front to rear.
Circular Queues – Another form of linear queue in which the last position is connected to the first position of the list. The circular queue is similar to linear queue has two ends, the front end and the rear end. The rear end is where we insert elements and front end is where we delete elements. We can traverse in a circular queue in only one direction ie) from front to rear.
Double-Ended-Queue – Another form of queue in which insertions and deletions are made at both the front and rear ends of the queue.

+ Linear queue: single rear and front.
+ Circular queue: reuses freed slots with modulo arithmetic.
+ Priority queue: dequeues by priority.
+ Double-ended queue: insert and delete at both ends.

```python
class CircularQueue:
    def __init__(self, size):
        self.size = size
        self.data = [None] * size
        self.front = self.rear = 0

    def enqueue(self, value):
        if (self.rear + 1) % self.size == self.front:
            raise OverflowError("queue full")
        self.data[self.rear] = value
        self.rear = (self.rear + 1) % self.size

    def dequeue(self):
        if self.front == self.rear:
            raise IndexError("queue empty")
        value = self.data[self.front]
        self.front = (self.front + 1) % self.size
        return value

q = CircularQueue(3)
q.enqueue(1)
q.enqueue(2)
assert q.dequeue() == 1
```

[Table of Contents](#Data-Structures)

## What are the objectives of studying data structures?

To identify and create useful mathematical entities and operations to determine what classes of problems can be solved using these entities and operations.
To determine the representation of these abstract entities and to implement the abstract operations on these concrete representation.

[Table of Contents](#Data-Structures)

## State the difference between persistent and ephemeral data structure?

Persistent data structures are the data structures which retain their previous state and modifications can be done by performing certain operations on it. Eg) Stack Ephemeral data structures are the data structures which cannot retain its previous state. Eg) Queues.

[Table of Contents](#Data-Structures)

## State the difference between primitive and non-primitive data types?

Primitive data types are the fundamental data types. Eg) int, float, double, char Non-primitive data types are user defined data types. Eg) Structure, Union and enumerated data types.

[Table of Contents](#Data-Structures)

## What are the advantages of modularity?

It is much easier to debug small routines than large routines
It is easier for several people to work on a modular program simultaneously
A well-written modular program places certain dependencies in only one routine, making changes easier

[Table of Contents](#Data-Structures)

## Define an abstract data type?

An abstract data type is a set of operations. ADTs are mathematical abstractions; now here in an ADTs definition is there any mention of how the set of operations is implemented. Objects such as lists, sets and graphs, along with their operations can be viewed as abstract data types.

[Table of Contents](#Data-Structures)

## Define data type and what are the types of data type?

Data type refers to the kinds of data that variables may hold in the programming language. Eg) int, float, char, double – C
The following are the types of data type:
Built in data type- int, float, char, double which are defined by programming language itself
User defined data type- Using the set of built in data types user can define their own data type
Eg: typedef struct student

{
int roll;
char name;
}S;
S s1;
Where S is a tag for user defined data type which defines the structure student and s1 is a variable of data type S.

[Table of Contents](#Data-Structures)

## Difference between abstract data type and data type and data structure?

An Abstract data type is the specification of the data type which specifies the logical and mathematical model of the data type.
A data type is the implementation of an abstract data type.
Data structure refers to the collection of computer variables that are connected in some specific manner.
i.e) Data type has its root in the abstract data type and a data structure comprises a set of computer variables of same or different data types.

[Table of Contents](#Data-Structures)

## State the difference between queues and linked lists?

The difference between queues and linked lists is that insertions and deletions may occur anywhere in the linked list, but in queues insertions can be made only in the rear end and deletions can be made only in the front end.

[Table of Contents](#Data-Structures)

## How do you deduplicate records at scale?

Deduplication means choosing one surviving row per business key. The reliable pattern is to rank rows inside each key,
then keep the winner, rather than relying on `DISTINCT` (which compares every column) or on load order.

Key points:

+ Define the key and the tie-breaker explicitly, for example `customer_id` with `updated_at DESC, ingest_ts DESC`.
+ Rank deterministically so reruns produce the same winner.
+ Deduplicate after every union of sources, and again before the final mart.
+ For very large tables, partition by the key and deduplicate each partition independently.

```sql
WITH ranked AS (
    SELECT
        order_id,
        customer_id,
        amount,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY updated_at DESC, ingest_ts DESC
        ) AS rn
    FROM silver.orders_union
)
SELECT order_id, customer_id, amount
FROM ranked
WHERE rn = 1;
```

PySpark version that avoids a full shuffle where possible:

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

window = Window.partitionBy("order_id").orderBy(
    F.col("updated_at").desc(), F.col("ingest_ts").desc()
)
deduped = (
    orders_union
    .withColumn("rn", F.row_number().over(window))
    .filter("rn = 1")
    .drop("rn")
)
```

Trade-off: `ROW_NUMBER` needs a shuffle by the key. If the key is already the clustering key, the shuffle is cheap; if
not, pre-repartition or use `dropDuplicates` only when the natural key is the full row.

[Table of Contents](#Data-Structures)

## How do you order tasks with a dependency graph (DAG)?

A DAG is the right structure whenever work has prerequisites: Airflow tasks, dbt models, Spark stages, or table
builds. Kahn's algorithm repeatedly removes nodes with indegree zero and detects cycles when some nodes remain.

+ Validate the graph is acyclic before running anything.
+ Topological order is not unique; break ties by priority or critical path.
+ A non-empty result after the loop means there is a cycle, so fail fast.

```python
from collections import deque

def topo_sort(graph):
    indegree = {node: 0 for node in graph}
    for children in graph.values():
        for child in children:
            indegree[child] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in graph[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(graph):
        raise ValueError("cycle detected in dependency graph")
    return order

dag = {"extract": ["clean"], "clean": ["load"], "load": [], "seed": ["clean"]}
assert topo_sort(dag)[-1] == "load"
```

[Table of Contents](#Data-Structures)

## How do you find connected components for data lineage?

Connected components group records that are transitively related: the same person across systems, or tables linked
by a shared column. Union-find with path compression answers this in near-linear time, and BFS is the alternative when
you only need the members of one component.

+ Union every edge, then group by root.
+ Use this for entity resolution, lineage clusters, and account rollups.
+ On a cluster, run it per partition and union the partition roots.

```python
class DisjointSet:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

def components(edges):
    ds = DisjointSet()
    for a, b in edges:
        ds.union(a, b)
    groups = {}
    for node in ds.parent:
        groups.setdefault(ds.find(node), []).append(node)
    return list(groups.values())

edges = [("crm:1", "erp:9"), ("erp:9", "web:4"), ("crm:2", "web:8")]
groups = sorted(sorted(g) for g in components(edges))
assert groups == [["crm:1", "erp:9", "web:4"], ["crm:2", "web:8"]]
```

[Table of Contents](#Data-Structures)

## How do you compute a streaming median?

A median needs the middle of a sorted stream, but the stream is unbounded. Keep two heaps: a max-heap for the lower
half and a min-heap for the upper half, rebalancing so their sizes differ by at most one. Insert is O(log n) and the
median is O(1).

+ Lower half stored negated so Python's min-heap behaves as a max-heap.
+ Rebalance after every insert.
+ The median is the top of the larger heap, or the average of both tops when sizes match.

```python
import heapq

class StreamingMedian:
    def __init__(self):
        self.lower = []   # max-heap (store negatives)
        self.upper = []   # min-heap

    def add(self, value):
        heapq.heappush(self.lower, -value)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def median(self):
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0

stream = StreamingMedian()
for value in (5, 15, 1, 3):
    stream.add(value)
assert stream.median() == 4.0
```

[Table of Contents](#Data-Structures)

## When should you use a hash map instead of a join?

A hash join and a Python hash map are the same idea: build a table from the smaller side, then probe it with the larger
side. Use an in-memory map when one side is small enough to broadcast; use a distributed join when both sides are large.

+ Small dimension (fits in memory) -> broadcast hash join or `dict` lookup.
+ Large on both sides -> sort-merge or shuffled hash join.
+ Uneven keys and hot partitions -> salt the key or pre-aggregate first.
+ A map gives O(1) probe time but costs memory; a join costs a shuffle but scales.

PySpark broadcast join for a small dimension:

```python
from pyspark.sql import functions as F

enriched = (
    fact_orders.join(F.broadcast(dim_customer), on="customer_sk", how="left")
)
```

The equivalent pure-Python map lookup, useful for small reference data in a UDF or a driver-side job:

```python
def enrich(orders, customers):
    lookup = {customer["id"]: customer["segment"] for customer in customers}
    return [{**order, "segment": lookup.get(order["customer_id"], "unknown")}
            for order in orders]

orders = [{"customer_id": 1, "amount": 10}]
assert enrich(orders, [{"id": 1, "segment": "gold"}])[0]["segment"] == "gold"
```

[Table of Contents](#Data-Structures)

## Real world use cases for data structures in data engineering

These are the patterns that come up most often in data engineering interviews. Each one pairs the data structure with
the pipeline problem it solves.

+ Deduplication at scale: rank rows per key with a window function, or keep the latest record in a hash map.
+ Top-N per tenant: a bounded heap per partition, merged at the end, instead of a global sort.
+ Graph traversal for lineage: BFS or DFS over an adjacency list to find upstream and downstream tables.
+ Streaming median and percentiles: two heaps for an exact median, or t-digest for approximate quantiles.
+ Join strategy selection: hash map for a small dimension, sort-merge for two large tables.
+ Dependency ordering: a DAG plus topological sort to schedule models in the right order.

Example: deduplicate events by key, then compute the top 3 customers per day.

```python
import heapq
from collections import defaultdict

def top_customers_per_day(events, k=3):
    daily = defaultdict(lambda: defaultdict(float))
    for event in events:
        daily[event["day"]][event["customer"]] += event["amount"]
    return {day: heapq.nlargest(k, totals.items(), key=lambda pair: pair[1])
            for day, totals in daily.items()}

events = [
    {"day": "2026-10-01", "customer": "a", "amount": 5},
    {"day": "2026-10-01", "customer": "b", "amount": 9},
    {"day": "2026-10-01", "customer": "a", "amount": 7},
]
result = top_customers_per_day(events, k=1)
assert result["2026-10-01"] == [("a", 12.0)]
```

The same result in SQL, which is what you would run in the warehouse:

```sql
SELECT day, customer, revenue
FROM (
    SELECT
        day,
        customer,
        SUM(amount) AS revenue,
        ROW_NUMBER() OVER (PARTITION BY day ORDER BY SUM(amount) DESC) AS rn
    FROM fact_events
    GROUP BY day, customer
) ranked
WHERE rn <= 3
ORDER BY day, revenue DESC;
```

Example: upstream lineage traversal over a table-dependency graph.

```python
from collections import deque

def upstream_tables(graph, table):
    seen, queue, order = {table}, deque([table]), []
    while queue:
        node = queue.popleft()
        for parent in graph.get(node, []):
            if parent not in seen:
                seen.add(parent)
                order.append(parent)
                queue.append(parent)
    return order

lineage = {
    "gold.revenue": ["silver.orders"],
    "silver.orders": ["bronze.orders", "bronze.customers"],
}
assert upstream_tables(lineage, "gold.revenue") == [
    "silver.orders", "bronze.orders", "bronze.customers"
]
```

Example: streaming median with two heaps, for a latency or price metric that must be reported continuously.

```python
import heapq

lower, upper = [], []   # lower is a max-heap via negation
for value in (10, 20, 5):
    heapq.heappush(lower, -value)
    heapq.heappush(upper, -heapq.heappop(lower))
    if len(upper) > len(lower):
        heapq.heappush(lower, -heapq.heappop(upper))
median = -lower[0] if len(lower) > len(upper) else (-lower[0] + upper[0]) / 2
assert median == 10.0
```

Trade-off: an exact streaming median needs O(n) memory for the two heaps; approximate quantiles (t-digest) use far
less memory when the stream is huge.

[Table of Contents](#Data-Structures)
